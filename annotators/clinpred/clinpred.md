# ClinPred: Prediction tool to identify disease-relevant nonsynonymous single nucleotide variants

ClinPred is an efficient tool for identifying disease-relevant nonsynonymous variants. Our predictor incorporates two machine learning algorithms that use existing pathogenicity scores and, notably, benefits from inclusion of normal population allele frequency from the gnomAD database as an input feature.In our approach we used  ClinVar – a rapidly growing database that allows selection of confidently annotated disease causing variants - as a training set. 

Compared to other methods, ClinPred showed superior accuracy for predicting pathogenicity, achieving the highest Area Under the Curve (AUC) score and increasing both the specificity and sensitivity in different test datasets. It also obtained the best performance according to various other metrics. Moreover, ClinPred performance remained robust with respect to disease type (cancer or rare disease) and mechanism (gain or loss of function). We provide pre-computed ClinPred scores for all possible human missense variants in the exome to facilitate its use by the community. 

Information from https://sites.google.com/site/clinpred/



