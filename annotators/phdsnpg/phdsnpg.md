# PhD-SNPg

A binary classifier for predicting pathogenic variants in coding and non-coding regions.

PhD-SNPg is a binary classifier that implements Gradient Boosting-based algorithm from scikit-learn package (http://scikit-learn.org/). PhD-SNPg has been trained and tested using a set of ~37,000 Pathogenic and Benign SNVs extracted from Clinvar dataset.

![Screenshot](phdsnpg_screenshot_1.png)
<br />

## Clinical Application

 The ClinGen Sequence Variant Interpretation Working Group reccommends that calibrated scores from select variant effect predictors are reliable as Very Strong, Strong, or Moderate evidence for Pathogenicity (PP3) or Benignity (BP4) within ACMG/AMP Guidelines (Pejaver, Vikas et al. “Calibration of computational tools for missense variant pathogenicity classification and ClinGen recommendations for PP3/BP4 criteria.” American journal of human genetics vol. 109,12 (2022): 2163-2177. doi:10.1016/j.ajhg.2022.10.013). PhD-SNPg scores have been calbrated by the Karchin Lab according to these methods using the code and variant sites.

 | PhD-SNPg Thresholds |        |          |                |                  |          |        |             |
 |---------------------|--------|----------|----------------|------------------|----------|--------|-------------|
 | Benign (BP4)        |        |          |                | Pathogenic (PP3) |          |        |             |
 | Very Strong         | Strong | Moderate | Supporting     | Supporting       | Moderate | Strong | Very Strong |
 | -                   | -      | <= 0.322 | (0.322, 0.771] | (0.968, 0.987]   | >0.987   | -      | -           |

 \* A "-" means that PhD-SNPg did not meet the posterior probability threshold. Note that "(" and ")" indicate exclusion of the end value and “[” and “]” indicate inclusion of the end value.

 ### Indeterminate Scores

 If the PhD-SNPg score does not fit within the thresholds above, Benign (BP4) and Pathogenic (PP3) columns are left blank and described as "Indeterminate" in the corresponding PhD-SNPg widget.

