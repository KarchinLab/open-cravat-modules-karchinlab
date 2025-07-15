# MutationTaster 

## Bayes Classifier 
MutationTaster employs a Bayes classifier to eventually predict the disease potential of an alteration. The Bayes classifier is fed with the outcome of all tests and the features of the alterations and calculates probabilities for the alteration to be either a disease mutation or a harmless polymorphism. For this prediction, the frequencies of all single features for known disease mutations/polymorphisms were studied in a large training set composed of >390,000 known disease mutations from HGMD Professional and >6,800,000 harmless SNPs and Indel polymorphisms from the 1000 Genomes Project (TGP).

## Models
We provide three different models aimed at different types of alterations, either aimed at 'silent' (non-synonymous or intronic) alterations (without_aae model), at those leading to the substitution/insertion/deletion of a single amino acid (simple_aae model) or at more complex changes of the amino acid sequence (e.g. mutations introducing a premature stop codon, etc - complex_aae model). All models were trained with all available and suitable common polymorphisms and disease mutations. MutationTaster automatically determines the correct model for each alteration.

## Prediction
MutationTaster predicts an alteration as one of four possible types:

* disease causing - i.e. probably deleterious
* disease causing automatic - i.e. known to be deleterious
* polymorphism - i.e. probably harmless
* polymorphism automatic - i.e. known to be harmless

## Automatic Predictions

Any known polymorphism(s) or known disease variant that have been found at the position in question. Our database contains all single nucleotide polymorphisms (SNPs) from the NCBI SNP database (dbSNP). Moreover, we have stored all HapMap genotype frequencies as well as variants from the 1000 Genomes Project [4] (abbreviated here as TGP). If an alteration is located at the same position as a known dbSNP, MutationTaster provides the SNP ID (or rs ID) and a link together with the HapMap genotype frequencies, if available. If every of the three possible geno-types is observed in at least one HapMap population, the alteration is automatically regarded as a polymorphism and predicted as polymorphism automatic (the naive Bayes classifier is run nevertheless and the p value for the prediction is shown). Please note that there may be differences between your alteration and the alleles in dbSNP. For the 1000 Genomes Project, MutationTaster provides information in either of the following formats:
* more than 4 cases homozygous in TGP: TGP: allele_alt/allele_alt found more than 4 times in TGP data: #homozygous_hits
* more than 4 cases heterozygous in TGP: TGP: allele_ref/allele_alt found more than 4 times in TGP data: #heterozygous_hits (#homozygous_hits for allele_alt/allele_alt)
* less than 4 cases homo-/heterozygous in TGP: TGP: allele_ref/allele_alt found #heterozygous_hits times in TGP data, allele_alt/allele_alt #homozygous_hits times.

If an alteration was found more than 4 times homozygously in TGP, it is automatically regarded as polymorphism.
We also display known disease variants from dbSNP ClinVar. If a variant is marked as probable-pathogenic or pathogenic in ClinVar, it is automatically predicted to be disease-causing, i.e. disease causing automatic (the naive Bayes classifier is run nevertheless and the p value for the prediction is shown).

Information from http://www.mutationtaster.org/info/documentation.html

## Clinical Application

The ClinGen Sequence Variant Interpretation Working Group reccommends that calibrated scores from select variant effect predictors are reliable as Very Strong, Strong, or Moderate evidence for Pathogenicity (PP3) or Benignity (BP4) within ACMG/AMP Guidelines (Pejaver, Vikas et al. “Calibration of computational tools for missense variant pathogenicity classification and ClinGen recommendations for PP3/BP4 criteria.” American journal of human genetics vol. 109,12 (2022): 2163-2177. doi:10.1016/j.ajhg.2022.10.013).

MutationTaster scores have been calbrated and validated as reliable to support the Benign Supporting classification ACMG/AMP evidence for purposes of variant classification in the clinic.

| ACMG Category    | Strength    | MutationTaster Thresholds |
|------------------|-------------|--------------------------:|
| Benign (BP4)     | Very Strong |                         - |
|                  | Strong      |                         - |
|                  | Moderate    |                         - |
|                  | Supporting  |               < 0.995135) |
| Pathogenic (PP3) | Supporting  |                         - |
|                  | Moderate    |                         - |
|                  | Strong      |                         - |
|                  | Very Strong |                         - |

\* A "-" means that MutationTaster did not meet the posterior probability threshold. Note that "(" and ")" indicate exclusion of the end value and “[” and “]” indicate inclusion of the end value.
