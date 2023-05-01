import sys
from cravat import BaseAnnotator

class CravatAnnotator(BaseAnnotator):

    def annotate(self, input_data, secondary_data=None):
        out = {}
        q = '''SELECT
                allele_registry_id,
                disease,
                mode_of_inheritance,
                assertion,
                evidence_codes,
                summary_of_interpretation,
                chrom,
                pos,
                ref,
                alt
            FROM allele_registry
            WHERE chrom = ? AND pos = ? AND ref = ? AND alt = ?
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
                'allele_registry_id': row[0],
                'disease': row[1],
                'mode_of_inheritance': row[2],
                'assertion': row[3],
                'evidence_codes': row[4],
                'summary_of_interpretation': row[5]
            }
        return out

    
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
