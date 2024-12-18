## For local installations, read the installation section. This module requires the python package `pytabix`, and is not available for Windows operating system.

# FATHMM XF 

FATHMM-XF (FATHMM with eXtended Features) represents a substantial improvement over our earlier predictor, FATHMM-MKL. By using an extended set of feature groups and by exploring an expanded set of possible models, the new method yields even greater accuracy than its predecessor on independent test sets. As with FATHMM-MKL, FATHMM-XF predicts whether single nucleotide variants (SNVs) in the human genome are likely to be functional or non-functional in inherited diseases. Also like its predecessor, it uses distinct models for coding and non-coding regions, to improve overall accuracy. Unlike FATHMM-MKL, FATHMM-XF models are build up on single-kernel datasets. The models may then learn interactions between data sources that help to boost its accuracy in all regions of the genome.

## Predicted Interpretation

Predictions are given as p-values in the range [0, 1]: values above 0.5 are predicted to be deleterious, while those below 0.5 are predicted to be neutral or benign. P-values close to the extremes (0 or 1) are the highest-confidence predictions that yield the highest accuracy.

We use distinct predictors for positions either in coding regions (positions within coding-sequence exons). The coding predictor is based on six groups of features representing sequence conservation, nucleotide sequence characteristics, genomic features (codons, splice sites, etc.), amino acid features and expression levels in different tissues. 

Information from http://fathmm.biocompute.org.uk/fathmm-xf/about.html

# Local Installation

Install the `FATHMM XF` module

```bash
oc module install fathmm_xf
```
FATHMM XF uses the python package pytabix for querying the data. On Mac and Linux systems, this can be installed with `pip3 install --user pytabix`. If this does not work, consult the [pytabix website](https://pypi.org/project/pytabix/) for more options.

