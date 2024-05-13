import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

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
                    transc_revel_result = [transc, score, rankscore, prediction]
                    precomp_data.append({'transcript':transc, 'score': score, 'rankscore': rankscore, 'prediction': prediction, 'full_result' : transc_revel_result})
            if precomp_data:
                all_transcripts = set()
                all_predictions = set()
                scores = [x['score'] for x in precomp_data]
                all_results_list = [x['full_result'] for x in precomp_data]
                # min score is used because the smaller the score the more pathogenic it is.
                min_score = min(scores)
                for x in precomp_data:
                    if x['score'] == min_score:
                        all_transcripts.add(x['transcript'])
                        all_predictions.add(x['prediction'])
                all_transcripts = list(all_transcripts)
                all_transcripts = ';'.join(all_transcripts)
                all_predictions = list(all_predictions )
                all_predictions  = ';'.join(all_predictions)
                min_index = scores.index(min_score)
                best_mapping = precomp_data[min_index]
                rankscore = best_mapping['rankscore']
                out = {'transcript': all_transcripts, 'score': min_score, 'rankscore': rankscore, 'prediction': all_predictions, 'all': all_results_list}
                return out

        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()