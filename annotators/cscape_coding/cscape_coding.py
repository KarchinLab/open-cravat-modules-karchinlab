import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):
    def annotate(self, input_data, secondary_data=None):
        out = {}
        q = 'select score, rankscore from {chrom} where pos = {pos} and ref = "{ref}" and alt = "{alt}"'.format(
            chrom = input_data['chrom'], pos = int(input_data['pos']), ref = input_data['ref_base'], alt = input_data['alt_base'])
        self.cursor.execute(q)
        row = self.cursor.fetchone()
        if row:
            score = row[0]
            rankscore = row[1]
            out['score'] = score
            out['rankscore'] = rankscore
            return out

    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()