# GERP++: Genomic Evolutionary Rate Profiling
GERP++ identifies constrained elements in multiple alignments by quantifying substitution deficits. These deficits represent substitutions that would have occurred if the element were neutral DNA, but did not occur because the element has been under functional constraint. We refer to these deficits as "Rejected Substitutions" (RS).

## Clinical Application

The ClinGen Sequence Variant Interpretation Working Group reccommends that calibrated scores from select variant effect predictors are reliable as Very Strong, Strong, or Moderate evidence for Pathogenicity (PP3) or Benignity (BP4) within ACMG/AMP Guidelines (Pejaver, Vikas et al. “Calibration of computational tools for missense variant pathogenicity classification and ClinGen recommendations for PP3/BP4 criteria.” American journal of human genetics vol. 109,12 (2022): 2163-2177. doi:10.1016/j.ajhg.2022.10.013).

GERP++ RS (Rejected Substitution) scores have been calbrated and validated as reliable to support Benign Supporting and Benign Moderate ACMG/AMP evidence for purposes of variant classification in the clinic.

| ACMG Category    | Strength    | GERP++ Thresholds |
|------------------|-------------|------------------:|
| Benign (BP4)     | Very Strong |                 - |
|                  | Strong      |                 - |
|                  | Moderate    |           ≤ −4.54 |
|                  | Supporting  |     (−4.54, 2.70] |
| Pathogenic (PP3) | Supporting  |                 - |
|                  | Moderate    |                 - |
|                  | Strong      |                 - |
|                  | Very Strong |                 - |

\* A "-" means that GERP++ did not meet the posterior probability threshold. Note that "(" and ")" indicate exclusion of the end value and “[” and “]” indicate inclusion of the end value.

### Indeterminate Scores

If the GERP++ score does not fit within the thresholds above, Benign (BP4) and Pathogenic (PP3) columns are left blank and described as "Indeterminate" in the corresponding GERP++ widget.
