SIFT predicts whether an amino acid substitution affects protein function based on sequence homology and the physical properties of amino acids. SIFT can be applied to naturally occurring nonsynonymous polymorphisms and laboratory-induced missense mutations. It is widely used in bioinformatics, genetics, disease, and mutation studies. It annotates and provides damaging/tolerated predictions for single nucleotide variants.

## Brief Summary

SIFT takes a query sequence and uses multiple alignment information to predict tolerated and deleterious substitutions for every position of the query sequence.

SIFT is a multistep procedure that:

- searches for similar sequences,
- chooses closely related sequences that may share similar function to the query sequence ,
- obtains the alignment of these chosen sequences, and
- calculates normalized probabilities for all possible substitutions from the alignment.

## Interpreting Results

Positions with normalized probabilities less than 0.05 are predicted to be deleterious, those greater than or equal to 0.05 are predicted to be tolerated.

## Clinical Application

The ClinGen Sequence Variant Interpretation Working Group reccommends that calibrated scores from select variant effect predictors are reliable as Very Strong, Strong, or Moderate evidence for Pathogenicity (PP3) or Benignity (BP4) within ACMG/AMP Guidelines (Pejaver, Vikas et al. “Calibration of computational tools for missense variant pathogenicity classification and ClinGen recommendations for PP3/BP4 criteria.” American journal of human genetics vol. 109,12 (2022): 2163-2177. doi:10.1016/j.ajhg.2022.10.013).

SIFT scores have been calbrated and validated as reliable to support Benign Supporting, Benign Moderate, Pathogenic Supporting and Pathogenic Moderate ACMG/AMP evidence for purposes of variant classification in the clinic.

| SIFT Thresholds |                 |                |                |                |                |                |                |                |
|--------------|-----------------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|
| Benign (BP4) |||| Pathogenic (PP3)|
|Very Strong   |Strong      |Moderate     |Supporting   |Supporting   |Moderate     |Strong      |Very Strong   |
|-|-|≥0.327|[0.080, 0.327)|(0, 0.001]|0|	-|   -   |

\* A "-" means that BayesDel did not meet the posterior probability threshold. Note that "(" and ")" indicate exclusion of the end value and “[” and “]” indicate inclusion of the end value.

### Indeterminate Scores

If the SIFT score does not fit within the thresholds above, Benign (BP4) and Pathogenic (PP3) columns are left blank and described as "Indeterminate" in the corresponding SIFT widget.