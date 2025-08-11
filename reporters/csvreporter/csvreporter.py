from cravat.cravat_report import CravatReport
import sys
import datetime
import re
import csv
import zipfile
import os
import sqlite3
import json

class Reporter(CravatReport):

    def setup (self):
        self.wf = None
        self.csvwriter = None
        self.filenames = []
        self.filename = None
        self.filename_prefix = None
        if self.savepath == None:
            self.filename_prefix = 'cravat_result'
        else:
            self.filename_prefix = self.savepath
        self.levels_to_write = self.get_standardized_module_option(self.confs.get('pages', 'variant'))
        self.separate_header_file = self.get_standardized_module_option(self.confs.get('separate-header-file', 'false')) == True
        self.zip = self.get_standardized_module_option(self.confs.get('zip', 'false')) == True
        self.module_col_sep = '.'
        self.filename_postfix = '.csv'

    def should_write_level (self, level):
        if self.levels_to_write is None:
            return True
        elif level in self.levels_to_write:
            return True
        else:
            return False

    def end (self):
        if self.wf is not None:
            self.wf.close()
        if self.zip:
            zipfile_path = self.filename_prefix + f'{self.filename_postfix}.zip'
            zf = zipfile.ZipFile(zipfile_path, mode='w', compression=zipfile.ZIP_DEFLATED)
            for filename in self.filenames:
                zf.write(filename, os.path.relpath(filename, start=os.path.dirname(filename)))
            zf.close()
        else:
            zipfile_path = self.filenames
        return zipfile_path

    def write_preface (self, level): 
        self.level = level
        if level not in self.levels_to_write:
            return
        if self.wf is not None:
            self.wf.close()
        if self.separate_header_file:
            self.filename = f'{self.filename_prefix}.{level}{self.filename_postfix}.header'
        else:
            self.filename = f'{self.filename_prefix}.{level}{self.filename_postfix}'
            self.filenames.append(self.filename)
        self.wf = open(self.filename, 'w', encoding='utf-8', newline='')
        self.csvwriter = csv.writer(self.wf, lineterminator='\n')

    def write_header (self, level):
        if level not in self.levels_to_write:
            return
        colno = 0
        display_colno = 0
        row = []
        for colgroup in self.colinfo[level]['colgroups']:
            count = colgroup['count']
            if count == 0:
                continue
            for col in self.colinfo[level]['columns'][colno:colno+count]:
                module_col_name = col['col_name']
                [module_name, col_name] = module_col_name.split('__')
                if module_name == 'base':
                    new_colname = col_name
                else:
                    new_colname = module_name + self.module_col_sep + col_name
                if module_col_name in self.colnames_to_display[level]:
                    row.append(new_colname)
                    display_colno += 1
                colno += 1
        if self.separate_header_file:
            self.wf.close()
            self.filename = f'{self.filename_prefix}.{level}{self.filename_postfix}'
            self.filenames.append(self.filename)
            self.wf = open(self.filename, 'w', encoding='utf-8', newline='')
            self.csvwriter = csv.writer(self.wf, lineterminator='\n')
        self.write_body_line(row)

    def write_table_row (self, row):
        if self.level not in self.levels_to_write:
            return
        self.write_body_line([str(v) if v != None else '' for v in list(row)])

    def write_body_line (self, row):
        if self.level not in self.levels_to_write:
            return
        self.csvwriter.writerow(row)

    def write_preface_lines (self, lines):
        if self.level not in self.levels_to_write:
            return
        for line in lines:
            self.write_preface_line(line)

    def write_preface_line (self, line):
        if self.level not in self.levels_to_write:
            return
        self.wf.write('#' + line + '\n')

def main ():
    reporter = Reporter(sys.argv)
    reporter.run()

if __name__ == '__main__':
    main()
