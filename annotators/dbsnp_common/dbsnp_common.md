# dbNSP Common

Contains information about a subset of the single nucleotide polymorphisms and small insertions and deletions (indels) — collectively Simple Nucleotide Polymorphisms — from [dbSNP](https://www.ncbi.nlm.nih.gov/snp/), available from ftp.ncbi.nlm.nih.gov/snp. Only SNPs that have a minor allele frequency (MAF) of at least 1% and are mapped to a single location in the reference genome assembly are included in this subset. Frequency data are not available for all SNPs, so this subset is incomplete. Allele counts from all submissions that include frequency data are combined when determining MAF, so for example the allele counts from the 1000 Genomes Project and an independent submitter may be combined for the same variant.

dbSNP provides download files in the Variant Call Format (VCF) that include a "COMMON" flag in the INFO column. That is determined by a different method, and is generally a superset of the UCSC Common set. dbSNP uses frequency data from the 1000 Genomes Project only, and considers a variant COMMON if it has a MAF of at least 0.01 in any of the five super-populations:

* African (AFR)
* Admixed American (AMR)
* East Asian (EAS)
* European (EUR)
* South Asian (SAS)

The selection of SNPs with a minor allele frequency of 1% or greater is an attempt to identify variants that appear to be reasonably common in the general population. Taken as a set, common variants should be less likely to be associated with severe genetic diseases due to the effects of natural selection, following the view that deleterious variants are not likely to become common in the population. However, the significance of any particular variant should be interpreted only by a trained medical geneticist using all available information.

Information from https://genome.ucsc.edu/cgi-bin/hgTrackUi?hgsid=784649537_AtjYqLFz0CTNkRh8qWf8vOHQpNXp&c=chr1&g=snp151Common