import sys
from collections import defaultdict

from cravat import BaseAnnotator

class CravatAnnotator(BaseAnnotator):
    def format_data(self, data):
        out = {
            'entrez': data[0],
            'symbol': data[1],
            'organ_system': data[2],
            'primary_site': data[3],
            'cancer_type': data[4],
            'cgl_annotation': data[5],
            'saito_annotation': data[6],
            'ncg_annotation': data[7],
            'duplicability': data[8],
            'origin': data[9],
            'essential_celllines_percentage': data[10],
            'ppin_degree': data[11],
            'ppin_betweenness': data[12],
            'ppin_clustering': data[13],
            'complexes': data[14],
            'mirna': data[15],
            'expressed_tissues_mRNA_GTEx': data[16],
            'expressed_tissues_mRNA_protatlas': data[17],
            'expressed_tissues_protein_protatlas': data[18],
            'expressed_celllines_CLP': data[19],
            'expressed_celllines_GNE': data[20],
            'expressed_celllines_CCLE': data[21],
            'germline_SNVs': data[22],
            'germline_SVs': data[23],
            'LOEUF_score': data[24]
        }
        return out

    def annotate(self, input_data, secondary_data=None):
        hugo = input_data['hugo']
        query = '''
            SELECT 
                entrez, symbol, organ_system, primary_site, cancer_type, cgl_annotation, saito_annotation,
                ncg_annotation, duplicability, origin, essential_celllines_percentage, ppin_degree,
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
