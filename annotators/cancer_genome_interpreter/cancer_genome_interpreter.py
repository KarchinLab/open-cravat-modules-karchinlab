import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):
    def annotate(self, input_data, secondary_data=None):
        q = 'select association, biomarker, drug, evidence, source, tumor from cgi where chrom = "{chrom}" and pos = {pos} and ref = "{ref}" and alt = "{alt}"'.format(
            chrom = input_data["chrom"], pos = int(input_data["pos"]), ref = input_data["ref_base"], alt = input_data["alt_base"])
        self.cursor.execute(q)
        rows = self.cursor.fetchall()
        if rows is not None:
            all_results = []
            for row in rows:
                assoc = row[0]
                biomarker = row[1]
                drug = row[2]
                evidence = row[3]
                source = row[4]
                tumor = row[5]
                full_result = [assoc, biomarker, drug, evidence, source, tumor]
                all_results.append({'association': assoc, 'biomarker': biomarker, 'drug': drug, 'evidence': evidence, 'source': source, 'tumor': tumor, 'full_result': full_result})

        if all_results:
            all_results_list = [x['full_result'] for x in all_results]
            best_mapping = all_results[0]
            assoc = best_mapping["association"]
            biomarker = best_mapping["biomarker"]
            drug = best_mapping["drug"]
            evidence = best_mapping["evidence"]
            source = best_mapping["source"]
            tumor = best_mapping["tumor"]
            return {'association': assoc, 'biomarker': biomarker, 'drug': drug, 'evidence': evidence, 'source': source, 'tumor': tumor, 'all': all_results_list}

    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
