import os
import json
from cravat import ConfigLoader
from cravat import admin_util as au
from cravat import CravatFilter
from cravat.constants import base_smartfilters
from cravat.config_loader import ConfigLoader
import requests
import oyaml
import datetime

from flask import jsonify, abort
import cravat

oncokb_cache = {}

def test (request):
    return jsonify({'result': 'success'})

def get_live_annotation_post(request):
    queries = request.json if request.is_json else request.form.to_dict()
    if not queries:
        return jsonify({'error': "Variant Information Required"}), 400
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    confloader = ConfigLoader()
    mtb_config = confloader.get_module_conf('moleculartumorboard')
    if 'oc_api_url' not in mtb_config:
        raise abort(500, description='"oc_api_url" not found in moleculartumorboard configuration.')
    url = mtb_config['oc_api_url']
    annotators = mtb_config['live_modules']
    all_annotators = []
    for a in annotators + queries.get('annotators', []):
        if a not in all_annotators:
            all_annotators.append(a)
    queries['annotators'] = all_annotators
    resp = requests.post(url=url, data=json.dumps(queries), headers=headers)
    resp.raise_for_status()
    return resp.json()


def get_oncokb_annotation (request):
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
    return abort(500, description='Temporarily disabled to avoid scraping cosmic')
    # queries = request.rel_url.query
    # hugo = queries['hugo']
    # if hugo == '':
    #     return web.json_response({})
    # url = 'https://cancer.sanger.ac.uk/cosmic/census-page/' + hugo
    # r = requests.get(url)
    # text = r.text[r.text.index('<p class="census-hallmark-desc">') + 32:]
    # func_summary = text[:text.index('<a href=')].strip()
    # content = {'func_summary': func_summary}
    # return web.json_response(content)

def get_litvar (request):
    queries = request.rel_url.query
    rsid = queries['rsid']
    url = 'https://www.ncbi.nlm.nih.gov/research/bionlp/litvar/api/v1/public/rsids2pmids?rsids=' + rsid
    r = requests.get(url)
    response = r.json()
    n = 0
    if len(response) > 0:
        n = len(response[0]['pmids'])
    return jsonify({'n': n})

def save_oncokb_token (request):
    queries = request.rel_url.query
    token = queries['token']
    oncokb_conf = {'token': token}
    response = jsonify({"result": "success"})
    response.cookies['oncokb_token'] = token
    return response

oncokb_conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'oncokb_conf.yml')

if os.path.exists(oncokb_conf_path):
    f = open(oncokb_conf_path)
    oncokb_conf = oyaml.safe_load(f)
    f.close()
else:
    oncokb_conf = None

routes = [
   ['GET', 'test', test],
   ['POST', 'annotate', get_live_annotation_post],
   ['GET', 'oncokb', get_oncokb_annotation],
   ['GET', 'saveoncokbtoken', save_oncokb_token],
   ['GET', 'hallmarks', get_hallmarks],
   ['GET', 'litvar', get_litvar],
]

canonicals = None
