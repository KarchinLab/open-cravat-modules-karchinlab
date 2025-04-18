import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os
import time


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
    (-0.3, "Moderate"),
    (0.99, "Supporting"),
    (float("inf"), "")
]

PP3_CUTOFFS = [
    (2.88, ""),
    (3.62, "Supporting"),
    (float("inf"), "Moderate"),
]

class CravatAnnotator(BaseAnnotator):    
    def annotate(self, input_data, secondary_data=None):
        out = {}
        achanges = []
        subs = {'H':'High', 'M':'Medium', 'L':'Low', 'N':'Neutral'}
        allmappings = eval(input_data['all_mappings'])
        hugo = input_data['hugo']
        if hugo:
            precomp = []
            for i in range(len(allmappings[hugo])):
                transcript = allmappings[hugo][i][3]
                achange = allmappings[hugo][i][1]
                achange = str(achange).replace('p.','')
                aa_321 = {
                'Asp': 'D', 'Ser': 'S', 'Gln': 'Q', 'Lys': 'K',
                'Trp': 'W', 'Asn': 'N', 'Pro': 'P', 'Thr': 'T',
                'Phe': 'F', 'Ala': 'A', 'Gly': 'G', 'Cys': 'C',
                'Ile': 'I', 'Leu': 'L', 'His': 'H', 'Arg': 'R',
                'Met': 'M', 'Val': 'V', 'Glu': 'E', 'Tyr': 'Y',
                'Ter': '*','':''}
                for key, value in aa_321.items():
                    achange = achange.replace(key, value)
                stmt = 'SELECT impact, score, rankscore FROM genes where gene = "{hugo}" and annotation = "{achange}"'.format(
                    hugo = input_data['hugo'], achange = achange)
                self.cursor.execute(stmt)
                row = self.cursor.fetchone()
                if row:
                    impact = row[0]
                    score = row[1]
                    rankscore = row[2]
                    mut_data = [transcript, impact, score, rankscore]
                    precomp.append({'transcript': transcript, 'impact': impact, 'score': score, 'rankscore': rankscore, 'full_result': mut_data})
            if precomp:
                all_transcripts = set()
                scores = [x['score'] for x in precomp]
                all_results_list = [x['full_result'] for x in precomp]
                max_score = max(scores)
                for x in precomp:
                    if x['score'] == max_score:
                        all_transcripts.add(x['transcript'])
                all_transcripts = list(all_transcripts)
                all_transcripts.sort()
                all_transcripts = ';'.join(all_transcripts)
                max_index = scores.index(max_score)
                worst_mapping = precomp[max_index]
                worst_rankscore = worst_mapping['rankscore']
                worst_impact = worst_mapping['impact']
                out = {
                    'transcript': all_transcripts,
                    'score': max_score,
                    'rankscore': worst_rankscore,
                    'impact': worst_impact,
                    'bp4_benign': discretize_scalar(max_score, BP4_CUTOFFS),
                    'pp3_pathogenic': discretize_scalar(max_score, PP3_CUTOFFS),
                    'all': all_results_list
                }
                return out
    
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
