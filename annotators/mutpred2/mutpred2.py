import sys
from cravat import BaseAnnotator
from cravat import InvalidData
from cravat.util import discretize_scalar
import sqlite3
import os
import re

class CravatAnnotator(BaseAnnotator):

    def setup(self):
        pass
    
    def annotate(self, input_data, secondary_data=None):
        query = (
            'SELECT transcript, score, rankscore, prediction, top_5_mechanisms '
            f'FROM {input_data["chrom"]} WHERE pos = ?AND ref = ?AND alt = ?;'
        )

        self.cursor.execute(query, (input_data['pos'], input_data['ref_base'], input_data['alt_base']))
        rows = self.cursor.fetchall()
        out = {}
        if not rows:
            return {}
        else:
            all_mappings = []
            for result in rows:
                single_mapping = {
                    'transcript': result[0],
                    'score': result[1],
                    'rankscore': result[2],
                    'prediction': result[3],
                    'top_5': result[4]
                }
                all_mappings.append(single_mapping)

            # find the max score
            max_index = -1
            max_score = -1
            for i in range(len(all_mappings)):
                m = all_mappings[i]
                if m['score'] > max_score:
                    max_index = i

            max_mapping = all_mappings[max_index]
            out = {
                'score': max_mapping['score'],
                'prediction': max_mapping['prediction'],
                'rankscore': max_mapping['rankscore'],
                'top5_mechanisms': max_mapping['top_5'],
                'all_annotations': all_mappings
            }
            return out
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
