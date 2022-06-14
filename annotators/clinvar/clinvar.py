import sys
import os
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3

class CravatAnnotator(BaseAnnotator):

    def annotate(self, input_data):
        chrom = input_data['chrom']
        self.cursor.execute(
            f'select sig, disease_refs, disease_names, rev_stat, id, sig_conf from {chrom} where pos=? and ref=? and alt=?;',
            (input_data['pos'], input_data['ref_base'], input_data['alt_base'])
        )
        qr = self.cursor.fetchone()
        if qr is not None:
            return {
                'sig':qr[0],
                'disease_refs':qr[1],
                'disease_names':qr[2],
                'rev_stat':qr[3],
                'id': qr[4],
                'sig_conf':qr[5]
            }

        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
