import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import urllib.parse

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        pass
    
    def annotate(self, input_data, secondary_data=None):
        pos_range = '{chrom}:{beg}-{end}'.format(
            chrom = input_data['chrom'],
            beg = input_data['pos'],
            end = input_data['gposend'],
        )
        out = {
            'link': pos_range,
        }
        return out
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()