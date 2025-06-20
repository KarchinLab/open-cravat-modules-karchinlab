# Calibrated Classification

## Package for clinical interpretation of variant effect predictor scores

This package helps users apply ACMG/AMP variant interpretation guidelines—specifically PP3 (support for pathogenicity) and BP4 (support for benignity)—using calibrated computational scores. It enables standardized, evidence-based integration of predictive tools within OpenCRAVAT to support clinical curation and rare disease analysis.

It is especially valuable for:

* Clinical variant curators using ACMG/AMP guidelines
* Genomic researchers prioritizing candidate variants
* Pipelines requiring harmonized pathogenicity classification from multiple in silico tools

The ClinGen Sequence Variant Interpretation Working Group reccommends that calibrated scores from select 
variant effect predictors are reliable as Strong, NA, Moderate, or Supporting evidence for Pathogenicity (PP3) 
or Benignity (BP4) within ACMG/AMP Guidelines (Pejaver, Vikas et al. “Calibration of computational tools 
for missense variant pathogenicity classification and ClinGen recommendations for PP3/BP4 criteria.” 
nAmerican journal of human genetics vol. 109,12 (2022): 2163-2177. doi:10.1016/j.ajhg.2022.10.013).

OpenCRAVAT provides calibrated score classifications for pathogenic or benign categories as additional columns 
in the variant interface. Additionally, widgets show the score categorization for each calibrated variant annotator.

The Calibrated Classification Package provides pathogenicity and benignity classifictions the top seven predictors, as ranked by accuracy yield. The accuracy of the predictors was assessed on a set of ClinVar variants as described in a forthcoming manuscript.

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
