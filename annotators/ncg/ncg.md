# NCG Cancer Drivers

The Network of Cancer Genes (NCG) is a curated, open-access resource that collects genes whose somatic alterations are reported to drive either cancer evolution or clonal expansion in non-cancer tissues. In addition to driver-gene labels, NCG annotates a broad set of gene systems-level properties including duplicability, evolutionary origin, expression breadth, essentiality, protein-network topology, miRNA regulation, and germline constraint. NCG was built through expert manual curation of published sequencing screens and driver-gene resources. The database integrates literature support with systems-level annotations that help characterize how driver genes differ from the rest of the human genome.

## Summary
This annotator reports genes with known or predicted **driver roles in cancer** together with cancer-context labels and systems-level properties from the Network of Cancer Genes. In NCG, cancer drivers are genes whose somatic alterations have been reported to contribute to tumor development or clonal selection in cancer, based on curated resources and sequencing screens.

The cancer-driver view is designed to support both quick interpretation and deeper prioritization. The context columns describe where the driver evidence comes from, while the systems-level columns describe how the gene behaves as a gene across evolution, expression, cellular dependency, interaction networks, and germline constraint. Within this hierarchical resource, **Cancer Drivers** should be interpreted alongside the parallel **Healthy Drivers** sub-tile, which captures genes involved in non-malignant somatic clonal expansion.

## What Cancer Drivers are
Cancer drivers are genes whose somatic alterations confer a selective advantage to cancer cells. NCG compiles both well-established canonical drivers and candidate drivers reported in sequencing studies, then augments them with systems-level annotations that help explain why driver genes often occupy especially central and constrained roles in the cell.

## Column descriptions

### Gene Entrez ID
This is the **Entrez Gene identifier** for the annotated gene. It is a stable numeric gene identifier that helps link the record to external databases and avoids ambiguity caused by changing gene symbols or aliases. Each value corresponds to one recognized human gene identifier.

### Gene symbol
This is the standard **gene symbol** associated with the annotated record. 

### Organ system
This field gives the broad **anatomical system** associated with the driver evidence in NCG. It helps group driver observations into high-level biological contexts such as blood, digestive, nervous, or reproductive systems. 

### Primary site
This field records the **primary anatomical site** linked to the cancer-driver evidence. It is more specific than organ system and corresponds to the tissue or organ where the cancer originates, such as colon, skin, lung, or liver.

### Cancer type
This field specifies the **cancer type** associated with the driver call. It provides the disease-level context for the observation and is often more granular than primary site, distinguishing biologically or clinically distinct tumor entities within the same anatomical location. 

### CGL driver annotation
This column records the driver-role label from **Cancer Gene Landscape**. Expected values are `TSG`, `Oncogene`, or blank. `TSG` indicates a tumor suppressor gene annotation, `Oncogene` indicates an oncogene annotation, and blank indicates that no driver-role label is provided for that gene in this source.

### Saito driver annotation
This column records the driver-role label from the **Saito** source used in this module. Expected values are `TSG`, `Oncogene`, or blank. `TSG` indicates a tumor suppressor gene annotation, `Oncogene` indicates an oncogene annotation, and blank indicates that no driver-role label is available for that gene in this source.

### NCG driver annotation
This column records the driver-role label from **NCG** itself. Expected values are `TSG`, `Oncogene`, or blank. `TSG` indicates tumor suppressor behavior, `Oncogene` indicates oncogenic behavior, and blank indicates that no role label is provided in the NCG-derived dataset loaded by this module.

### Number of duplicated loci at 60% coverage
This feature captures **gene duplicability**, defined in NCG using additional genomic loci that match at least 60% of the gene sequence. Lower values indicate lower duplicability, while higher values indicate that similar loci exist elsewhere in the genome. Values are non-negative integers with a minimum of 0 and no strict fixed upper bound, although most genes tend to have relatively modest counts.

### Evolutionary conservation (taxonomic group)
This field summarizes the **evolutionary origin or conservation depth** of the gene across taxonomic groups. In NCG, evolutionary appearance is traced using orthologs across major branches of life, so older genes are typically interpreted as more deeply conserved. Values are ordered categorical labels rather than numbers, typically corresponding to taxonomic levels such as primates, mammals, vertebrates, metazoans, opisthokonts, eukaryotes, or pre-metazoan origin.

### Percentage of cell lines in which the gene was found to be essential
This column reports how often the gene was classified as **essential** across surveyed cell lines. Biologically, higher percentages indicate that a gene is required for survival or proliferation in a larger fraction of tested cell lines. Values range from **0 to 100 percent**, where 0 means essential in none of the profiled lines and 100 means essential in all profiled lines considered by the underlying dataset.

### Number of tissues in which the gene is expressed according to RNA-seq data (out of 43)
This field counts in how many of the **43 unique healthy tissues** the gene is considered expressed based on the union or matching logic used by NCG from GTEx and Protein Atlas RNA-seq resources. It is a breadth-of-expression measure: larger values indicate broader expression across normal tissues, while smaller values indicate more restricted expression. Values range from **0 to 43**.

### Degree of the gene in the protein-protein interaction network (PPIN)
Degree is the number of **direct interaction partners** the encoded protein has in the protein-protein interaction network. Higher degree means the protein behaves more like a network hub and may participate in many cellular processes. Values are non-negative integers starting at **0**; there is no fixed universal maximum because it depends on the network used.

### Betweenness in the PPIN
Betweenness measures how often a node lies on the **shortest paths** connecting other nodes in the interaction network. A high betweenness value suggests that the protein acts as a network bottleneck or bridge between modules, even if it is not the most highly connected node by degree. Values are continuous and non-negative; the exact numeric range depends on whether the network metric is normalized, so there is no single fixed upper bound across implementations.

### Clustering coefficient in the PPIN
The clustering coefficient quantifies how strongly a protein’s immediate interaction partners also interact with one another. Higher values indicate membership in a tightly interconnected local neighborhood, while lower values indicate a more dispersed interaction pattern. This metric typically ranges from **0 to 1**, where 0 means no local neighbor-neighbor connectivity and 1 means a fully connected local neighborhood.

### Number of complexes in which the protein is a component
This feature counts how many annotated **protein complexes** include the encoded protein. Higher values suggest broader involvement in multi-protein assemblies and can reflect central or multifunctional cellular roles. Values are non-negative integers.

### Number of targeting miRNAs
This field counts the number of **microRNAs predicted or reported to target the gene**. Larger values suggest broader post-transcriptional regulatory control, whereas lower values indicate fewer known miRNA-gene interactions. Values are non-negative integers.

### Number of expressed tissues on mRNA level in GTEx
This column counts the number of GTEx tissues in which the gene is considered expressed at the **mRNA** level according to the thresholding scheme used by NCG. Higher values indicate broader expression across normal tissues in GTEx. Values are non-negative integers.

### Number of expressed tissues on mRNA level in Protein Atlas
This field counts the number of Protein Atlas tissues in which the gene is considered expressed at the **mRNA** level. It complements the GTEx-based expression breadth measure and can help distinguish broadly expressed genes from tissue-restricted genes. Values are non-negative integers from **0** up to the number of tissues profiled in the Protein Atlas release used by NCG.

### Number of expressed tissues on protein level in Protein Atlas
This column counts the number of tissues in which the **protein product** is detected in Protein Atlas. Compared with RNA-based measures, it reflects protein-level breadth of expression and may better capture whether the gene product is translated and observed across tissues. Values are non-negative integers starting at **0**; the upper bound depends on the Protein Atlas release.

### Number of expressed cell lines in CLP
This field counts the number of profiled cell lines in the **Cancer Cell Line Project (CLP)** in which the gene is expressed. It is a breadth-of-expression measure across cancer models rather than healthy tissues. Values are non-negative integers from **0** up to the number of CLP cell lines represented in the source dataset.

### Number of expressed cell lines in GNE
This field counts the number of **Genentech (GNE)** cell lines in which the gene is expressed. As with the CLP column, larger values indicate broader expression across cancer cell line models. Values are non-negative integers with minimum **0** and a dataset-dependent upper bound.

### Number of expressed cell lines in CCLE
This column counts the number of **CCLE** cell lines in which the gene is expressed. Higher values indicate broader expression across the Cancer Cell Line Encyclopedia panel and can be informative for model availability and lineage breadth. Values are non-negative integers with minimum **0** and a maximum equal to the number of CCLE lines in the release used.

### Number of germline damaging SNVs and indels/gene length
This feature normalizes the count of **damaging germline SNVs and indels** by gene length. It is intended to make genes of different sizes more comparable by accounting for mutational opportunity. Values are continuous and non-negative, with **0** meaning no such variants per unit length in the source dataset; there is no fixed universal upper bound.

### Number of germline SVs/gene length
This field reports the number of **germline structural variants** normalized by gene length. As with the SNV and indel metric, normalization supports comparison across genes of different sizes. Values are continuous and non-negative, typically starting at **0**, with no single fixed upper limit across datasets.

### LOEUF score
LOEUF is the **loss-of-function observed/expected upper bound fraction**, a widely used gene-constraint metric. Lower LOEUF values indicate stronger depletion of loss-of-function variants in the germline and therefore stronger selective constraint, while higher values indicate greater tolerance. Values are continuous and non-negative; there is no strict universal maximum, but interpretation is primarily relative, with **lower = more constrained**.
