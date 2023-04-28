import sys
import os
from cravat import BasePostAggregator
from cravat import InvalidData
import sqlite3

class CravatPostAggregator (BasePostAggregator):

    def check(self):
        self.cursor.execute('select colval from info where colkey="_converter_format"')
        return self.cursor.fetchone()[0] == 'vcf'
    
    def setup(self):
        # For single sample inputs, make columns filterable. Set some columns
        # to filterable types. By default columns are all string and not
        # filterable
        new_col_types = {
            'phred': 'float',
            'alt_reads': 'int',
            'tot_reads': 'int',
            'af': 'float',
            'hap_block': 'int',
            'hap_strand': 'int',
        }
        self.cursor.execute('select count(distinct base__sample_id) from sample;')
        n_samples = self.cursor.fetchone()[0]
        self.multi_sample = n_samples > 1
        if not self.multi_sample:
            for col in self.conf["output_columns"]:
                col_base_name = col['name'].split('__')[1]
                col['type'] = new_col_types.get(col_base_name, col['type'])
                col['filterable'] = True

    def annotate (self, input_data):
        uid = str(input_data['base__uid'])
        q = 'select base__sample_id, base__phred, base__filter, ' +\
            'base__zygosity, ' +\
            'base__alt_reads, base__tot_reads, base__af, ' +\
            'base__hap_block, base__hap_strand from sample ' +\
            'where base__uid=' + uid
        self.cursor.execute(q)
        phred_l = []
        filter_l = []
        zygosity_l = []
        alt_reads_l = []
        tot_reads_l = []
        af_l = []
        hap_block_l = []
        hap_strand_l = []
        for row in self.cursor.fetchall():
            (sample, phred, filt, zygosity, altread, totread, af, hap_block, hap_strand) = row
            phred_l.append(phred)
            filter_l.append(filt)
            zygosity_l.append(zygosity)
            alt_reads_l.append(altread)
            tot_reads_l.append(totread)
            af_l.append(af)
            hap_block_l.append(hap_block)
            hap_strand_l.append(hap_strand)
        if self.multi_sample:
            phred = ';'.join(['' if v == None else str(v) for v in phred_l])
            s = list(set(phred))
            if len(s) == 0 or (len(s) == 1 and s[0] == ';'):
                phred = None
            filter = ';'.join(['' if v == None else str(v) for v in filter_l])
            s = list(set(filter))
            if len(s) == 0 or (len(s) == 1 and s[0] == ';'):
                filter = None
            zygosity = ';'.join(['' if v == None else str(v) for v in zygosity_l])
            s = list(set(zygosity))
            if len(s) == 0 or (len(s) == 1 and s[0] == ';'):
                zygosity = None
            alt_reads = ';'.join(['' if v == None else str(v) for v in alt_reads_l])
            s = list(set(alt_reads))
            if len(s) == 0 or (len(s) == 1 and s[0] == ';'):
                alt_reads = None
            tot_reads = ';'.join(['' if v == None else str(v) for v in tot_reads_l])
            s = list(set(tot_reads))
            if len(s) == 0 or (len(s) == 1 and s[0] == ';'):
                tot_reads = None
            af = ';'.join(['' if v == None else str(v) for v in af_l])
            s = list(set(af))
            if len(s) == 0 or (len(s) == 1 and s[0] == ';'):
                af = None
            hap_block = ';'.join(['' if v == None else str(v) for v in hap_block_l])
            s = list(set(hap_block))
            if len(s) == 0 or (len(s) == 1 and s[0] == ';'):
                hap_block = None
            hap_strand = ';'.join(['' if v == None else str(v) for v in hap_strand_l])
            s = list(set(hap_strand))
            if len(s) == 0 or (len(s) == 1 and s[0] == ';'):
                hap_strand = None
        else:
            phred = phred_l[0] if len(phred_l) > 0 else None
            filter = filter_l[0] if len(filter_l) > 0 else None
            zygosity = zygosity_l[0] if len(zygosity_l) > 0 else None
            alt_reads = alt_reads_l[0] if len(alt_reads_l) > 0 else None
            tot_reads = tot_reads_l[0] if len(tot_reads_l) > 0 else None
            af = af_l[0] if len(af_l) > 0 else None
            hap_block = hap_block_l[0] if len(hap_block_l) > 0 else None
            hap_strand = hap_strand_l[0] if len(hap_strand_l) > 0 else None
        out = {
            'phred': phred,
            'filter': filter,
            'zygosity': zygosity,
            'alt_reads': alt_reads,
            'tot_reads': tot_reads,
            'af': af,
            'hap_block': hap_block,
            'hap_strand': hap_strand,
        }
        return out

if __name__ == '__main__':
    summarizer = CravatPostAggregator(sys.argv)
    summarizer.run()
