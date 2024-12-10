import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        dir_path = os.path.dirname(os.path.realpath(__file__))
        db_path = os.path.join(dir_path, "data", "phylop.sqlite")
        self.conn = sqlite3.connect(db_path)
        self.curs = self.conn.cursor()
        assert isinstance(self.conn, sqlite3.Connection)
        assert isinstance(self.curs, sqlite3.Cursor)
        self.curs.execute('select name from sqlite_master where type="table"')
        if hasattr(self, 'supported_chroms'):
            self.supported_chroms |= {r[0] for r in self.curs}
        else:
            self.supported_chroms = {r[0] for r in self.curs}
    
    def annotate(self, input_data, secondary_data=None):
        out = {}
        stmt = 'SELECT phylop100_vert, phylop100_vert_r, phylop470_mamm, phylop470_mamm_r, phylop17_primate, phylop17_primate_r FROM {chr} WHERE pos = {pos} AND alt = "{alt}"'.format(chr=input_data["chrom"], pos=int(input_data["pos"]), alt = input_data["alt_base"])
        self.curs.execute(stmt)
        row = self.curs.fetchone()
        if row is not None:
            phylop100Vert = float(row[0])
            if phylop100Vert <= 0.021:
                benign = 'Moderate'
                pathogenic = ''
            elif phylop100Vert > 0.021 and phylop100Vert <= 1.879:
                benign = 'Supporting'
                pathogenic = ''
            elif phylop100Vert >= 7.367 and phylop100Vert < 9.741:
                benign = ''
                pathogenic = 'Supporting'
            elif phylop100Vert >= 9.741:
                benign = ''
                pathogenic = 'Moderate'
            out['phylop100_vert'] = float(row[0])
            out['phylop100_vert_r'] = float(row[1])
            out['phylop470_mamm'] = float(row[2])
            out['phylop470_mamm_r'] = float(row[3])
            out['phylop17_primate'] = float(row[4])
            out['phylop17_primate_r'] = float(row[5])
            out['benign'] = benign
            out['pathogenic'] = pathogenic
        return out
    
    def cleanup(self):
        self.conn.close()
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
