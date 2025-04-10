# About MutPred

MutPred is a web application tool developed to classify an amino acid substitution (AAS) as disease-associated or neutral in human. In addition, it predicts molecular cause of disease/deleterious AAS. MutPred is based upon SIFT [1] and a gain/loss of 14 different structural and functional properties. For instance, gain of helical propensity or loss of a phosphorylation site. It was trained using the deleterious mutations from the Human Gene Mutation Database [2] and neutral polymorphisms from Swiss-Prot [3]. Current version of MutPred is 1.2. The update consists of replacing SIFT score by a more stable version of code that calculates evolutionary conservation. In addition, the I-mutant software was replaced by a more stable MUpro [4], by the Baldi group. The training data set was updated to contain 39,218 disease-associated mutations from HGMD and 26,439 putatively neutral substitutions from Swiss-Prot. 

## How do I interpret the results? 
The output of MutPred contains a general score (g), i.e., the probability that the amino acid substitution is deleterious/disease-associated, and top 5 property scores (p), where p is the P-value that certain structural and functional properties are impacted. 

Certain combinations of high values of general scores and low values of property scores are referred to as hypotheses.

- Scores with g > 0.5 and p < 0.05 are referred to as **actionable hypotheses**.
- Scores with g > 0.75 and p < 0.05 are referred to as **confident hypotheses**.
- Scores with g > 0.75 and p < 0.01 are referred to as **very confident hypotheses**.

## How are the MutPred scores in Open-CRAVAT generated?
MutPred was first run on dbNSFP, a database of functional prediction scores for all theoretically possible single nucleotide variants (SNVs), i.e. every base in a given exonic region is substituted to the remaining three possible nucleotides, scored and stored [5]. MutPred requires protein sequences and amino acid substitution information as inputs. To this end, we mapped chromosomal information to the protein information available in dbNSFP v2.7, downloaded the corresponding sequences from UniProt and Ensembl and ran MutPred on these sequences and substitutions. In the case of multiple isoforms, only one isoform (and thus, one protein or transcript ID) was selected. When UniProt IDs were available, the canonical UniProt isoform was chosen. If this did not exist, the canonical Ensembl transcript was chosen. If even this did not exist, the longest secondary UniProt isoform was chosen and if this was also unavailable, the longest secondary Ensembl transcript was chosen.

The general and property scores are included in the Open-CRAVAT annotation along with the selected isoform and amino acid substitution information. However, there may be inconsistencies in the annotations between MutPred and other tools in Open-CRAVAT due to the following reasons:

- Incorrect co-ordinates in dbNSFP (leading to incorrect protein ID or non-coding region in genome)
- Inability to map protein/transcript IDs to the correct sequence
- Inconsistent isoform selection based on the above procedure
- Changes between genome versions (hg19 was used to generate MutPred scores but Open-CRAVAT relies on hg38)

Please keep these and other possible issues in mind when evaluating or using the MutPred annotator.

MutPred is a collaborative effort between the Mooney group from the University of Washington and the Radivojac group from the School of Informatics and Computing, Indiana University. The precomputed scores were generated for a collaboration on the development of REVEL [6] and are also hosted at [http://mutpred1.mutdb.org/dbnsfp/](http://mutpred1.mutdb.org/dbnsfp/).

We welcome any suggestions and comments.


## Clinical Application

 The ClinGen Sequence Variant Interpretation Working Group reccommends that calibrated scores from select variant effect predictors are reliable as Very Strong, Strong, or Moderate evidence for Pathogenicity (PP3) or Benignity (BP4) within ACMG/AMP Guidelines (Pejaver, Vikas et al. “Calibration of computational tools for missense variant pathogenicity classification and ClinGen recommendations for PP3/BP4 criteria.” American journal of human genetics vol. 109,12 (2022): 2163-2177. doi:10.1016/j.ajhg.2022.10.013). MutPred scores have been calbrated by the Karchin Lab according to these methods using the code and variant sites.

 | MutPred Thresholds |        |          |            |                  |          |        |             |
 |--------------------|--------|----------|------------|------------------|----------|--------|-------------|
 | Benign (BP4)       |        |          |            | Pathogenic (PP3) |          |        |             |
 | Very Strong        | Strong | Moderate | Supporting | Supporting       | Moderate | Strong | Very Strong |
 | -                  | -      | < 0.222  | 0.395      | (0.707, 0.82]    | > 0.82   |        | -           |


 \* A "-" means that MutPred did not meet the posterior probability threshold. Note that "(" and ")" indicate exclusion of the end value and “[” and “]” indicate inclusion of the end value.

 ### Indeterminate Scores

 If the MutPred score does not fit within the thresholds above, Benign (BP4) and Pathogenic (PP3) columns are left blank and described as "Indeterminate" in the corresponding MutPred widget.


# Supported By

The work is funded by:
- NIH K22LM009135 (PI: Mooney)
- NIH 1R01LM009722 (PI: Mooney)
- NIH 5R01LM009722 (PI: Mooney)
- Indiana Genomics Initiative. The Indiana Genomics Initiative (INGEN) is supported in part by Lily Endowment.
- National Science Foundation, DBI-0644017 (PI: Predrag Radivojac)

# References

1. Ng, P.C. and Henikoff, S. (2003) SIFT: Predicting amino acid changes that affect protein function, Nucleic Acids Res, **31**, 3812-3814.

2. Stenson, P.D., et al. (2009) The Human Gene Mutation Database: 2008 update, Genome Med, **1**, 13.

3. Boeckmann, B., et al. (2003) The SWISS-PROT protein knowledgebase and its supplement TrEMBL in 2003, Nucleic Acids Res, **31**, 365-370.

4. Cheng, J., Randall, A. and Baldi, P. (2006) Prediction of protein stability changes for single-site mutations using support vector machines. Proteins, **62**, 1125-1132.

5. Liu, X., Jian, X., Boerwinkle, E. (2011) dbNSFP: a lightweight database of human nonsynonymous SNPs and their functional predictions. Human Mutat, **32**, 894-899.

6. Ioannidis, N.M., et al. (2016) REVEL: an ensemble method for predicting the pathogenicity of rare missense variants. Am J Hum Genet, **99**, 877-885.

# Contact Us

Prof. Predrag Radivojac
Department of Computer Science and Informatics
Indiana University
150 S. Woodlawn Avenue
Bloomington, IN 47405
Tel: (812) 856-1851
Web: www.cs.indiana.edu/~predrag 

Prof. Sean Mooney 
Department of Biomedical Informatics and Medical Education
Universiy of Washington
850 Republican Street
Seattle, WA 98109 
Tel: (206) 685-0249
Web: http://faculty.washington.edu/sdmooney 

# Disclaimer

The purpose of this resource is to distribute functional prediction of mutation data. The data is meant to be used for basic research. Do not use this data to make clinical decisions. 

