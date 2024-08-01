import sys
import os
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import re
import stouffer

class CravatAnnotator(BaseAnnotator):

    def setup(self):
        pvalue_basedir = os.path.join(self.data_dir,'VESTpvalue')
        self.pvalue_table = {}
        self.pvalue_table['MIS'] = self.get_pval_table(os.path.join(pvalue_basedir,'missense_hg38.pval.csv'))
        self.pvalue_table['FV'] = self.get_pval_table(os.path.join(pvalue_basedir,'frameshift_hg38.pval.csv'))
        self.pvalue_table['IV'] = self.get_pval_table(os.path.join(pvalue_basedir,'inframe_hg38.pval.csv'))
        self.pvalue_table['SPL'] = self.get_pval_table(os.path.join(pvalue_basedir,'splicesite_hg38.pval.csv'))
        self.pvalue_table['STG'] = self.get_pval_table(os.path.join(pvalue_basedir,'stopgain_hg38.pval.csv'))
        self.pvalue_table['STL'] = self.get_pval_table(os.path.join(pvalue_basedir,'stoploss_hg38.pval.csv'))
        self.transc_aa_so_re = re.compile('(.*):([A-Z,\*,_]*)(\d*)([A-Z,\*,_]*)\((.*)\)')
        self.transc_aa_re = re.compile('(.*):([A-Z,\*,_]*)(\d*)([A-Z,\*,_]*)')
        self.cannonical_chrom_re = re.compile('(?i)chr(\d{1,2}|x|y|un)')
    
    def annotate(self, input_data):
        chrom = input_data['chrom']
        if len(chrom) > 5:
            chrom_main = self.cannonical_chrom_re.match(chrom).group(0)
        else:
            chrom_main = chrom
        p = input_data['mapping_parser']
        
        primary_transcript = input_data['transcript']
        if primary_transcript is None:
            return
        primary_mapping = p.get_transcript_mapping(input_data['transcript'])
        primary_so = primary_mapping.so
        pos = input_data['pos']
        alt = input_data['alt_base']
        
        transc_ontologies = {}
        for mapping in p.mappings:
            sos = mapping.so.split(',')
            for so in sos:
                if so in ['MIS','STG','STL', 'missense_variant', 'stop_gained', 'stop_lost']:
                    transc_ontologies[mapping.transcript.split('.')[0]] = so
        if transc_ontologies == {}:
            return
                    
        q = 'select v.score, t.name from '+chrom_main+' as v join transcript '\
             +'as t on v.tid=t.tid join chrom as c on v.cid=c.cid where '\
             +'c.name="'+chrom+'" and v.pos='+str(pos)+' and v.alt="'+alt+'";'
        self.cursor.execute(q)
        qr = self.cursor.fetchall()
        if qr:
            precomp_data = []
            for r in qr:
                score = r[0]
                if score <= 0.302:
                    benign = "Moderate"
                    pathogenic = ""
                elif score > 0.302 and score <= 0.449:
                    benign = "Supporting"
                    pathogenic = ""
                elif score  >= 0.764 and score < 0.861: 
                    benign = ""
                    pathogenic = "Supporting"
                elif score >= 0.861 and score < 0.965:
                    benign = ""
                    pathogenic = "Moderate"
                elif score >= 0.965:
                    benign = ""
                    pathogenic = "Strong"
                else:
                    benign = ""
                    pathogenic = ""
                transc = r[1]
                transc_base = transc.split('.')[0]
                if transc_base not in transc_ontologies:
                    continue
                transc_so = transc_ontologies[transc_base]
                if transc_so in self.pvalue_table:
                    pval = self.pvalue_table[transc_so][score]
                else:
                    pval = 0.0
                transc_vest_result = [transc, score, pval, benign, pathogenic]
                precomp_data.append({'score':score,
                                     'transcript':transc,
                                     'pval':pval,
                                     'benign': benign,
                                     'pathogenic': pathogenic,
                                     'full_result':transc_vest_result})
            if precomp_data:
                scores = [x['score'] for x in precomp_data]
                all_results_list = [x['full_result'] for x in precomp_data]
                max_score = max(scores)
                max_index = scores.index(max_score)
                worst_mapping = precomp_data[max_index]
                worst_transcript = worst_mapping['transcript']
                worst_pval = worst_mapping['pval']
                worst_pathogenic = worst_mapping['pathogenic']
                worst_benign = worst_mapping['benign']

                #all_results_list[max_index] = '*'+all_results_list[max_index]
                ret = {
                    'transcript': worst_transcript,
                    'score': max_score,
                    'pval': worst_pval,
                    'pathogenic': worst_pathogenic,
                    'benign': worst_benign,
                    'all': all_results_list,
                    'hugo': input_data['hugo'],
                }
                return ret

    def get_pval_table(self, pfile):
        pval_tab=dict()
        
        pval_file = open(pfile, 'r')
        pval_file.readline()
        for line in pval_file:
            items=line.strip().split(',')
            score = float(items[0].strip('\"'))
            pval = float(items[1])
            pval_tab[score] = pval
    
        return pval_tab

    def summarize_by_gene (self, hugo, input_data):
        out = None
        in_scores = input_data['score']
        in_pvals = input_data['pval']
        scores = [s for s in in_scores if s is not None]
        pvals_non_unique = [v for v in in_pvals if v is not None]
        pvals = list(set(pvals_non_unique))
        if len(scores) > 0:
            out = {}
            raw_gene_pval = stouffer.stouffer(pvals)[1]
            out['max_score'] = max(scores)
            out['mean_score'] = round(sum(scores)/len(scores),3)
            out['gene_pval'] = round(raw_gene_pval, 3)
        return out

if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
