import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        assert isinstance(self.dbconn, sqlite3.Connection)
        assert isinstance(self.cursor, sqlite3.Cursor)
    
    def annotate(self, input_data, secondary_data=None):
        out = {}
        stmt = 'SELECT gerp_nr, gerp_rs, gerp_rs_rank FROM {chr} WHERE pos = {pos} AND alt = "{alt}"'.format(chr=input_data["chrom"], pos=int(input_data["pos"]), alt = input_data["alt_base"])
        self.cursor.execute(stmt)
        row = self.cursor.fetchone()
        if row is not None:
            out['gerp_nr'] = self.myCast(row[0])
            out['gerp_rs'] = self.myCast(row[1])
            out['gerp_rs_rank'] = self.myCast(row[2])
            return out
    
    def cleanup(self):
        self.dbconn.close()
        pass
        
    def myCast(self, item):
        if item is None:
            return item
        else:
            return float(item)

if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()