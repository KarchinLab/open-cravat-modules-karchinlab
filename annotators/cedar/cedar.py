import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os
import csv
from pathlib import Path
import json
import re

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
        q = f'select epi_id from {chrom} where pos=? and ref=? and alt=?'
        self.cursor.execute(q, (input_data['pos'], input_data['ref_base'], input_data['alt_base']))
        r = self.cursor.fetchone()
        if r:
            out['epi_id'] = r[0]
            return out
        mappings = json.loads(input_data['all_mappings'])
        for gene in mappings:
            for mapping in mappings[gene]:
                print(mapping[1])
                match = re.match(r'p\.[A-Za-z]{3}(\d+)[A-Za-z]{3}',mapping[1])
                if match:
                    print(mapping)
                    apos = match.group(1)
                    print(apos)
                    ensp = self.t2p.get(mapping[3])
                    if ensp:
                        q = 'select epi_id from {chrom} where apos={apos} and ensp={ensp}'
                        self.cursor.execute(q)
                        r = self.cursor.fetchone()
                        if r:
                            out['epi_id'] = r[0]
                            return out


    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()