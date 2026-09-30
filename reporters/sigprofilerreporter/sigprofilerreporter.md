# SigProfiler Reporter

Exports somatic variants as a tab-delimited file in the **CNAqc joint-table
format** that the [nf-core `sigprofiler`
module](https://github.com/nf-core/modules/tree/master/modules/nf-core/sigprofiler)
consumes as input.

## Output format

A plain TSV with the fixed header and one row per (variant, sample):

```
chr	Indiv	from	to	ref	alt	NV
chr1	TCGA-E9-A1N9-01A-11D-A14G-09	17953367	17953367	G	A	5
```

This matches the columns the nf-core `sigprofiler` module reads in its
`process_tsv_join` / `input_processing` functions: it strips the `chr` prefix,
keeps rows with `NV != "0"`, and feeds the mutations to
`SigProfilerMatrixGenerator`.

| Column | Source in the OpenCRAVAT database |
|--------|-----------------------------------|
| `chr`  | `base__chrom` (normalized to carry the `chr` prefix) |
| `Indiv`| `sample.base__sample_id` (per carrying sample) |
| `from` | `base__pos` |
| `to`   | `base__gposend` (falls back to `from` for SNVs) |
| `ref`  | `base__ref_base` |
| `alt`  | `base__alt_base` |
| `NV`   | `sample.base__alt_reads` (variant-level `vcfinfo__alt_reads`, then `default-nv`) |

## Usage

Run all samples in a **single** `oc run` so they land in one SQLite, then run
the reporter to get one combined TSV:

```bash
# 50 TCGA BRCA VCFs -> one SQLite with all samples
oc run sample1.vcf sample2.vcf ... sample50.vcf \
    -a clinvar gnomad cgl civic -l hg38 -d <out_dir>

# one SQLite -> one combined TSV (all samples)
oc report <run_name>.sqlite -t sigprofiler -d <out_dir> --md <modules_dir>
```

This produces `<run_name>.sigprofiler.tsv` containing one row per
(variant, sample) across **all** input VCFs, ready to feed directly to the
nf-core `sigprofiler` module's `tsv_list` input (a single file is fine).

> `oc run` with multiple VCFs produces a single SQLite whose `sample` table
> holds every input sample (matched normals are excluded automatically; only
> the tumor/sample column of each VCF is kept). The reporter expands each
> variant to one row per carrying sample, so a multi-sample run yields a joint
> mutation table in one file.

Alternatively, if you already have per-sample SQLite databases, you can run
the reporter on each and pass all the resulting TSVs as the `tsv_list` input;
the nf-core module's `process_tsv_join` concatenates them.

## Options

Pass via `--module-option sigprofilerreporter.<key>=<value>`:

- `include-indels` (bool, default `false`): also emit indels and MNPs. Off by
  default because the nf-core module assigns `mut_type = "SNP"` to every row,
  so only single-base substitutions are processed correctly.
- `default-nv` (string, default `1`): NV value used when per-sample alternate
  read count is unavailable, so called variants are not dropped by the
  module's `NV != "0"` filter.

## Notes

- SigProfiler builds a per-sample mutation matrix (one column per sample), so
  the reporter writes one row per (variant, sample). Aggregating a cohort into a
  single sample is not supported: signatures are deconvolved from the
  per-sample distribution of mutations, which a pooled count cannot represent.
- The reporter emits variants from the `variant` level. Filters applied to the
  report (e.g. via `-f`/`-F`) are respected.
- For mitochondrial chromosomes, the nf-core module strips the `chr` prefix to
  `M`/`MT`; verify the reference genome expected by SigProfiler if your data
  contains `chrM`.
