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
    

PP3_CUTOFFS = [
    (-24.0, "Strong"),
    (-12.2, "Moderate"),
    (-10.7, "Supporting"),
    (float("inf"), "")
]

BP4_CUTOFFS = [
    (-6.3, ""),
    (-3.1, "Supporting"),
    (float("inf"), "Moderate"),
]

class CravatAnnotator(BaseAnnotator):
    def annotate(self, input_data, secondary_data=None):
        out = None
        q = 'select transcript_id, esm1b_score, esm1b_rankscore, esm1b_pred from {tname} where pos={pos} and alt="{alt}"'.format(
            tname = input_data['chrom'],
            pos = input_data['pos'],
            alt = input_data['alt_base'],
        )
        self.cursor.execute(q)
        out = {}
        rows = self.cursor.fetchall()
        if rows:
            precomp_data = []
            for row in rows:
                scores = [float(v) for v in str(row[1]).split(';')]
                rankscore = row[2]
                predictions = [v for v in str(row[3]).split(';')]
                transcripts = str(row[0]).strip().split(';')
                for i in range(len(transcripts)):
                    transc = transcripts[i]
                    score = scores[i]
                    if predictions[i] == "T":
                        prediction = "Tolerated"
                    elif predictions[i] == "D":
                        prediction = "Deleterious"
                    else:
                        prediction = ""
                    
                    transc_revel_result = [transc, score, rankscore, prediction]
                    precomp_data.append({
                        'transcript':transc,
                        'score': score,
                        'rankscore': rankscore,
                        'prediction': prediction,
                        'full_result' : transc_revel_result,
                        'bp4_benign': get_bin(score, BP4_CUTOFFS),
                        'pp3_pathogenic': get_bin(score, PP3_CUTOFFS)
                    })
            if precomp_data:
                all_transcripts = set()
                all_predictions = set()
                pathogenicity = ""
                scores = [x['score'] for x in precomp_data]
                all_results_list = [x['full_result'] for x in precomp_data]
                # min score is used because the smaller the score the more pathogenic it is.
                min_score = min(scores)
                for x in precomp_data:
                    if x['score'] == min_score:
                        all_transcripts.add(x['transcript'])
                        all_predictions.add(x['prediction'])
                        benign = x['bp4_benign']
                        pathogenic = x['pp3_pathogenic']
                all_transcripts = list(all_transcripts)
                all_transcripts = ';'.join(all_transcripts)
                all_predictions = list(all_predictions )
                all_predictions  = ';'.join(all_predictions)
                min_index = scores.index(min_score)
                best_mapping = precomp_data[min_index]
                rankscore = best_mapping['rankscore']
                return {
                    'transcript': all_transcripts,
                    'score': min_score,
                    'rankscore': rankscore,
                    'prediction': all_predictions,
                    'bp4_benign': benign,
                    'pp3_pathogenic': pathogenic,
                    'all': all_results_list
                }

        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
