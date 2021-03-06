import sys
from cravat import BaseAnnotator
from cravat.util import get_ucsc_bins

class CravatAnnotator(BaseAnnotator):

    def setup(self):
        pass
    
    def annotate(self, input_data, secondary_data=None):
        if not secondary_data or len(secondary_data['hg19']) == 0:
            return
        chrom = secondary_data['hg19'][0]['chrom']
        pos = secondary_data['hg19'][0]['pos']
        if chrom is None or pos is None:
            return
        lowbin = get_ucsc_bins(pos)[0]
        self.cursor.execute(
            f'select s.cell, s.quality, s.antibody, s.dccAccession, s.factor from {chrom} as c join studies as s on c.study=s.id where c.bin=? and c.beg<=? and c.end>?',
            [lowbin, pos, pos],
        )
        rows = self.cursor.fetchall()
        if rows:
            studies = sorted([list(v) for v in rows], key=lambda x: x[2])
            factor = sorted(list(set(map(lambda x: x[4], rows))), key=str.lower)
            return {
                'factor': factor,
                'all': studies,
            }
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
