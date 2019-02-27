import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        dir_path = os.path.dirname(os.path.realpath(__file__))
        db_path = os.path.join(dir_path, "data", "phastcons100-phastcons20_sqlite.db")
        self.conn = sqlite3.connect(db_path)
        self.curs = self.conn.cursor()
        assert isinstance(self.conn, sqlite3.Connection)
        assert isinstance(self.curs, sqlite3.Cursor)
    
    def annotate(self, input_data, secondary_data=None):
        out = {}
        stmt = 'SELECT phastcons100_vert, phastcons100_vert_r, phastcons30_mamm, phastcons30_mamm_r,phastcons17way_primate,phastcons17way_primate_r FROM {chr} WHERE pos = {pos} AND alt = "{alt}"'.format(chr=input_data["chrom"], pos=int(input_data["pos"]), alt = input_data["alt_base"])
        self.curs.execute(stmt)
        row = self.curs.fetchone()
        if row is not None:
            out['phastcons100_vert'] = float(row[0])
            out['phastcons100_vert_r'] = float(row[1])
            out['phastcons30_mamm'] = float(row[2])
            out['phastcons30_mamm_r'] = float(row[3])
            out['phastcons17way_primate'] = float(row[4])
            out['phastcons17way_primate_r'] = float(row[5])
        return out
    
    def cleanup(self):
        self.conn.close()
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()