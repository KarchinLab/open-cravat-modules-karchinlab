import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):
    def annotate(self, input_data, secondary_data=None):
        q = 'select tf_binding, dnase_peak, motif, dnase_footprint, eqtl, matched_tf_motif, matched_dnase_footprint,'\
            + 'ranking from regulome where chrom = "{chrom}" and pos = {pos}'.format(
            chrom = input_data['chrom'], pos = int(input_data['pos']))
        self.cursor.execute(q)
        row = self.cursor.fetchone()
        if row:
            out = {'tf_binding': row[0], 'dnase_peak': row[1], 'motif': row[2], 'dnase_footprint': row[3], 'eqtl': row[4],'matched_tf_motif': row[5], 'matched_dnase_footprint': row[6], 'ra': row[7]}
            return out
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()