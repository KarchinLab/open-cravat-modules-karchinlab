# MetaRNN

MetaRNN is a pathogenicity prediction score for human nonsynonymous SNVs (nsSNVs). It integrates information from 28 high-level annotation scores (16 functional prediction scores including SIFT, Polyphen2_HDIV, Polyphen2_HVAR, MutationAssessor, PROVEAN, VEST4, M-CAP, REVEL, MutPred, MVP, PrimateAI, DEOGEN2, CADD, fathmm-XF, Eigen and GenoCanyon, 8 conservation scores including GERP, phyloP100way_vertebrate, phyloP30way_mammalian, phyloP17way_primate, phastCons100way_vertebrate, phastCons30way_mammalian, phastCons17way_primate and SiPhy, and 4 allele frequency information from the 1000 Genomes Project, ExAC, gnomAD exome, and gnomAD genome) to produce an ensemble prediction model with a deep recurrent neural network (RNN). The final prediction is the likelihood of a nsSNV being pathogenic. 

## Clinical Application

WARNING: This predictor used population allele frequency of a variant as a feature. If you are using the ACMG/AMP framework “Population Data” and “Computational Predictions” are two independent categories. Therefore, if you use this predictor you cannot also include any “Population Data” evidence towards your final classification. If you use a variant effect predictor that did not include populaqtion allele frequency as a feature, it is fine to use both the “Computational Predictions” and “Population Data” evidence categories in your final classification. MetaRNN is based on 16 component scores (SIFT, Polyphen2_HDIV, Polyphen2_HVAR, MutationAssessor, PROVEAN, VEST4, M-CAP, REVEL, MutPred, MVP, PrimateAI, DEOGEN2, CADD, fathmm-XF, Eigen and GenoCanyon), 8 conservation scores (GERP, phyloP100way_vertebrate, phyloP30way_mammalian, phyloP17way_primate, phastCons100way_vertebrate, phastCons30way_mammalian, phastCons17way_primate and SiPhy) and allele frequency information from the 1000 Genomes Project, ExAC, and gnomAD. 

 The ClinGen Sequence Variant Interpretation Working Group reccommends that calibrated scores from select variant effect predictors are reliable as Very Strong, Strong, or Moderate evidence for Pathogenicity (PP3) or Benignity (BP4) within ACMG/AMP Guidelines (Pejaver, Vikas et al. “Calibration of computational tools for missense variant pathogenicity classification and ClinGen recommendations for PP3/BP4 criteria.” American journal of human genetics vol. 109,12 (2022): 2163-2177. doi:10.1016/j.ajhg.2022.10.013). MetaRNN scores have been calbrated by the Karchin Lab according to these methods using the code and variant sites.

| ACMG Category    | Strength    |   MetaRNN Thresholds |
|------------------|-------------|---------------------:|
| Benign (BP4)     | Very Strong |                    - |
|                  | Strong      |          <= 0.052789 |
|                  | Moderate    | (0.052789, 0.188378] |
|                  | Supporting  | (0.188378, 0.295726] |
| Pathogenic (PP3) | Supporting  | (0.655095, 0.786338] |
|                  | Moderate    | (0.786338, 0.934075] |
|                  | Strong      |           > 0.934075 |
|                  | Very Strong |                    - |


 \* A "-" means that MetaRNN did not meet the posterior probability threshold. Note that "(" and ")" indicate exclusion of the end value and “[” and “]” indicate inclusion of the end value.

 ### Indeterminate Scores

 If the MetaRNN score does not fit within the thresholds above, Benign (BP4) and Pathogenic (PP3) columns are left blank and described as "Indeterminate" in the corresponding MetaRNN widget.
