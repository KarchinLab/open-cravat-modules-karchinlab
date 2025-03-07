import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os
import json

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        pass
    
    def annotate(self, input_data, secondary_data=None):
        chrom = input_data['chrom']
        q = f'select Ensembl_transcriptid, gMVP_score, gMVP_rankscore from {chrom} where pos=? and ref=? and alt=?'
        self.cursor.execute(q, (input_data['pos'],input_data['ref_base'],input_data['alt_base']))
        row = self.cursor.fetchone()
        if row is None:
            return None
        rank_score = row[2]
        all_annotations = []
        patho_score = None
        repr_transcript = None
        for transcript, score in zip(row[0].split(';'),row[1].split(';')):
            if score == '.':
                continue
            score = float(score)
            all_annotations.append([transcript, score])
            if patho_score is None or score > patho_score:
                patho_score = score
                repr_transcript = transcript
        out = {
            'transcript': repr_transcript,
            'score': patho_score,
            'rank_score': rank_score,
            'all_annotations': json.dumps(all_annotations),
        }
        return out
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()