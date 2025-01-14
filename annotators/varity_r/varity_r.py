import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os


def get_bin(score, cutoffs):
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
    return labels[-1]  ## when we run out of cutoffs


PATHOGENICITY_CUTOFFS = [
    (0.036, 'BP4 Strong (-4 Benign)'),
    (0.063, 'BP4 [Firm] (-3 Benign)'),
    (0.116, 'BP4 Moderate (-2 Benign)'),
    (0.251, 'BP4 Supporting (-1 Benign)'),
    (0.675, 'Indeterminate (0)'),
    (0.841, 'PP3 Supporting (+1 Pathogenic)'),
    (0.914, 'PP3 Moderate (+2 Pathogenic)'),
    (0.964, 'PP3 [Firm] (+3 Pathogenic) '),
    (float("inf"), 'PP3 Strong (+4 Pathogenic)')
]

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        pass
    
    def annotate(self, input_data, secondary_data=None):
        chrom = input_data['chrom']
        pos = input_data['pos']
        ref = input_data['ref_base']
        alt = input_data['alt_base']
        self.cursor.execute(f'select p_vid, varity_r, varity_er, varity_r_loo, varity_er_loo from {chrom} where pos=? and ref=? and alt=?',
            (pos, ref, alt),
        )
        row = self.cursor.fetchone()
        if row is not None:
            return {
                'p_vid': row[0],
                'varity_r': row[1],
                'varity_r_pathogenicity': get_bin(row[1], PATHOGENICITY_CUTOFFS),
                'varity_er': row[2],
                'varity_r_loo': row[3],
                'varity_er_loo': row[4],
            }
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
