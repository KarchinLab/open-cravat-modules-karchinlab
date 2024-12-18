## _For local installation, read the installation section. This module requires the python package `pytabix`, and is not available for Windows operating system._

# CScape

CScape Coding predicts the oncogenic status (disease-driver or neutral) of somatic point mutations specifically in the coding region of the cancer genome.

# Prediction Interpretation

Predictions are given as p-values in the range [0, 1]: values above 0.5 are predicted to be deleterious, while those below 0.5 are predicted to be neutral or benign. P-values close to the extremes (0 or 1) are the highest-confidence predictions that yield the highest accuracy.

We also apply cautious classification thresholds, defined as those thresholds that yield the highest possible accuracy (see our paper for details). These are reported using different thresholds for coding (0.89 or above) and noncoding (0.70 or above) SNVs.

We use distinct predictors for positions either in coding regions (positions within coding-sequence exons) and non-coding regions (positions in intergenic regions, introns or non-coding genes).

Information from http://cscape.biocompute.org.uk/

# Local Installation

Install the `CScape` module

```bash
oc module install CScape
```
CScape uses the python package pytabix for querying the data. On Mac and Linux systems, this can be installed with `pip3 install --user pytabix`. If this does not work, consult the [pytabix website](https://pypi.org/project/pytabix/) for more options.

