import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os
import pickle

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        pickle_path = os.path.join(self.data_dir,'ncrna.pickle')
        with open(pickle_path,'rb') as f:
            self.data = pickle.load(f)
    
    def annotate(self, input_data, secondary_data=None):
        
        chrom = input_data['chrom']
        if chrom in self.data:
            pos = input_data['pos']
            ivs = self.data[chrom][pos]
            classes = []
            names = []
            for iv in ivs:
                classes.append(iv.data[1])
                names.append(iv.data[2])
            data = list(zip(classes, names))
            data.sort()
            classes = [_[0] for _ in data]
            names = [_[1] for _ in data]
            if classes and names:
                out = {
                    'ncrnaclass': ','.join(classes),
                    'ncrnaname': ','.join(names)                    
                    }
                return out
        return None

    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()