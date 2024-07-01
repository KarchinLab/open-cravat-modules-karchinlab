import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os
import pandas as pd

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        data_path = os.path.join(self.data_dir, 'Cosmic_Fusion_v99_GRCh37.tsv')
        self.data = pd.read_csv(data_path, sep='\t')
    
    def annotate(self, input_data, secondary_data=None):
        out = {}
        chrn_left = input_data['left_chrom'].replace('chr','')
        chrn_right = input_data['right_chrom'].replace('chr','')
        chr_match = self.data[(self.data['FIVE_PRIME_CHROMOSOME']==chrn_left) & (self.data['THREE_PRIME_CHROMOSOME']==chrn_right)]
        strand_match = chr_match[(self.data['FIVE_PRIME_STRAND']==input_data['left_break_strand']) & (self.data['THREE_PRIME_STRAND']==input_data['right_break_strand'])]
        pos_match = strand_match[(self.data['FIVE_PRIME_GENOME_STOP_FROM']==input_data['left_break_pos']) & (self.data['THREE_PRIME_GENOME_START_FROM']==input_data['right_break_pos'])]
        out['fusion_id'] = pos_match.iloc[0]['COSMIC_FUSION_ID']
        return out
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()