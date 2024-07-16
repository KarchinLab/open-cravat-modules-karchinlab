import sys
import os
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3

col_order = [
    'af_go_esp',
    'af_exac',
    'af_tgp',
    'clinvar_allele_id',
    'disease_names',
    'clinvar_preferred_names',
    'disease_refs',
    'disease_refs_incl',
    'hgvs',
    'rev_stat',
    'sig',
    'sig_conf',
    'sig_incl',
    'variant_type',
    'variant_type_sequence_ontology',
    'variant_clinical_sources',
    'dbvar_id',
    'clinvar_gene_info',
    'molecular_consequences',
    'onc_disease_name',
    'onc_disease_name_incl',
    'onc_disease_refs',
    'onc_disease_refs_incl',
    'onc_classification',
    'onc_classification_type',
    'onc_rev_stat',
    'onc_classification_conflicting',
    'allele_origin',
    'dbsnp_id',
    'somatic_disease_name',
    'somatic_disease_name_incl',
    'somatic_refs',
    'somatic_refs_incl',
    'somatic_rev_stat',
    'somatic_impact',
    'somatic_impact_incl'
]
info_cols = ', '.join([f'{x}' for x in col_order[:]])


class CravatAnnotator(BaseAnnotator):

    def setup(self):
        self.cursor.execute('select name from sqlite_master where type="table"')
        if hasattr(self, 'supported_chroms'):
            self.supported_chroms |= {r[0] for r in self.cursor}
        else:
            self.supported_chroms = {r[0] for r in self.cursor}

    def annotate(self, input_data):
        chrom = input_data['chrom']
        self.cursor.execute(
            f'select {info_cols} from {chrom} where pos=? and ref=? and alt=?;',
            (input_data['pos'], input_data['ref_base'], input_data['alt_base'])
        )
        qr = self.cursor.fetchone()
        if qr is not None:
            data = {
                col_order[i]: qr[i] for i in range(0, len(col_order))
            }
            return data

        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
