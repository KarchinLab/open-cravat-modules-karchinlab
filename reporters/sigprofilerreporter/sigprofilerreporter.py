from cravat.cravat_report import CravatReport
import sys
import os
import sqlite3


class Reporter(CravatReport):
    """Exports somatic variants as a TSV in the CNAqc joint-table format that
    the nf-core ``sigprofiler`` module consumes as input.

    The output is a plain tab-delimited file with the fixed header::

        chr  Indiv  from  to  ref  alt  NV

    which is exactly what the nf-core ``sigprofiler`` module's
    ``process_tsv_join`` / ``input_processing`` functions read (the module
    strips the ``chr`` prefix and drops rows where ``NV == "0"`` before
    feeding the mutations to SigProfilerMatrixGenerator).

    One row is written per (variant, sample) so a multi-sample OpenCRAVAT run
    produces a joint table directly, and multiple per-sample runs can be
    concatenated by the nf-core module (its ``tsv_list`` input).

    By default only single-base substitutions (SBS) are emitted, because the
    nf-core module assigns ``mut_type = "SNP"`` to every row. Indels / MNPs can
    be included with the ``include-indels`` module option.
    """

    # OpenCRAVAT base variant columns we need (kept regardless of display set).
    NEEDED_COLS = (
        'base__uid',
        'base__chrom',
        'base__pos',
        'base__gposend',
        'base__ref_base',
        'base__alt_base',
    )

    # Output column header expected by the nf-core sigprofiler module.
    HEADER = 'chr\tIndiv\tfrom\tto\tref\talt\tNV\n'

    def setup(self):
        self.wf = None
        # Output filename: "<savepath>.sigprofiler.tsv" or
        # "<output_dir>/<run_name>.sigprofiler.tsv".
        if self.savepath is None:
            self.filename_prefix = os.path.join(self.output_dir, self.output_basename)
        else:
            self.filename_prefix = self.savepath
        self.filename = self.filename_prefix + '.sigprofiler.tsv'
        # Only the variant level is relevant for mutational signatures.
        self.levels_to_write = ['variant']
        # Module options (passed via --module-option sigprofilerreporter.<key>=<value>).
        confs = self.confs or {}
        self.include_indels = (
            self.get_standardized_module_option(confs.get('include-indels', 'false')) == True
        )
        self.default_nv = str(confs.get('default-nv', '1'))
        # Secondary sqlite connection for direct per-sample lookups.
        self.conn2 = sqlite3.connect(self.dbpath)
        self.cursor2 = self.conn2.cursor()
        # When oc run takes multiple input files the aggregator prefixes each
        # sample_id with the source file basename ("<vcf_basename>__<sample_id>")
        # to disambiguate across files. For SigProfiler we want the clean
        # sample ID as the ``Indiv`` column, so record those prefixes to strip.
        self.sample_prefixes = self._collect_sample_prefixes()
        # Precompute variant -> [(sample_id, alt_reads), ...] from the sample table.
        # sample.base__uid is the variant uid, so this naturally expands multi-sample
        # variants into one entry per carrying sample.
        self.sample_map = {}
        try:
            self.cursor2.execute(
                'select base__uid, base__sample_id, base__alt_reads from sample'
            )
            for uid, sample_id, alt_reads in self.cursor2.fetchall():
                self.sample_map.setdefault(uid, []).append((sample_id, alt_reads))
        except sqlite3.Error:
            self.sample_map = {}
        # Distinct sample ids, used as a fallback for variants lacking sample rows.
        self.all_sample_ids = []
        try:
            self.cursor2.execute('select distinct base__sample_id from sample')
            for (sid,) in self.cursor2.fetchall():
                if sid is not None:
                    self.all_sample_ids.append(sid)
        except sqlite3.Error:
            pass
        if not self.all_sample_ids:
            self.all_sample_ids = ['NOSAMPLEID']
        # Variant-level alternate read count (vcfinfo__alt_reads) as a fallback
        # for NV when no per-sample value is available.
        self.var_alt_reads = {}
        try:
            self.cursor2.execute('select base__uid, vcfinfo__alt_reads from variant')
            for uid, ar in self.cursor2.fetchall():
                self.var_alt_reads[uid] = ar
        except sqlite3.Error:
            self.var_alt_reads = {}

    def _collect_sample_prefixes(self):
        prefixes = set()
        try:
            self.cursor2.execute(
                'select colval from info where colkey="_input_paths"'
            )
            row = self.cursor2.fetchone()
            if row is not None:
                import json
                raw = row[0]
                if raw:
                    # Stored single-quoted; normalize to double quotes for JSON.
                    try:
                        paths = json.loads(raw.replace("'", '"'))
                    except json.JSONDecodeError:
                        paths = {}
                    for v in paths.values():
                        if v:
                            prefixes.add(os.path.basename(v))
        except sqlite3.Error:
            pass
        return prefixes

    def _clean_sample_id(self, sample_id):
        if sample_id is None:
            return 'NOSAMPLEID'
        sid = str(sample_id)
        if '__' in sid:
            prefix, rest = sid.split('__', 1)
            if prefix in self.sample_prefixes and rest:
                return rest
        return sid

    def end(self):
        if self.wf is not None:
            self.wf.close()
        try:
            self.cursor2.close()
            self.conn2.close()
        except Exception:
            pass
        return self.filename

    def should_write_level(self, level):
        return level == 'variant'

    def write_preface(self, level):
        # No comment preface -- the output is a plain TSV. Open the file here.
        if self.wf is not None:
            self.wf.close()
        self.wf = open(self.filename, 'w', encoding='utf-8', newline='')
        # Ensure the base columns we need are present in the display set so they
        # are passed through to write_table_row, even under --concise-report.
        needed = set(self.NEEDED_COLS)
        cols = self.colinfo[level]['columns']
        new_names = []
        new_nos = []
        for i, col in enumerate(cols):
            cn = col['col_name']
            if cn in self.colnames_to_display[level] or cn in needed:
                new_names.append(cn)
                new_nos.append(i)
        self.colnames_to_display[level] = new_names
        self.colnos_to_display[level] = new_nos
        # Force subset mode so get_extracted_row() uses colnos_to_display,
        # keeping the row aligned with extracted_cols.
        self.display_select_columns[level] = True
        self.extracted_cols[level] = self.get_extracted_header_columns(level)

    def write_header(self, level):
        # Fixed CNAqc-style header expected by the nf-core sigprofiler module.
        self.wf.write(self.HEADER)

    def write_table_row(self, row):
        columns = self.extracted_cols['variant']
        vals = {}
        for i, col in enumerate(columns):
            vals[col['col_name']] = row[i]
        chrom = vals.get('base__chrom')
        pos = vals.get('base__pos')
        gposend = vals.get('base__gposend')
        ref = vals.get('base__ref_base')
        alt = vals.get('base__alt_base')
        uid = vals.get('base__uid')
        if chrom is None or ref is None or alt is None:
            return
        chrom = str(chrom)
        # The nf-core module strips the "chr" prefix with str[3:], so the input
        # must carry it. Normalize to be safe across mappers.
        if not chrom.startswith('chr'):
            chrom = 'chr' + chrom
        ref = str(ref)
        alt = str(alt)
        # By default emit only single-base substitutions (SBS), which is what
        # the nf-core sigprofiler module (mut_type='SNP') handles. Indels / MNPs
        # are skipped unless include-indels is enabled.
        if not self.include_indels:
            if not (
                len(ref) == 1
                and len(alt) == 1
                and ref in 'ACGT'
                and alt in 'ACGT'
                and ref != alt
            ):
                return
        from_pos = '' if pos is None else pos
        to_pos = gposend if gposend is not None else from_pos
        samples = self.sample_map.get(uid)
        if not samples:
            # No per-sample rows: fall back to every known sample using the
            # variant-level alternate read count (if any) for NV.
            ar = self.var_alt_reads.get(uid)
            for sid in self.all_sample_ids:
                self._write_row(chrom, self._clean_sample_id(sid),
                                from_pos, to_pos, ref, alt, ar)
        else:
            for sid, ar in samples:
                self._write_row(chrom, self._clean_sample_id(sid),
                                from_pos, to_pos, ref, alt, ar)

    def _write_row(self, chrom, indiv, from_pos, to_pos, ref, alt, alt_reads):
        nv = alt_reads
        if nv is None or nv == '':
            nv = self.default_nv
        self.wf.write(
            f'{chrom}\t{indiv}\t{from_pos}\t{to_pos}\t{ref}\t{alt}\t{nv}\n'
        )


def main():
    reporter = Reporter(sys.argv)
    reporter.run()


if __name__ == '__main__':
    main()
