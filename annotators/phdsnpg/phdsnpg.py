import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os


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


BP4_CUTOFFS = [
    (0.322, "Moderate"),
    (0.771, "Supporting"),
    (float("inf"), "")
]

PP3_CUTOFFS = [
    (0.968, ""),
    (,0.987 "Supporting"),
    (float("inf"), "Moderate"),
]


class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        assert isinstance(self.dbconn, sqlite3.Connection)
        assert isinstance(self.cursor, sqlite3.Cursor)
        all_tables_query = 'SELECT name FROM sqlite_master WHERE type="table";'
        self.cursor.execute(all_tables_query)
        if hasattr(self, 'supported_chroms'):
            self.supported_chroms |= {r[0] for r in self.cursor}
        else:
            self.supported_chroms = {r[0] for r in self.cursor}
    
    def annotate(self, input_data, secondary_data=None):
        out = {}
        chrom = input_data['chrom']
        alt = input_data['alt_base'].replace('-','')
        pos = input_data['pos']
        if len(alt) == 1 and chrom in self.supported_chroms:
            main_query = 'select pathogenic, score, fdr from {chrom} where pos={pos} and alt="{alt}";'.format(
                chrom = chrom,
                pos = pos,
                alt = alt,
            )
            self.cursor.execute(main_query)
            row = self.cursor.fetchone()
            if row is not None:
                if row[0] == 1:
                    out['prediction'] = 'Pathogenic'
                else:
                    out['prediction'] = 'Benign'
                out['score'] = row[1]
                out['fdr'] = row[2]
                out['bp4_benign'] = discretize_scalar(row[1], BP4_CUTOFFS)
                out['pp3_pathogenic'] = discretize_scalar(row[1], PP3_CUTOFFS)
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
