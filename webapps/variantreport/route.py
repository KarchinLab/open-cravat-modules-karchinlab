import asyncio
import os
import webbrowser
import multiprocessing
from collections import namedtuple
from types import SimpleNamespace

import aiosqlite
import urllib.parse
import json
import sys
import argparse
import yaml
import re

from aiohttp.http_exceptions import HttpBadRequest
from cravat import ConfigLoader, InvalidData
from cravat import admin_util as au
from cravat import CravatFilter
from cravat.constants import base_smartfilters
from aiohttp import web
import time
from concurrent.futures import ProcessPoolExecutor
from cravat import get_live_annotator, get_live_mapper, get_module
from cravat.config_loader import ConfigLoader
import requests
import oyaml
import datetime
from pyliftover import LiftOver
import cravat

live_modules = {}
live_mapper = None
module_confs = {}
modules_to_run_ordered = []
oncokb_cache = {}
wgsreader = cravat.get_wgs_reader(assembly='hg38')
VARIANT_REPORT_CONFIG = {}
DBSNP_CONVERTER = None


async def test (request):
    return web.json_response({'result': 'success'})


def format_hgvs_string(hgvs_input):
    hgvs_parts = hgvs_input.upper().split(':')
    if len(hgvs_parts) != 2:
        raise InvalidData('HGVS input invalid.')
    prefix = hgvs_parts[1][0].lower()
    # TODO: if HGVS API is upgraded to support p., change this here to allow it on single variant page
    if prefix not in ('g', 'c'):
        raise InvalidData('HGVS input invalid. Only g. and c. prefixes are supported.')
    end = hgvs_parts[1][1:]
    return f'{hgvs_parts[0]}:{prefix}{end}'

def get_coordinates_from_hgvs_api(queries):
    global VARIANT_REPORT_CONFIG
    if not VARIANT_REPORT_CONFIG:
        confloader = ConfigLoader()
        VARIANT_REPORT_CONFIG = confloader.get_module_conf('variantreport')
    if 'hgvs_api_url' not in VARIANT_REPORT_CONFIG:
        raise web.HTTPInternalServerError(text='"hgvs_api_url" not found in variantreport configuration.')
    hgvs_input = format_hgvs_string(queries.get('hgvs'))
    data = {'hgvs': hgvs_input}
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(VARIANT_REPORT_CONFIG['hgvs_api_url'], data=json.dumps(data), headers=headers, timeout=20)
    try:
        resp.raise_for_status()
    except Exception as e:
        raise InvalidData(f"Error retrieving data from HGVS API. {hgvs_input} {e}")
    tokens = resp.json()
    return {
        'chrom': tokens['chrom'],
        'pos': tokens['pos'],
        'ref_base': tokens['ref'],
        'alt_base': tokens['alt'],
        'assembly': tokens['assembly']
    }

def format_allele(base):
    base_string = str(base)
    if not base_string or base_string == '':
        base_string = '-'
    return base_string

def coordinates_from_clingen_json(ca_id, data):
    genomic_alleles = data.get('genomicAlleles')
    for ga in genomic_alleles:
        if ga.get('referenceGenome') == 'GRCh38':
            coords = ga.get('coordinates')[0]
            return {
                'chrom': f'chr{ga.get("chromosome")}',
                'pos': int(coords.get('start')) + 1,
                'ref_base': format_allele(coords.get('referenceAllele')),
                'alt_base': format_allele(coords.get('allele')),
                'assembly': 'hg38'
            }
    raise web.HTTPInternalServerError(text=f'Could not find hg38 coordinates for clingen allele id {ca_id}.')


def get_coordinates_from_clingen_id(queries):
    global VARIANT_REPORT_CONFIG
    if not VARIANT_REPORT_CONFIG:
        confloader = ConfigLoader()
        VARIANT_REPORT_CONFIG = confloader.get_module_conf('variantreport')
    if 'clingen_api_url' not in VARIANT_REPORT_CONFIG:
        raise web.HTTPInternalServerError(text='"clingen_api_url" not found in variantreport configuration.')
    ca_id = queries['clingen'].strip().upper()
    headers = {'Content-Type': 'application/json'}
    request_url = f"{VARIANT_REPORT_CONFIG['clingen_api_url']}/{ca_id}"
    resp = requests.get(request_url, headers=headers, timeout=20)
    try:
        resp.raise_for_status()
    except Exception as e:
        raise InvalidData(f"Error retrieving data from Clingen Allele registry. Clingen Allele Registry Id should be formatted like 'CA12345'. {e}")
    data = resp.json()
    return coordinates_from_clingen_json(ca_id, data)


def get_coordinates_from_dbsnp(queries):
    global DBSNP_CONVERTER
    if not DBSNP_CONVERTER:
        converter_module = get_module('dbsnp-converter')
        DBSNP_CONVERTER = converter_module()

    dbsnp = queries.get('dbsnp').strip().lower()
    try:
        all_params = DBSNP_CONVERTER.convert_line(dbsnp)
    except Exception as e:
        raise InvalidData(f"Could not parse DBSNP '{dbsnp}'. Should be formatted like 'rs12345'.")
    params = all_params[0]
    params['assembly'] = 'hg38'
    alternates = None
    if len(all_params) > 1:
        alternates = all_params[1:]
    return params, alternates


async def get_coordinates_from_request_params(queries):
    parameters = {}
    original_input = {}
    alternate_alleles = None
    required_coordinate_params = {'chrom', 'pos', 'ref_base', 'alt_base', 'assembly'}
    if (required_coordinate_params <= queries.keys()
        and None not in {queries[x] for x in required_coordinate_params}):
        parameters = {
            x: queries[x].upper() for x in required_coordinate_params
        }
        parameters['chrom'] = parameters['chrom'].lower()
        original_input = {'type': 'coordinates', 'input': f'{queries["assembly"]} {queries["chrom"]} {queries["pos"]} {queries["ref_base"]} {queries["alt_base"]}'}
    elif 'hgvs' in queries.keys() and queries['hgvs'] and 'assembly' in queries.keys():
        # make hgvs api call
        original_input = {'type': 'hgvs', 'input': queries['hgvs']}
        parameters = get_coordinates_from_hgvs_api(queries)
    elif 'clingen' in queries.keys() and queries.get('clingen'):
        # make clingen api call
        original_input = {'type': 'clingen', 'input': queries['clingen']}
        parameters = get_coordinates_from_clingen_id(queries)
    elif 'dbsnp' in queries.keys() and queries.get('dbsnp'):
        # use dbsnp-converter
        original_input = {'type': 'dbsnp', 'input': queries['dbsnp']}
        parameters, alternate_alleles = get_coordinates_from_dbsnp(queries)
    else:
        raise web.HTTPBadRequest(reason='Required parameters missing. Need either "chrom", "pos", "ref_base", and "alt_base", or "hgvs", or "dbsnp", or "clingen". Parameter "assembly" always required.')
    parameters['uid'] = queries.get('uid', '')
    if 'annotators' in queries.keys():
        parameters['annotators'] = queries.get('annotators', '')
    return parameters, original_input, alternate_alleles


async def get_live_annotation_post (request):
    queries = await request.post()
    try:
        coords, original_input, alternate_alleles = await get_coordinates_from_request_params(queries)
    except Exception as e:
        text = str(e)
        q = {key: value for key, value in queries.items()}
        return web.json_response(data={'error': text, 'originalInput': q})
    response = await get_live_annotation(coords)
    response['originalInput'] = original_input
    response['alternateAlleles'] = alternate_alleles
    return web.json_response(response)

async def get_live_annotation_get (request):
    queries = request.rel_url.query
    try:
        coords, original_input, alternate_alleles = await get_coordinates_from_request_params(queries)
    except Exception as e:
        text = str(e)
        q = {key: value for key, value in queries.items()}
        return web.json_response(data={'error': text, 'originalInput': q})
    response = await get_live_annotation(coords)
    response['originalInput'] = original_input
    response['alternateAlleles'] = alternate_alleles
    return web.json_response(response)

async def get_live_annotation (queries):
    chrom = queries['chrom']
    pos = queries['pos']
    ref_base = queries['ref_base']
    alt_base = queries['alt_base']
    assembly = queries['assembly']
    if 'uid' not in queries:
        uid = ''
    else:
        uid = queries['uid']
    input_data = {
        'uid': uid, 
        'chrom': chrom, 
        'pos': int(pos), 
        'ref_base': ref_base, 
        'alt_base': alt_base,
        'assembly': assembly}
    if 'annotators' in queries:
        annotators = queries['annotators'].split(',')
    else:
        annotators = None
    global live_modules
    if len(live_modules) == 0:
        await load_live_modules()
        response = await live_annotate(input_data, annotators)
    else:
        response = await live_annotate(input_data, annotators)
    return response

def clean_annot_dict (d):
    keys = d.keys()
    for key in keys:
        value = d[key]
        if value == '' or value == {}:
            d[key] = None
        elif type(value) is dict:
            d[key] = clean_annot_dict(value)
    if type(d) is dict:
        all_none = True
        for key in keys:
            if d[key] is not None:
                all_none = False
                break
        if all_none:
            d = None
    return d

def liftover(input_data, lifter):
    global wgsreader
    chrom = input_data['chrom']
    pos = input_data['pos']
    ref = input_data['ref_base']
    alt = input_data['alt_base']
    reflen = len(ref)
    altlen = len(alt)
    if reflen == 1 and altlen == 1:
        res = lifter.convert_coordinate(chrom, pos - 1)
        if res is None or len(res) == 0:
            raise LiftoverFailure('Liftover failure')
        if len(res) > 1:
            raise LiftoverFailure('Liftover failure')
        try:
            el = res[0]
        except:
            raise LiftoverFailure('Liftover failure')
        newchrom = el[0]
        newpos = el[1] + 1
    elif reflen >= 1 and altlen == 0: # del
        pos1 = pos
        pos2 = pos + reflen - 1
        res1 = lifter.convert_coordinate(chrom, pos1 - 1)
        res2 = lifter.convert_coordinate(chrom, pos2 - 1)
        if res1 is None or res2 is None or len(res1) == 0 or len(res2) == 0:
            raise LiftoverFailure('Liftover failure')
        if len(res1) > 1 or len(res2) > 1:
            raise LiftoverFailure('Liftover failure')
        el1 = res1[0]
        el2 = res2[0]
        newchrom1 = el1[0]
        newpos1 = el1[1] + 1
        newchrom2 = el2[0]
        newpos2 = el2[1] + 1
        newchrom = newchrom1
        newpos = newpos1
        newpos = min(newpos1, newpos2)
    elif reflen == 0 and altlen >= 1: # ins
        res = lifter.convert_coordinate(chrom, pos - 1)
        if res is None or len(res) == 0:
            raise LiftoverFailure('Liftover failure')
        if len(res) > 1:
            raise LiftoverFailure('Liftover failure')
        el = res[0]
        newchrom = el[0]
        newpos = el[1] + 1
    else:
        pos1 = pos
        pos2 = pos + reflen - 1
        res1 = lifter.convert_coordinate(chrom, pos1 - 1)
        res2 = lifter.convert_coordinate(chrom, pos2 - 1)
        if res1 is None or res2 is None or len(res1) == 0 or len(res2) == 0:
            raise LiftoverFailure('Liftover failure')
        if len(res1) > 1 or len(res2) > 1:
            raise LiftoverFailure('Liftover failure')
        el1 = res1[0]
        el2 = res2[0]
        newchrom1 = el1[0]
        newpos1 = el1[1] + 1
        newchrom2 = el2[0]
        newpos2 = el2[1] + 1
        newchrom = newchrom1
        newpos = min(newpos1, newpos2)
    hg38_ref = wgsreader.get_bases(newchrom, newpos)
    if hg38_ref == cravat.util.reverse_complement(ref):
        newref = hg38_ref
        newalt = cravat.util.reverse_complement(alt)
    else:
        newref = ref
        newalt = alt
    return [newchrom, newpos, newref, newalt]

async def live_annotate (input_data, annotators):
    from cravat.constants import mapping_parser_name
    from cravat.constants import all_mappings_col_name
    from cravat.inout import AllMappingsParser
    global live_modules
    global live_mapper
    global module_confs
    global modules_to_run_ordered
    response = {}
    assembly = input_data.get('assembly', 'hg38')
    if assembly in cravat.constants.liftover_chain_paths:
        lifter = LiftOver(cravat.constants.liftover_chain_paths[assembly])
        chrom, pos, ref, alt = liftover(input_data, lifter)
        input_data['chrom'] = chrom
        input_data['pos'] = pos
        input_data['ref'] = ref
        input_data['alt'] = alt
    crx_data = live_mapper.map(input_data)
    crx_data = live_mapper.live_report_substitute(crx_data)
    crx_data[mapping_parser_name] = AllMappingsParser(crx_data[all_mappings_col_name])
    for module_name in modules_to_run_ordered:
        module = live_modules[module_name]
        if annotators is not None and module_name not in annotators:
            continue
        try:
            conf = module_confs[module_name]
            json_colnames = []
            for col in conf['output_columns']:
                if 'table' in col and col['table'] == True:
                    json_colnames.append(col['name'])
            if 'secondary_inputs' in conf:
                sec_mods = conf['secondary_inputs']
                secondary_data = {}
                for sec_mod in sec_mods:
                    secondary_data[sec_mod] = [response[sec_mod]]
                annot_data = module.annotate(
                        input_data=crx_data, 
                        secondary_data=secondary_data)
            else:
                annot_data = module.annotate(input_data=crx_data)
            annot_data = module.live_report_substitute(annot_data)
            if annot_data == '' or annot_data == {}:
                annot_data = None
            elif type(annot_data) is dict:
                annot_data = clean_annot_dict(annot_data)
            if annot_data is not None:
                for colname in json_colnames:
                    json_data = annot_data.get(colname, None)
                    if json_data is not None and type(json_data) == str:
                        json_data = json.loads(json_data)
                    annot_data[colname] = json_data
            response[module_name] = annot_data
        except Exception as e:
            import traceback
            traceback.print_exc()
            if 'annotationErrors' not in response:
                response['annotationErrors'] = {}
            response['annotationErrors'][module_name] = repr(e)
            response[module_name] = None
    del crx_data[mapping_parser_name]
    set_crx_canonical(crx_data)
    response['crx'] = crx_data
    return response

def set_crx_canonical (crx_data):
    global canonicals
    if canonicals is None:
        f = open(os.path.join(os.path.dirname(__file__), 'canonical_transcripts.txt'))
        canonicals = {}
        for line in f:
            [hugo, enstnv] = line[:-1].split()
            canonicals[hugo] = enstnv
        f.close()
    all_mappings = json.loads(crx_data['all_mappings'])
    for hugo in all_mappings.keys():
        if hugo not in canonicals:
            continue
        mappings = all_mappings[hugo]
        for mapping in mappings:
            [uniprot, achange, sos, tr, cchange] = mapping
            if tr.split('.')[0] == canonicals[hugo]:
                crx_data['hugo'] = hugo
                crx_data['transcript'] = tr
                crx_data['so'] = sos
                crx_data['cchange'] = cchange
                crx_data['achange'] = achange
                break
    return crx_data

async def load_live_modules ():
    global live_modules
    global live_mapper
    global module_confs
    global modules_to_run_ordered
    global VARIANT_REPORT_CONFIG
    confloader = ConfigLoader()
    if not VARIANT_REPORT_CONFIG:
        VARIANT_REPORT_CONFIG = confloader.get_module_conf('variantreport')
    module_names_to_load = VARIANT_REPORT_CONFIG['live_modules']
    if live_mapper is None:
        cravat_conf = au.get_cravat_conf()
        if 'genemapper' in cravat_conf:
            default_mapper = cravat_conf['genemapper']
        else:
            default_mapper = 'hg38'
        live_mapper = get_live_mapper(default_mapper)
        module_confs[default_mapper] = confloader.get_module_conf(default_mapper)
    for module_name in module_names_to_load:
        if module_name in live_modules:
            continue
        annotator = get_live_annotator(module_name)
        live_modules[module_name] = annotator
        module_confs[module_name] = confloader.get_module_conf(module_name)
    modules_to_run_ordered = []
    module_names = list(module_confs.keys())
    num_module_names = len(module_names)
    while True:
        for module_name in module_names:
            if module_name in modules_to_run_ordered:
                continue
            if module_name == default_mapper:
                continue
            conf = module_confs[module_name]
            if 'secondary_inputs' not in conf:
                modules_to_run_ordered.append(module_name)
            else:
                sec_mods = conf['secondary_inputs']
                all_sec_mods_already = True
                for sec_mod in sec_mods:
                    if sec_mod not in modules_to_run_ordered:
                        all_sec_mods_alreay = False
                        break
                if all_sec_mods_already:
                    modules_to_run_ordered.append(module_name)
        if len(modules_to_run_ordered) == num_module_names - 1:
            break

async def get_oncokb_annotation (request):
    global oncokb_conf
    global oncokb_cache
    queries = request.rel_url.query
    chrom = queries['chrom']
    start = queries['start']
    end = queries['end']
    ref_base = queries['ref_base']
    alt_base = queries['alt_base']
    cache_key = f'{chrom}:{start}:{end}:{ref_base}:{alt_base}'
    cookies = request.cookies
    if 'oncokb_token' in cookies:
        token = cookies['oncokb_token']
        if token == '':
            token = None
    elif oncokb_conf is not None and 'token' in oncokb_conf:
        token = oncokb_conf['token']
    else:
        token = None
    if cache_key in oncokb_cache:
        cache_date = oncokb_cache[cache_key]['date']
        now = datetime.datetime.now()
        diff = now - cache_date
        if diff.days > 30:
            del oncokb_cache[cache_key]
            use_cache = False
        else:
            use_cache = True
    else:
        use_cache = False
    if use_cache:
        response = web.json_response(oncokb_cache[cache_key]['rjson'])
    else:
        if token is None:
            response = web.json_response({'notoken': True})
        else:
            url = f'https://www.oncokb.org/api/v1/annotate/mutations/byGenomicChange?genomicLocation={chrom},{start},{end},{ref_base},{alt_base}&referenceGenome=GRCh38'
            headers = {'Authorization': 'Bearer ' + token}
            r = requests.get(url, headers=headers)
            rjson = r.json()
            if 'status' in rjson and rjson['status'] == 401:
                response = web.json_response({'notoken': True})
                response.cookies['oncokb_token'] = ''
            else:
                response = web.json_response(rjson)
                oncokb_cache[cache_key] = {'date': datetime.datetime.now(), 'rjson': rjson}
    return response

async def get_hallmarks (request):
    queries = request.rel_url.query
    hugo = queries['hugo']
    if hugo == '':
        return web.json_response({})
    url = 'https://cancer.sanger.ac.uk/cosmic/census-page/' + hugo
    r = requests.get(url)
    text = r.text[r.text.index('<p class="census-hallmark-desc">') + 32:]
    func_summary = text[:text.index('<a href=')].strip()
    content = {'func_summary': func_summary}
    return web.json_response(content)

async def get_litvar (request):
    queries = request.rel_url.query
    rsid = queries['rsid']
    url = 'https://www.ncbi.nlm.nih.gov/research/bionlp/litvar/api/v1/public/rsids2pmids?rsids=' + rsid
    r = requests.get(url)
    response = r.json()
    n = 0
    if len(response) > 0:
        n = len(response[0]['pmids'])
    return web.json_response({'n': n})

async def save_oncokb_token (request):
    queries = request.rel_url.query
    token = queries['token']
    oncokb_conf = {'token': token}
    response = web.json_response({"result": "success"})
    response.cookies['oncokb_token'] = token
    return response

async def get_module_info (request):
    content = {}
    queries = request.rel_url.query
    module_name = queries['module']
    module_info = au.get_local_module_info(module_name)
    module_dir = module_info.directory
    if module_name in au.mic.local:
        content = au.mic.local[module_name].conf
    content['has_logo'] = os.path.exists(os.path.join(module_dir, 'logo.png'))
    return web.json_response(content)

async def get_modules_info(request):
    queries = request.rel_url.query
    module_names = queries['modules'].split(",")
    response = []
    for module_name in module_names:
        if module_name not in au.mic.local:
            conf = {}
            title = ""
            desc = ""
            url = ""
        else:
            conf = au.mic.local[module_name].conf
            title = conf.get("title", "")
            desc = conf.get("description", "")
            url = conf.get("developer", {}).get("website", "")
        response.append({"name": module_name, "title": title, "desc": desc, "url": url})
    return web.json_response(response)

oncokb_conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'oncokb_conf.yml')

if os.path.exists(oncokb_conf_path):
    f = open(oncokb_conf_path)
    oncokb_conf = oyaml.safe_load(f)
    f.close()
else:
    oncokb_conf = None

routes = [
   ['GET', 'test', test],
   ['GET', 'annotate', get_live_annotation_get],
   ['POST', 'annotate', get_live_annotation_post],
   ['GET', 'loadlivemodules', load_live_modules],
   ['GET', 'oncokb', get_oncokb_annotation],
   ['GET', 'saveoncokbtoken', save_oncokb_token],
   ['GET', 'hallmarks', get_hallmarks],
   ['GET', 'litvar', get_litvar],
   ['GET', 'modulesinfo', get_modules_info],
   ['GET', 'moduleinfo', get_module_info],
]

canonicals = None

if __name__ == '__main__':
    # queries = request.rel_url.query
    query_params = {
        'dbsnp': 'RSRSrsRSRSrs'
        # 'clingen': 'cacaca'
       # 'clingen': 'ca12345'
    }
    RelUrlMock = namedtuple('rel_url', 'query')
    RequestMock = namedtuple('Request', 'rel_url')
    rel_url = RelUrlMock(query_params)
    req = RequestMock(rel_url)
    r = asyncio.run(get_live_annotation_get(req))
    print(r.body)
    # params = get_coordinates_from_clingen_id({'clingen': 'CA12345'})
    # print(f'params: {params}')
