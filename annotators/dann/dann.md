## _For local installation, read the installation section. This module requires the python package `pytabix`, and is not available for Windows operating system._

# DANN: a deep learning approach for annotating the pathogenicity of genetic variants

Annotating genetic variants for the purpose of identifying pathogenic variants remains a challenge. Combined annotation-dependent depletion (CADD) is an algorithm designed to annotate coding variants, and has been shown to outperform other annotation algorithms. CADD trains a linear kernel support vector machine (SVM) to differentiate evolutionarily derived, likely benign, alleles from simulated, likely deleterious, variants. However, SVMs cannot capture non-linear relationships among the features, which can limit performance. To address this issue, we have developed DANN. DANN uses the same feature set and training data as CADD to train a deep neural network (DNN). DNNs can capture non-linear relationships among features and are better suited than SVMs for problems with a large number of samples and features.  DANN achieves about a 19% relative reduction in the error rate and about a 14% relative increase in the area under the curve (AUC) metric over CADD’s SVM methodology.

Information from https://academic.oup.com/bioinformatics/article/31/5/761/2748191

# Local Installation

Install the `DANN` module

```bash
oc module install dann
```
DANN uses the python package pytabix for querying the data. On Mac and Linux systems, this can be installed with `pip3 install --user pytabix`. If this does not work, consult the [pytabix website](https://pypi.org/project/pytabix/) for more options.

