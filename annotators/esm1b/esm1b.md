# ESM1b
ESM1b is a 650-million-parameter protein language model used to predict all ~450 million possible missense variant effects in the human genome. The model was trained on 250 million protein sequences across all organisms via the masked language modeling task, where random residues are masked from input sequences and the model has to predict the correct amino acid at each position (including the missing residues).

## Scores
Each variant’s effect score is the log-likelihood ratio (LLR) between the variant and wild-type (WT) residue. The scores range from -24.538 to 6.937. The smaller the score, the more likely the variant is pathogenic.

## Results
To assess the performance of ESM1b in predicting the clinical impact of variants, the model’s effect scores between pathogenic and benign variants annotated in ClinVar and variants annotated by HGMD as disease-causing and benign variants from gnomAD (defined by allele frequency >1%) were compared. Only high-confidence variants were included. The distribution of ESM1b effect scores shows a substantial difference between pathogenic and benign variants in both datasets. Using an LLR threshold of −7.5 to distinguish between pathogenic and benign variants yields a true-positive rate of 81% and a true-negative rate of 82% in both datasets.

Information from https://doi.org/10.1038/s41588-023-01465-0