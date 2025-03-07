import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os
import json

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
            'all_annotations': json.dumps(all_annotations),
        }
        return out
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()