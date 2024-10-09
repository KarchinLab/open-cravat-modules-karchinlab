import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        self.cursor.execute('select * from prefixes;')
        self.which_col = {}
        for row in self.cursor:
            ref, alt, prefix = row
            self.which_col[ref+alt] = prefix
        self.cursor.execute('select name from sqlite_master where type="table" and name like "chr%";')
        self.valid_chroms = set([row[0] for row in self.cursor])

    def annotate(self, input_data, secondary_data=None):
        chrom = input_data['chrom']
        if chrom not in self.valid_chroms:
            return
        prefix_key = input_data['ref_base']+input_data['alt_base']
        prefix = self.which_col.get(prefix_key)
        if prefix is None:
            return
        score_col = prefix+'_score'
        phred_col = prefix+'_phred'
        pos = input_data['pos']
        q = f'select {score_col}, {phred_col} from {chrom} where pos={pos}'
        self.cursor.execute(q)
        row = self.cursor.fetchone()
        if row:
            score = row[0]
            phred = row[1]
            if phred <= 0.15:
                benign = "Strong"
                pathogenic = ""
            elif phred > 0.15 and phred <= 17.3:
                benign = "Moderate"
                pathogenic = ""
            elif phred > 17.3 and phred <= 22.7:
                benign = "Supporting"
                pathogenic = ""
            elif phred  >= 25.3 and phred < 28.1: 
                benign = ""
                pathogenic = "Supporting"
            elif phred >= 28.1:
                benign = ""
                pathogenic = "Moderate"
            else:
                benign = ""
                pathogenic = ""
            return {'score': score,'phred': phred, 'benign': benign, 'pathogenic': pathogenic}
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
