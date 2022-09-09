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
                if assoc not in ("Resistant", "Responsive"):
                    assoc = "Other"
                all_results.append({"Association": assoc, "full_result": full_result})

        if all_results:
            all_results_list = [x['full_result'] for x in all_results]
            assoc = [x['Association'] for x in all_results]
            resistant = assoc.count("Resistant")
            responsive = assoc.count("Responsive")
            other = assoc.count("Other")
            return {'resistant': resistant, 'responsive': responsive, 'other': other, 'all': all_results_list}

    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
