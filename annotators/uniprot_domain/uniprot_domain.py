import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os
from collections import defaultdict
from intervaltree import IntervalTree

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        bedfile = os.path.join(self.data_dir, 'UP000005640_9606_domain.bed')
        self.itrees = defaultdict(IntervalTree)
        with open(bedfile) as f:
            for l in f:
                toks = l.strip().split()
                chrom = toks[0]
                beg = int(toks[1])
                end = int(toks[2])
                domain = ' '.join(toks[13:])
                try:
                    self.itrees[chrom][beg:end] = domain
                except:
                    pass
    
    def annotate(self, input_data, secondary_data=None):
        intervals = self.itrees[input_data['chrom']][input_data['pos']]
        if len(intervals) > 0:
            out = {}
            out['domain'] = list(intervals)[0].data
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