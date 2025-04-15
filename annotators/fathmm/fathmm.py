import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

BP4_CUTOFFS = [
    (3.32, ""),
    (4.69, "Supporting"),
    (float("inf"), "Moderate")
]

PP3_CUTOFFS = [
    (-5.04, "Moderate"),
    (-4.14, "Supporting"),
    (float("inf"), ""),
]


def discretize_scalar(score, cutoffs):
    """Locate the location of `score` in a list[tuple(float, str)] of
    `cutoffs`, where the float cutoff is the maximum value, inclusive
    of the value, for that label. The last tuple should typically have
    `float("inf")` as the cutoff, otherwise the function may retun
    `None`

    The cutoffs must be sorted in increasing value.
    """
    prev_cutoff = None
    for cutoff, label in cutoffs:
        if score <= cutoff:
            return label
        if prev_cutoff is not None and prev_cutoff > cutoff:
            raise ValueError("cutoffs are not sorted")
        prev_cutoff = cutoff


## If our version of cravat is recent enough to have discretize_scalar,
## use that.
##
## TODO: replace with a direct import after broad distribution
try:
    from cravat.util import discretize_scalar as cravat_discretize_scalar
    discretize_scalar = cravat_discretize_scalar
except (ImportError, AttributeError):
    pass

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
            min_score = min([float(x) for x in row[2].split(";")])
            out['ens_tid'] = row[0]
            out['ens_pid'] = row[1]
            out['fathmm_score'] = row[2]
            out['fathmm_rscore'] = float(row[3])
            out['fathmm_pred'] = row[4]
            out['bp4_benign'] = discretize_scalar(min_score, BP4_CUTOFFS)
            out['pp3_pathogenic'] = discretize_scalar(min_score, PP3_CUTOFFS)
        return out
    
    def cleanup(self):
        self.conn.close()
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
