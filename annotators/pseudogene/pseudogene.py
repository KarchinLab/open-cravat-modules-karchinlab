import sys
import os
import sqlite3
from cravat import BaseAnnotator
from cravat.util import get_ucsc_bins
import pickle

class CravatAnnotator (BaseAnnotator):

    def setup(self):
        pickle_path = os.path.join(self.data_dir, 'pseudogene.pickle')
        self.data = pickle.load(open(pickle_path,'rb'))

    def annotate(self, input_data):
        chrom = input_data['chrom']
        pos = input_data['pos']
        if chrom in self.data.tids:
            ivs = self.data.tids[chrom][pos]
            ensts = []
            hugos = []
            for iv in sorted(ivs):
                tid = iv.data
                enst, hugo = self.data.tinfo.get(tid,(None,None))
                if enst and hugo:
                    ensts.append(enst)
                    hugos.append(hugo)
            if ensts and hugos:
                out = {
                    'transcript': ';'.join(ensts),
                    'hugo': ';'.join(hugos),
                }
                return out

if __name__ == '__main__':
    module = CravatAnnotator(sys.argv)
    module.run()
