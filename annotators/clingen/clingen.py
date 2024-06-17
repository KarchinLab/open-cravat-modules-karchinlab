import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os
import pickle
from collections import defaultdict

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        data_path = os.path.join(self.data_dir, 'clingen.pickle')
        self.data = pickle.load(open(data_path,'rb'))
    
    def annotate(self, input_data, secondary_data=None):
        out = {}
        r = self.data.get(input_data['hugo'])
        if r is None:
            return None
        temp = defaultdict(list)
        for hit in r:
            for k,v in hit.items():
                temp[k].append(v)
        for k,l in temp.items():
            out["gene_link"] = input_data['hugo']
            out[k] = ';'.join(l)
        return out
    
    def cleanup(self):
        """
        cleanup is called after every input line has been processed. Use it to
        close database connections and file handlers. Automatically opened
        database connections are also automatically closed.
        """
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()