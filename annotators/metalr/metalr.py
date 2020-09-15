import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):
    def annotate(self, input_data, secondary_data=None):
        q = 'select metalr_score, metalr_rankscore, metalr_pred from {chr} where pos = {pos} and ref = "{ref}" and alt = "{alt}"'.format(
            chr=input_data["chrom"], pos=int(input_data["pos"]), ref = input_data["ref_base"], alt = input_data["alt_base"])
        self.cursor.execute(q)
        row = self.cursor.fetchone()
        metalr_pred = str(row[2]).replace('T', 'Tolerated')
        metalr_pred = metalr_pred.replace('D', 'Damaging')
        if row:
            out = {'metalr_score': row[0], 'metalr_rankscore': row[1], 'metalr_pred': metalr_pred}
        return out

    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()