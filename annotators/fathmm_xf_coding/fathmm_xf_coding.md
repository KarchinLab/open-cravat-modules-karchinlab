# FATHMM XF 

FATHMM-XF (FATHMM with eXtended Features) represents a substantial improvement over our earlier predictor, FATHMM-MKL. By using an extended set of feature groups and by exploring an expanded set of possible models, the new method yields even greater accuracy than its predecessor on independent test sets. As with FATHMM-MKL, FATHMM-XF predicts whether single nucleotide variants (SNVs) in the human genome are likely to be functional or non-functional in inherited diseases. Also like its predecessor, it uses distinct models for coding and non-coding regions, to improve overall accuracy. Unlike FATHMM-MKL, FATHMM-XF models are build up on single-kernel datasets. The models may then learn interactions between data sources that help to boost its accuracy in all regions of the genome.

## Predicted Interpretation

Predictions are given as p-values in the range [0, 1]: values above 0.5 are predicted to be deleterious, while those below 0.5 are predicted to be neutral or benign. P-values close to the extremes (0 or 1) are the highest-confidence predictions that yield the highest accuracy.

We use distinct predictors for positions either in coding regions (positions within coding-sequence exons). The coding predictor is based on six groups of features representing sequence conservation, nucleotide sequence characteristics, genomic features (codons, splice sites, etc.), amino acid features and expression levels in different tissues. 

Information from http://fathmm.biocompute.org.uk/fathmm-xf/about.html

## Clinical Application

 The ClinGen Sequence Variant Interpretation Working Group reccommends that calibrated scores from select variant effect predictors are reliable as Very Strong, Strong, or Moderate evidence for Pathogenicity (PP3) or Benignity (BP4) within ACMG/AMP Guidelines (Pejaver, Vikas et al. “Calibration of computational tools for missense variant pathogenicity classification and ClinGen recommendations for PP3/BP4 criteria.” American journal of human genetics vol. 109,12 (2022): 2163-2177. doi:10.1016/j.ajhg.2022.10.013). FATHMM XF Coding scores have been calbrated by the Karchin Lab according to these methods using the code and variant sites.

 | FATHMM XF Coding Thresholds |        |          |            |                      |            |        |             |
 |-----------------------------|--------|----------|------------|----------------------|------------|--------|-------------|
 | Benign (BP4)                |        |          |            | Pathogenic (PP3)     |            |        |             |
 | Very Strong                 | Strong | Moderate | Supporting | Supporting           | Moderate   | Strong | Very Strong |
 | -                           | -      | -        | -          | (0.869754, 0.955427] | > 0.955427 | -      | -           |


 \* A "-" means that FATHMM XF Coding did not meet the posterior probability threshold. Note that "(" and ")" indicate exclusion of the end value and “[” and “]” indicate inclusion of the end value.

 ### Indeterminate Scores

 If the FATHMM XF Coding score does not fit within the thresholds above, Benign (BP4) and Pathogenic (PP3) columns are left blank and described as "Indeterminate" in the corresponding FATHMM XF Coding widget.
