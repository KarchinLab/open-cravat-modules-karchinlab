import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os
import csv
from pathlib import Path
import json
import re
from cravat.util import aa_321

class CravatAnnotator(BaseAnnotator):

    def setup(self):
        self.t2p = {}
        with open(Path(self.data_dir)/'prot2trans.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['proteinId']:
                    ensp = row['proteinId'].split('.')[0]
                    enst = row['transcriptId'].split('.')[0]
                    self.t2p[enst] = ensp
    
    def annotate(self, input_data, secondary_data=None):
        out = {}
        chrom = input_data['chrom']
        q = f'select epi_id, epi_ref, epi_alt, pubmed_id from {chrom} where pos=? and ref=? and alt=?'
        self.cursor.execute(q, (input_data['pos'], input_data['ref_base'], input_data['alt_base']))
        r = self.cursor.fetchone()
        if r:
            out = {
                'epi_id': r[0],
                'epi_ref': r[1],
                'epi_alt': r[2],
                'pubmed_id': r[3],
            }
            return out
        mappings = json.loads(input_data['all_mappings'])
        for gene in mappings:
            for mapping in mappings[gene]:
                match = re.match(r'p\.([A-Za-z]{3})(\d+)([A-Za-z]{3})',mapping[1])
                if match:
                    aa_ref = aa_321[match.group(1)]
                    aa_pos = int(match.group(2))
                    aa_alt = aa_321[match.group(3)]
                    ensp = self.t2p.get(mapping[3].split('.')[0])
                    if ensp:
                        q = f'select epi_id, epi_ref, epi_alt, pubmed_id from {chrom} where ensp=? and aa_pos=? and aa_ref=? and aa_alt=?'
                        self.cursor.execute(q, (ensp, aa_pos, aa_ref, aa_alt))
                        r = self.cursor.fetchone()
                        if r:
                            out = {
                                'epi_id': r[0],
                                'epi_ref': r[1],
                                'epi_alt': r[2],
                                'pubmed_id': r[3],
                            }
                            return out

    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()