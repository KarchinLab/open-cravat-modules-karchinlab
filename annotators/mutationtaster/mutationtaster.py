import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

BP4_CUTOFFS = [
    (0.995135, "Supporting"),
    (float("inf"), "")
]

PP3_CUTOFFS = [
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
    def annotate(self, input_data, secondary_data=None):
        q = 'select transcript, score, rankscore, prediction, model from {chrom} where pos = {pos} and alt = "{alt}"'.format(
            chrom = input_data["chrom"], pos = int(input_data["pos"]), alt = input_data["alt_base"])
        self.cursor.execute(q)
        rows = self.cursor.fetchall()
        if rows:
            precomp_data = []
            out = {}
            for row in rows:
                transcripts = str(row[0]).strip().split(';')
                score = row[1]
                rankscore = row[2]
                prediction = row[3]
                if prediction == 'A':
                    prediction = 'Automatic Disease Causing'
                elif prediction == 'D':
                    prediction = "Damaging"
                elif prediction == 'P':
                    prediction = 'Automatic Polymorphism'
                elif prediction == 'N':
                    prediction = 'Polymorphism'
                model = row[4]
                for i in range(len(transcripts)):
                    transcript = transcripts[i]
                    mut = [transcript, score, rankscore, prediction, model]
                    precomp_data.append({'transcript': transcript, 'score': score, 'rankscore': rankscore, 'prediction': prediction, 'model': model, 'full_result': mut})
            if precomp_data:
                all_transcripts = set()
                scores = [x['score'] for x in precomp_data]
                all_results_list = [x['full_result'] for x in precomp_data]
                min_score = min(scores)
                for x in precomp_data:
                    if x['score'] == min_score:
                        all_transcripts.add(x['transcript'])
                all_transcripts = list(all_transcripts)
                all_transcripts.sort()
                all_transcripts = ';'.join(all_transcripts)
                max_index = scores.index(min_score)
                worst_mapping = precomp_data[max_index]
                worst_rankscore = worst_mapping['rankscore']
                worst_prediction = worst_mapping['prediction']
                worst_model = worst_mapping['model']
                out = {
                    'transcript': all_transcripts,
                    'score': min_score,
                    'rankscore': worst_rankscore,
                    'prediction': worst_prediction,
                    'model': worst_model,
                    'bp4_benign': discretize_scalar(min_score, BP4_CUTOFFS),
                    'pp3_pathogenic': discretize_scalar(min_score, PP3_CUTOFFS),
                    'all': all_results_list}
                return out


    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
