import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

query = '''SELECT
        patient,
        sample,
        supporting_reads_count,
        breakpoint_pubmed_id
    FROM st_judes_fusion
    WHERE l_chrom = ? AND l_pos = ? AND l_strand = ? and r_chrom = ? and r_pos = ? and r_strand = ?
'''

class CravatAnnotator(BaseAnnotator):

    def annotate(self, input_data, secondary_data=None):
        out = {}
        l_chrom = input_data['left_chrom']
        l_pos = input_data['left_break_pos']
        l_strand = input_data['left_break_strand']
        r_chrom = input_data['right_chrom']
        r_pos = input_data['right_break_pos']
        r_strand = input_data['right_break_strand']
        params = (l_chrom, l_pos, l_strand, r_chrom, r_pos, r_strand)
        patients = []
        samples = []
        supporting_read_counts = []
        pubmed_ids = []
        for (patient, sample, supporting_reads_count, breakpoint_pubmed_id) in self.cursor.execute(query, params):
            patients.append(patient)
            samples.append(sample)
            supporting_read_counts.append(supporting_reads_count)
            pubmed_ids.append(breakpoint_pubmed_id)

        out['patients'] = patients
        out['samples'] = samples
        out['supporting_read_counts'] = supporting_read_counts
        out['pubmed_ids'] = pubmed_ids
        return out

    def cleanup(self):
        pass


if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
