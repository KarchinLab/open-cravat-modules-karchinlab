
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
    (float("inf"), "")
]

PP3_CUTOFFS = [
    (0.5804, ""),
    (0.8573, "Supporting"),
    (float("inf"), "Moderate")
]

class CravatAnnotator(BaseAnnotator):
    
    def annotate(self, input_data, secondary_data=None):
        q = 'select metasvm_score, metasvm_rankscore, metasvm_pred from {chr} where pos = {pos} and ref = "{ref}" and alt = "{alt}"'.format(
            chr = input_data["chrom"] ,pos=int(input_data["pos"]), alt = input_data["alt_base"], ref = input_data["ref_base"])
        self.cursor.execute(q)
        row = self.cursor.fetchone()
        if row:
            if row[2] == 'T':
                pred = 'Tolerated'
            elif row[2] == 'D':
                pred = 'Damaging'
            else:
                pred = None
            out = {
                'score': row[0],
                'rankscore': row[1],
                'pred': pred,
                "bp4_benign": discretize_scalar(row[0], BP4_CUTOFFS),
                "pp3_pathogenic": discretize_scalar(row[0], PP3_CUTOFFS),
            }
            return out
    
    def cleanup(self):
        pass


        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
