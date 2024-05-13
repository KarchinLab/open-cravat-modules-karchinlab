import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):
    def annotate(self, input_data, secondary_data=None):
        q = 'select bayesdel_addAF_score, bayesdel_addAF_rankscore, bayesdel_addAF_pred, bayesdel_noAF_score, bayesdel_noAF_rankscore, bayesdel_noAF_pred from {chr} where pos = {pos} and alt = "{alt}"'.format(
            chr = input_data["chrom"], pos = int(input_data["pos"]), alt = input_data["alt_base"])
        self.cursor.execute(q)
        row = self.cursor.fetchone()
        if row:
            if row[2] == "T":
                addaf_pred = "Tolerated"
            elif row[2] == "D":
                addaf_pred = "Deleterious"
            if row[5] == "T":
                noaf_pred = "Tolerated"
            elif row[5] == "D":
                noaf_pred = "Deleterious"
            out = {'bayesdel_addAF_score': row[0],
                   'bayesdel_addAF_rankscore': row[1], 
                   'bayesdel_addAF_pred': addaf_pred, 
                   'bayesdel_noAF_score': row[3], 
                   'bayesdel_noAF_rankscore': row[4],
                   'bayesdel_noAF_pred': noaf_pred
                   }
        else:
            out = None
        return out        
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()