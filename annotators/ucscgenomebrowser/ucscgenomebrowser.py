import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import urllib.parse

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        pass
    
    def annotate(self, input_data, secondary_data=None):
        display_range = '{chrom}:{beg}-{end}'.format(
            chrom = input_data['chrom'],
            beg = input_data['pos']-10,
            end = input_data['gposend']+10,
        )
        highlight_range = '{chrom}:{beg}-{end}'.format(
            chrom = input_data['chrom'],
            beg = input_data['pos'],
            end = input_data['gposend'],
        )
        out = {
            'link': f'https://genome.ucsc.edu/cgi-bin/hgTracks?db=hg38&position={display_range}&highlight={highlight_range}',
        }
        return out
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()