import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os
import json

BP4_CUTOFFS = [
    (0.052789, "Strong"),
    (0.188378, "Moderate"),
    (0.295726, "Supporting"),
    (float("inf"), "")
]

PP3_CUTOFFS = [
    (0.655095, ""),
    (0.786338, "Supporting"),
    (0.934075, "Moderate"),
    (float("inf"), "Strong"),
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
        self.prediction_map = {'D':'Damaging','T':'Tolerated'}
    
    def annotate(self, input_data, secondary_data=None):
        chrom = input_data['chrom']
        q = f'select Ensembl_transcriptid, MetaRNN_score, MetaRNN_rankscore, MetaRNN_pred from {chrom} where pos=? and ref=? and alt=?'
        self.cursor.execute(q, (input_data['pos'],input_data['ref_base'],input_data['alt_base']))
        row = self.cursor.fetchone()
        if row is None:
            return None
        rank_score = row[2]
        all_annotations = []
        patho_score = None
        repr_transcript = None
        repr_pred = None
        for transcript, score, pred_letter in zip(row[0].split(';'),row[1].split(';'),row[3].split(';')):
            if score == '.':
                continue
            score = float(score)
            pred = self.prediction_map.get(pred_letter,None)
            all_annotations.append([transcript, score, pred])
            if patho_score is None or score > patho_score:
                patho_score = score
                repr_transcript = transcript
                repr_pred = pred
        out = {
            'transcript': repr_transcript,
            'score': patho_score,
            'rank_score': rank_score,
            'pred': repr_pred,
            "bp4_benign": discretize_scalar(patho_score, BP4_CUTOFFS),
            "pp3_pathogenic": discretize_scalar(patho_score, PP3_CUTOFFS),
            'all_annotations': json.dumps(all_annotations),
        }
        return out
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
