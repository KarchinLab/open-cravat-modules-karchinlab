import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        pass
        self.chroms = set(['chr'+str(n) for n in range(1,23)]+['chrX','chrY','chrM'])
    
    def annotate(self, input_data, secondary_data=None):
        out = {}
        chrom = input_data['chrom']
        pos = input_data['pos']
        ref = input_data['ref_base']
        alt = input_data['alt_base']
        if (len(ref) != 1 and len(alt) != 1) or (chrom not in self.chroms):
            return out
        self.cursor.execute(f'select transcript, score, rankscore, med, seqs from {chrom} where pos=? and ref=? and alt=?', [pos, ref, alt])
        rows = self.cursor.fetchall()
        if rows:
            precomp_data = []
            for row in rows:
                transcript = str(row[0])
                if transcript == None:
                    continue
                score = row[1]
                if score <= 0.05:
                    prediction = 'Damaging'
                else:
                    prediction = 'Tolerated'
                rankscore = row[2]
                if score >= 0.327:
                    benign = 'Moderate'
                    pathogenic = ''
                elif score >= 0.080 and score < 0.327:
                    benign = 'Supporting'
                    pathogenic = ''
                elif score > 0 and score <= 0.001:
                    benign = ''
                    pathogenic ='Supporting'
                elif score == 0:
                    benign = ''
                    pathogenic ='Moderate'
                else:
                    benign = ''
                    pathogenic = ''
                med = row[3]
                if med <= 3.25:
                    confidence = 'High'
                else:
                    confidence = 'Low'
                seqs = row[4]
                new = transcript.strip().split(';')
                for i in range(len(new)):
                    transc = new[i]
                    transc_revel_result = [transc, score, prediction, rankscore, med, confidence, seqs, benign, pathogenic]
                    precomp_data.append({'transcript':transc, 'score': score, 'prediction': prediction, 'rankscore': rankscore, 'med': med, 'confidence': confidence,'seqs': seqs,'benign': benign, 'pathogenic': pathogenic, 'full_result' : transc_revel_result})
            if precomp_data:
                all_transcripts = set()
                scores = [x['rankscore'] for x in precomp_data]
                all_results_list = [x['full_result'] for x in precomp_data]
                max_score = max(scores)
                for x in precomp_data:
                    if x['rankscore'] == max_score:
                        all_transcripts.add(x['transcript'])
                all_transcripts = list(all_transcripts)
                all_transcripts.sort()
                all_transcripts = ';'.join(all_transcripts)
                max_index = scores.index(max_score)
                worst_mapping = precomp_data[max_index]
                worst_score = worst_mapping['score']
                worst_prediction = worst_mapping['prediction']
                worst_med = worst_mapping['med']
                worst_confidence = worst_mapping['confidence']
                worst_seqs = worst_mapping['seqs']
                worst_pathogenic = worst_mapping['pathogenic']
                worst_benign = worst_mapping['benign']
                if all_results_list:
                    out['transcript'] = all_transcripts
                    out['score'] = worst_score
                    out['prediction'] = worst_prediction
                    out['rankscore'] = max_score
                    out['med'] = worst_med
                    out['confidence'] = worst_confidence
                    out['seqs'] = worst_seqs
                    out['benign'] = worst_benign
                    out['pathogenic'] = worst_pathogenic
                    out['all'] = all_results_list
                    out['multsite'] = 'True' if len(all_results_list) > 1 else None
                    return out
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()