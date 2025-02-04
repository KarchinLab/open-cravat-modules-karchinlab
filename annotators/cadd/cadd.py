import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os
import tabix
class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        datafile = os.path.join(self.data_dir,'cadd.tsv.gz')
        self.tb = tabix.open(datafile) 
    
    def annotate(self, input_data, secondary_data=None):
        chrom = input_data['chrom'][3:]
        pos = input_data['pos']
        ref = input_data['ref_base']
        alt = input_data['alt_base']
        try:
            records = list(self.tb.query(chrom, pos - 1, pos))
        except tabix.TabixError:
            pass
        for record in records:
            if record[3] == alt:
                phred = float(record[5])
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
                return {'score':record[4], 'phred': phred, 'bp4_benign': benign, 'pp3_pathogenic': pathogenic}
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
