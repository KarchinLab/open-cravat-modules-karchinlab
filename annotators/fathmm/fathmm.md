# FATHMM: functional analysis through hidden markov models
FATHMM is capable of predicting the functional effects of protein missense mutations by combining sequence conservation within hidden Markov models (HMMs), representing the alignment of homologous sequences and conserved protein domains, with "pathogenicity weights", representing the overall tolerance of the protein/domain to mutations. 

NOTE: Data provided by [dbNSFP](https://sites.google.com/site/jpopgen/dbNSFP) version 3.5a

1. Transcript ID: Ensembl transcript ID, multiple entries separated by ";"
2. Protein ID: Ensembl protein ID, multiple entries separated by ";" corresponding to Transcript IDs
3. Score: FATHMM default score (weighted for human inherited-disease mutations with Disease Ontology) (FATHMMori). Scores range from -16.13 to 10.64. The smaller the score the more likely the SNP has damaging effect. Multiple scores separated by ";", corresponding to Protein ID.
4. Converted Rank Score: FATHMMori scores were first converted to FATHMMnew=1-(FATHMMori+16.13)/26.77, then ranked among all FATHMMnew scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of FATHMMnew scores in dbNSFP. If there are multiple scores, only the most damaging (largest) rankscore is presented. The scores range from 0 to 1.
5. Prediction: If a FATHMMori score is <=-1.5 (or rankscore >=0.81332) the corresponding nsSNV is predicted as "D(AMAGING)"; otherwise it is predicted as "T(OLERATED)". Multiple predictions separated by ";", corresponding to Protein ID.

## Clinical Application

The ClinGen Sequence Variant Interpretation Working Group reccommends that calibrated scores from select variant effect predictors are reliable as Very Strong, Strong, or Moderate evidence for Pathogenicity (PP3) or Benignity (BP4) within ACMG/AMP Guidelines (Pejaver, Vikas et al. “Calibration of computational tools for missense variant pathogenicity classification and ClinGen recommendations for PP3/BP4 criteria.” American journal of human genetics vol. 109,12 (2022): 2163-2177. doi:10.1016/j.ajhg.2022.10.013).

FATHMM scores have been calbrated and validated as reliable to support Benign Supporting, Benign Moderate, Pathogenic Supporting, and Pathogenic Moderate ACMG/AMP evidence for purposes of variant classification in the clinic.

| ACMG Category    | Strength    | FATHMM Thresholds |
|------------------|-------------|------------------:|
| Benign (BP4)     | Very Strong |                 - |
|                  | Strong      |                 - |
|                  | Moderate    |             >4.69 |
|                  | Supporting  |      [3.32, 4.69) |
| Pathogenic (PP3) | Supporting  |    [−5.04, −4.14) |
|                  | Moderate    |           ≤ −5.04 |
|                  | Strong      |                 - |
|                  | Very Strong |                 - |

\* A "-" means that FATHMM did not meet the posterior probability threshold. Note that "(" and ")" indicate exclusion of the end value and “[” and “]” indicate inclusion of the end value.

### Indeterminate Scores

If the FATHMM score does not fit within the thresholds above, Benign (BP4) and Pathogenic (PP3) columns are left blank and described as "Indeterminate" in the corresponding FATHMM widget.
