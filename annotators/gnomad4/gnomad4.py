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
        self.af_keys = set([
            'AF',
            'AF_afr',
            'AF_ami',
            'AF_amr',
            'AF_asj',
            'AF_eas',
            'AF_fin',
            'AF_mid',
            'AF_nfe',
            'AF_sas',
            ])

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
            if int(record[1]) == pos and record[3] == ref and record[4] == alt:
                for info_item in record[7].split(';'):
                    info_toks = info_item.split('=')
                    if info_toks[0] in self.af_keys:
                        out[info_toks[0].lower()] = float(info_toks[1])
        if len(out) > 0:
            for af_key in self.af_keys:
                out[af_key.lower()] = out.get(af_key.lower(),0.0)
        return out
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()