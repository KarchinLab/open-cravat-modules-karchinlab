from cravat import BaseConverter
from cravat import BadFormatError

"""
    CRAVAT Input format:  chr pos +/- ref alt [Sample] [Tag(s)]
    Sample is an optional sample identifier for cohort studies
    Tags is a string with identifiers or categorical tags. It is also
    optional and is delimited with semicolons if there is more than one
    tag. 
"""     
class CravatConverter(BaseConverter):
    comp_base = {'A':'T','T':'A','C':'G','G':'C','-':'-','N':'N'}

    def __init__(self):
        self.format_name = 'starr_fusion'
        self.variant_type = self.GENE_FUSION_VARIANT_TYPE
    
    def check_format(self, f):
        l = f.readline()
        return l.startswith('#FusionName')
    
    def setup(self, f):
        pass
    
    def convert_line(self, l):
        if l.startswith('#'):
            return self.IGNORE
        toks = l.strip().split()
        left_break = toks[5]
        right_break = toks[7]
        left_items = left_break.split(':')
        right_items = right_break.split(':')
        wdict = {
            'left_chrom':left_items[0],
            'left_break_pos':int(left_items[1]),
            'left_break_strand':left_items[2],
            'right_chrom':right_items[0],
            'right_break_pos':int(right_items[1]),
            'right_break_strand':right_items[2],
            'sample_id':None,
            'tags':None,
        }
        return [wdict]
