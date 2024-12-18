## _For local installation, read the installation section. This module requires the python package `pytabix`, and is not available for Windows operating system._

# FunSeq2

## Overview

This tool is specialized to prioritize somatic variants from cancer whole genome sequencing. It contains two components : 1) building data context from various resources; 2) variants prioritization.

The framework combines an adjustable data context integrating large-scale genomics and cancer resources with a streamlined variant-prioritization pipeline. The pipeline has a weighted scoring system combining: inter- and intra-species conservation; loss- and gain-of-function events for transcription-factor binding; enhancer-gene linkages and network centrality; and per-element recurrence across samples. We further highlight putative drivers with information specific to a particular sample, such as differential expression.

FunSeq2 also uses the python package scipy for statistical tests. On most systems, this can be installed with `pip3 install scipy`. If this does not work, consult the [scipy website](https://www.scipy.org/install.html) for more options.

## HOT Region (Transcription factor highly occupied region)
If a variant occurs in HOT regions, the corresponding cell lines (5 in total) are shown.

## Motif-Breaking Analysis 

 Motif-breaking events are defined as variants decreasing the PWM scores, whereas motif-conserving events are those that do not change or increase the PWM (Position Weight Matrix) scores [29] (we calculated the difference between mutated and germline alleles in the PWMs). Variants causing motif-breaking events are reported in the output together with the corresponding PWM changes. Transcription factor PWMs are obtained from ENCODE project [15], including TRANSFAC and JASPAR motifs.

 ## Motif-Gaining Analysis

 Whole-genome motif scanning generally discovers millions of motifs, of which a large fraction are false positives. We focused on variants occurring in promoters (defined as -2.5 kb from transcription starting sites) or regulatory elements significantly associated with genes. For each variant, +/- 29 bp are concatenated from the human reference genome (motif length is generally <30 bp). For each PWM, we scanned the 59 bp sequence. For each candidate motif encompassing the variant, we evaluated the sequence scores using TFM-Pvalue [30] (with respect to the PWM). Given a particular PWM (frequencies are transformed to log likelihoods), sequence score is computed by summing up the relevant values at each position in the PWM. If the P value with mutated allele < = 4e-8 and the P value with germline allele >4e-8, we define the variant creating a novel motif. The process is repeated for all PWMs and all variants. The sequence score changes are reported in the output.

 ## Alternate and Reference Scores

 The alternate and reference scores depend on the type of motif-analysis:

 **Motif-Breaking:** Alternate allele frequency in PWM, Reference allele frequency in PWM.

 **Motif-Gaining:** Sequence Score with alternate allele, Sequence Score with reference allele.

## Coding Scoring Scheme

Variants in coding regions (GENCODE 16 for the current version; users can replace this with other GENECODE versions) are analyzed with VAT (variant annotation tool) [57]. Variants are ranked based on the following scheme (each criterion gets score 1): (1) non-synonymous; (2) premature stop; (3) is the gene under strong selection; (4) is the gene a network hub; (5) recurrent; (6) GERP score >2.

## Non-coding Scoring Scheme (Weighted Scoring Scheme)

 In general, features can be classified into two classes: discrete and continuous. Discrete features are binary, such as in ultra-conserved elements or not. Continuous features: (1) GERP score; (2) motif-breaking score is the difference between germline and mutated alleles in PWMs; (3) motif-gaining score is the sequence score difference between mutated and germline alleles; (4) network centrality score (the cumulative probability, see `Network analysis of variants associated with genes’. If one variant has multiple values of a particular feature (for example, breaking multiple motifs), the largest value is used.

 We weighted each feature based on the mutation patterns observed in the 1000 Genomes polymorphisms. We randomly selected 10% of the 1000 Genomes Phase 1 SNPs (approximately 3.7 M) and ran them through our pipeline. For each discrete feature d, we calculated the probability p d that overlaps a natural polymorphism. Then we computed 1-Shannon entropy (1) as its weighted value. The value ranges from 0 to 1 and is monotonically decreasing when the probability is between 0 and 0.5c below 0.5).

 Finally, for each cancer variant, we scored it by summing the weighted values of all its features (3). If a particular feature is not observed, it is not used in the scoring. Considering the situation that some features are subsets of other features, to avoid overweighting similar features, we took into account feature dependencies when calculating the summed scores. As shown in Additional file 1: Table S3, when having leaf features, the weighted values of root features are ignored. For example, when a variant occurs in sensitive regions, the score of `in functional annotations’ is not used in the sum-up. Leaf features are assumed independent. Variants ranked on top of the output are those with higher scores and are most likely to be deleterious.

 Information from http://info.gersteinlab.org/Funseq2 and https://genomebiology.biomedcentral.com/articles/10.1186/s13059-014-0480-5#citeas

## Local Installation

Install the `FunSeq2` module

```bash
oc module install FunSeq2
```
FunSeq2 uses the python package pytabix for querying the data. On Mac and Linux systems, this can be installed with `pip3 install --user pytabix`. If this does not work, consult the [pytabix website](https://pypi.org/project/pytabix/) for more options.
