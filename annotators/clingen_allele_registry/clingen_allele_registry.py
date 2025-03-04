import sys
import urllib.parse

import requests
from cravat import BaseAnnotator

class CravatAnnotator(BaseAnnotator):

    def annotate(self, input_data, secondary_data=None):
        ALLELE_REGISTRY_ENDPOINT = self.conf['api_url']
        out = {}
        chrom = input_data['chrom']
        pos = input_data['pos']
        ref = input_data['ref_base']
        alt = input_data['alt_base']
        transcript = input_data.get('transcript')
        cchange = input_data.get('cchange')
        so = input_data.get('so')

        if '2KD' == so or '2KU' == so or not cchange:
            return { 'allele_registry_id': '' }

        hgvs = f'{transcript}:{cchange}'
        resp = requests.get(f'{ALLELE_REGISTRY_ENDPOINT}{hgvs}')
        resp.raise_for_status()
        result = resp.json()

        if result:
            full_id = result.get('@id')
            ca_id = str.split(full_id, '/')[-1]
            if ca_id and not ca_id.startswith('CA'):
                ca_id = ''
            out = {
                'allele_registry_id': ca_id
            }
        return out

    
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
