# HGVS Converter

Converts from a list of HGVS strings. This is enabled by a proxy api that converts HGVS strings to genomic coordinates using the HGVS python package.

Example Input:

```text
# HGVS strings one per line
# Comments are allowed with a # at the beginning of the line
NC_000023.11:g.32389644G>A
NM_001002261.3:c.805_809del5
NM_004333.4:c.1799T>A
```