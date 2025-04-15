# FATHMM MKL

FATHMM MKL is database capable of predicting the effects of coding variants using nucleotide-based HMMs. Our method utilizes various genomic annotations, which have recently become available, and learns to weight the significance of each component annotation source.  We used 10 feature groups, denoted [A–J], which could be predictive of disease association and are therefore used to annotate out datasets using a customized pipeline. These feature groups can all indicate whether an SNV is functional or not, and hence we use a classifier based on multiple kernel learning (MKL). In MKL, different types of input data are encoded into kernel matrices, which quantify the similarity of data objects.

## Prediction Interpretation

Predictions are given as p-values in the range [0, 1]: values above 0.5 are predicted to be deleterious, while those below 0.5 are predicted to be neutral or benign. P-values close to the extremes (0 or 1) are the highest-confidence predictions that yield the highest accuracy.

Feature groups (letters A-J) are described in the Supplementary detail of the [main paper](https://academic.oup.com/bioinformatics/article/31/10/1536/177080), and summarised in section 2.1 of the paper.

We use distinct predictors for positions either in coding regions (positions within coding-sequence exons) and non-coding regions (positions in intergenic regions, introns or non-coding genes). The coding predictor is based on 10 groups of features, labeled A-J; the non-coding predictor uses a subset of 4 of these feature groups, A-D (see our related publication for details on the groups and their sources).

Annotations are not yet available in all feature groups for all genomic positions. To produce a p-value for these positions, we adjust our weights relative to the features that are available. For example, if our weights for A-D were 0.5, 0.1, 0.1 and 0.3, respectively, and there were no annotations for group A, then the missing weight would be distributed proportionally across remaining weights, which would become 0.2, 0.2 and 0.6. This allows us to make predictions for any combination of feature groups while yielding p-values in the [0,1] range.

Note that predictions based only on a subset of features may not be as accurate as those based on complete feature sets. In particular, predictions that are missing the conservation score features (groups A and E) will tend to be less accurate than other predictions. To aid in interpreting these predictions, we provide a list of the feature groups that contributed to each prediction.

## Feauture Groups

We used 10 feature groups, denoted [A–J], which could be predictive of disease association and are therefore used to annotate out datasets using a customized pipeline. Here is a description as follows:

**A. 46-Way Sequence Conservation:** based on multiple sequence alignment scores, at the nucleotide level, of 46 vertebrate genomes compared with the human genome.

**B.Histone Modifications (ChIP-Seq):** based on ChIP-Seq peak calls for histone modifications.

**C.Transcription Factor Binding Sites (TFBS PeakSeq):** based on PeakSeq peak calls for various transcription factors.

**D.Open Chromatin (DNase-Seq):** based on DNase-Seq peak calls.

**E.100-Way Sequence Conservation:** based on multiple sequence alignment scores, at the nucleotide level, of 100 vertebrate genomes compared with the human genome.

**F.GC Content:** based on a single measure for GC content calculated using a span of five nucleotide bases from the UCSC Genome Browser.

**G.Open Chromatin (FAIRE):** based on formaldehyde-assisted isolation of regulatory elements (FAIRE) peak calls.

**H.Transcription Factor Binding Sites (TFBS SPP):** based on SPP peak calls for various transcription factors.

**I.Genome Segmentation:** based on genome-segmentation states using a consensus merge of segmentations produced by the ChromHMM and Segway software.

**J.Footprints:** based on annotations describing DNA footprints across cell types from ENCODE.

Information from http://fathmm.biocompute.org.uk/fathmmMKL.htm#interpretation and https://academic.oup.com/bioinformatics/article/31/10/1536/177080


## Clinical Application

 The ClinGen Sequence Variant Interpretation Working Group reccommends that calibrated scores from select variant effect predictors are reliable as Very Strong, Strong, or Moderate evidence for Pathogenicity (PP3) or Benignity (BP4) within ACMG/AMP Guidelines (Pejaver, Vikas et al. “Calibration of computational tools for missense variant pathogenicity classification and ClinGen recommendations for PP3/BP4 criteria.” American journal of human genetics vol. 109,12 (2022): 2163-2177. doi:10.1016/j.ajhg.2022.10.013). FATHMM MKL scores have been calbrated by the Karchin Lab according to these methods using the code and variant sites.

| ACMG Category    | Strength    | FATHMM MKL Thresholds |
|------------------|-------------|----------------------:|
| Benign (BP4)     | Very Strong |                     - |
|                  | Strong      |                     - |
|                  | Moderate    |              <=0.2513 |
|                  | Supporting  |      (0.2513, 0.6779] |
| Pathogenic (PP3) | Supporting  |              > 0.9747 |
|                  | Moderate    |                     - |
|                  | Strong      |                     - |
|                  | Very Strong |                     - |


 \* A "-" means that FATHMM MKL did not meet the posterior probability threshold. Note that "(" and ")" indicate exclusion of the end value and “[” and “]” indicate inclusion of the end value.

 ### Indeterminate Scores

 If the FATHMM MKL score does not fit within the thresholds above, Benign (BP4) and Pathogenic (PP3) columns are left blank and described as "Indeterminate" in the corresponding FATHMM MKL widget.
