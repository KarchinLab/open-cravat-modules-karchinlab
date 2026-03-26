# NCG Healthy Drivers

The Network of Cancer Genes (NCG) is a curated, open-access resource that collects genes whose somatic alterations are reported to drive either cancer evolution or clonal expansion in non-cancer tissues. In addition to driver-gene labels, NCG annotates a broad set of gene systems-level properties including duplicability, evolutionary origin, expression breadth, essentiality, protein-network topology, miRNA regulation, and germline constraint. NCG was built through expert manual curation of published sequencing screens and driver-gene resources. The database integrates literature support with systems-level annotations that help characterize how driver genes differ from the rest of the human genome.

## Summary
This annotator reports **Healthy Drivers** from the Network of Cancer Genes. In NCG, Healthy Drivers are genes whose somatic alterations have been reported to drive **non-malignant clonal expansion** in histologically normal or non-cancer tissues.

The Healthy Drivers view is designed to support both quick interpretation and deeper prioritization. The context columns describe **where** the healthy-driver evidence comes from, while the systems-level columns describe **how the gene behaves as a gene** across evolution, expression, cellular dependency, interaction networks, and germline constraint. Within this hierarchical resource, **Healthy Drivers** should be interpreted alongside the parallel **Cancer Drivers** sub-tile, which captures genes involved in malignant somatic evolution.

## What Healthy Drivers are
Healthy Drivers are genes whose somatic alterations confer a selective advantage in non-cancer tissues, allowing mutant clones to expand while the tissue remains non-malignant. NCG’s Healthy Drivers resource was created to compare these genes directly with Cancer Drivers and to identify the shared and distinct systems-level properties of the two groups.

## Column descriptions

### Gene Entrez ID
This is the **Entrez Gene identifier** for the healthy-driver gene. It provides a stable numeric identifier that supports consistent mapping across releases and external resources. Values are positive integers with no biologically meaningful fixed upper bound.

### Gene symbol
This is the standard **gene symbol** for the annotated gene. It is the most recognizable human-readable label and is typically what users will inspect first in OpenCRAVAT output. Values are text strings rather than numbers.

### Organ system
This field records the broad **anatomical system** associated with the healthy-driver observation. It helps organize non-cancer clonal expansions into broader biological contexts, such as blood, skin, esophagus, or other tissue systems. Values are categorical labels with no numeric range.

### Primary site
This field records the **specific tissue or anatomical site** in which the healthy-driver evidence was observed. It is more specific than organ system and identifies the local tissue context of the non-cancer clonal expansion. Values are categorical text labels.

### Healthy tissue
This column names the **healthy or non-cancer tissue context** from which the driver evidence was derived. It distinguishes normal-tissue clonal expansion from malignant disease context and is one of the key fields separating this sub-tile from the Cancer Drivers view. Values are categorical strings rather than numbers.

### Number of duplicated loci at 60% coverage
This column measures **gene duplicability**, using the number of loci that match at least 60% of the gene sequence under the NCG framework. Lower values indicate lower duplicability, whereas higher values indicate more duplicated sequence content in the genome. Values are non-negative integers with a minimum of **0**.

### Evolutionary conservation (taxonomic group)
This field summarizes the gene’s **evolutionary depth or origin** across major taxonomic groups. More ancient origins generally imply deeper conservation, while more recent origins correspond to more lineage-restricted genes. Values are ordered categorical labels such as primates, mammals, vertebrates, metazoans, opisthokonts, eukaryotes, or pre-metazoan categories depending on the source representation.

### Percentage of cell lines in which the gene was found to be essential
This field reports the fraction of surveyed cell lines in which the gene was classified as **essential**. In practical terms, larger percentages indicate genes whose loss is less well tolerated across many cell contexts. Values range from **0 to 100 percent**.

### Number of tissues in which the gene is expressed according to RNA-seq data (out of 43)
This column counts in how many of **43 unique healthy tissues** the gene is expressed according to the NCG integration of GTEx and Protein Atlas RNA-seq data. It reflects expression breadth across normal tissues, with higher values indicating broader expression. Values range from **0 to 43**.

### Degree of the gene in the protein-protein interaction network (PPIN)
Degree measures the number of **direct protein interaction partners** in the PPIN. Genes with higher degree tend to encode hub proteins with many direct interactions. Values are non-negative integers starting at **0**, with no fixed universal maximum.

### Betweenness in the PPIN
Betweenness measures how frequently the gene’s protein lies on **shortest paths** connecting other proteins in the PPIN. High values suggest a bottleneck or bridging role that may connect otherwise separate functional neighborhoods. Values are continuous and non-negative, with scale depending on the normalization of the network analysis.

### Clustering coefficient in the PPIN
This metric describes how densely interconnected the immediate neighbors of the protein are in the PPIN. Higher values indicate more local cohesiveness and potential participation in tightly connected modules or complexes. Values typically range from **0 to 1**.

### Number of complexes in which the protein is a component
This field counts the number of annotated **protein complexes** that include the encoded protein. Larger values suggest broader participation in multi-protein cellular machinery. Values are non-negative integers with minimum **0**.

### Number of targeting miRNAs
This column gives the number of **miRNAs targeting the gene** according to the underlying annotation source. It reflects the breadth of known or predicted post-transcriptional regulation. Values are non-negative integers beginning at **0**.

### Number of expressed tissues on mRNA level in GTEx
This field counts the number of **GTEx tissues** in which the gene is expressed at the mRNA level under the thresholds used by NCG. Higher values indicate broader expression across normal tissues in GTEx. Values are non-negative integers from **0** up to the number of GTEx tissue categories in the relevant release.

### Number of expressed tissues on mRNA level in Protein Atlas
This field counts the number of tissues in **Protein Atlas** where the gene is expressed at the mRNA level. It complements GTEx and offers a second expression-breadth view from a different source. Values are non-negative integers with minimum **0** and a release-dependent upper bound.

### Number of expressed tissues on protein level in Protein Atlas
This field reports the number of tissues where the **protein product** is detected in Protein Atlas. It can diverge from RNA-based breadth because transcript detection does not always translate directly into protein detection. Values are non-negative integers starting at **0**.

### Number of expressed cell lines in CLP
This column counts the number of **CLP cell lines** in which the gene is expressed. It reflects expression breadth across cancer cell line models rather than healthy tissues, which can still be useful for experimental planning and comparison. Values are non-negative integers from **0** to the number of profiled CLP lines in the source release.

### Number of expressed cell lines in GNE
This field counts the number of **GNE cell lines** in which the gene is expressed. It is another breadth-of-expression metric across cell line models. Values are non-negative integers starting at **0**, with a dataset-specific upper bound.

### Number of expressed cell lines in CCLE
This field counts the number of **CCLE cell lines** in which the gene is expressed. Larger values mean broader expression across the CCLE panel and may indicate broader model representation across lineages. Values are non-negative integers with minimum **0** and a maximum set by the underlying CCLE release.

### Number of germline damaging SNVs and indels/gene length
This column reports damaging germline **SNVs and indels normalized by gene length**. The normalization is useful because longer genes have more opportunity to accumulate raw variants. Values are continuous and non-negative, with **0** indicating no such variation per unit length in the source data.

### Number of germline SVs/gene length
This field reports **germline structural variants normalized by gene length**. As with the SNV/indel measure, normalization helps support fairer comparison among genes of different sizes. Values are continuous and non-negative, typically beginning at **0**.

### LOEUF score
LOEUF is the **loss-of-function observed/expected upper bound fraction** and measures intolerance to germline loss-of-function variation. Lower values indicate stronger germline constraint and therefore stronger depletion of observed loss-of-function variants relative to expectation. Values are continuous and non-negative, and interpretation is primarily comparative rather than based on a hard threshold.
