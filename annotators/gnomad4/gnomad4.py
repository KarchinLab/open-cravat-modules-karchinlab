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
        self.af_keys = {
            'AF_joint':     'af',
            'AF_joint_afr': 'af_afr',
            'AF_joint_ami': 'af_ami',
            'AF_joint_amr': 'af_amr',
            'AF_joint_asj': 'af_asj',
            'AF_joint_eas': 'af_eas',
            'AF_joint_fin': 'af_fin',
            'AF_joint_mid': 'af_mid',
            'AF_joint_nfe': 'af_nfe',
            'AF_joint_sas': 'af_sas',
        }

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
        for record in records:
            if pos == int(record[1]) and ref == record[3] and alt == record[4]:
                for info_item in record[7].split(';'):
                    info_toks = info_item.split('=')
                    if info_toks[0] in self.af_keys:
                        out[self.af_keys[info_toks[0]]] = float(info_toks[1])
        # Fill missing AF with 0.0
        if len(out) > 0:
            for af_key in self.af_keys.values():
                out[af_key] = out.get(af_key,0.0)
        return out
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()