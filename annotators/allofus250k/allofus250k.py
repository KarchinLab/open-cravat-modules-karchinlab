import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def setup(self): 
        pass

    def annotate(self, input_data, secondary_data=None):
        chrom = input_data['chrom']
        pos = input_data['pos']
        ref_base = input_data['ref_base']
        alt_base = input_data['alt_base']

        query = f'select gvs_all_ac, gvs_all_an, gvs_all_af, gvs_max_af, gvs_max_ac, gvs_max_an, gvs_max_subpop, gvs_afr_ac, gvs_afr_an, gvs_afr_af, gvs_amr_ac, gvs_amr_an, gvs_amr_af, gvs_eas_ac, gvs_eas_an, gvs_eas_af, gvs_eur_ac, gvs_eur_an, gvs_eur_af, gvs_mid_ac, gvs_mid_an, gvs_mid_af, gvs_oth_ac, gvs_oth_an, gvs_oth_af, gvs_sas_ac, gvs_sas_an, gvs_sas_af from allofus250k where chrom="{chrom}" and pos={pos} and ref="{ref_base}" and alt="{alt_base}";'
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result is not None:
            gvs_all_ac = result[0]
            gvs_all_an = result[1]
            gvs_all_af = result[2]
            gvs_max_af = result[3]
            gvs_max_ac = result[4]
            gvs_max_an = result[5]
            gvs_max_subpop = result[6]
            gvs_afr_ac = result[7]
            gvs_afr_an = result[8]
            gvs_afr_af = result[9]
            gvs_amr_ac = result[10]
            gvs_amr_an = result[11]
            gvs_amr_af = result[12]
            gvs_eas_ac = result[13]
            gvs_eas_an = result[14]
            gvs_eas_af = result[15]
            gvs_eur_ac = result[16]
            gvs_eur_an = result[17]
            gvs_eur_af = result[18]
            gvs_mid_ac = result[19]
            gvs_mid_an = result[20]
            gvs_mid_af = result[21]
            gvs_oth_ac = result[22]
            gvs_oth_an = result[23]
            gvs_oth_af = result[24]
            gvs_sas_ac = result[25]
            gvs_sas_an = result[26]
            gvs_sas_af = result[27]

            return {
                'gvs_all_ac': gvs_all_ac,
                'gvs_all_an': gvs_all_an,
                'gvs_all_af': gvs_all_af,
                'gvs_max_af': gvs_max_af,
                'gvs_max_ac': gvs_max_ac,
                'gvs_max_an': gvs_max_an,
                'gvs_max_subpop': gvs_max_subpop,
                'gvs_afr_ac': gvs_afr_ac,
                'gvs_afr_an': gvs_afr_an,
                'gvs_afr_af': gvs_afr_af,
                'gvs_amr_ac': gvs_amr_ac,
                'gvs_amr_an': gvs_amr_an,
                'gvs_amr_af': gvs_amr_af,
                'gvs_eas_ac': gvs_eas_ac,
                'gvs_eas_an': gvs_eas_an,
                'gvs_eas_af': gvs_eas_af,
                'gvs_eur_ac': gvs_eur_ac,
                'gvs_eur_an': gvs_eur_an,
                'gvs_eur_af': gvs_eur_af,
                'gvs_mid_ac': gvs_mid_ac,
                'gvs_mid_an': gvs_mid_an,
                'gvs_mid_af': gvs_mid_af,
                'gvs_oth_ac': gvs_oth_ac,
                'gvs_oth_an': gvs_oth_an,
                'gvs_oth_af': gvs_oth_af,
                'gvs_sas_ac': gvs_sas_ac,
                'gvs_sas_an': gvs_sas_an,
                'gvs_sas_af': gvs_sas_af}
        else:
            return None

    def cleanup(self):
        pass

if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
