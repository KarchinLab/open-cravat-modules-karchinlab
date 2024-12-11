# DITTO

DITTO is a transcript-aware XML (explainable machine learning) tool for scoring the pathogenicity of single nucleotide variants as well as insertion/deletions variants in the human genome.

While many variant annotation and scoring tools are around, many of them are specialized for one type of variant
consequence i.e. different tools for interpreting missense vs Splice site variants. We developed DITTO, an XML
neural network-based variant impact predictor that generates interpretable and transparent explanations for all its
predictions. By providing a single classification and explanation system for any class of small variant, including
substitutions, insertions, indels etc., and across all consequences including missense, frameshifts, splice site,
intronic, intergenic etc., this method streamlines variant interpretation.

For more information, please refer to [DITTO GitHub repo](https://github.com/uab-cgds-worthey/DITTO)

## Installation

Install the `DITTO` module

```bash
oc module install ditto
```

**Note** DITTO uses the python package pytabix for querying the data. On Mac and Linux systems, this can be installed
with `pip3 install --user pytabix`. If this does not work, consult the [pytabix website](https://pypi.org/project/pytabix/) for more options.
