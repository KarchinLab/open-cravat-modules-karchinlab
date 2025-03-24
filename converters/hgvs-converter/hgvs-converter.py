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
        self.batch_size = self.conf.get('batch_size', 10000)
        self.coordinates_endpoint = self.api_url + '/coordinates_all'
        self.format_name = 'hgvs'
        self.valid_sequence_types = ['c', 'g', 'm', 'n', 'o', 'p', 'r']
        self.exc_handler = None

    def _initialize_dict(self, line_number, line):
        hgvs_string, sample, tags = self._get_string_sample_and_tags(line)
        return {
            'line': line,
            'line_number': line_number,
            'hgvs': hgvs_string,
            'sample_id': sample,
            'tags': tags
        }

    def _get_batch(self, file):
        numbered_file = enumerate(file, start=1)
        filtered_file = [self._initialize_dict(ln, l) for (ln, l) in numbered_file if self._check_line(ln, l)]
        for batch in batched(filtered_file, self.batch_size):
            yield list(batch)


    def _validate_id(self, hgvs_string):
        # check that the hgvs string is something like aaaa:X.bbb where X is a valid reference sequence type
        parts = hgvs_string.split(':')
        if len(parts) != 2:
            return False, 'HGVS token incorrectly formatted'
        desc_parts = parts[1].split('.')
        if len(desc_parts) != 2:
            return False, 'HGVS token incorrectly formatted'
        if desc_parts[0] not in self.valid_sequence_types:
            return False, 'HGVS token incorrectly formatted'
        return True, ''

    def _check_line(self, line_number, line):
        """For non-comment lines, ensure that the first token is an HGVS string

        Check Line has a side effect of logging an error for invalid lines
        that are not comments."""
        tokens = line.strip(' \r\n').split('\t')
        if len(tokens) == 1:
            # ignore blank lines
            if not tokens[0]:
                return False
            tokens = tokens[0].split()

        # check that the first token is hgvs-like
        valid, message = self._validate_id(tokens[0])
        # report invalid lines
        if not valid and not tokens[0].startswith('#') and self.exc_handler:
            self.exc_handler(line_number, line, message)
        return valid

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
        ln = 1
        for l in f:
            if not (l.startswith('#')) and not len(l.strip()) == 0:
                format_correct = self._check_line(ln, l)
                if format_correct:
                    break
            ln += 1
        return format_correct

    def setup(self, f):
        """Ensure connection to the HGVS API, raise exception if anything goes wrong"""
        r = requests.get(f'{self.api_url}/hello', timeout=2)
        r.raise_for_status()

    def _call_api(self, hgvs_wdicts):
        hgvs_list = [x['hgvs'] for x in hgvs_wdicts]
        data = {'hgvs': hgvs_list}
        headers = {'Content-Type': 'application/json'}
        r = requests.post(self.coordinates_endpoint, data=json.dumps(data), headers=headers)
        r.raise_for_status()
        try:
            js = r.json()
        except JSONDecodeError:
            js = f'{{"body": "{r.status_code} - {r.text}"}}'
        return r.json()

    def _combine_data(self, batch, results):
        for variant in batch:
            hgvs_string = variant.get('hgvs')
            if hgvs_string in results.get('coordinates'):
                # add coordinates to wdict
                result = results.get('coordinates').get(hgvs_string)
                variant['chrom'] = result.get('chrom')
                variant['pos'] = result.get('pos')
                variant['alt_base'] = result.get('alt')
                variant['ref_base'] = result.get('ref')
            elif hgvs_string in results.get('errors'):
                variant['error'] = results.get('errors').get(hgvs_string)

        return batch


    def convert_file(self, file, exc_handler=None, *args, **kwargs):
        self.exc_handler = exc_handler
        for batch in self._get_batch(file):
            hgvs_results = self._call_api(batch)
            batch_wdicts = self._combine_data(batch, hgvs_results)
            for wdict in batch_wdicts:
                if 'error' in wdict:
                    if exc_handler:
                        exc_handler(wdict.get('line_number'), wdict.get('line'), wdict.get('error'))
                    else:
                        raise BadFormatError(wdict.get('error'))
                else:
                    yield wdict['line_number'], wdict['line'], [wdict]
