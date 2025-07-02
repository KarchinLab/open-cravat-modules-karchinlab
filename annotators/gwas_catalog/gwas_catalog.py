import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        pass
    
    def annotate(self, input_data):
        main = {}
        out = {}
        cols = [
            'disease',
            'pmid',
            'init_samp',
            'rep_samp',
            'risk_allele',
            'pval',
            'or_beta',
            'ci'
        ]
        q = 'select {} from gwas where chrom="{}" and pos={}'.format(
            ', '.join(cols),
            input_data['chrom'],
            input_data['pos']
        )
        self.cursor.execute(q)
        if self.cursor.rowcount:
            first_row = next(self.cursor)
            main = dict(zip(cols, first_row))
            match = main['risk_allele'] == input_data['ref_base'] or main['risk_allele'] == input_data['alt_base']
            main['risk_allele_match'] = match
            out = main.copy()
            all_anots = []
            all_anots.append(main)
            has_match = match
            for qr in self.cursor:
                line_data = dict(zip(cols, qr))
                match = line_data['risk_allele'] == input_data['ref_base'] or line_data['risk_allele'] == input_data['alt_base']
                line_data['risk_allele_match'] = match
                has_match = has_match or match
                all_anots.append(line_data)
            out['risk_allele_match'] = has_match
            out['all_annots'] = all_anots

        return out
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()