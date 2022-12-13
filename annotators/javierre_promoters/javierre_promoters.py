import sys
import os
import sqlite3
from cravat import BaseAnnotator
from cravat import InvalidData
from cravat.util import get_ucsc_bins
import pickle

class CravatAnnotator (BaseAnnotator):

    def setup(self):
        pickle_path = os.path.join(self.data_dir, 'javierre_promoters.pickle')
        self.data = pickle.load(open(pickle_path,'rb'))

    def annotate(self, input_data):
        out = {}
        chrom = input_data['chrom']
        pos = input_data['pos']
        it = self.data.get(chrom)
        if it:
            regions = [iv.data for iv in it[pos]]
        else:
            regions = []
        regions.sort()
        if regions:
            out['regions'] = ';'.join(regions)
            return out
        else:
            return None
        
if __name__ == '__main__':
    module = CravatAnnotator(sys.argv)
    module.run()
