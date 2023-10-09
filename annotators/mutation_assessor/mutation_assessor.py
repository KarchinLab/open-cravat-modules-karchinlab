import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os
import time

class CravatAnnotator(BaseAnnotator):    
    def annotate(self, input_data, secondary_data=None):
        out = {}
        achanges = []
        subs = {'H':'High', 'M':'Medium', 'L':'Low', 'N':'Neutral'}
        allmappings = eval(input_data['all_mappings'])
        hugo = input_data['hugo']
        if hugo:
            precomp = []
            for i in range(len(allmappings[hugo])):
                transcript = allmappings[hugo][i][3]
                achange = allmappings[hugo][i][1]
                achange = str(achange).replace('p.','')
                aa_321 = {
                'Asp': 'D', 'Ser': 'S', 'Gln': 'Q', 'Lys': 'K',
                'Trp': 'W', 'Asn': 'N', 'Pro': 'P', 'Thr': 'T',
                'Phe': 'F', 'Ala': 'A', 'Gly': 'G', 'Cys': 'C',
                'Ile': 'I', 'Leu': 'L', 'His': 'H', 'Arg': 'R',
                'Met': 'M', 'Val': 'V', 'Glu': 'E', 'Tyr': 'Y',
                'Ter': '*','':''}
                for key, value in aa_321.items():
                    achange = achange.replace(key, value)
                stmt = 'SELECT impact, score, rankscore FROM genes where gene = "{hugo}" and annotation = "{achange}"'.format(
                    hugo = input_data['hugo'], achange = achange)
                self.cursor.execute(stmt)
                row = self.cursor.fetchone()
                if row:
                    impact = row[0]
                    score = row[1]
                    rankscore = row[2]
                    mut_data = [transcript, impact, score, rankscore]
                    precomp.append({'transcript': transcript, 'impact': impact, 'score': score, 'rankscore': rankscore, 'full_result': mut_data})
            if precomp:
                all_transcripts = set()
                scores = [x['score'] for x in precomp]
                all_results_list = [x['full_result'] for x in precomp]
                max_score = max(scores)
                for x in precomp:
                    if x['score'] == max_score:
                        all_transcripts.add(x['transcript'])
                all_transcripts = list(all_transcripts)
                all_transcripts.sort()
                all_transcripts = ';'.join(all_transcripts)
                max_index = scores.index(max_score)
                worst_mapping = precomp[max_index]
                worst_rankscore = worst_mapping['rankscore']
                worst_impact = worst_mapping['impact']
                out = {'transcript': all_transcripts, 'score': max_score, 'rankscore': worst_rankscore,'impact': worst_impact, 'all': all_results_list}
                return out
    
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()