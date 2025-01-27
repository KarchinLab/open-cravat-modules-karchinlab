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


BP4_CUTOFFS = [
    (0.036, 'Strong'),
    (0.116, 'Moderate '),
    (0.251, 'Supporting'),
    (float("inf"), '')
]

PP3_CUTOFFS = [
    (0.675, ''),
    (0.841, 'Supporting'),
    (0.964, 'Moderate'),
    (float("inf"), 'Strong')
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
            varity_r = float(row[1])
            return {
                'p_vid': row[0],
                'varity_r': varity_r,
                'bp4_benign': get_bin(varity_r, BP4_CUTOFFS),
                'pp3_pathogenic': get_bin(varity_r, PP3_CUTOFFS),
                'varity_er': row[2],
                'varity_r_loo': row[3],
                'varity_er_loo': row[4],
            }
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
