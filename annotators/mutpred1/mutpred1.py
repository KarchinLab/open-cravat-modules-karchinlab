import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os
import re


def discretize_scalar(score, cutoffs):
    """Locate the location of `score` in a list[tuple(float, str)] of
    `cutoffs`, where the float cutoff is the maximum value, inclusive
    of the value, for that label. The last tuple should typically have
    `float("inf")` as the cutoff, otherwise the function may retun
    `None`

    The cutoffs must be sorted in increasing value.
    """
    prev_cutoff = None
    for cutoff, label in cutoffs:
        if score <= cutoff:
            return label
        if prev_cutoff is not None and prev_cutoff > cutoff:
            raise ValueError("cutoffs are not sorted")
        prev_cutoff = cutoff


## If our version of cravat is recent enough to have discretize_scalar,
## use that.
##
## TODO: replace with a direct import after broad distribution
try:
    from cravat.util import discretize_scalar as cravat_discretize_scalar
    discretize_scalar = cravat_discretize_scalar
except (ImportError, AttributeError):
    pass


BP4_CUTOFFS = [
    (0.222, "Moderate"),
    (0.395, "Supporting"),
    (float("inf"), "")
]

PP3_CUTOFFS = [
    (0.707, ""),
    (0.82, "Supporting"),
    (float("inf"), "Moderate")
]

class CravatAnnotator(BaseAnnotator):

    def setup(self):
        self.cursor.execute('select mech_id, mech_name from mechanisms')
        self.mid2mech = {row[0]:row[1] for row in self.cursor}
        pass
    
    def expand_mechanisms(self, mechs_compact):
        matches = re.finditer(r'{(\d+)}', mechs_compact)
        mechs_full = mechs_compact
        for match in matches:
            mid = int(match.group(1))
            mech_name = self.mid2mech[mid]
            placeholder = match.group(0)
            mechs_full = mechs_full.replace(placeholder, mech_name)
        return mechs_full

    def annotate(self, input_data, secondary_data=None):
        # input_data['chrom'] is formatted as chr1, chr2, chrX etc. The chrom
        # column of the database omits the 'chr'. Need to convert formats.
        #chrom = input_data['chrom'].replace('chr', '')

        # Construct the query as a string
        #prot_query = 'select external_protein_id from mutpred_precomputed where chr="%s" and position="%s" and ref="%s" and alt="%s"' % chrom, pos, ref_base, alt_base
        #aa_query = 'select amino_acid_substitution from mutpred_precomputed where chr="%s" and position="%s" and ref="%s" and alt="%s"' % chrom, pos, ref_base, alt_base
        #general_query = 'select mutpred_general_score from mutpred_precomputed where chr="%s" and position="%s" and ref="%s" and alt="%s"' % chrom, pos, ref_base, alt_base
        #mech_query = 'select mutpred_top5_mechanisms from mutpred_precomputed where chr="%s" and position="%s" and ref="%s" and alt="%s"' % chrom, pos, ref_base, alt_base
        query = 'select transcript, external_protein_id, amino_acid_substitution, mutpred_general_score, mutpred_top5_mechanisms, mutpred_rankscore from {chr} where pos = {pos} and alt = "{alt}"'.format(
            chr = input_data["chrom"], pos = int(input_data["pos"]), alt = input_data["alt_base"])
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        transcript = None
        external_protein_id = None
        amino_acid_substitution = None
        mutpred_general_score = None
        mutpred_top5_mechanisms = None
        mutpred_rankscore = None
        if rows:
            out = {}
            precomp_data = []
            for result in rows:
                transcript = result[0]
                # Absent values are returned as None from the db
                external_protein_id = result[1]
                amino_acid_substitution = result[2]
                mutpred_general_score = result[3]
                mutpred_rankscore = result[5]
                # Top 5 mechanisms stored in compact form, must be expanded
                mutpred_top5_mechanisms = []
                top5tmp = self.expand_mechanisms(result[4])
                new = transcript.strip().split(';')
                for i in range(len(new)):
                    transc = new[i]
                    for r in [v.strip() for v in top5tmp.split(';')]:
                        [v1, v2] = r.split('(')
                        mechanism = v1.strip()
                        pvalue = float(v2.split('=')[1].split(')')[0])
                        mutpred_top5_mechanisms = [transc,external_protein_id, mechanism, pvalue, mutpred_general_score, mutpred_rankscore]
                        precomp_data.append({'transcript': transc, 'external_protein_id': external_protein_id, 'amino_acid_substitution': amino_acid_substitution, 'mutpred_general_score': mutpred_general_score, 'mutpred_rankscore': mutpred_rankscore, 'full_result':mutpred_top5_mechanisms})
                if precomp_data:
                    all_transcripts = set()
                    scores = [x['mutpred_rankscore'] for x in precomp_data]
                    all_results_list = [x['full_result'] for x in precomp_data]
                    max_rankscore = max(scores)
                    for x in precomp_data:
                        if x['mutpred_rankscore'] == max_rankscore:
                            all_transcripts.add(x['transcript'])
                    all_transcripts = list(all_transcripts)
                    all_transcripts.sort()
                    all_transcripts = ';'.join(all_transcripts)
                    max_index = scores.index(max_rankscore)
                    worst_mapping = precomp_data[max_index]
                    worst_score = worst_mapping['mutpred_general_score']
                    worst_protein_id = worst_mapping['external_protein_id']
                    worst_aa = worst_mapping['amino_acid_substitution']
                    out['transcript'] = all_transcripts
                    out['external_protein_id'] = worst_protein_id
                    out['amino_acid_substitution'] = worst_aa
                    out['mutpred_general_score'] = worst_score
                    out['bp4_benign'] = discretize_scalar(worst_score, BP4_CUTOFFS)
                    out['pp3_benign'] = discretize_scalar(worst_score, PP3_CUTOFFS)
                    if mutpred_top5_mechanisms is not None:
                        out['mutpred_top5_mechanisms'] = all_results_list
                    else:
                        out['mutpred_top5_mechanisms'] = all_results_list
                    out['mutpred_rankscore'] = max_rankscore
            return out
    
    def cleanup(self):
        """
        cleanup is called after every input line has been processed. Use it to
        close database connections and file handlers. Automatically opened
        database connections are also automatically closed.
        """
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
