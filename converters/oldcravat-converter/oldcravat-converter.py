from cravat import BaseConverter
from cravat import BadFormatError

class CravatConverter(BaseConverter):
    comp_base = {'A':'T','T':'A','C':'G','G':'C','-':'-','N':'N'}
    
    def __init__(self):
        self.format_name = 'oldcravat'
    
    def _switch_strand(self, bases):
        return ''.join([self.comp_base[base] for base in bases[::-1]])
    
    def _check_line(self, l): #could take tokens not l
        toks = l.strip('\r\n').split('\t')
        if len(toks) == 7:
            _, _, pos, strand, ref, alt, _ = toks
        elif len(toks) == 6:
            _, _, pos, strand, ref, alt = toks
        else:
            return False, "Wrong number of columns"
        valid_bases = list(self.comp_base.keys())
        try:
            int(pos)
        except ValueError:
            return False, '3rd column must be integer'
        if not(strand in ['-','+']): return False, '4th column must be + or -'
        ref = ref.upper()
        alt = alt.upper()
        for char in ref.upper():
            if char not in valid_bases: return False, 'Bad ref base'
        for char in alt.upper():
            if char not in valid_bases: return False, 'Bad alt base'
        return True, ''

    def check_format(self, f):
        for l in f:
            if not(l.startswith('#')):
                format_correct, _ = self._check_line(l)
                return format_correct

    def setup(self, f):
        pass

    def convert_line(self, l):
        if l.startswith('#'): return self.IGNORE
        format_correct, format_msg= self._check_line(l)
        if not(format_correct): raise BadFormatError(format_msg)
        toks = l.strip('\r\n').split('\t')
        if len(toks) == 6: toks.append('')
        tags, chrom, pos, strand, ref, alt, sample = toks
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
