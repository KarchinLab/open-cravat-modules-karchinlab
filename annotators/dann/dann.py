import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os
import tabix

BP4_CUTOFFS = [
    (0.356222, "Strong"),
    (0.90647, "Moderate"),
    (0.949523, "Supporting"),
    (float("inf"), "")
]

PP3_CUTOFFS = [
    (0.99145, ""),
    (float("inf"), "Supporting"),
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
        datafile = os.path.join(self.data_dir,'dann.tsv.bgz')
        self.tb = tabix.open(datafile) 
    
    def annotate(self, input_data, secondary_data=None):
        chrom = input_data['chrom'][3:]
        pos = input_data['pos']
        ref = input_data['ref_base']
        alt = input_data['alt_base']
        try:
            records = list(self.tb.query(chrom, pos - 1, pos))
        except tabix.TabixError:
            pass
        for record in records:
            if record[3] == alt:
                score = float(record[4])
                return {
                    'score': score,
                    'bp4_benign': discretize_scalar(score, BP4_CUTOFFS),
                    'pp3_pathogenic': discretize_scalar(score, PP3_CUTOFFS)
                }

    
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
