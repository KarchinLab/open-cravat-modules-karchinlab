# MetaLR

MetaLR is a ensemble-based prediction algorithm devloped by integrating 10 component scores (SIFT, PolyPhen-2 HDIV, PolyPhen-2 HVAR, GERP++, MutationTaster, Mutation Assessor, FATHMM, LRT, SiPhy, PhyloP) and the maximum frequency observed in the 1000 genomes populations, using a logistic regression model.

## Scores

**MetaLR_score:** Our logistic regression (LR) based ensemble prediction score. Larger value means the SNV is more likely to be damaging. 
		Scores range from 0 to 1.

**MetaLR_rankscore:** MetaLR scores were ranked among all MetaLR scores in dbNSFP. The rankscore
		is the ratio of the rank of the score over the total number of MetaLR scores in dbNSFP. 
		The scores range from 0 to 1.

**MetaLR_pred:** Prediction of our MetaLR based ensemble prediction score,"T(olerated)" or
		"D(amaging)". The score cutoff between "D" and "T" is 0.5. The rankscore cutoff between 
		"D" and "T" is 0.81101.

## Logistic Regression and Support Vector Machine Models

MetaLR has a sister database, metaSVM, that explores the same concepts using a support vector machine model.

Quality of machine learning models, such as Support Vector Machine (SVM) and Logistic Regression (LR), can be influenced by selection of component scores as well as the selection of parameters. To optimize the selection of component scores and parameters for our SVM and LR model, we collected training dataset, on which we performed feature selection and parameter tuning for our models. 

Output scores were harvested from all of the prediction methods for all mutations in all of our datasets, combined them with MMAF from various populations and integrated them into input files for constructing LR and SVM, with linear kernel, radial kernel and polynomial kernel using R package e1071 (44). Performance for each model under each specific setting was tested on testing datasets I and II and was evaluated using R package ROCR (45). Because testing dataset III contains only TN observations, we applied manually calculated TNR for evaluating its performance.

Moreover, in order to assess the relative contribution of each prediction score to the performance of LR and SVM, we tested several modified SVM and LR models with one prediction score deleted from the original models and plotted average ROC curve and AUC value. In addition, in order to test whether our model can be further improved by using different combinations of prediction scores, we applied step-wise model selection using Akaike Information Criterion (AIC) statistic as a criterion. 

Information from https://academic.oup.com/hmg/article/24/8/2125/651446#81269181

## Clinical Application

WARNING: This predictor used population allele frequency of a variant as a feature. If you are using the ACMG/AMP framework “Population Data” and “Computational Predictions” are two independent categories. Therefore, if you use this predictor you cannot also include any “Population Data” evidence towards your final classification. If you use a variant effect predictor that did not include populaqtion allele frequency as a feature, it is fine to use both the “Computational Predictions” and “Population Data” evidence categories in your final classification. The component scores for MetaLR come from SIFT, PolyPhen-2 HDIV, PolyPhen-2 HVAR, GERP++, MutationTaster, Mutation Assessor, FATHMM, LRT, SiPhy, PhyloP, and the  maximum frequency observed in the 1000 genomes populations.

 The ClinGen Sequence Variant Interpretation Working Group reccommends that calibrated scores from select variant effect predictors are reliable as Very Strong, Strong, or Moderate evidence for Pathogenicity (PP3) or Benignity (BP4) within ACMG/AMP Guidelines (Pejaver, Vikas et al. “Calibration of computational tools for missense variant pathogenicity classification and ClinGen recommendations for PP3/BP4 criteria.” American journal of human genetics vol. 109,12 (2022): 2163-2177. doi:10.1016/j.ajhg.2022.10.013). MetaLR scores have been calbrated by the Karchin Lab according to these methods using the code and variant sites.

| ACMG Category    | Strength    | MetaLR Thresholds |
|------------------|-------------|------------------:|
| Benign (BP4)     | Very Strong |                 - |
|                  | Strong      |                 - |
|                  | Moderate    |          < 0.0576 |
|                  | Supporting  |  (0.0576, 0.1762] |
| Pathogenic (PP3) | Supporting  |  (0.8198, 0.9025] |
|                  | Moderate    |          > 0.9025 |
|                  | Strong      |                 - |
|                  | Very Strong |                 - |


 \* A "-" means that MetaLR did not meet the posterior probability threshold. Note that "(" and ")" indicate exclusion of the end value and “[” and “]” indicate inclusion of the end value.

 ### Indeterminate Scores

 If the MetaLR score does not fit within the thresholds above, Benign (BP4) and Pathogenic (PP3) columns are left blank and described as "Indeterminate" in the corresponding MetaLR widget.
