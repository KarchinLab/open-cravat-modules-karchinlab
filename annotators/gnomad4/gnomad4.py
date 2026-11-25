import sys
import sqlite3
from cravat import BaseAnnotator
from pathlib import Path


def _af(ac, an):
    return ac / an if an > 0 else None


_QUERY = 'SELECT ' + ','.join(f'v{i}' for i in range(30)) + \
         ' FROM gnomad4 WHERE pos=? AND ref=? AND alt=? LIMIT 1'


class CravatAnnotator(BaseAnnotator):

    def setup(self):
        self.db_cursors = {}
        data_path = Path(self.data_dir)
        for db_path in data_path.glob('*.sqlite'):
            chrom = db_path.stem
            # mode=ro prevents accidental writes and avoids NFS write-lock issues
            conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
            conn.execute('PRAGMA cache_size=-16384')  # 16 MB per chromosome
            conn.execute('PRAGMA temp_store=MEMORY')
            conn.execute('PRAGMA mmap_size=0')        # disable mmap; unreliable on NFS
            self.db_cursors[chrom] = conn.cursor()

    def _make_output(self, row):
        # row: (v0..v29) = AN[0:10], AC[10:20], nhomalt[20:30]
        # population order: afr ami amr asj eas fin mid nfe sas rem
        pops = ('afr', 'ami', 'amr', 'asj', 'eas', 'fin', 'mid', 'nfe', 'sas', 'rem')
        out = {}
        for i, pop in enumerate(pops):
            an, ac, nh = row[i], row[i + 10], row[i + 20]
            out[f'an_{pop}'] = an
            out[f'ac_{pop}'] = ac
            out[f'nhomalt_{pop}'] = nh
            out[f'af_{pop}'] = _af(ac, an)
        out['an'] = sum(row[0:10])
        out['ac'] = sum(row[10:20])
        out['nhomalt'] = sum(row[20:30])
        out['af'] = _af(out['ac'], out['an'])
        return out

    def annotate(self, input_data):
        cursor = self.db_cursors.get(input_data['chrom'])
        if cursor is None:
            return
        cursor.execute(_QUERY, (input_data['pos'], input_data['ref_base'], input_data['alt_base']))
        row = cursor.fetchone()
        if row is None:
            return
        return self._make_output(row)

    def cleanup(self):
        pass


if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
