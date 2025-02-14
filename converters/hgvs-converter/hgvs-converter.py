import json
from itertools import chain, islice
from json import JSONDecodeError

from cravat import BaseConverter
from cravat import BadFormatError
import requests


def batched(iterable, n):
    """
    group the iterator into a new iterator of batches of size n.

    backfill for python 3.12 itertools.batched. borrowed from python.org discussion
    https://discuss.python.org/t/add-batching-function-to-itertools-module/19357/19?page=2
    """
    it = iter(iterable)
    for first in it:
        batch = chain((first,), islice(it, n - 1))
        yield batch
        next(islice(batch, n, n), None)

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
        self.api_url = self.conf['api_url']
        self.coordinates_endpoint = self.api_url + '/coordinates'
        self.format_name = 'hgvs'
        self.valid_sequence_types = ['c', 'g', 'm', 'n', 'o', 'p', 'r']
        self.exc_handler = None

    def _check_line(self, line):
        """For non-comment lines, ensure that the first token is at least vaguely HGVS-like"""
        tokens = line.strip('\r\n').split('\t')
        if len(tokens) == 1:
            tokens = tokens[0].split()

        # check that the first token is something like aaaa:X.bbb where X is a valid reference sequence type
        parts = tokens[0].split(':')
        if len(parts) != 2:
            return False, 'HGVS token incorrectly formatted'
        desc_parts = parts[1].split('.')
        if len(desc_parts) != 2:
            return False, 'HGVS token incorrectly formatted'
        if desc_parts[0] not in self.valid_sequence_types:
            return False, 'HGVS token incorrectly formatted'
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
        if f.name.endswith('.hgvs'):
            return True
        format_correct = False
        for l in f:
            if not (l.startswith('#')) and not len(l.strip()) == 0:
                format_correct, _ = self._check_line(l)
                if format_correct:
                    break
        return format_correct

    def setup(self, f):
        """Ensure connection to the HGVS API, raise exception if anything goes wrong"""
        r = requests.get(f'{self.api_url}/hello', timeout=1)
        r.raise_for_status()

    def _call_api(self, hgvs):
        data = {'hgvs': hgvs}
        headers = {'Content-Type': 'application/json'}
        r = requests.post(self.coordinates_endpoint, data=json.dumps(data), headers=headers)
        r.raise_for_status()
        try:
            js = r.json()
        except JSONDecodeError:
            js = f'{{"body": "{r.status_code} - {r.text}"}}'
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
        assembly = tokens['assembly']
        if self.input_assembly and self.input_assembly != assembly:
            raise BadFormatError(
                f'HGVS {hgvs_string} found to be from assembly {assembly}; expected {self.input_assembly}')
        wdict = {
            'tags': tags,
            'chrom': tokens['chrom'],
            'pos': tokens['pos'],
            'ref_base': tokens['ref'],
            'alt_base': tokens['alt'],
            'sample_id': sample,
            'assembly': tokens['assembly']
        }
        return [wdict]

    def convert_file(self, file, exc_handler=None, *args, **kwargs):
        self.exc_handler = exc_handler
        for batch in self._get_batch(file):
            hgvs_results = self._call_api(batch)
            batch_wdicts = self._combine_data(batch, clingen_results)
            for wdict in batch_wdicts:
                if 'error' in wdict:
                    if exc_handler:
                        exc_handler(wdict.get('line_number'), wdict.get('line'), wdict.get('error'))
                    else:
                        raise BadFormatError(wdict.get('error'))
                else:
                    yield wdict['line_number'], wdict['line'], [wdict]
