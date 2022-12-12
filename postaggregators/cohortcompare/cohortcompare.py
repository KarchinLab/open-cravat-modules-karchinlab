import sys
import os
from cravat import BasePostAggregator
from cravat import InvalidData
import sqlite3
from collections import defaultdict
from pathlib import Path

class CravatPostAggregator (BasePostAggregator):

    def check(self):
        self.cursor.execute('select name from sqlite_master where type="table" and name="cohorts"')
        r = self.cursor.fetchone()
        return r is not None

    def setup (self):
        from scipy.stats import fisher_exact
        self.fisher_exact = fisher_exact
        self.cursor_samples = self.dbconn.cursor()
        q = 'select distinct base__sample_id from sample'
        self.cursor_samples.execute(q)
        self.all_samples = {r[0] for r in self.cursor_samples}
        self.cohorts = defaultdict(set)
        self.cursor.execute('select sample, cohort from cohorts;')
        for r in self.cursor:
            self.cohorts[r[1]].add(r[0])
        self.case_samples = self.all_samples & self.cohorts['case']
        self.cont_samples = self.all_samples & self.cohorts['control']
        notfound_case = len(self.cohorts['case'] - self.all_samples)
        notfound_cont = len(self.cohorts['control'] - self.all_samples)
        if (notfound_case + notfound_cont) > 0:
            msg = f'WARNING: Some {self.conf["title"]} samples were not found in the job. {notfound_case} case and {notfound_cont} control'
            self.logger.warn(msg)
            print(msg, file=sys.stderr)
        q = 'pragma table_info(sample);'
        self.cursor_samples.execute(q)
        samp_cols = {r[1] for r in self.cursor_samples}
        self.has_zygosity = 'base__zygosity' in samp_cols
        self.qt_samples_plain = 'select base__sample_id from sample where base__uid=?'
        self.qt_samples_zyg = 'select base__sample_id, base__zygosity from sample where base__uid=?'

        # Flag multi-allelic sites
        self.multiallelic_uids = set()
        q = 'select group_concat(base__uid) as uids, count(base__uid) as uid_count from mapping group by base__original_line having uid_count > 1;'
        for row in self.dbconn.execute(q):
            self.multiallelic_uids.update((int(x) for x in row[0].split(',')))
    
    def cleanup (self):
        pass
        
    def annotate (self, input_data):
        uid = input_data['base__uid']
        if self.has_zygosity:
            hom_samples = set()
            het_samples = set()
            self.cursor_samples.execute(self.qt_samples_zyg,(uid,))
            for sid, zyg in self.cursor_samples:
                if zyg=='hom':
                    hom_samples.add(sid)
                elif zyg=='het':
                    het_samples.add(sid)                
        else:
            self.cursor_samples.execute(self.qt_samples_plain,(uid,))
            hom_samples = {r[0] for r in self.cursor_samples}
            het_samples = set()
        hom_case = len(self.case_samples & hom_samples)
        het_case = len(self.case_samples & het_samples)
        ref_case = len(self.case_samples) - hom_case - het_case
        hom_cont = len(self.cont_samples & hom_samples)
        het_cont = len(self.cont_samples & het_samples)
        ref_cont = len(self.cont_samples) - hom_cont - het_cont
        dom_table = [
            [hom_case + het_case, ref_case],
            [hom_cont + het_cont, ref_cont]
        ]
        dom_pvalue = self.fisher_exact(dom_table,'greater')[1]
        rec_table = [
            [hom_case, ref_case + het_case],
            [hom_cont, ref_cont + het_cont]
        ]
        rec_pvalue = self.fisher_exact(rec_table,'greater')[1]
        all_table = [
            [2*hom_case + het_case, 2*ref_case + het_case],
            [2*hom_cont + het_cont, 2*ref_cont + het_cont]
        ]
        all_pvalue = self.fisher_exact(all_table,'greater')[1]
        multiallelic = 'Y' if uid in self.multiallelic_uids else None
        return {
            'dom_pvalue': dom_pvalue,
            'rec_pvalue': rec_pvalue,
            'all_pvalue': all_pvalue,
            'hom_case': hom_case,
            'het_case': het_case,
            'ref_case': ref_case,
            'hom_cont': hom_cont,
            'het_cont': het_cont,
            'ref_cont': ref_cont,
            'multiallelic': multiallelic,
        }

if __name__ == '__main__':
    summarizer = CravatPostAggregator(sys.argv)
    summarizer.run()
