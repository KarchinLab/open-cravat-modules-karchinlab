import json
from json import JSONDecodeError

from cravat import BaseConverter
from cravat import BadFormatError
import requests

_HGVS_API_URL = 'http://localhost:8000'
_COORDINATES_ENDPOINT = _HGVS_API_URL + '/coordinates'


class CravatConverter(BaseConverter):
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
        super().__init__()
        self.format_name = 'hgvs'

    def _check_line(self, line):
        tokens = line.strip('\r\n').split('\t')
        if len(tokens) == 1:
            tokens = tokens[0].split()
        return True, ''

    def _get_string_sample_and_tags(self, line):
        sample = ''
        tags = ''
        parts = line.split('\t')
        if len(parts) == 1:
            parts = line.split()
        hgvs_string = parts[0]
        if len(parts) > 1:
            sample = parts[1]
        if len(parts) > 2:
            tags = parts[2]
        return hgvs_string, sample, tags

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
        r = requests.get(f'{_HGVS_API_URL}/hello')
        pass

    def _call_api(self, hgvs):
        data = {'hgvs': hgvs}
        headers = {'Content-Type': 'application/json'}
        r = requests.post(_COORDINATES_ENDPOINT, data=json.dumps(data), headers=headers)
        if r.status_code != 200:
            try:
                js = r.json()
            except JSONDecodeError:
                js = f'{{"body": "{r.status_code} - {r.text}"}}'
            raise BadFormatError(r.json()['body'])
        return r.json()

    def convert_line(self, line):
        line = line.strip()
        if not line:
            return self.IGNORE
        if line.startswith('#'):
            return self.IGNORE
        format_correct, format_msg = self._check_line(line)
        if not format_correct:
            raise BadFormatError(format_msg)

        hgvs_string, sample, tags = self._get_string_sample_and_tags(line)

        tokens = self._call_api(hgvs_string)
        # {'alt': 'A', 'assembly': 'hg38', 'body': 'HGVS successfully converted to coordinates', 'chrom': 'chrX', 'code': 200, 'hgvs': 'NC_000023.11:g.32389644G>A', 'is_valid': True, 'original': 'NM_004006.2:c.4375C>T', 'pos': 32389644, 'ref': 'G'}
        wdict = {
            'tags': tags,
            'chrom': tokens['chrom'],
            'pos': tokens['pos'],
            'ref_base': tokens['ref'],
            'alt_base': tokens['alt'],
            'sample_id': sample,
        }
        return [wdict]
