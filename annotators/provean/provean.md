# PROVEAN 

(Protein Variation Effect Analyzer) is a software tool which predicts whether an amino acid substitution or indel has an impact on the biological function of a protein.

PROVEAN is useful for filtering sequence variants to identify nonsynonymous or indel variants that are predicted to be functionally important.

The performance of PROVEAN is comparable to popular tools such as SIFT or PolyPhen-2.

A fast computation approach to obtain pairwise sequence alignment scores enabled the generation of precomputed PROVEAN predictions for 20 single AA substitutions and a single AA deletion at every amino acid position of all protein sequences.

Information from http://provean.jcvi.org/index.php


## Clinical Application

 The ClinGen Sequence Variant Interpretation Working Group reccommends that calibrated scores from select variant effect predictors are reliable as Very Strong, Strong, or Moderate evidence for Pathogenicity (PP3) or Benignity (BP4) within ACMG/AMP Guidelines (Pejaver, Vikas et al. “Calibration of computational tools for missense variant pathogenicity classification and ClinGen recommendations for PP3/BP4 criteria.” American journal of human genetics vol. 109,12 (2022): 2163-2177. doi:10.1016/j.ajhg.2022.10.013). Provean scores have been calbrated by the Karchin Lab according to these methods using the code and variant sites.

 | Provean Thresholds |        |          |            |                  |          |        |             |
 |--------------------|--------|----------|------------|------------------|----------|--------|-------------|
 | Benign (BP4)       |        |          |            | Pathogenic (PP3) |          |        |             |
 | Very Strong        | Strong | Moderate | Supporting | Supporting       | Moderate | Strong | Very Strong |
 | -                  | -      | -        | -          | -                | -        | -      | -           |


 \* The "-" indicates that Provean did not meet any posterior probability thresholds.
