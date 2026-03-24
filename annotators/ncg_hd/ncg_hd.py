import sys
from collections import defaultdict

from cravat import BaseAnnotator

class CravatAnnotator(BaseAnnotator):
    def format_data(self, data):
        out = {
            'entrez': data[0],
            'symbol': data[1],
            'organ_system': data[2],
            'organ_site': data[3],
            'tissue_type': data[4],
            'duplicability': data[5],
            'origin': data[6],
            'essential_celllines_percentage': data[7],
            'ppin_degree': data[8],
            'ppin_betweenness': data[9],
            'ppin_clustering': data[10],
            'complexes': data[11],
            'mirna': data[12],
            'expressed_tissues_mRNA_GTEx': data[13],
            'expressed_tissues_mRNA_protatlas': data[14],
            'expressed_tissues_protein_protatlas': data[15],
            'expressed_celllines_CLP': data[16],
            'expressed_celllines_GNE': data[17],
            'expressed_celllines_CCLE': data[18],
            'germline_SNVs': data[19],
            'germline_SVs': data[20],
            'LOEUF_score': data[21]
        }
        return out

    def annotate(self, input_data, secondary_data=None):
        hugo = input_data['hugo']
        query = '''
            SELECT 
                entrez, symbol, organ_system, organ_site, tissue_type, 
                duplicability, origin, essential_celllines_percentage, ppin_degree,
                ppin_betweenness, ppin_clustering, complexes, mirna, expressed_tissues_mRNA_GTEx,
                expressed_tissues_mRNA_protatlas, expressed_tissues_protein_protatlas, expressed_celllines_CLP,
                expressed_celllines_GNE, expressed_celllines_CCLE, germline_SNVs, germline_SVs, LOEUF_score
            FROM ncg
            WHERE symbol = ?;
            '''

        self.cursor.execute(query, (hugo,))
        data = self.cursor.fetchone()
        if not data:
            return None

        return self.format_data(data=data)


if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
