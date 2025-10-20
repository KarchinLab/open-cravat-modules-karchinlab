# About MutPred2

## What is MutPred2
[**MutPred2**](http://mutpred.mutdb.org/) is a computational tool (available as both a web server and standalone software) designed to predict the pathogenicity of **missense (single amino acid substitution)** variants in human proteins, and to propose the likely **molecular mechanisms** by which such variants may have deleterious effects.
In other words, beyond simply classifying a variant as “pathogenic” or “benign,” MutPred2 attempts to provide hypotheses about *how* a given amino acid change might disrupt protein function (for example, via altered stability, loss/gain of binding sites, disruption of post-translational modifications, etc.).
MutPred2 is part of the broader “MutPred” suite of tools. Other related tools include versions tailored for non-frameshifting insertions/deletions (**MutPred-Indel**), splice disruptions (**MutPred-Splice**), and loss-of-function (**MutPred-LOF**) variants.

## Underlying Methodology
### Training Data and Model Design

- MutPred2 is trained using a large set of known or presumed variant data: **~53,180 pathogenic variants** and **~206,946 unlabeled (putatively benign or unknown)** variants.
- The model uses a **bagged ensemble of 30 feed-forward neural networks**, each trained on balanced subsets of pathogenic vs. unlabeled variants.
- It is a *sequence-based* predictor, meaning it does not rely on 3D structural data, but instead uses inferred structural and functional properties derived from sequence.
- MutPred2 maintains an ontology of **50+ protein properties** (e.g. secondary structure, catalytic or binding residues, post-translational modifications, metal binding, disorder, allostery) to track potential gain or loss of function.
### Feature Extraction and Scoring

When evaluating a variant, MutPred2 performs the following steps:
1. **Feature Extraction** – For both wild-type and mutant sequences, MutPred2 computes a large number of sequence-derived features (e.g. conservation, amino acid physicochemical changes, predicted structural context, and functional annotations).
2. **Loss/Gain Modeling** – For each protein property in its ontology, MutPred2 estimates whether the substitution is likely to cause a *loss* or *gain* of that property.
3. **Neural Network Ensemble Scoring** – All features (including gain/loss estimates) are input to the ensemble of neural networks, which yield a general **pathogenicity score** (0–1; higher indicates more likely pathogenic).
4. **Mechanism Ranking** – MutPred2 also reports a ranked list of molecular mechanisms (from its ontology) that are most likely impacted, with associated probabilities or *p*-values.
For each variant, users receive:
- A **pathogenicity score** (0–1)
- A **list of candidate molecular consequences** (e.g. “loss of metal binding,” “gain of disorder,” “loss of phosphorylation site”)
- Associated **confidence metrics** or *p*-values for each predicted mechanism

## Strengths and Applications
- **Interpretability & Mechanistic Insight** – MutPred2 does not just classify variants as pathogenic vs. benign; it offers mechanistic hypotheses that can guide experimental validation.
- **Competitive Performance** – Benchmarks show that MutPred2 often improves the prioritization of deleterious variants while maintaining good specificity.
- **Broad Functional Coverage** – Because it considers many structural and functional properties (not just conservation or stability), it can capture diverse molecular effects.
- **Scalability & Usability** – The web server supports small batch submissions (~100 substitutions), while the standalone version can handle genome-scale datasets (with higher computational cost).

## Limitations and Caveats
- **Probabilistic, Not Definitive** – Predictions are hypothesis-generating; they should not be treated as conclusive evidence of pathogenicity.
- **Training Biases** – The pathogenic/unlabeled training data may contain biases, affecting generalizability.
- **Lack of Structural Resolution** – Since it primarily uses sequence-based features, subtle 3D structural effects may be missed.
- **Scope** – MutPred2 is designed for **missense variants** only; other variant types (nonsense, frameshift, splice) require other modules like MutPred-Indel, MutPred-LOF, or MutPred-Splice.

# Disclaimer

The purpose of this resource is to distribute functional prediction of mutation data. The data is meant to be used for basic research. Do not use this data to make clinical decisions. 

