import sys
import urllib.parse

import requests
from cravat import BaseAnnotator

class CravatAnnotator(BaseAnnotator):
    def annotate_batch(self, batch):
        """Annotate a batch of variants

        Use the ClinGen Allele Registry to API to annotate many variants at once.
        annotate_batch will be provided with a batch of input lines. This method
        will create an HGVS string for each variant, then call the batch version
        of the API. ClinGen Allele Registry recommends 100,000 variants per batch.
        """
        hgvs_strings = {}
        lines_to_skip = []

        # build hgvs strings for each input line
        for lnum, line, input_data, secondary_data in batch:
            transcript = input_data.get('transcript')
            cchange = input_data.get('cchange')
            so = input_data.get('so')
            # skip far up/downstream variants
            if '2KD' == so or '2KU' == so or not cchange:
                lines_to_skip.append(lnum)
                continue
            hgvs_strings[lnum] = f'{transcript}:{cchange}'

        # list hgvs strings to post to allele registry api
        post_data = '\n'.join(hgvs_strings.values())
        ALLELE_REGISTRY_ENDPOINT = self.conf['api_url']
        resp = requests.post(ALLELE_REGISTRY_ENDPOINT, data=post_data)
        if resp.status_code != 200:
            self.logger.error(f'Clingen Allele Registry API Error: {resp.status_code}\n{resp.text}')

        resp.raise_for_status()
        results = resp.json()

        # build the output
        out_batch = []
        if results:
            result_index = 0
            for lnum, line, input_data, secondary_data in batch:
                if lnum in lines_to_skip:
                    # remember to skip 2k up/down variants
                    out_batch.append((lnum, line, input_data, secondary_data, {'allele_registry_id': ''}))
                    continue

                result = results[result_index]
                result_index += 1
                full_id = result.get('@id')
                ca_id = ''
                if full_id:
                    ca_id = str.split(full_id, '/')[-1]
                    # cleanup error values
                    if ca_id and not ca_id.startswith('CA'):
                        ca_id = ''
                out = {
                    'allele_registry_id': ca_id
                }
                out_batch.append((lnum, line, input_data, secondary_data, out))
        return out_batch


if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
