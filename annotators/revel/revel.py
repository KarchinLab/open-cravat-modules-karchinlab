import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):
    def annotate(self, input_data, secondary_data=None):
        out = None
        # Don't run on alt contigs
        if len(input_data['chrom']) > 5: return None
        # Dont run on non-missense mutations
        ref = input_data['ref_base']
        alt = input_data['alt_base']
        if not(len(ref.replace('-','')) == 1 and len(ref.replace('-','')) == 1): return None
        q = 'select trans, score, rank from {tname} where pos={pos} and alt="{alt}"'.format(
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
                transcript = str(row[0])
                if transcript == None:
                    continue
                scores = [float(v) for v in str(row[1]).split(';')]
                rankscore = row[2]
                new = transcript.strip().split(';')
                for i in range(len(new)):
                    transc = new[i]
                    score = scores[i]
                    if score <= 0.003:
                        benign = "Very Strong"
                        pathogenic = ""
                    elif score > 0.003 and score <= 0.016:
                        benign = "Strong"
                        pathogenic = ""
                    elif score > 0.016 and score <= 0.183:
                        benign = "Moderate"
                        pathogenic = ""
                    elif score > 0.183 and score <= 0.290:
                        benign = "Supporting"
                        pathogenic = ""
                    elif score  >= 0.664 and score < 0.773: 
                        benign = ""
                        pathogenic = "Supporting"
                    elif score >= 0.773 and score < 0.932:
                        benign = ""
                        pathogenic = "Moderate"
                    elif score >= 0.932:
                        benign = ""
                        pathogenic = "Strong"
                    else:
                        benign = ""
                        pathogenic = ""
                    transc_revel_result = [transc, score, rankscore, benign, pathogenic]
                    precomp_data.append({'transcript':transc, 
                                         'score': score, 
                                         'rankscore': rankscore, 
                                         'benign': benign,
                                         'pathogenic': pathogenic, 
                                         'full_result' : transc_revel_result})
            if precomp_data:
                all_transcripts = set()
                scores = [x['score'] for x in precomp_data]
                all_results_list = [x['full_result'] for x in precomp_data]
                max_score = max(scores)
                for x in precomp_data:
                    if x['score'] == max_score:
                        all_transcripts.add(x['transcript'])
                all_transcripts = list(all_transcripts)
                all_transcripts.sort()
                all_transcripts = ';'.join(all_transcripts)
                max_index = scores.index(max_score)
                worst_mapping = precomp_data[max_index]
                worst_rankscore = worst_mapping['rankscore']
                worst_pathogenic = worst_mapping['pathogenic']
                worst_benign = worst_mapping['benign']
                out = {'transcript': all_transcripts, 'score': max_score, 'rankscore': worst_rankscore, 'pathogenic': worst_pathogenic, 'benign': worst_benign, 'all': all_results_list}
                return out

        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
