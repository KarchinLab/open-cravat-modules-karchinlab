import sys
import os
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
from pathlib import Path
import tabix


class CravatAnnotator(BaseAnnotator):

    def setup(self):
        self.tabix_archives = {}
        data_path = Path(self.data_dir)
        for item in data_path.glob('*.vcf.gz'):
            chrom = item.name.split('.')[0]
            self.tabix_archives[chrom] = tabix.open(str(item))
        self.key_order = [
            'AN_joint_afr',
            'AN_joint_ami',
            'AN_joint_amr',
            'AN_joint_asj',
            'AN_joint_eas',
            'AN_joint_fin',
            'AN_joint_mid',
            'AN_joint_nfe',
            'AN_joint_sas',
            'AN_joint_remaining',
            'AC_joint_afr',
            'AC_joint_ami',
            'AC_joint_amr',
            'AC_joint_asj',
            'AC_joint_eas',
            'AC_joint_fin',
            'AC_joint_mid',
            'AC_joint_nfe',
            'AC_joint_sas',
            'AC_joint_remaining',
            'nhomalt_joint_afr',
            'nhomalt_joint_ami',
            'nhomalt_joint_amr',
            'nhomalt_joint_asj',
            'nhomalt_joint_eas',
            'nhomalt_joint_fin',
            'nhomalt_joint_mid',
            'nhomalt_joint_nfe',
            'nhomalt_joint_sas',
            'nhomalt_joint_remaining'
        ]

    def annotate(self, input_data):
        out = {}
        chrom = input_data['chrom']
        pos = input_data['pos']
        ref = input_data['ref_base']
        alt = input_data['alt_base']
        if chrom not in self.tabix_archives:
            return
        records = list(self.tabix_archives[chrom].query(chrom, pos - 1, pos))
        if len(records) == 0:
            return
        oc_data_l = None
        oc_data_d = None
        for record in records:
            if pos == int(record[1]) and ref == record[3] and alt == record[4]:
                for info_item in record[7].split(';'):
                    info_toks = info_item.split('=')
                    if info_toks[0] == 'OC_DATA':
                        oc_data_l = [int(_) for _ in info_toks[1].split(',')]
                        oc_data_d = dict(zip(
                            self.key_order,
                            oc_data_l,
                        ))
                        break
                break
        if oc_data_l is None or oc_data_d is None:
            return
        out = {
            # African
            'af_afr': oc_data_d['AC_joint_afr']/oc_data_d['AN_joint_afr'],
            'an_afr': oc_data_d['AN_joint_afr'],
            'ac_afr': oc_data_d['AC_joint_afr'],
            'nhomalt_afr': oc_data_d['nhomalt_joint_afr'],
            # Amish
            'af_ami': oc_data_d['AC_joint_ami']/oc_data_d['AN_joint_ami'],
            'an_ami': oc_data_d['AN_joint_ami'],
            'ac_ami': oc_data_d['AC_joint_ami'],
            'nhomalt_ami': oc_data_d['nhomalt_joint_ami'],
            # Ad-Mixed American
            'af_amr': oc_data_d['AC_joint_amr']/oc_data_d['AN_joint_amr'],
            'an_amr': oc_data_d['AN_joint_amr'],
            'ac_amr': oc_data_d['AC_joint_amr'],
            'nhomalt_amr': oc_data_d['nhomalt_joint_amr'],
            # Ashkenazi Jewish
            'af_asj': oc_data_d['AC_joint_asj']/oc_data_d['AN_joint_asj'],
            'an_asj': oc_data_d['AN_joint_asj'],
            'ac_asj': oc_data_d['AC_joint_asj'],
            'nhomalt_asj': oc_data_d['nhomalt_joint_asj'],
            # East Asian
            'af_eas': oc_data_d['AC_joint_eas']/oc_data_d['AN_joint_eas'],
            'an_eas': oc_data_d['AN_joint_eas'],
            'ac_eas': oc_data_d['AC_joint_eas'],
            'nhomalt_eas': oc_data_d['nhomalt_joint_eas'],
            # Finnish
            'af_fin': oc_data_d['AC_joint_fin']/oc_data_d['AN_joint_fin'],
            'an_fin': oc_data_d['AN_joint_fin'],
            'ac_fin': oc_data_d['AC_joint_fin'],
            'nhomalt_fin': oc_data_d['nhomalt_joint_fin'],
            # Middle Eastern
            'af_mid': oc_data_d['AC_joint_mid']/oc_data_d['AN_joint_mid'],
            'an_mid': oc_data_d['AN_joint_mid'],
            'ac_mid': oc_data_d['AC_joint_mid'],
            'nhomalt_mid': oc_data_d['nhomalt_joint_mid'],
            # Non-Finnish European
            'af_nfe': oc_data_d['AC_joint_nfe']/oc_data_d['AN_joint_nfe'],
            'an_nfe': oc_data_d['AN_joint_nfe'],
            'ac_nfe': oc_data_d['AC_joint_nfe'],
            'nhomalt_nfe': oc_data_d['nhomalt_joint_nfe'],
            # South Asian
            'af_sas': oc_data_d['AC_joint_sas']/oc_data_d['AN_joint_sas'],
            'an_sas': oc_data_d['AN_joint_sas'],
            'ac_sas': oc_data_d['AC_joint_sas'],
            'nhomalt_sas': oc_data_d['nhomalt_joint_sas'],
            # Remaining
            'af_rem': oc_data_d['AC_joint_remaining']/oc_data_d['AN_joint_remaining'],
            'an_rem': oc_data_d['AN_joint_remaining'],
            'ac_rem': oc_data_d['AC_joint_remaining'],
            'nhomalt_rem': oc_data_d['nhomalt_joint_remaining'],
        }
        out['an'] = sum(oc_data_l[0:10])
        out['ac'] = sum(oc_data_l[10:20])
        out['nhomalt'] = sum(oc_data_l[20:30])
        out['af'] = out['ac']/out['an']
        return out
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()