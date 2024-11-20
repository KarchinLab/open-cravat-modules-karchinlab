# DITTO

DITTO is a transcript-aware XML (explainable machine learning) tool for scoring the deleteriousness of single nucleotide variants as well as insertion/deletions variants in the human genome.

While many variant annotation and scoring tools are around, many of them are specialized for one type of variant
consequence (e.g. Alphamissense for missense and SpliceAI for Splice site variants). We developed DITTO, an XML
neural network-based variant impact predictor that generates interpretable and transparent explanations for all
predictions. DITTO provides scores that accurately predict variant impact across all consequences taking into account
known transcripts. By providing a single classification and explanation system for any class of small variant, including
substitutions, insertions, indels etc., and across all consequences including missense, frameshifts, splice site,
intronic, intergenic etc., this method streamlines variant interpretation.  Most importantly, our DITTO variant
classification method outperforms existing methods (even single use methods) across variant classes and consequences.

## Installation

Install the `DITTO` module

```bash
oc module install ditto
```

**Note** DITTO uses the python package pytabix for querying the data. On Mac and Linux systems, this can be installed
with `pip3 install --user pytabix`. If this does not work, consult the [pytabix website](https://pypi.org/project/pytabix/) for more options.

## Short method summary

Genomic sequencing has significantly enhanced our ability to identify disease-causing variants, generate new molecular
insights, accelerating diagnosis; however, significant challenges persist. Many patients receive variants of uncertain
significance (VUS) or conflicting classifications, limiting actionable outcomes. While numerous ML methods exist, they
often address limited variant types, lack transcript awareness, and operate as opaque black boxes. Our study
demonstrates that our classifier DITTO can accurately classify any class and consequence of small variant with an overall accuracy of 99.6%.
DITTO demonstrated superior performance compared to the other tools evaluated, generating accurate predictions spanning
all chromosomes and variant consequences. To our knowledge, this is the first study to compare tools across consequences
and chromosomes.

For more information, please refer to [DITTO GitHub repo](https://github.com/uab-cgds-worthey/DITTO)
