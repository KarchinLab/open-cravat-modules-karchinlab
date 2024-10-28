# Clingen Allele Registry Converter

Converts from a list of Clingen Allele Registy CA IDs. This converter requires an internet connection to call the Clingen Allele Registry API.

Example Input:

```text
# CA IDs one per line
# Comments are allowed with a # at the beginning of the line
# Optionally, sample ids and tags can be added as tab-delimited columns.
# e.g.
# CA12345   sample_name  tag_name
CA16043531
CA10583404
CA114360
```

This annotator uses the bulk query endpoint, for example like this:
```bash
curl --location 'https://reg.clinicalgenome.org/alleles?file=id' \
--header 'Content-Type: application/javascript' \
--data 'CA37220
CA337437888
CA415748309'
```