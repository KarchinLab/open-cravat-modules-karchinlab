import json
from json import JSONDecodeError

from cravat import BaseConverter
from cravat import BadFormatError
import requests
from itertools import chain, islice


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
        Clingen Allele Registry Input format:
        One CA ID per line
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
        self.format_name = 'clingen'
        self.assembly = 'GRCh38'
        self.exc_handler = None

    def _validate_id(self, ca_id):
        upper_id = ca_id.upper()
        if upper_id[0:2] != 'CA':
            return False, 'Clingen Allele Registry Id must start with "CA"'
        try:
            int(upper_id[2:])
        except ValueError:
            return False, 'Clingen Allele Registry Id incorrectly formatted'
        return True, ''

    def _check_line(self, line_number, line):
        """For non-comment lines, ensure that the first token is a CA ID

        Check Line has a side effect of logging an error for invalid lines
        that are not comments."""
        tokens = line.strip(' \r\n').split('\t')
        if len(tokens) == 1:
            # ignore blank lines
            if not tokens[0]:
                return False
            tokens = tokens[0].split()

        # check that the first token is like CA######
        valid, message = self._validate_id(tokens[0])
        # report invalid lines
        if not valid and not tokens[0].startswith('#') and self.exc_handler:
            self.exc_handler(line_number, line, message)
        return valid

    def _initialize_dict(self, line_number, line):
        ca_id, sample, tags = self._get_caid_sample_and_tags(line)
        return {
            'line': line,
            'line_number': line_number,
            'ca_id': ca_id,
            'sample_id': sample,
            'tags': tags
        }

    def _get_batch(self, file):
        numbered_file = enumerate(file, start=1)
        filtered_file = [self._initialize_dict(ln, l) for (ln, l) in numbered_file if self._check_line(ln, l)]
        for batch in batched(filtered_file, self.batch_size):
            yield list(batch)

    def _get_caid_sample_and_tags(self, line):
        sample = ''
        tags = ''
        parts = line.split('\t')
        if len(parts) == 1:
            parts = line.split()
        ca_id = parts[0].strip()
        if len(parts) > 1:
            sample = parts[1].strip()
        if len(parts) > 2:
            tags = parts[2].strip()
        return ca_id, sample, tags

    def check_format(self, f):
        if f.name.endswith('.clingen'):
            return True
        format_correct = False
        ln = 0
        for line in f:
            if not (line.startswith('#')) and not len(line.strip()) == 0:
                format_correct = self._check_line(ln, line)
                if format_correct:
                    break
                ln += 1
        return format_correct

    def setup(self, f):
        """Ensure connection to the Clingen API, raise exception if anything goes wrong"""
        headers = {'Content-Type': 'application/json'}
        r = requests.post(self.api_url, data='CA000123', headers=headers, timeout=1)
        r.raise_for_status()
        pass

    def _call_api(self, line_dicts):
        data = "\n".join([x['ca_id'] for x in line_dicts])
        headers = {'Content-Type': 'application/json'}
        r = requests.post(self.api_url, data=data, headers=headers)
        r.raise_for_status()
        try:
            js = r.json()
        except JSONDecodeError:
            js = f'{{"body": "{r.status_code} - {r.text}"}}'
        return js

    def _get_genomic_coordinates(self, record, assembly):
        for coords in record['genomicAlleles']:
            if coords['referenceGenome'] == assembly:
                return coords
        return None

    def _format_allele(self, base):
        base_string = str(base)
        if not base_string or base_string == '':
            base_string = '-'
        return base_string

    def _combine_data(self, batch, results):
        for info, result in zip(batch, results):
            if '@id' not in result:
                ca_id = result.get('inputLine')
                info['error'] = f"{result.get('errorType', 'error')}: {result.get('description', 'unknown api error')}"
                continue

            try:
                full_id = result['@id']
                ca_id = full_id.split('/')[-1]
                info['ca_id'] = ca_id
                coord_data = self._get_genomic_coordinates(result, self.assembly)
                pos_data = coord_data['coordinates'][0]

                info['chrom'] = f"chr{coord_data['chromosome']}"
                info['pos'] = str(pos_data['start'])
                info['ref_base'] = self._format_allele(pos_data['referenceAllele'])
                info['alt_base'] = self._format_allele(pos_data['allele'])
            except Exception as e:
                info['error'] = e
        return batch

    def convert_file(self, file, exc_handler=None, *args, **kwargs):
        self.exc_handler = exc_handler
        for batch in self._get_batch(file):
            clingen_results = self._call_api(batch)
            batch_wdicts = self._combine_data(batch, clingen_results)
            for wdict in batch_wdicts:
                if 'error' in wdict:
                    if exc_handler:
                        exc_handler(wdict.get('line_number'), wdict.get('line'), wdict.get('error'))
                    else:
                        raise BadFormatError(wdict.get('error'))
                else:
                    yield wdict['line_number'], wdict['line'], [wdict]


if __name__ == '__main__':
    conv = CravatConverter({'api_url': 'https://reg.clinicalgenome.org/alleles?file=id'})
    conv.convert_file(['CA250637', 'CA386951973', 'CA10580924', 'CA10585116'])
