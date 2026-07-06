"""
Convert gnomAD4 per-chromosome VCF.GZ files to SQLite databases.

Usage:
    python convert_to_sqlite.py [data_dir]

data_dir defaults to the current directory. Produces one .sqlite file
per .vcf.gz file alongside the originals. The VCF.GZ files are not removed.
"""

import gzip
import re
import sqlite3
import sys
from pathlib import Path

OC_RE = re.compile(r'OC_DATA=([^;]+)')

CREATE_SQL = '''
    CREATE TABLE gnomad4 (
        pos INTEGER NOT NULL,
        ref TEXT NOT NULL,
        alt TEXT NOT NULL,
        %s
    )
''' % ', '.join(f'v{i} INTEGER' for i in range(30))

INSERT_SQL = 'INSERT INTO gnomad4 VALUES (%s)' % ', '.join('?' * 33)


def convert(vcf_gz_path: Path) -> None:
    db_path = vcf_gz_path.with_suffix('').with_suffix('.sqlite')
    if db_path.exists():
        print(f'  {db_path.name} already exists, skipping (delete it to reconvert)')
        return

    print(f'Converting {vcf_gz_path.name} -> {db_path.name} ...', flush=True)
    conn = sqlite3.connect(str(db_path))
    try:
        conn.execute('PRAGMA page_size = 4096')
        conn.execute('PRAGMA journal_mode = OFF')   # safe for a fresh build
        conn.execute('PRAGMA synchronous = OFF')
        conn.execute(CREATE_SQL)

        rows = []
        total = 0
        with gzip.open(str(vcf_gz_path), 'rt') as f:
            conn.execute('BEGIN')
            for line in f:
                if line.startswith('#'):
                    continue
                fields = line.split('\t', 8)
                m = OC_RE.search(fields[7])
                if not m:
                    continue
                vals = m.group(1).split(',')
                if len(vals) != 30:
                    continue
                rows.append((int(fields[1]), fields[3], fields[4], *(int(v) for v in vals)))
                if len(rows) >= 50_000:
                    conn.executemany(INSERT_SQL, rows)
                    total += len(rows)
                    rows.clear()
                    print(f'  {total:,} rows ...', end='\r', flush=True)
            if rows:
                conn.executemany(INSERT_SQL, rows)
                total += len(rows)
            conn.execute('COMMIT')

        print(f'  {total:,} rows inserted, building index ...', flush=True)
        conn.execute('CREATE INDEX idx ON gnomad4 (pos, ref, alt)')
        conn.execute('PRAGMA journal_mode = DELETE')
        conn.execute('PRAGMA optimize')
        print(f'  done: {db_path.name}', flush=True)
    except Exception:
        conn.close()
        db_path.unlink(missing_ok=True)
        raise
    finally:
        conn.close()


def main():
    data_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    vcf_files = sorted(data_dir.glob('*.vcf.gz'))
    if not vcf_files:
        print(f'No .vcf.gz files found in {data_dir}')
        sys.exit(1)
    for vcf in vcf_files:
        convert(vcf)
    print('All done.')


if __name__ == '__main__':
    main()
