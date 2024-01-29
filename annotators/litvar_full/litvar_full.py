import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os
import requests

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        pass
    
    @staticmethod
    def query_rsid(rsid):
        r = requests.get(f'https://www.ncbi.nlm.nih.gov/research/litvar2-api/variant/get/litvar@{rsid}%23%23/publications')
        if r.status_code == 200:
            return r.json().get('pmids',[])
        else:
            return []
        
    def annotate(self, input_data, secondary_data=None):
        if not secondary_data['dbsnp'] or secondary_data['dbsnp'][0] is None:
            return None
        dbsnp_result = secondary_data['dbsnp'][0].get('snp')
        if dbsnp_result is None:
            dbsnp_result = secondary_data['dbsnp'][0].get('rsid')
        if dbsnp_result is None:
            return None
        rsids = dbsnp_result.split(',')
        reference_count = 0
        pmids = []
        for rsid in rsids:
            self.cursor.execute('select rsid, litvar_count from litvar_full where rsid=?',(rsid,))
            r = self.cursor.fetchone()
            if r:
                reference_count += r[1]
                pmids += [str(_) for _ in self.query_rsid(rsid)]
        if reference_count == 0:
            return None
        return {
            'rsid': ','.join(rsids),
            'reference_count': reference_count,
            'pmids': ','.join(pmids),
        }
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()