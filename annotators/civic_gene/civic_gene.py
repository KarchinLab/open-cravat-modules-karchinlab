import sys
from cravat import BaseAnnotator

class CravatAnnotator(BaseAnnotator):
    def format_data(self, data_row):
        out = {
            'id': data_row[0],
            'name': data_row[1],
            'description': data_row[2],
            'aliases': data_row[3]
        }
        return out

    def annotate(self, input_data, secondary_data=None):
        hugo = input_data['hugo']
        name_query = 'SELECT id, name, description, aliases FROM civic_gene WHERE name == ?'
        name_params = (hugo,)
        self.cursor.execute(name_query, name_params)
        data = self.cursor.fetchone()
        if data is not None:
            return self.format_data(data_row=data)

        # try to query the aliases if no direct name match
        alias_query = 'SELECT id, name, description, aliases FROM civic_gene WHERE aliases LIKE ? OR aliases LIKE ? OR aliases LIKE ? OR aliases LIKE ?'
        # Check if the gene name provided is in the alias list as a whole word, either by itself, starting the list,
        # ending the list, or in the middle of the list. Do not allow it to be in the middle of a bigger word
        alias_params = (
            hugo,
            f'{hugo},%',
            f'%,{hugo},%',
            f'%,{hugo}',
        )
        self.cursor.execute(alias_query, alias_params)
        data = self.cursor.fetchone()
        if data is not None:
            return self.format_data(data_row=data)

        return None


if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
