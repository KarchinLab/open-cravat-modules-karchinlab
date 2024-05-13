# BayesDel

BayesDel is a meta-score that assesses the pathogenicity of genetic variants. BayesDel provides scores and prediction both with and without the inclusion of Max Allele Frequency (this is the highest background population frequency among available continental popoulations). The higher the score, the more likely the variant is pathogenic. The author provides a universal cutoff value between Deleterious and Tolerated predictions that was obtained by maximizing sensitivity and specificity in classifying ClinVar variants. The cutoff is 0.0692655 with MaxAF and -0.0570105 without MaxAF.

## Data Disclaimer

The author of BayesDel does not provide precalculated scores for all genomic variants, therefore the BayesDel annotator only includes missense variants.

Information from https://doi.org/10.1002/humu.23158


