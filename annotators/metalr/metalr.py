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

## If our version of cravat is recent enough to have discretize_scalar,
## use that.
##
## TODO: replace with a direct import after broad distribution
try:
    from cravat.util import discretize_scalar as cravat_discretize_scalar
    discretize_scalar = cravat_discretize_scalar
except (ImportError, AttributeError):
    pass


BP4_CUTOFFS = [
    (0.0576, "Moderate"),
    (0.1762, "Supporting"),
    (float("inf"), "")
]

PP3_CUTOFFS = [
    (0.8198, ""),
    (0.9025, "Supporting"),
    (float("inf"), "Moderate"),
]

class CravatAnnotator(BaseAnnotator):
    def annotate(self, input_data, secondary_data=None):
        q = 'select metalr_score, metalr_rankscore, metalr_pred from {chr} where pos = {pos} and ref = "{ref}" and alt = "{alt}"'.format(
            chr=input_data["chrom"], pos=int(input_data["pos"]), ref = input_data["ref_base"], alt = input_data["alt_base"])
        self.cursor.execute(q)
        row = self.cursor.fetchone()
        if row:
            score = row[0]
            rankscore = row[1]
            
            # Determine prediction
            if row[2] == 'T':
                pred = 'Tolerated'
            elif row[2] == 'D':
                pred = 'Damaging'
            else:
                pred = None
            
            out = {
                'score': score, 
                'rankscore': rankscore, 
                'pred': pred,
                'bp4_benign': discretize_scalar(score, BP4_CUTOFFS),
                'pp3_pathogenic': discretize_scalar(score, PP3_CUTOFFS)
            }
        else:
            out = {}
        return out

    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
