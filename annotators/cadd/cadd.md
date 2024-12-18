## _For local installation, read the installation section. This module requires the python package `pytabix`, and is not available for Windows operating system._

# CADD

CADD is a tool for scoring the deleteriousness of single nucleotide variants as well as insertion/deletions variants in the human genome.

While many variant annotation and scoring tools are around, most annotations tend to exploit a single information type (e.g. conservation) and/or are restricted in scope (e.g. to missense changes). Thus, a broadly applicable metric that objectively weights and integrates diverse information is needed. Combined Annotation Dependent Depletion (CADD) is a framework that integrates multiple annotations into one metric by contrasting variants that survived natural selection with simulated mutations.

C-scores strongly correlate with allelic diversity, pathogenicity of both coding and non-coding variants, and experimentally measured regulatory effects, and also highly rank causal variants within individual genome sequences. Finally, C-scores of complex trait-associated variants from genome-wide association studies (GWAS) are significantly higher than matched controls and correlate with study sample size, likely reflecting the increased accuracy of larger GWAS.

CADD can quantitatively prioritize functional, deleterious, and disease causal variants across a wide range of functional categories, effect sizes and genetic architectures and can be used prioritize causal variation in both research and clinical settings. 

## Short method summary

Fixed or nearly fixed recent evolutionary changes were identified as differences between 1000 Genomes and the Ensembl Compara inferred human-chimpanzee ancestral genome (derived allele frequency (DAF) of at least 95%, 14.9 million SNVs and 1.7 million indels). To simulate an equivalent number of mutations, we used an empirical model of sequence evolution with CpG dinucleotide-specific rates and mutation rates locally scaled in megabase windows. For annotation, we used the Ensembl Variant Effect Predictor (VEP), data from the ENCODE project and information from UCSC genome browser tracks. These annotations span a wide range of data types including conservation metrics like GERP, phastCons, and phyloP; functional genomic data like DNase hypersensitivity and transcription factor binding; transcript information like distance to exon-intron boundaries or expression levels in commonly studied cell lines; and protein-level scores like Grantham, SIFT, and PolyPhen. 

## Notes on using scaled vs. unscaled C-scores

We believe that CADD scores are useful in two distinct forms, namely "raw" and "scaled", and we provide both in our output files. "Raw" CADD scores come straight from the model, and are interpretable as the extent to which the annotation profile for a given variant suggests that the variant is likely to be "observed" (negative values) vs "simulated" (positive values). These values have no absolute unit of meaning and are incomparable across distinct annotation combinations, training sets, or model parameters. However, raw values do have relative meaning, with higher values indicating that a variant is more likely to be simulated (or "not observed") and therefore more likely to have deleterious effects.

Since the raw scores do have relative meaning, one can take a specific group of variants, define the rank for each variant within that group, and then use that value as a "normalized" and now externally comparable unit of analysis. In our case, we scored and ranked all ~8.6 billion SNVs of the GRCh37/hg19 reference and then "PHRED-scaled" those values by expressing the rank in order of magnitude terms rather than the precise rank itself. For example, reference genome single nucleotide variants at the 10th-% of CADD scores are assigned to CADD-10, top 1% to CADD-20, top 0.1% to CADD-30, etc. The results of this transformation are the "scaled" CADD scores. 

## Clinical Application

The ClinGen Sequence Variant Interpretation Working Group reccommends that calibrated scores from select variant effect predictors are reliable as Very Strong, Strong, or Moderate evidence for Pathogenicity (PP3) or Benignity (BP4) within ACMG/AMP Guidelines (Pejaver, Vikas et al. “Calibration of computational tools for missense variant pathogenicity classification and ClinGen recommendations for PP3/BP4 criteria.” American journal of human genetics vol. 109,12 (2022): 2163-2177. doi:10.1016/j.ajhg.2022.10.013).

CADD phred scores have been calbrated and validated as reliable to support Benign Supporting, Benign Moderate, Benign Strong, Benign Very Strong, Pathogenic Supporting and Pathogenic Moderate ACMG/AMP evidence for purposes of variant classification in the clinic.

| CADD Thresholds |                 |                |                |                |                |                |                |                |
|--------------|-----------------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|
| Benign (BP4) |||| Pathogenic (PP3)|
|Very Strong   |Strong      |Moderate     |Supporting   |Supporting   |Moderate     |Strong      |Very Strong   |
|-|<= 0.15|(0.15, 17.3]|(17.3, 22.7]|[25.3, 28.1)|>= 28.1|-|   -   |

\* A "-" means that CADD did not meet the posterior probability threshold. Note that "(" and ")" indicate exclusion of the end value and “[” and “]” indicate inclusion of the end value.

### Indeterminate Scores

If the CADD score does not fit within the thresholds above, Benign (BP4) and Pathogenic (PP3) columns are left blank and described as "Indeterminate" in the corresponding CADD widget.

Information from https://cadd.gs.washington.edu/info

# Local Installation

To install the `CADD` module

```bash
oc module install cadd
```
CADD uses the python package pytabix for querying the data. On Mac and Linux systems, this can be installed with `pip3 install --user pytabix`. If this does not work, consult the [pytabix website](https://pypi.org/project/pytabix/) for more options.

