# Network of Cancer Genes

## Summary
The **Network of Cancer Genes (NCG)** is a curated, open-access resource that collects genes whose somatic alterations are reported to drive either **cancer evolution** or **clonal expansion in non-cancer tissues**. In addition to driver-gene labels, NCG annotates a broad set of gene systems-level properties including duplicability, evolutionary origin, expression breadth, essentiality, protein-network topology, miRNA regulation, and germline constraint.

## What this resource contains
NCG was built through expert manual curation of published sequencing screens and driver-gene resources. The database integrates literature support with systems-level annotations that help characterize how driver genes differ from the rest of the human genome.

The properties represented in this module are especially useful for:
- prioritizing candidate driver genes,
- comparing malignant versus non-malignant somatic evolution,
- studying network centrality and dosage sensitivity of driver genes,
- assessing gene breadth of expression and intolerance to germline loss-of-function variation.

## Annotators

This annotator group contains two annotators: **NCG Cancer Drivers** and **NCG Healthy Drivers**.

Together, these annotators allow users to explore genes that drive malignant evolution and genes that promote somatic clonal expansion in histologically normal tissues. Although these groups overlap substantially, they are not identical, and NCG was designed in part to help compare them systematically.

### NCG Cancer Drivers
This annotator focuses on genes with known or predicted driver roles in cancer, along with cancer-context labels such as organ system, primary site, and cancer type. It also includes driver-role annotations from the CGL, Saito, and NCG sources and a panel of systems-level properties that distinguish many cancer drivers from other genes.

### NCG Healthy Drivers
This annotator focuses on genes whose somatic alterations have been reported to drive clonal expansion in non-cancer tissues. These genes are called **Healthy Drivers** in NCG because they can promote somatic evolution in normal tissues without necessarily causing malignant transformation.

## Data source
- Resource: **Network of Cancer Genes (NCG)**
- Website: http://network-cancer-genes.org/
- Scope: curated cancer drivers, healthy drivers, and associated systems-level properties
- Current public site labeling indicates the NCG7.2 series for the web resource

## Notes
- This is a **gene-level** annotation resource.
- Some numeric columns are counts, some are percentages, and some are continuous scores.
- Lower **LOEUF** values indicate stronger depletion of germline loss-of-function variants and therefore stronger intolerance to germline loss-of-function.

## Citation

- Repana D, Nulsen J, Dressler L, et al. *The Network of Cancer Genes (NCG): a comprehensive catalogue of known and candidate cancer genes from cancer sequencing screens.* Genome Biology. 2018.
- Dueso-Barroso A, et al. *Comparative assessment of genes driving cancer and somatic evolution in non-cancer tissues: an update of the Network of Cancer Genes (NCG) resource.* Genome Biology. 2022.
