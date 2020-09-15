# MetaSVM

MetaSVM is a ensemble-based prediction algorithm devloped by integrating 10 component scores (SIFT, PolyPhen-2 HDIV, PolyPhen-2 HVAR, GERP++, MutationTaster, Mutation Assessor, FATHMM, LRT, SiPhy, PhyloP) and the maximum frequency observed in the 1000 genomes populations, using a support vector machine model.

## Scores

**MetaSVM_score:** Our support vector machine (SVM) based ensemble prediction score. Larger value means the SNV is more likely to be damaging. 
		Scores range from -2 to 3 in dbNSFP.

**MetaSVM_rankscore:** MetaSVM scores were ranked among all MetaSVM scores in dbNSFP.The rankscore is the ratio of the rank of the score over the total number of MetaSVM 
		scores in dbNSFP. The scores range from 0 to 1.

**MetaSVM_pred:** Prediction of our SVM based ensemble prediction score,"T(olerated)" or
		"D(amaging)". The score cutoff between "D" and "T" is 0.5. The rankscore cutoff between
		"D" and "T" is 0.82257.

## Logistic Regression and Support Vector Machine Models

MetaSVM has a sister database, metaLR, that explores the same concepts using a logistic regression model.

Quality of machine learning models, such as Support Vector Machine (SVM) and Logistic Regression (LR), can be influenced by selection of component scores as well as the selection of parameters. To optimize the selection of component scores and parameters for our SVM and LR model, we collected training dataset, on which we performed feature selection and parameter tuning for our models. 

Output scores were harvested from all of the prediction methods for all mutations in all of our datasets, combined them with MMAF from various populations and integrated them into input files for constructing LR and SVM, with linear kernel, radial kernel and polynomial kernel using R package e1071 (44). Performance for each model under each specific setting was tested on testing datasets I and II and was evaluated using R package ROCR (45). Because testing dataset III contains only TN observations, we applied manually calculated TNR for evaluating its performance.

Moreover, in order to assess the relative contribution of each prediction score to the performance of LR and SVM, we tested several modified SVM and LR models with one prediction score deleted from the original models and plotted average ROC curve and AUC value. In addition, in order to test whether our model can be further improved by using different combinations of prediction scores, we applied step-wise model selection using Akaike Information Criterion (AIC) statistic as a criterion. 

Information from https://academic.oup.com/hmg/article/24/8/2125/651446#81269181