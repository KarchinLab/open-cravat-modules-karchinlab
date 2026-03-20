from cravat.cravat_report import CravatReport
import sys
import datetime
import re
import csv
import zipfile
import os
import sqlite3
from cravat.util import detect_encoding
import json

class Reporter(CravatReport):

    # Replacement of % must come first
    perc_encode = [
        [r'%', r'%25'],
        [r':', r'%3A'],
        [r';', r'%3B'],
        [r'=', r'%3D'],
        [r',', r'%2C'],
        [r'\n', r'%0A'],
        [r'\t', r'%09'],
        [r'\r', r'%0D'],
    ]

    def vcf_encode(self, orig):
        new = orig
        if type(new) == str:
            for k,v in self.perc_encode:
                new = new.replace(k,v)
        return new

    def vcf_decode(self, orig):
        new = orig
        for k,v in self.perc_encode[::-1]:
            new = new.replace(v,k)
        return new

    def setup (self):
        self.wf = None
        self.filename = None
        self.filename_prefix = None
        self.levels_to_write = ['variant']
        if self.savepath == None:
            self.filename_prefix = 'cravat_result'
        else:
            self.filename_prefix = self.savepath
        self.filename = self.filename_prefix + '.vcf'
        if not 'type' in self.confs:
            self.info_type = 'separate'
        else:
            info_type = self.confs['type']
            if info_type in ['separate', 'combined']:
                self.info_type = self.confs['type']
            else:
                self.info_type = 'combined'
        self.info_fieldname_prefix = 'CRV'
        self.col_names_to_skip = {'base__uid', 'base__chrom', 'base__pos', 'base__ref_base', 'base__alt_base',
            'base__numsample','base__samples','base__tags',
            }
        q = 'select colval from info where colkey="_converter_format"'
        self.cursor2.execute(q)
        r = self.cursor2.fetchone()
        self.input_format = r[0]
        if self.input_format == 'vcf' and self.args.inputfiles is not None and len(self.args.inputfiles) > 1:
            msg = 'VCF reporter can handle jobs with only 1 VCF input file'
            self.logger.info(msg)
            print(msg)
            wf = open(self.filename, 'w')
            wf.write(msg + '\n')
            wf.close()
            return False

    def end (self):
        if self.wf is not None:
            self.wf.close()
        return self.filename

    def connect_db (self, dbpath=None):
        if dbpath != None:
            self.dbpath = dbpath
        if self.dbpath == None:
            sys.stderr.write('Provide a path to aggregator output')
            exit()
        if os.path.exists(self.dbpath) == False:
            sys.stderr.write(self.dbpath + ' does not exist.')
            exit()
        self.conn = sqlite3.connect(self.dbpath)
        self.cursor = self.conn.cursor()
        self.conn2 = sqlite3.connect(self.dbpath)
        self.cursor2 = self.conn2.cursor()

    def close_db (self):
        self.cursor2.close()
        self.conn2.close()
        self.cursor.close()
        self.conn.close()
        self.cf.close_db()

    def write_preface (self, level): 
        self.level = level
        if self.wf is not None:
            self.wf.close()
        if level != 'variant':
            return
        if 'base__samples' not in self.colnames_to_display[level]:
            newcolnames_to_display = []
            newcolnos_to_display = []
            cols = self.colinfo[level]['columns']
            for i in range(len(cols)):
                col = cols[i]
                colname = col['col_name']
                if colname in self.colnames_to_display[level]:
                    newcolnames_to_display.append(colname)
                    newcolnos_to_display.append(i)
                elif colname == 'base__samples':
                    newcolnames_to_display.append(colname)
                    newcolnos_to_display.append(i)
            self.colnames_to_display[level] = newcolnames_to_display
            self.colnos_to_display[level] = newcolnos_to_display
        self.extracted_cols[level] = self.get_extracted_header_columns(level)
        self.wf = open(self.filename, 'w', encoding='utf-8', newline='')
        lines = ['#fileformat=VCFv4.2',
            '#OpenCRAVATFileDate=' + datetime.datetime.now().strftime('%Y%m%d'),
        ]
        self.write_preface_lines(lines)
        self.vcflines = {}
        self.input_path_dict = {}
        if self.input_format == 'vcf' and self.args.inputfiles is not None and len(self.args.inputfiles) == 1:
            if self.args.inputfiles is not None:
                if type(self.args.inputfiles) is str:
                    self.args.inputfiles = [self.args.inputfiles]
                for i in range(len(self.args.inputfiles)):
                    self.input_path_dict[self.args.inputfiles[i]] = i
                written_headers = []
                self.samples = []
                num_inputfiles = len(self.args.inputfiles)
                for inputfile in self.args.inputfiles:
                    inputfile_prefix = os.path.basename(inputfile).split('.')[0]
                    input_path_no = self.input_path_dict[inputfile]
                    encoding = detect_encoding(inputfile)
                    if inputfile.endswith('.gz'):
                        import gzip
                        f = gzip.open(inputfile, 'rt', encoding=encoding)
                    else:
                        f = open(inputfile)
                    lineno = 0
                    self.vcflines[input_path_no] = {}
                    for line in f:
                        lineno += 1
                        if line.startswith('##fileformat='):
                            continue
                        if line.startswith('##'):
                            if not line in written_headers:
                                self.wf.write(line)
                                written_headers.append(line)
                        elif line.startswith('#CHROM'):
                            toks = line[:-1].split('\t')
                            if len(toks) >= 10:
                                if num_inputfiles == 1:
                                    self.samples.extend([v for v in toks[9:]])
                                else:
                                    self.samples.extend([inputfile_prefix + '_' + v for v in toks[9:]])
                        elif line.startswith('#') == False:
                            self.vcflines[input_path_no][lineno] = line.rstrip('\n').rstrip('\r')
                    f.close()
        else:
            self.cursor2.execute('select distinct(base__sample_id) from sample')
            self.samples = []
            rows = self.cursor2.fetchall()
            if rows is None or len(rows) == 0:
                self.samples.append('NOSAMPLEID')
            else:
                for row in rows:
                    v = row[0]
                    if v is None:
                        v = 'NOSAMPLEID'
                    self.samples.append(v)
    
    @staticmethod
    def oc2vcf_key(col_name):
        return f'OC_{col_name}'
    
    def include_column(self, col_name):
        if col_name in self.col_names_to_skip:
            return False
        if col_name.startswith('extra_vcf_info__'):
            return False
        if col_name.startswith('vcfinfo__'):
            return False
        if col_name.startswith('tagsampler__'):
            return False
        if col_name.endswith('__original_line'):
            return False
        return True

    def write_header (self, level):
        self.level = level
        if self.level != 'variant':
            return
        self.output_candidate = {}
        self.col_names = []
        if self.info_type == 'separate':
            for column in self.extracted_cols[level]:
            #for column in self.colinfo[self.level]['columns']:
                col_name = column['col_name']
                col_type = column['col_type'].capitalize()
                col_desc = column['col_desc']
                if not self.include_column(col_name):
                    continue
                if col_desc is None:
                    col_desc = ''
                if col_type == 'Int':
                    col_type = 'Integer'
                line = '#INFO=<ID={},Number=A,Type={},Description="{}">'.format(self.oc2vcf_key(col_name), col_type, col_desc)
                self.write_preface_line(line)
                self.col_names.append(col_name)
            if len(self.samples) == 0:
                line = 'CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO'
            else:
                line = 'CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t'
                line += '\t'.join(self.samples)
            self.write_preface_line(line)
        elif self.info_type == 'combined':
            line = '#INFO=<ID={},Number=.,Type=String,Description="OpenCRAVAT annotation. Format: '.format(self.info_fieldname_prefix)
            columns_to_add = []
            desc = []
            for column in self.extracted_cols[level]:
            #for column in self.colinfo[self.level]['columns']:
                col_name = column['col_name']
                col_desc = column['col_desc']
                if not(self.include_column(col_name)):
                    continue
                columns_to_add.append(col_name)
                if col_desc is not None:
                    desc.append(col_name + '=' + col_desc)
                self.col_names.append(col_name)
            line += '|'.join(columns_to_add)
            line += ' Explanation: {}'.format('|'.join(desc))
            line += '">'
            self.write_preface_line(line)
            if len(self.samples) == 0:
                line = 'CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO'
            else:
                line = 'CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t'
                line += '\t'.join(self.samples)
            self.write_preface_line(line)

    def write_table_row (self, row):
        if self.level != 'variant':
            return
        #columns = self.colinfo[self.level]['columns']
        columns = self.extracted_cols[self.level]
        row = list(row)
        writerow = []
        info = []
        chrom = None
        pos = None
        uid = None
        ref = None
        alt = None
        qual = None
        filt = None
        fmt = None
        pathno = None
        lineno = None
        for i in range(len(columns)):
            column = columns[i]
            col_name = column['col_name']
            cell = row[i]
            if col_name == 'base__uid':
                uid = cell
                q = 'select base__fileno, base__original_line from mapping where base__uid={}'.format(uid)
                self.cursor2.execute(q)
                rows2 = self.cursor2.fetchall()
                for row2 in rows2:
                    (pathno, lineno) = row2
                    if pathno not in self.output_candidate:
                        self.output_candidate[pathno] = {}
                    if self.input_format == 'vcf':
                        vcfline = self.vcflines[pathno][lineno]
                        if lineno not in self.output_candidate[pathno]:
                            alts = vcfline.split('\t')[4].split(',')
                            noalts = len(alts)
                            noalts_starless = len([alt for alt in alts if alt!='*' and alt != '<NON_REF>'])
                            self.output_candidate[pathno][lineno] = {'noalts': noalts, 'noalts_starless':noalts_starless, 'alts':alts, 'line': vcfline, 'annots': []}
                continue
            elif col_name == 'base__all_mappings':
            #     cell = cell.replace('; ', '&')
                cell = cell.replace(' ', '-')
            #     cell = cell.replace(',','/')
            #     info.append(cell)
            #     continue
            if self.input_format == 'vcf' and not(self.include_column(col_name)):
                    continue
            if cell is None:
                infocell = ''
            elif type(cell) is str:
                # cell = cell.replace('; ', '&')
                # cell = cell.replace(';', '&')
                # cell = cell.replace(' ', '-')
                # cell = cell.replace(',','/')
                try:
                    o = json.loads(cell)
                    if type(o) in (dict, list):
                        if len(o) == 0:
                            infocell=''
                        jsoncell = json.dumps(o, separators=(',',':'))
                        infocell = self.vcf_encode(jsoncell)
                    else:
                        infocell = self.vcf_encode(cell)
                except json.JSONDecodeError:
                    infocell = self.vcf_encode(cell)
            else:
                infocell = str(cell)
            info.append(infocell)
            if self.input_format != 'vcf':
                if col_name == 'base__chrom':
                    chrom = cell.lstrip('chr')
                elif col_name == 'base__pos':
                    pos = cell
                elif col_name == 'base__ref_base':
                    ref = cell
                elif col_name == 'base__alt_base':
                    alt = cell
                elif col_name == 'base__numsample':
                    continue
                elif col_name == 'base__samples':
                    samples_with_variant = cell.split(',')
                    sample_cols = []
                    for s in self.samples:
                        if s in samples_with_variant:
                            sample_cols.append('1|1')
                        else:
                            sample_cols.append('.|.')
                elif col_name == 'vcfinfo__phred':
                    qual = cell.split(';')[0]
                elif col_name == 'vcfinfo__filter':
                    filt = cell.split(';')[0]
        if self.input_format == 'vcf':
            out = self.output_candidate[pathno][lineno]
            noalts = out['noalts']
            noalts_starless = out['noalts_starless']
            annots = out['annots']
            alts = out['alts']
        else:
            noalts = noalts_starless = 1
            annots = []
            alts = [alt]
        annots.append(info)
        if len(annots) == noalts_starless:
            numfields = len(annots[0])
            combined_annots = [['.' for j in range(noalts)] for i in range(numfields)]
            for fieldno in range(len(annots[0])):
                star_offset = 0
                for altno in range(noalts):
                    alt = alts[altno]
                    if alt == '*':
                        star_offset += 1
                    elif alt == "<NON_REF>":
                        star_offset += 1
                    else:
                        combined_annots[fieldno][altno] = annots[altno-star_offset][fieldno]
            if self.info_type == 'separate':
                info_add_list = []
                for colno in range(len(self.col_names)):
                    vals = combined_annots[colno]
                    has_value = False
                    for val in vals:
                        if val != '' and val != '""':
                            has_value = True
                            break
                    if has_value:
                        info_add_list.append(
                            self.oc2vcf_key(self.col_names[colno]) + '=' + ','.join(combined_annots[colno]))
                info_add_str = ';'.join(info_add_list)
            elif self.info_type == 'combined':
                info_add_str = self.info_fieldname_prefix + '=' + '|'.join([','.join(altlist) for altlist in combined_annots])
            if self.input_format == 'vcf':
                toks = out['line'].split('\t')
                if toks[7] == '.' or toks[7] == '':
                    toks[7] = info_add_str
                else:
                    toks[7] = toks[7] + ';' + info_add_str
                writerow = toks
                del self.output_candidate[pathno][lineno]
            else:
                writerow = [str(chrom), str(pos), str(uid), ref, alt, '.', '.', info_add_str, 'GT']
                writerow.extend(sample_cols)
            self.write_body_line(writerow)

    def write_body_lines (self, lines):
        if self.level != 'variant':
            return
        for line in lines:
            self.write_body_line(line)
    
    def write_body_line (self, row):
        if self.level != 'variant':
            return
        self.wf.write('\t'.join(row) + '\n')
    
    def write_preface_lines (self, lines):
        if self.level != 'variant':
            return
        for line in lines:
            self.write_preface_line(line)
    
    def write_preface_line (self, line):
        if self.level != 'variant':
            return
        self.wf.write('#' + line + '\n')

def main ():
    reporter = Reporter(sys.argv)
    reporter.run()

if __name__ == '__main__':
    main()
