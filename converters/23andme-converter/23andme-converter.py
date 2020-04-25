from cravat import BaseConverter
from cravat import BadFormatError
import cravat.constants as constants
from pyliftover import LiftOver
import os
from cravat.exceptions import LiftoverFailure, InvalidData
from cravat.inout import CravatWriter
from cravat import get_wgs_reader

class CravatConverter(BaseConverter):
    
    def __init__(self):
        self.format_name = '23andme'
        self.addl_cols = [
            {
                'name':'zygosity',
                'title':'Zygosity',
                'type':'string'
            },
        ]
    
    def check_format(self, f):
        return '23andMe' in f.readline()
    
    def setup(self, f):
        self.wgs = get_wgs_reader(assembly='hg19')
        self.good_vars = set(['T','C','G','A'])

    def convert_line(self, l):
        ret = []
        if l.startswith('#'): return self.IGNORE
        toks = l.strip('\r\n').split('\t')
        tags = toks[0]
        chrom = toks[1]
        if chrom=='MT':
            chrom = 'M'
        chrom = 'chr'+chrom
        pos = int(toks[2])
        try:
            ref = self.wgs.slice(chrom, pos).upper()
        except KeyError:
            raise InvalidData(f'Bad chrom {chrom}')
        except IndexError:
            raise InvalidData(f'Bad position {pos}')
        sample = ''
        geno = toks[3]
        zygosity = None
        try:
            if geno[0]==geno[1]:
                zygosity = 'hom'
            else:
                zygosity = 'het'
        except IndexError:
            zygosity = 'hom'
            
        for var in geno:
            if var in self.good_vars and var != ref:
                alt = var
                wdict = {
                    'tags':tags,
                    'chrom':chrom,
                    'pos':pos,
                    'ref_base':ref,
                    'alt_base':alt,
                    'sample_id':sample,
                    'zygosity':zygosity,
                }
                ret.append(wdict)
        if ret and zygosity == 'hom':
            ret = ret[:1]
        return ret
