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
        self.format_name = 'ancestrydna'
        self.addl_cols = [
            {
                'name':'zygosity',
                'title':'Zygosity',
                'type':'string'
            },
        ]
    
    def check_format(self, f):
        return 'AncestryDNA' in f.readline()
    
    def setup(self, f):
        self.wgs = get_wgs_reader(assembly='hg19')
        self.good_vars = set(['T','C','G','A'])

    def convert_line(self, l):
        ret = []
        if l.startswith('#'): return self.IGNORE
        if l.startswith('rsid'): return self.IGNORE
        toks = l.strip('\r\n').split('\t')
        tags = toks[0]
        chrom = toks[1]
        chromint = int(chrom)
        if chromint == 23:
            chrom = 'X'
        elif chromint==24 or chromint==25:
            chrom = 'Y'
        elif chromint == 26:
            chrom = 'M'
        chrom = 'chr'+chrom
        pos = int(toks[2])
        try:
            ref = self.wgs.slice(chrom, pos).upper()
        except KeyError:
            raise InvalidData(f'Bad chrom {chrom}')
        except IndexError:
            raise InvalidData(f'Bad position {pos}')      
        except ValueError:
            raise InvalidData(f'Bad position {pos}')
        sample = ''
        zygosity = None
        try:
            if toks[3]==toks[4]:
                zygosity = 'hom'
            else:
                zygosity = 'het'
        except IndexError:
            zygosity = 'hom'

        for var in toks[3:]:
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
        if not ret:
            return self.IGNORE
        if zygosity == 'hom':
            ret = ret[:1]
        return ret
