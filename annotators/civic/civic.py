import sys
from cravat import BaseAnnotator


class CravatAnnotator(BaseAnnotator):
    def annotate(self, input_data, secondary_data=None):
        q = '''SELECT
                id,
                description,
                molecular_profile_score,
                diseases,
                chromosome,
                start,
                reference_base,
                reference_build,
                variant_base
            FROM civic
            WHERE chromosome = ? AND start = ? AND reference_base = ? AND variant_base = ?
        '''
        chrom = input_data['chrom']
        pos = input_data['pos']
        ref = input_data['ref_base']
        alt = input_data['alt_base']
        params = (chrom, pos, ref, alt)
        self.cursor.execute(q, params)
        row = self.cursor.fetchone()
        if row:
            out = {
                'id': row[0],
                'description': row[1],
                'molecular_profile_score': row[2],
                'diseases': row[3]
            }
            return out


if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
