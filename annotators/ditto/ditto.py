import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os
import tabix
class CravatAnnotator(BaseAnnotator):

    def setup(self):
        datafile = os.path.join(self.data_dir,'ditto.tsv.gz')
        self.tb = tabix.open(datafile)

    def annotate(self, input_data, secondary_data=None):
        chrom = input_data['chrom']
        pos = input_data['pos']
        ref = input_data['ref_base']
        alt = input_data['alt_base']
        out = {}
        precomp_data = []
        try:
            records = list(self.tb.query(chrom, pos - 1, pos))
        except tabix.TabixError:
            pass
        for record in records:
            if (record[3] == alt and record[2] == ref):
                transcripts = record[4]
                score = record[7]
                mut = [transcripts, score]
                precomp_data.append(mut)

        if precomp_data:
            scores = [x['score'] for x in precomp_data]
            max_score = max(scores)
            max_score_index = scores.index(max_score)
            out = {'transcript': precomp_data[max_score_index][0], 'score': precomp_data[max_score_index][1],'all': precomp_data}
            return out
        else:
            return None


    def cleanup(self):
        pass

if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
