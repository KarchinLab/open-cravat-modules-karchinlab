# AlphaMissense

AlphaMissense is a deep learning model that builds on the protein structure prediction tool AlphaFold2. The model is trained on population frequency data and uses sequence and predicted structural context, all of which contribute to its performance.

AlphaMissense leverages advances on multiple fronts: (i) unsupervised protein language modeling to learn amino acid distributions conditioned on sequence context; (ii) incorporating structural context by using an AlphaFold-derived system; and (iii) fine-tuning on weak labels from population frequency data, thereby avoiding bias from human-curated annotations. AlphaMissense achieves state-of-the-art missense pathogenicity predictions in clinical annotation, de novo disease variants, and experimental assay benchmarks without explicitly training on such data.

## Clinical Application

The ClinGen Sequence Variant Interpretation Working Group reccommends that calibrated scores from select variant effect predictors are reliable as Strong, NA, Moderate, or Supporting evidence for Pathogenicity (PP3) or Benignity (BP4) within ACMG/AMP Guidelines (Pejaver, Vikas et al. “Calibration of computational tools for missense variant pathogenicity classification and ClinGen recommendations for PP3/BP4 criteria.” American journal of human genetics vol. 109,12 (2022): 2163-2177. doi:10.1016/j.ajhg.2022.10.013).

AlphaMissense scores have been calbrated and validated as reliable to support Benign Supporting, Benign Moderate, Pathogenic Supporting, Pathogenic Moderate, and Pathogenic Strong ACMG/AMP evidence for purposes of variant classification in the clinic.

| ACMG Category    | Strength   | AlphaMissense Thresholds |
|------------------|------------|-------------------------:|
| Benign (BP4)     | Strong     |                        - |
|                  | Moderate   |                 <= 0.099 |
|                  | Supporting |           (0.099, 0.169] |
| Pathogenic (PP3) | Supporting |           [0.792, 0.906) |
|                  | Moderate   |           [0.906, 0.990) |
|                  | Strong     |                   ≥0.990 |

\* A "-" means that BayesDel did not meet the posterior probability threshold. Note that "(" and ")" indicate exclusion of the end value and “[” and “]” indicate inclusion of the end value.

### Indeterminate Scores

If the AlphaMissense score does not fit within the thresholds above, Benign (BP4) and Pathogenic (PP3) columns are left blank and described as "Indeterminate" in the corresponding AlphaMissense widget.
