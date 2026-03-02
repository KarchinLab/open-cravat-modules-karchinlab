# Calibrated Classification

## Package for clinical interpretation of variant effect predictor scores

This package helps users apply ACMG/AMP variant interpretation guidelines—specifically PP3 (support for pathogenicity) and BP4 (support for benignity)—using calibrated computational scores. It enables standardized, evidence-based integration of predictive tools within OpenCRAVAT to support clinical curation.

It is especially valuable for:

* Clinical variant curators using ACMG/AMP guidelines
* Genomic researchers prioritizing candidate variants
* Pipelines requiring harmonized pathogenicity classification from multiple in silico tools

The ClinGen Sequence Variant Interpretation Working Group published a procedure to map variant effect predictor scores to strength of evidence categories for Pathogenicity (PP3) 
or Benignity (BP4) within ACMG/AMP Guidelines (Pejaver, Vikas et al. “Calibration of computational tools 
for missense variant pathogenicity classification and ClinGen recommendations for PP3/BP4 criteria.” 
American journal of human genetics vol. 109,12 (2022): 2163-2177. doi:10.1016/j.ajhg.2022.10.013).

The Calibrated Classification Package provides pathogenicity and benignity strength of evidence classifictions for seven variant effect predictors. These predictors were selected based on a test set ClinVar variants not used in the training of these predictors. The following table shows the performance of these predictors according to Yield (percentage of variants with a score yielding a strength of evidence classification), Accuracy (percentage of predictions that match the ClinVar label), F1 Score (a balanced accuracy metric), F1 * Yield (the mathematical product of F1 Score and Yield).

| Predictor     | Yield | Accuracy | F1 Score | F1 * Yield |
|---------------|-------|----------|----------|------------|
| MetaRNN       | 92.8% | 98.0%    | 97.7%    | 90.7%      |
| BayesDel      | 85.5% | 96.4%    | 95.9%    | 82.0%      |
| REVEL         | 83.2% | 97.6%    | 97.3%    | 80.9%      |
| VEST          | 80.7% | 95.5%    | 95.1%    | 76.8%      |
| AlphaMissense | 76.0% | 96.3%    | 95.4%    | 72.5%      |
| CADD exome    | 79.1% | 91.1%    | 89.6%    | 70.9%      |
| ESM1b         | 74.6% | 93.8%    | 92.2%    | 68.7%      |

# External Links
* ClinGen SVI Working Group: https://clinicalgenome.org/working-groups/sequence-variant-interpretation/
* Pejaver et al. 2022 paper: https://doi.org/10.1016/j.ajhg.2022.10.013
* OpenCRAVAT project: https://opencravat.org
* MetaRNN GitHub: https://github.com/WGLab/MetaRNN
* BayesDel resource: https://github.com/Chanda-lab/BayesDel
* REVEL documentation: https://sites.google.com/site/revelgenomics/
* AlphaMissense: https://www.deepmind.com/research/publications/alphamissense-predicting-the-pathogenicity-of-human-missense-variants
* ESM1b: (https://github.com/ntranoslab/esm-variants)
