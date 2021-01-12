import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def annotate(self, input_data):
        out = {}
        hugo = input_data['hugo']
        
        q = 'select primarysites, primarysitenos, occurrences from cosmic_accession where genename="%s";' \
            %(hugo)
        self.cursor.execute(q)
        result = self.cursor.fetchone()
        if result:
            (primarysites, primarysitenos, occurences) = result
            gclist = []
            pslist = primarysites.split(';')
            psnlist = primarysitenos.split(';')
            for i, site in enumerate(pslist):
                #list.append("%s(%s)" % (site, psnlist[i]))
                gclist.append([site, psnlist[i]])
            #out['gene_count'] = ';'.join(list)
            out['gene_count'] = sorted(gclist, key=lambda x: int(x[1]), reverse=True)
            out['occurrences'] = occurences
        return out

if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
