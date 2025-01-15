# ESM1b
ESM1b is a 650-million-parameter protein language model used to predict all ~450 million possible missense variant effects in the human genome. The model was trained on 250 million protein sequences across all organisms via the masked language modeling task, where random residues are masked from input sequences and the model has to predict the correct amino acid at each position (including the missing residues).

## Scores
Each variant’s effect score is the log-likelihood ratio (LLR) between the variant and wild-type (WT) residue. The scores range from -24.538 to 6.937. The smaller the score, the more likely the variant is pathogenic.

## Results
To assess the performance of ESM1b in predicting the clinical impact of variants, the model’s effect scores between pathogenic and benign variants annotated in ClinVar and variants annotated by HGMD as disease-causing and benign variants from gnomAD (defined by allele frequency >1%) were compared. Only high-confidence variants were included. The distribution of ESM1b effect scores shows a substantial difference between pathogenic and benign variants in both datasets. Using an LLR threshold of −7.5 to distinguish between pathogenic and benign variants yields a true-positive rate of 81% and a true-negative rate of 82% in both datasets.

Information from https://doi.org/10.1038/s41588-023-01465-0

## Clinical Application

 The ClinGen Sequence Variant Interpretation Working Group reccommends that calibrated scores from select variant effect predictors are reliable as Very Strong, Strong, or Moderate evidence for Pathogenicity (PP3) or Benignity (BP4) within ACMG/AMP Guidelines (Pejaver, Vikas et al. “Calibration of computational tools for missense variant pathogenicity classification and ClinGen recommendations for PP3/BP4 criteria.” American journal of human genetics vol. 109,12 (2022): 2163-2177. doi:10.1016/j.ajhg.2022.10.013).

ESM1b scores have been calbrated and validated as reliable to support Benign Supporting, Benign Moderate, Benign Strong, Benign Very Strong, Pathogenic Supporting, Pathogenic Moderate, and Pathogenic Strong ACMG/AMP evidence for purposes of variant classification in the clinic. Calibration cutoffs were obtained from Bergquist et al., “Calibration of Additional Computational Tools Expands ClinGen Recommendation Options for Variant Classification with PP3/BP4 Criteria.” bioRxiv 2024.09.17.611902; doi:10.1101/2024.09.17.611902

 | ESM1b Thresholds |        |          |              |                  |                |        |             |
 |------------------|--------|----------|--------------|------------------|----------------|--------|-------------|
 | Benign (BP4)     |        |          |              | Pathogenic (PP3) |                |        |             |
 | Very Strong      | Strong | Moderate | Supporting   | Supporting       | Moderate       | Strong | Very Strong |
 | -                | -      | >-3.2    | (-6.2, -3.2] | (-12.2, -10.7]   | [-12.2, -24.0) | ≤-24.0 | -           |


 \* A "-" means that ESM1b did not meet the posterior probability threshold. Note that "(" and ")" indicate exclusion of the end value and “[” and “]” indicate inclusion of the end value.

 ### Indeterminate Scores

 If the ESM1b score does not fit within the thresholds above, Benign (BP4) and Pathogenic (PP3) columns are left blank and described as "Indeterminate" in the corresponding ESM1b widget.
