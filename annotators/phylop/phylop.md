# phyloP 100 Way Vertebrate, phyloP 470 Way Mammalian, & phyloP 17 Way Primate: conservation scoring by phylogenetic p-values
The phyloP database contains conservation scoring by phyloP (phylogenetic p-values) for multiple alignments of 99 vertebrate genomes to the human genome as well as for multiple alignments of 469 mammalian genome sequences to the human genome and a 17 way alignment primate set.

## Clinical Application

The ClinGen Sequence Variant Interpretation Working Group reccommends that calibrated scores from select variant effect predictors are reliable as Very Strong, Strong, or Moderate evidence for Pathogenicity (PP3) or Benignity (BP4) within ACMG/AMP Guidelines (Pejaver, Vikas et al. “Calibration of computational tools for missense variant pathogenicity classification and ClinGen recommendations for PP3/BP4 criteria.” American journal of human genetics vol. 109,12 (2022): 2163-2177. doi:10.1016/j.ajhg.2022.10.013).

phyloP 100-way Vertebrate scores have been calbrated and validated as reliable to support Benign Supporting, Benign Moderate, Pathogenic Supporting, and Pathogenic Moderate ACMG/AMP evidence for purposes of variant classification in the clinic.

| phyloP Thresholds |                 |                |                |                |                |                |                |                |
|--------------|-----------------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|
| Benign (BP4) |||| Pathogenic (PP3)|
|Very Strong   |Strong      |Moderate     |Supporting   |Supporting   |Moderate     |Strong      |Very Strong   |
|-|-|≤0.021|(0.021, 1.879]|[7.367, 9.741)|≥9.741|-|   -   |

\* A "-" means that phyloP did not meet the posterior probability threshold. Note that "(" and ")" indicate exclusion of the end value and “[” and “]” indicate inclusion of the end value.

### Indeterminate Scores

If the phyloP score does not fit within the thresholds above, Benign (BP4) and Pathogenic (PP3) columns are left blank and described as "Indeterminate" in the corresponding phyloP widget.