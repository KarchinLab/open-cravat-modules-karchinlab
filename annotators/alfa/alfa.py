import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

def _af(ac, an):
    return ac / an if an > 0 else None


class CravatAnnotator(BaseAnnotator):
    def annotate(self, input_data, secondary_data=None):
        out = {}
        q = 'select total from {chrom} where pos = {pos} and ref = "{ref}" and alt = "{alt}"'.format(
            chrom = input_data["chrom"], pos = int(input_data["pos"]), ref = input_data["ref_base"], alt = input_data["alt_base"])
        self.cursor.execute(q)
        row = self.cursor.fetchone()
        if row:
            total = str(row[0]).split(':')
            total_total = int(total[0])
            total_alt  = int(total[1])
            total_freq = _af(total_alt, total_total)
            out['total_alt'] = total_alt
            out['total_freq'] = total_freq
            return out
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()