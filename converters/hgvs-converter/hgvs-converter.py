from cravat import BaseConverter
from cravat import BadFormatError


class HGVSConverter(BaseConverter):
    """
        HGVS Input format:
        One HGVS string per line
        Comment lines start with #
        Sample column (?)
        Tag column(?)
        Sample is an optional sample identifier for cohort studies
        Tags is a string with identifiers or categorical tags. It is also
        optional and is delimited with semicolons if there is more than one
        tag.
    """
    def __init__(self):
        super(HGVSConverter, self).__init__()
        self.format_name = 'hgvs'

    def _check_line(self, l):
        toks = l.strip('\r\n').split('\t')
        if len(toks) == 1:
            toks = toks[0].split()
        return True, ''
    
    def check_format(self, f):
        format_correct = False
        for l in f:
            if not (l.startswith('#')):
                format_correct, _ = self._check_line(l)
                if format_correct:
                    break
        return format_correct
    
    def setup(self, f):
        # Do some API connection test?
        pass

    def _call_api(self, hgvs):
        # pass
        return 'chr1', 10100, '+', 'C', 'T', 's0'

    def convert_line(self, l):
        l.lstrip()
        if l.startswith('#'): return self.IGNORE
        format_correct, format_msg = self._check_line(l)
        if not format_correct: raise BadFormatError(format_msg)

        toks = self._call_api('')
        chrom, pos, strand, ref, alt, sample, tags = toks
        wdict = {
            'tags':tags,
             'chrom':chrom,
             'pos':pos,
             'ref_base':ref,
             'alt_base':alt,
             'sample_id':sample,
             }
        return [wdict]
