import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import os
import tabix
class CravatAnnotator(BaseAnnotator):

    def setup(self):
        datafile = os.path.join(self.data_dir,'dittodb.tsv.gz')
        self.tb = tabix.open(datafile)

    def annotate(self, input_data, secondary_data=None):
        chrom = input_data['chrom']
        pos = int(input_data['pos'])
        ref = input_data['ref_base']
        alt = input_data['alt_base']
        out = {}
        precomp_data = []
        records = []
        try:
            records = list(self.tb.query(chrom, pos - 1, pos))
        except tabix.TabixError:
            pass
        if records:
            max_score = 0
            max_transcript = ''
            for record in records:
                if (record[3] == alt and record[2] == ref):
                    transcripts = record[4]
                    score = float(record[7])
                    mut = [transcripts, score]
                    precomp_data.append(mut)
                    if score > max_score:
                        max_score = score
                        max_transcript = transcripts

            if precomp_data:
                out = {'transcript': max_transcript, 'score': max_score,'all': precomp_data}
                return out
        else:
            return None


    def cleanup(self):
        pass

if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
