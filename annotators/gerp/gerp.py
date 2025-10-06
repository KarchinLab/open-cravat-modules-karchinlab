import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        assert isinstance(self.dbconn, sqlite3.Connection)
        assert isinstance(self.cursor, sqlite3.Cursor)
        self.cursor.execute('select name from sqlite_master where type="table"')
        if hasattr(self, 'supported_chroms'):
            self.supported_chroms |= {r[0] for r in self.cursor}
        else:
            self.supported_chroms = {r[0] for r in self.cursor}
    
    def annotate(self, input_data, secondary_data=None):
        out = {}
        self.logger.error(f"gerp annotate f{input_data}")
        stmt = 'SELECT gerp_nr, gerp_rs, gerp_rs_rank FROM {chr} WHERE pos = {pos} AND alt = "{alt}"'.format(chr=input_data["chrom"], pos=int(input_data["pos"]), alt = input_data["alt_base"])
        self.cursor.execute(stmt)
        row = self.cursor.fetchone()
        if row is not None:
            score = self.myCast(row[1])
            if score <= -4.54:
                benign = "Moderate"
            elif row[0] > -4.54 and row[0] <= 2.70:
                benign = "Supporting"
            else:
                benign = ""
            out['gerp_nr'] = self.myCast(row[0])
            out['gerp_rs'] = self.myCast(row[1])
            out['gerp_rs_rank'] = self.myCast(row[2])
            out['bp4_benign'] = benign
            out['bp4_pathogenic'] = ""
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
