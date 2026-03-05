import sys
from collections import defaultdict

from cravat import BaseAnnotator

class CravatAnnotator(BaseAnnotator):
    def format_data(self, data):
        out = {
            'entrez': data[0][0],
            'symbol': data[0][1],
            'pubmed_id': ';'.join([row[2] for row in data]),
            'type': ';'.join([row[3] for row in data]),
            'organ_system': ';'.join([row[3] for row in data]),
            'primary_site': ';'.join([row[4] for row in data]),
            'cancer_type': ';'.join([row[5] for row in data]),
            'method': ';'.join([row[6] for row in data]),
            'coding_status': ';'.join([row[7] for row in data]),
            'cgc_annotation': ';'.join([row[8] for row in data]),
            'vogelstein_annotation': ';'.join([row[9] for row in data]),
            'saito_annotation': ';'.join([row[10] for row in data]),
            'NCG_oncogene': ';'.join([row[11] for row in data]),
            'NCG_tsg': ';'.join([row[12] for row in data])
        }
        return out

    def annotate(self, input_data, secondary_data=None):
        hugo = input_data['hugo']
        query = '''
            SELECT entrez, symbol, pubmed_id, type, organ_system, primary_site,
                cancer_type, method, coding_status, cgc_annotation, vogelstein_annotation, saito_annotation,
                NCG_oncogene, NCG_tsg
            FROM ncg
            WHERE symbol = ?
            '''

        self.cursor.execute(query, (hugo,))
        data = self.cursor.fetchall()
        if len(data) == 0:
            return None

        return self.format_data(data=data)


if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
