import twobitreader
import os
from cravat import BaseCommonModule

class CravatCommonModule (BaseCommonModule):
    def setup (self):
        self.wgs_reader = twobitreader.TwoBitFile(os.path.join(os.path.dirname(__file__), 'data', 'hg19.2bit'))
        self.revbases = {'A':'T', 'T':'A', 'G':'C', 'C':'G', 'N':'N', 'a':'t', 't':'a', 'g':'c', 'c':'g', 'n':'n'}

    def __getitem__ (self, chrom):
        return self.wgs_reader[chrom]

    def get_bases (self, chrom, start, end=None, strand=None):
        if end is None:
            end = start
        if chrom not in self.wgs_reader:
            return None
        if strand is None or strand == '+':
            if start <= end:
                return self.wgs_reader[chrom][start - 1:end]
            else:
                bases = ''
                for pos in range(start - 1, end - 2, -1):
                    bases += self.wgs_reader[chrom][pos]
                return bases
        elif strand == '-':
            if start <= end:
                bases = ''
                for pos in range(end - 1, start - 2, -1):
                    bases += self.wgs_reader[chrom][pos]
                return ''.join([self.revbases[b] for b in bases])
            else:
                return ''.join([self.revbases[b] for b in self.wgs_reader[chrom][end - 1:start]])
        else:
            return None

    def slice (self, chrom, start, end=None):
        if end is None or end<start:
            end = start
        elif end == 0:
            raise IndexError(end)
        elif end > 0:
            end = end - 1
        if start <= 0:
            raise IndexError(start)
        else:
            start = start - 1
        try:
            out = self.wgs_reader[chrom][start:end]
            return out
        except ValueError as e:
            return None
