# BayesDel

BayesDel is a meta-score that assesses the pathogenicity of genetic variants. BayesDel provides scores and prediction both with and without the inclusion of Max Allele Frequency (this is the highest background population frequency among available continental popoulations). The higher the score, the more likely the variant is pathogenic. The author provides a universal cutoff value between Deleterious and Tolerated predictions that was obtained by maximizing sensitivity and specificity in classifying ClinVar variants. The cutoff is 0.0692655 with MaxAF and -0.0570105 without MaxAF.

The component scores for BayesDel include PolyPhen2, SIFT, FATHMM, LRT, Mutation Taster, Mutation Assessor, PhyloP, GERP++, and SiPhy. Scores with population allele frequency information include the maximum minor allele frequence across populations in the Exome Aggregation Consortium (ExAC) version 0.3 and the 1000 Genomes Project (G1K) phase 3.

## Data Disclaimer

The author of BayesDel does not provide precalculated scores for all genomic variants, therefore the BayesDel annotator only includes missense variants.

Information from https://doi.org/10.1002/humu.23158

## Clinical Application

The ClinGen Sequence Variant Interpretation Working Group reccommends that calibrated scores from select variant effect predictors are reliable as Very Strong, Strong, or Moderate evidence for Pathogenicity (PP3) or Benignity (BP4) within ACMG/AMP Guidelines (Pejaver, Vikas et al. “Calibration of computational tools for missense variant pathogenicity classification and ClinGen recommendations for PP3/BP4 criteria.” American journal of human genetics vol. 109,12 (2022): 2163-2177. doi:10.1016/j.ajhg.2022.10.013).

BayesDel scores (that do not include the background population frequency of the variant) have been calbrated and validated as reliable to support Benign Supporting, Benign Moderate, Pathogenic Supporting, Pathogenic Moderate, and Pathogenic Strong ACMG/AMP evidence for purposes of variant classification in the clinic.

| ACMG Category    | Strength    | BayesDel Thresholds |
|------------------|-------------|--------------------:|
| Benign (BP4)     | Very Strong |                   - |
|                  | Strong      |                   - |
|                  | Moderate    |             ≤ −0.36 |
|                  | Supporting  |      (−0.36, −0.18] |
| Pathogenic (PP3) | Supporting  |        [0.13, 0.27) |
|                  | Moderate    |        [0.27, 0.50) |
|                  | Strong      |               ≥0.50 |
|                  | Very Strong |                   - |

\* A "-" means that BayesDel did not meet the posterior probability threshold. Note that "(" and ")" indicate exclusion of the end value and “[” and “]” indicate inclusion of the end value.

### Indeterminate Scores

If the BayesDel score does not fit within the thresholds above, Benign (BP4) and Pathogenic (PP3) columns are left blank and described as "Indeterminate" in the corresponding BayesDel widget.
