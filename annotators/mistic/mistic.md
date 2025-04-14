# MISTIC - MISsense deleTeriousness predICtor

MISTIC uses a supervised machine-learning model dedicated to the prediction of deleterious missense variants. MISTIC incorporates a Soft Voting system using the machine-learning algorithms Random Forest and Logistic Regression. The algorithms were trained to distinguish deleterious from benign missense variants based on a selection of 113 missense features. Examples of these features include multi-ethnic minor allele frequencies and evolutionary conservation, and physiochemical and biochemical properties of amino acids.

## Scores

The Soft Voting system generates a score from 0 to 1 and represents the probability of a given missense variant to be classified as deleterious. By default, missense variants with scores >0.5 are classified as deleterious and missense variants with scores <0.5 are classified as benign.

Information from https://lbgi.fr/mistic/

## Clinical Application

The ClinGen Sequence Variant Interpretation Working Group reccommends that calibrated scores from select variant effect predictors are reliable as Very Strong, Strong, or Moderate evidence for Pathogenicity (PP3) or Benignity (BP4) within ACMG/AMP Guidelines (Pejaver, Vikas et al. “Calibration of computational tools for missense variant pathogenicity classification and ClinGen recommendations for PP3/BP4 criteria.” American journal of human genetics vol. 109,12 (2022): 2163-2177. doi:10.1016/j.ajhg.2022.10.013).

MISTIC scores (that do not include the background population frequency of the variant) have been calbrated and validated as reliable to support Benign Supporting, Benign Moderate, Pathogenic Supporting, Pathogenic Moderate, and Pathogenic Strong ACMG/AMP evidence for purposes of variant classification in the clinic.

| MISTIC Thresholds |        |          |                |                  |              |        |             |   |
|-------------------|--------|----------|----------------|------------------|--------------|--------|-------------|---|
| Benign (BP4)      |        |          |                | Pathogenic (PP3) |              |        |             |   |
| Very Strong       | Strong | Moderate | Supporting     | Supporting       | Moderate     | Strong | Very Strong |   |
| -                 | -      | ≤ −0.36  | (−0.36, −0.18] | [0.13, 0.27)     | [0.27, 0.50) | ≥0.50  | -           |   |

\* A "-" means that MISTIC did not meet the posterior probability threshold. Note that "(" and ")" indicate exclusion of the end value and “[” and “]” indicate inclusion of the end value.
