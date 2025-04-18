# PrimateAI: deep residual neural network for classifying the pathogenicity of missense mutations

PrimateAI used a semi-supervised benign vs unlabeled training regimen to train ~380,000 missense variants from humans and six from non-human primates. Amino acid sequences flanking the variant of interest and the orthologous sequence alignments in other species are input into the network. The result is a pathogenicity score ranging from 0 to 1, the larger the score the more pathogenic the variant is. To incorporate information about protein structure, PrimateAI learns to predict secondary structure and solvent accessibility from amino acid sequence, and includes these as sub-networks in the full model. The total size of the network, with protein structure included, is 36 layers of convolutions, consisting of roughly 400,000 trainable parameters.

## Clinical Application

The ClinGen Sequence Variant Interpretation Working Group reccommends that calibrated scores from select variant effect predictors are reliable as Very Strong, Strong, or Moderate evidence for Pathogenicity (PP3) or Benignity (BP4) within ACMG/AMP Guidelines (Pejaver, Vikas et al. “Calibration of computational tools for missense variant pathogenicity classification and ClinGen recommendations for PP3/BP4 criteria.” American journal of human genetics vol. 109,12 (2022): 2163-2177. doi:10.1016/j.ajhg.2022.10.013).

PrimateAI scores have been calbrated and validated as reliable to support Benign Supporting, Benign Moderate, Pathogenic Supporting, and Pathogenic Moderate ACMG/AMP evidence for purposes of variant classification in the clinic.

| ACMG Category    | Strength    | PrimateAI Thresholds |
|------------------|-------------|---------------------:|
| Benign (BP4)     | Very Strong |                    - |
|                  | Strong      |                    - |
|                  | Moderate    |               ≤0.362 |
|                  | Supporting  |       (0.362, 0.483] |
| Pathogenic (PP3) | Supporting  |       [0.790, 0.867) |
|                  | Moderate    |               ≥0.867 |
|                  | Strong      |                    - |
|                  | Very Strong |                    - |

\* A "-" means that PrimateAI did not meet the posterior probability threshold. Note that "(" and ")" indicate exclusion of the end value and “[” and “]” indicate inclusion of the end value.

### Indeterminate Scores

If the PrimateAI score does not fit within the thresholds above, Benign (BP4) and Pathogenic (PP3) columns are left blank and described as "Indeterminate" in the corresponding PrimateAI widget.

Information from https://doi.org/10.1038/s41588-018-0167-z
