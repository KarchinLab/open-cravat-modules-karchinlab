import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        dir_path = os.path.dirname(os.path.realpath(__file__))
        db_path = os.path.join(dir_path, "data", "FATHMM.db")
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
        stmt = 'SELECT ens_tid, ens_pid, fathmm_score, fathmm_rscore, fathmm_pred FROM {chr} WHERE pos = {pos} AND alt = "{alt}"'.format(chr=input_data["chrom"], pos=int(input_data["pos"]), alt = input_data["alt_base"])
        self.curs.execute(stmt)
        row = self.curs.fetchone()
        if row is not None:
            pathogenicity_list = []
            scores = row[2].split(";")
            for val in scores:
                score = float(val)
                if score >= 4.69:
                    pathogenicity_list.append("BP4 Moderate")
                elif score >= 3.32 and score < 4.69:
                    pathogenicity_list.append("BP4 Supporting")
                elif score > -5.04 and score >= -4.14:
                    pathogenicity_list.append("PP3 Supporting")
                elif score <= -5.04:
                    pathogenicity_list.append("PP3 Moderate")
                else:
                    pathogenicity_list.append("Indeterminate")
            out['ens_tid'] = row[0]
            out['ens_pid'] = row[1]
            out['fathmm_score'] = row[2]
            out['fathmm_rscore'] = float(row[3])
            out['fathmm_pred'] = row[4]
            out['fathmm_pathogenicity'] = ';'.join(pathogenicity_list)
        return out
    
    def cleanup(self):
        self.conn.close()
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()