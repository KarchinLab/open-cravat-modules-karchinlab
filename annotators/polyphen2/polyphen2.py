import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

pred_order = {'D': 1, 'P': 2, 'B': 3}

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        pass
    
    def annotate(self, input_data, secondary_data=None):
        global pred_order
        if len(input_data['ref_base']) > 1 and not(input_data['ref_base'] == '-'):
            return
        q = f'select uniprot, hdiv_score, hdiv_rankscore, hdiv_prediction, hvar_score, hvar_rankscore, hvar_prediction, trans from {input_data["chrom"]} where pos=? and alt=?'
        self.cursor.execute(q, (input_data['pos'], input_data['alt_base']))
        rows = self.cursor.fetchall()
        if len(rows) > 0:
            precomp_data = []
            for r in rows:
                uniprots = r[0].split(';')
                transcripts = r[7].split(';')
                hdiv_scores = [float(v) for v in str(r[1]).split(';')]
                hdiv_rank = r[2]
                hdiv_preds = r[3].split(';')
                hvar_scores = [float(v) for v in str(r[4]).split(';')]
                hvar_rank = r[5]
                hvar_preds = r[6].split(';')
                hdiv_pred = hdiv_preds[0]
                for i in range(len(transcripts)):
                    transc = transcripts[i]
                    if len(hdiv_scores) == 1:
                        hdiv_s = hdiv_scores[0]
                        uniprot = uniprots[0]
                    else:
                        hdiv_s = hdiv_scores[i]
                        uniprot = uniprots[i]
                    if len(hvar_scores) == 1:
                        hvar_s = hvar_scores[0]
                    else:
                        hvar_s = hvar_scores[i]
                    for v in hdiv_preds[1:]:
                        if pred_order[v] < pred_order[hdiv_pred]:
                            hdiv_pred = v
                    hvar_pred = hvar_preds[0]
                    for v in hvar_preds[1:]:
                        if pred_order[v] < pred_order[hvar_pred]:
                            hvar_pred = v
                    transc_poly_result = [transc, uniprot, hdiv_s, hdiv_rank, hdiv_pred, hvar_s, hvar_rank, hvar_pred]
                    precomp_data.append({'transcript':transc, 'uniprots': uniprot, 'hdiv_score': hdiv_s, 'hdiv_rank': hdiv_rank, 'hdiv_pred': hdiv_pred, 'hvar_score': hvar_s, 'hvar_rank': hvar_rank, 'hvar_pred': hvar_pred, 'full_result' : transc_poly_result})
                if precomp_data:
                    hdivscores = [x['hdiv_rank'] for x in precomp_data]
                    hvarscores = [x['hvar_rank'] for x in precomp_data]
                    all_results_list = [x['full_result'] for x in precomp_data]
                    hdiv_max_score = max(hdivscores)
                    hvar_max_score = max(hvarscores)
                    hdiv_max_index = hdivscores.index(hdiv_max_score)
                    hvar_max_index = hvarscores.index(hvar_max_score)
                    hdiv_worst_mapping = precomp_data[hdiv_max_index]
                    hvar_worst_mapping = precomp_data[hvar_max_index]
                    hdiv_worst_score = hdiv_worst_mapping['hdiv_score']
                    hdiv_worst_pred = hdiv_worst_mapping['hdiv_pred']
                    hvar_worst_score = hvar_worst_mapping['hvar_score']
                    hvar_worst_pred = hvar_worst_mapping['hvar_pred']
                    out = {'transcript':transc, 'uniprots': uniprots, 'hdiv_score': hdiv_worst_score, 'hdiv_rank': hdiv_max_score, 'hdiv_pred': hdiv_worst_pred,'hvar_score': hvar_worst_score, 'hvar_rank': hvar_max_score, 'hvar_pred': hvar_worst_pred, 'all' : all_results_list}
            return out

        
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
