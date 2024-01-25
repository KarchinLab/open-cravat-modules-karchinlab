import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def setup(self):
        self.cursor.execute('select name from sqlite_master where type="table" and name like "chr%"')
        if hasattr(self, 'supported_chroms'):
            self.supported_chroms |= {r[0] for r in self.cursor}
        else:
            self.supported_chroms = {r[0] for r in self.cursor}
    
    def annotate(self, input_data, secondary_data=None):
        if len(input_data['ref_base']) != 1 or len(input_data['alt_base']) != 1:
            return
        chrom = input_data['chrom']
        self.cursor.execute(f'''
            SELECT
                c.am_pathogenicity,
                am.am_class,
                t.transcript_id,
                u.uniprot_id,
                c.protein_variant
            FROM
                {chrom} AS c
                JOIN am_class AS am
                    ON c.am_fk = am.am_fk
                JOIN transcript AS t
                    ON c.transcript_fk = t.transcript_fk
                JOIN uniprot AS u
                    ON c.uniprot_fk = u.uniprot_fk
            WHERE
                    c.pos = ?
                AND c.ref = ?
                AND c.alt = ?
            ;''', (input_data['pos'], input_data['ref_base'], input_data['alt_base'])
        )
        row = self.cursor.fetchone()
        if row:
            return {
                'am_pathogenicity': row[0],
                'am_class': row[1],
                'transcript_id': row[2],
                'uniprot_id': row[3],
                'protein_variant': row[4],
            }
    
    def cleanup(self):
        """
        cleanup is called after every input line has been processed. Use it to
        close database connections and file handlers. Automatically opened
        database connections are also automatically closed.
        """
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()