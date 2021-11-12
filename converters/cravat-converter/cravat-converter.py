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
        self.format_name = 'cravat'

    def _switch_strand(self, bases):
        return ''.join([self.comp_base[base] for base in bases[::-1]])

    def _strand_present (self, toks):
        if toks[2] in ['+', '-']:
            return True
        else:
            return False

    def _check_line(self, l): #could take tokens not l
        toks = l.strip('\r\n').split('\t')
        if len(toks) == 1:
            toks = toks[0].split()
        if len(toks) == 7:
            _, pos, strand, ref, alt, _, _ = toks
        elif len(toks) == 6:
            if self._strand_present(toks):
                _, pos, strand, ref, alt, _ = toks
            else:
                strand = '+'
                _, pos, ref, alt, _, _ = toks
        elif len(toks) == 5:
            if self._strand_present(toks):
                _, pos, strand, ref, alt = toks
            else:
                strand = '+'
                _, pos, ref, alt, _ = toks
        elif len(toks) == 4:
            if self._strand_present(toks):
                return False, "Wrong number of columns"
            else:
                strand = '+'
                _, pos, ref, alt = toks
        else:
            return False, "Wrong number of columns"
        valid_bases = list(self.comp_base.keys())
        try:
            int(pos)
        except ValueError:
            return False, '2nd column must be integer'
        if not(strand in ['-','+']): return False, '4th column must be + or -'
        ref = ref.upper()
        alt = alt.upper()
        for char in ref.upper():
            if char not in valid_bases: return False, 'Bad ref base'
        for char in alt.upper():
            if char not in valid_bases: return False, 'Bad alt base'
        return True, ''
    
    def check_format(self, f):
        format_correct = False
        for l in f:
            if not(l.startswith('#')):
                format_correct, _ = self._check_line(l)
                if format_correct == True:
                    break
        return format_correct
    
    def setup(self, f):
        pass
    
    def convert_line(self, l):
        if l.startswith('#'): return self.IGNORE
        format_correct, format_msg= self._check_line(l)
        if not(format_correct): raise BadFormatError(format_msg)
        toks = l.strip('\r\n').split('\t')
        if len(toks) == 1:
            toks = toks[0].split()
        if self._strand_present(toks) == False:
            toks.insert(2, '+')
        if len(toks) == 5: 
            toks.append('')
        if len(toks) == 6:
            toks.append('')    
        chrom, pos, strand, ref, alt, sample, tags = toks
        if strand == '-':
            pos = int(pos) - len(ref.replace('-','')) + 1
            alt = self._switch_strand(alt)
            ref = self._switch_strand(ref)
        wdict = {'tags':tags,
                 'chrom':chrom,
                 'pos':pos,
                 'ref_base':ref,                 
                 'alt_base':alt,
                 'sample_id':sample,
                 }
        return [wdict]
