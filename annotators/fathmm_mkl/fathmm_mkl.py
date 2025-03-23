import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

BP4_CUTOFFS = [
    (0, "Strong"),
    (0.4274, "Moderate"),
    (0.806, "Supporting"),
    (float("inf"), "")
]

PP3_CUTOFFS = [
    (0.9722, ""),
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


class CravatAnnotator(BaseAnnotator):
    def annotate(self, input_data, secondary_data=None):
        q = 'select fathmm_mkl_coding_score, fathmm_mkl_coding_rankscore, fathmm_mkl_coding_pred, fathmm_mkl_group from {chr} where pos = {pos} and ref = "{ref}" and alt = "{alt}"'.format(
            chr = input_data["chrom"], pos = int(input_data["pos"]), ref = input_data["ref_base"], alt = input_data["alt_base"])
        self.cursor.execute(q)
        row = self.cursor.fetchone()
        if row:
            if row[2] == 'D':
                pred = 'Damaging'
            elif row[2] == 'N':
                pred = 'Neutral'
            else:
                pred = None
            return {
                'fathmm_mkl_coding_score': row[0],
                'fathmm_mkl_coding_rankscore': row[1],
                'fathmm_mkl_coding_pred': pred,
                'fathmm_mkl_group': row[3]
                'bp4_pathogenic': discretize_scalar(row[0], BP4_CUTOFFS),
                'pp3_pathogenic': discretize_scalar(row[0], PP3_CUTOFFS),
            }
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
