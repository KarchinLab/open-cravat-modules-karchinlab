import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        assert isinstance(self.dbconn, sqlite3.Connection)
        assert isinstance(self.cursor, sqlite3.Cursor)
    
    def annotate(self, input_data, secondary_data=None):
        out = {}
        stmt = 'SELECT uniprot_acc, ensembl_transcriptid, interpro_domain, count FROM {chr} WHERE pos = {pos} AND alt = "{alt}"'.format(chr=input_data["chrom"], pos=int(input_data["pos"]), alt = input_data["alt_base"])
        self.cursor.execute(stmt)
        rows = self.cursor.fetchall()
        if rows is not None:
            all_results = []
            domain_set = set()
            for row in rows:
                accs = str(row[0]).split(';')
                trs = str(row[1]).split(';')
                domain = str(row[2]).split(';')
                count = str(row[3]).split(';')
                for i in range(len(domain)):
                    if '|' in domain[i]:
                        multdomains = domain[i].split('|')
                        multcounts = count[i].split('|')
                        for j in range(len(multdomains)):
                            domain_set.add(multdomains[j])
                            hits = [multdomains[j], accs[i], trs[i], multcounts[j]]
                            all_results.append(hits)
                    else:
                        domain_set.add(domain[i])
                        hits = [domain[i], accs[i], trs[i], count[i]]
                        all_results.append(hits)
            if all_results:
                out['domain'] = ';'.join(domain_set)
                out['all'] = all_results
        return out
    
    def cleanup(self):
        self.dbconn.close()
        pass

    def summarize_by_gene (self, hugo, input_data):
        domains = []
        for domain in input_data['domain']:
            if domain is None:
                continue
            ds = domain.split(';')
            for d in ds:
                if d == '.':
                    continue
                es = d.split('|')
                for e in es:
                    if e not in domains:
                        domains.append(e)
        if len(domains) == 0:
            out = None
        else:
            out = {'domain': ';'.join(domains)}
            return out

if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
