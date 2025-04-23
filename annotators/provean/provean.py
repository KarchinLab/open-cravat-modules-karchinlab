import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):    
    def annotate(self, input_data, secondary_data=None):
        ref = input_data['ref_base']
        alt = input_data['alt_base']
        if ref == '-' or alt == '-':
            return None
        q = 'select trans, uniprot, score, rankscore, prediction from {chrom} where pos = {pos} and alt = "{alt}"'.format(
            chrom = input_data["chrom"], pos = int(input_data["pos"]), alt = input_data["alt_base"])
        self.cursor.execute(q)
        rows = self.cursor.fetchall()
        if rows is not None:
            out = {}
            precomp_data = []
            for row in rows:
                transcript = row[0]
                uniprot = row[1]
                score = row[2]
                rankscore = row[3]
                prediction = row[4]
                if prediction == 'D':
                    prediction = 'Damaging'
                elif prediction == 'N':
                    prediction = 'Neutral'
                provean = [transcript, uniprot, score, rankscore, prediction]
                precomp_data.append({'transcript': transcript, 'uniprot': uniprot, 'score': score, 'rankscore': rankscore, 'prediction': prediction, 'full_result': provean})
            if precomp_data:
                scores = [x['score'] for x in precomp_data]
                all_results_list = [x['full_result'] for x in precomp_data]
                min_scores = min(scores)
                min_index = scores.index(min_scores)
                worst_mapping = precomp_data[min_index]
                worst_transcript = worst_mapping['transcript']
                worst_uniprot = worst_mapping['uniprot']
                worst_rankscore = worst_mapping['rankscore']
                worst_prediction = worst_mapping['prediction']
                out = {'transcript': worst_transcript, 'uniprot': worst_uniprot, 'score': min_scores, 'rankscore': worst_rankscore,'prediction': prediction, 'all': all_results_list, 'bp4_benign': None, 'pp3_pathogenic': None }
                return out

                
                

    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
