# DANN: a deep learning approach for annotating the pathogenicity of genetic variants

Annotating genetic variants for the purpose of identifying pathogenic variants remains a challenge. Combined annotation-dependent depletion (CADD) is an algorithm designed to annotate coding variants, and has been shown to outperform other annotation algorithms. CADD trains a linear kernel support vector machine (SVM) to differentiate evolutionarily derived, likely benign, alleles from simulated, likely deleterious, variants. However, SVMs cannot capture non-linear relationships among the features, which can limit performance. To address this issue, we have developed DANN. DANN uses the same feature set and training data as CADD to train a deep neural network (DNN). DNNs can capture non-linear relationships among features and are better suited than SVMs for problems with a large number of samples and features.  DANN achieves about a 19% relative reduction in the error rate and about a 14% relative increase in the area under the curve (AUC) metric over CADD’s SVM methodology.

Information from https://academic.oup.com/bioinformatics/article/31/5/761/2748191


## Clinical Application

 The ClinGen Sequence Variant Interpretation Working Group reccommends that calibrated scores from select variant effect predictors are reliable as Very Strong, Strong, or Moderate evidence for Pathogenicity (PP3) or Benignity (BP4) within ACMG/AMP Guidelines (Pejaver, Vikas et al. “Calibration of computational tools for missense variant pathogenicity classification and ClinGen recommendations for PP3/BP4 criteria.” American journal of human genetics vol. 109,12 (2022): 2163-2177. doi:10.1016/j.ajhg.2022.10.013). DANN scores have been calbrated by the Karchin Lab according to these methods using the code and variant sites.

| ACMG Category    | Strength    |     DANN Thresholds |
|------------------|-------------|--------------------:|
| Benign (BP4)     | Very Strong |                   - |
|                  | Strong      |         <= 0.356222 |
|                  | Moderate    | (0.356222, 0.90647] |
|                  | Supporting  | (0.90647, 0.949523] |
| Pathogenic (PP3) | Supporting  |          > 0.999145 |
|                  | Moderate    |                   - |
|                  | Strong      |                   - |
|                  | Very Strong |                   - |


 \* A "-" means that DANN did not meet the posterior probability threshold. Note that "(" and ")" indicate exclusion of the end value and “[” and “]” indicate inclusion of the end value.

 ### Indeterminate Scores

 If the DANN score does not fit within the thresholds above, Benign (BP4) and Pathogenic (PP3) columns are left blank and described as "Indeterminate" in the corresponding DANN widget.
