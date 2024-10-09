import os
import json
from cravat import admin_util as au
from cravat import get_live_annotator, get_live_mapper
from cravat.config_loader import ConfigLoader
import requests
import oyaml
import datetime
from pyliftover import LiftOver
import cravat

from flask import jsonify

oncokb_cache = {}
wgsreader = cravat.get_wgs_reader(assembly='hg38')

class LiveModules:
    def __init__(self):
        self.live_modules = {}
        self.module_confs = {}
        self.modules_to_run_ordered = []

        confloader = ConfigLoader()
        conf = confloader.get_module_conf('variantreportcedar')
        module_names_to_load = conf['live_modules']

        cravat_conf = au.get_cravat_conf()
        if 'genemapper' in cravat_conf:
            default_mapper = cravat_conf['genemapper']
        else:
            default_mapper = 'hg38'
        self.live_mapper = get_live_mapper(default_mapper)
        self.module_confs[default_mapper] = confloader.get_module_conf(default_mapper)

        for module_name in module_names_to_load:
            if module_name in self.live_modules:
                continue
            annotator = get_live_annotator(module_name)
            self.live_modules[module_name] = annotator
            self.module_confs[module_name] = confloader.get_module_conf(module_name)

        module_names = list(self.module_confs.keys())
        num_module_names = len(module_names)
        while True:
            for module_name in module_names:
                if module_name in self.modules_to_run_ordered:
                    continue
                if module_name == default_mapper:
                    continue
                conf = self.module_confs[module_name]
                if 'secondary_inputs' not in conf:
                    self.modules_to_run_ordered.append(module_name)
                else:
                    sec_mods = conf['secondary_inputs']
                    all_sec_mods_already = True
                    for sec_mod in sec_mods:
                        if sec_mod not in self.modules_to_run_ordered:
                            all_sec_mods_already = False
                            break
                    if all_sec_mods_already:
                        self.modules_to_run_ordered.append(module_name)

            if len(self.modules_to_run_ordered) == num_module_names - 1:
                break

    def live_annotate(self, input_data, annotators):
        from cravat.constants import mapping_parser_name
        from cravat.constants import all_mappings_col_name
        from cravat.inout import AllMappingsParser

        response = {}
        assembly = input_data.get('assembly', 'hg38')
        if assembly in cravat.constants.liftover_chain_paths:
            lifter = LiftOver(cravat.constants.liftover_chain_paths[assembly])
            chrom, pos, ref, alt = liftover(input_data, lifter)
            input_data['chrom'] = chrom
            input_data['pos'] = pos
            input_data['ref'] = ref
            input_data['alt'] = alt
        crx_data = self.live_mapper.map(input_data)
        crx_data = self.live_mapper.live_report_substitute(crx_data)
        crx_data[mapping_parser_name] = AllMappingsParser(crx_data[all_mappings_col_name])
        for module_name in self.modules_to_run_ordered:
            module = self.live_modules[module_name]
            if annotators is not None and module_name not in annotators:
                continue
            try:
                conf = self.module_confs[module_name]
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
                response[module_name] = None
        del crx_data[mapping_parser_name]
        set_crx_canonical(crx_data)
        response['crx'] = crx_data
        return response

def test (request):
    return jsonify({'result': 'success'})

def get_live_annotation_post(request):
    queries = request.values
    response = get_live_annotation(queries)
    return jsonify(response)

def get_live_annotation_get (request):
    queries = request.values
    response = get_live_annotation(queries)
    return jsonify(response)

def get_live_annotation (queries):
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

    live_modules = LiveModules()
    return live_modules.live_annotate(input_data, annotators)

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

def get_oncokb_annotation (request):
    global oncokb_conf
    global oncokb_cache
    queries = request.values
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
        response = jsonify(oncokb_cache[cache_key]['rjson'])
    else:
        if token is None:
            response = jsonify({'notoken': True})
        else:
            url = f'https://www.oncokb.org/api/v1/annotate/mutations/byGenomicChange?genomicLocation={chrom},{start},{end},{ref_base},{alt_base}&referenceGenome=GRCh38'
            headers = {'Authorization': 'Bearer ' + token}
            r = requests.get(url, headers=headers)
            rjson = r.json()
            if 'status' in rjson and rjson['status'] == 401:
                response = jsonify({'notoken': True})
                response.cookies['oncokb_token'] = ''
            else:
                response = jsonify(rjson)
                oncokb_cache[cache_key] = {'date': datetime.datetime.now(), 'rjson': rjson}
    return response

def get_hallmarks (request):
    queries = request.values
    hugo = queries['hugo']
    if hugo == '':
        return jsonify({})
    url = 'https://cancer.sanger.ac.uk/cosmic/census-page/' + hugo
    r = requests.get(url)
    text = r.text[r.text.index('<p class="census-hallmark-desc">') + 32:]
    func_summary = text[:text.index('<a href=')].strip()
    content = {'func_summary': func_summary}
    return jsonify(content)

def get_litvar (request):
    queries = request.values
    rsid = queries['rsid']
    url = 'https://www.ncbi.nlm.nih.gov/research/bionlp/litvar/api/v1/public/rsids2pmids?rsids=' + rsid
    r = requests.get(url)
    response = r.json()
    n = 0
    if len(response) > 0:
        n = len(response[0]['pmids'])
    return jsonify({'n': n})

def save_oncokb_token (request):
    queries = request.values
    token = queries['token']
    oncokb_conf = {'token': token}
    response = jsonify({"result": "success"})
    response.cookies['oncokb_token'] = token
    return response

def get_module_info (request):
    content = {}
    queries = request.values
    module_name = queries['module']
    module_info = au.get_local_module_info(module_name)
    module_dir = module_info.directory
    if module_name in au.mic.local:
        content = au.mic.local[module_name].conf
    content['has_logo'] = os.path.exists(os.path.join(module_dir, 'logo.png'))
    return jsonify(content)

def get_modules_info(request):
    queries = request.values
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
    return jsonify(response)

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
   ['GET', 'oncokb', get_oncokb_annotation],
   ['GET', 'saveoncokbtoken', save_oncokb_token],
   ['GET', 'hallmarks', get_hallmarks],
   ['GET', 'litvar', get_litvar],
   ['GET', 'modulesinfo', get_modules_info],
   ['GET', 'moduleinfo', get_module_info],
]

canonicals = None
