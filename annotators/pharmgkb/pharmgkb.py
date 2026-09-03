import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os
import pickle

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        data_path = os.path.join(self.data_dir, 'pharmgkb.pickle')
        self.data = pickle.load(open(data_path,'rb'))
    
    def annotate(self, input_data, secondary_data=None):
        key = ':'.join(map(str, [
            input_data['chrom'],
            input_data['pos'],
            input_data['ref_base'],
            input_data['alt_base'],
        ]))
        hits = self.data.get(key)
        if hits:
            pharmgkb_id = hits[0]['pharmgkb_id']
            assocs = []
            chem = set()
            cat = set()
            has_sig = 'no'
            for hit in hits:
                chemicals = hit['chemical']
                category = hit['pheno_cat']
                chem_urls = [
                    f'https://www.pharmgkb.org/chemical/{chemid}' 
                    for chemid in hit['chemid']
                ]
                c = ' '.join(chemicals)
                if category != '':
                    ca = ''.join(category)
                    cat.add(ca)
                chem.add(c)
                has_sig = hit['sig']
                assocs.append([
                    list(zip(chemicals, chem_urls)),
                    hit['sentence'],
                    hit['pheno_cat'],
                    hit['sig'],
                    hit['pmid'],
                    hit['notes'],
                ])
            chems = list(chem)
            categories = list(cat)
            return {
                'id': pharmgkb_id,
                'chemicals': ';'.join(chems),
                'pheno_cat': ';'.join(categories),
                'drug_assoc': assocs,
                'has_sig': 'yes' if has_sig == 'yes' else 'no'
            }
        else:
            return None
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
