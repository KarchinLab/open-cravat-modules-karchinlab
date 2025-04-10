# Mutation Assessor: database providing prediction of the functional impact of amino-acid substitutions in proteins
Functional impact is calculated based on evolutionary conservation of the affected amino acid in protein homologs. The method has been validated on a large set (60k) of disease associated (OMIM) and polymorphic variants.

1. Variant: Amino acid variant
2. Score: Mutation Assessor functional impact combined score (MAori). The score ranges from -5.135 to 6.49
3. Ranked Score: MAori scores were ranked among all MAori scores in the database. The rankscore is the ratio of the rank of the score over the total number of MAori scores in the database. The scores range from 0 to 1.
4. Functional Impact: Predicted functional, i.e. high ("H") or medium ("M"), or predicted non-functional, i.e. low ("L") or neutral ("N"). The MAori score cutoffs between "H" and "M", "M" and "L", and "L" and "N", are 3.5, 1.935 and 0.8, respectively. The rankscore cutoffs between "H" and "M", "M" and "L", and "L" and "N", are 0.92922, 0.51944 and 0.19719, respectively.


## Clinical Application

 The ClinGen Sequence Variant Interpretation Working Group reccommends that calibrated scores from select variant effect predictors are reliable as Very Strong, Strong, or Moderate evidence for Pathogenicity (PP3) or Benignity (BP4) within ACMG/AMP Guidelines (Pejaver, Vikas et al. “Calibration of computational tools for missense variant pathogenicity classification and ClinGen recommendations for PP3/BP4 criteria.” American journal of human genetics vol. 109,12 (2022): 2163-2177. doi:10.1016/j.ajhg.2022.10.013). Mutation Assessor scores have been calbrated by the Karchin Lab according to these methods using the code and variant sites.

 | Mutation Assessor Thresholds |        |          |              |                  |          |        |             |
 |------------------------------|--------|----------|--------------|------------------|----------|--------|-------------|
 | Benign (BP4)                 |        |          |              | Pathogenic (PP3) |          |        |             |
 | Very Strong                  | Strong | Moderate | Supporting   | Supporting       | Moderate | Strong | Very Strong |
 | -                            | -      | <= -0.3  | (-0.3, 0.99] | (2.88, 3.62]     | > 3.62   | -      | -           |

 \* A "-" means that Mutation Assessor did not meet the posterior probability threshold. Note that "(" and ")" indicate exclusion of the end value and “[” and “]” indicate inclusion of the end value.

 ### Indeterminate Scores

 If the Mutation Assessor score does not fit within the thresholds above, Benign (BP4) and Pathogenic (PP3) columns are left blank and described as "Indeterminate" in the corresponding Mutation Assessor widget.
