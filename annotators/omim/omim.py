import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def setup(self):
        self.cursor.execute('select distinct chr from omim where chr not null;')
        if hasattr(self, 'supported_chroms'):
            self.supported_chroms |= {r[0] for r in self.cursor}
        else:
            self.supported_chroms = {r[0] for r in self.cursor}

    def annotate(self, input_data, secondary_data=None):
        q = 'select omim_id from omim where chr = "{chr}" and pos = {pos} and ref = "{ref}" and alt = "{alt}"'.format(
            chr = input_data["chrom"], pos=int(input_data["pos"]), ref = input_data["ref_base"], alt = input_data["alt_base"])
        self.cursor.execute(q)
        row = self.cursor.fetchone()
        if row:
            omim_id = str(row[0]).replace('|', '; ')
            out = {'omim_id': omim_id}
        else:
            out = None
        return out
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()