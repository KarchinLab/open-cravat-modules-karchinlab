import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):
    def annotate(self, input_data, secondary_data=None):
        q = 'select primateai_score, primateai_rankscore, primateai_pred from {chr} where pos = {pos} and ref = "{ref}" and alt = "{alt}"'.format(
            chr = input_data["chrom"], pos = int(input_data["pos"]), ref = input_data["ref_base"], alt = input_data["alt_base"])
        self.cursor.execute(q)
        row = self.cursor.fetchone()
        if row:
            score = row[0]
            if score <= 0.362:
                benign = "Moderate"
                pathogenic = ""
            elif score > 0.362 and score <= 0.483:
                benign = "Supporting"
                pathogenic = ""
            elif score >= 0.790 and score < 0.867:
                benign = ""
                pathogenic = "Supporting"
            elif score >= 0.932:
                benign = ""
                pathogenic = "Moderate"
            else:
                benign = ""
                pathogenic = ""
            out = {'primateai_score': row[0],
                   'primateai_rankscore': row[1], 
                   'primateai_pred': row[2], 
                   'bp4_benign': benign,
                   'pp3_pathogenic': pathogenic
                   }
        else:
            out = None
        return out        
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
