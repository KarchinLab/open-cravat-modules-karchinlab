import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        pass
    
    def annotate(self, input_data, secondary_data=None):
        chrom = input_data['chrom']
        pos = input_data['pos']
        ref = input_data['ref_base']
        alt = input_data['alt_base']
        self.cursor.execute(f'select p_vid, varity_r, varity_er, varity_r_loo, varity_er_loo from {chrom} where pos=? and ref=? and alt=?',
            (pos, ref, alt),
        )
        row = self.cursor.fetchone()
        if row is not None:
            return {
                'p_vid': row[0],
                'varity_r': row[1],
                'varity_er': row[2],
                'varity_r_loo': row[3],
                'varity_er_loo': row[4],
            }
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()