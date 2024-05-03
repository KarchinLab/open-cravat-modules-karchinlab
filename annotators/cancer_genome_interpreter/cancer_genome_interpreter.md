# Cancer Genome Interpreter

*We are unable to update Cancer Genome Interpreter with latest October 2022 version because genomic coordinates of the mutations are no longer being provided.*

Cancer Genome Interpreter (CGI) is designed to support the identification of tumor alterations that drive the disease and detect those that may be therapeutically actionable. CGI relies on existing knowledge collected from several resources and on computational methods that annotate the alterations in a tumor according to distinct levels of evidence.

CGI Flags validated oncogenic alterations, and predicts cancer drivers among mutations of unknown significance. In addition to genomic biomarkers of drug response with different levels of clinical relevance.

## CGI Framework

With a list of genomic alterations in a tumor of a given cancer type as input, the CGI automatically recognizes the format, remaps the variants as needed and standardizes the annotation for downstream compatibility. Next, it identifies known driver alterations and annotates and classifies the remaining variants of unknown significance. Finally, alterations that are biomarkers of drug effect are identified according to current evidences.

## Identification of Driver Events

Alterations that are clinically or experimentally validated to drive tumor phenotypes –previously culled from public sources-- are identified by the CGI, whereas the effect of the remaining alterations of uncertain significance are predicted using in silico approaches, such as OncodriveMUT (for mutations).

### OncodriveMUT

OncodriveMUT is a bioinformatics method to identify the most likely driver mutations of a tumor. Its main innovation with respect to other existing tools with a similar purpose is the incorporation of features characterizing the genes (or regions within genes) where the mutations occur, derived from the analysis of cohorts of tumors (6,792 samples across 28 cancer types⁠) and samples from healthy donors (60,706 unrelated individuals⁠). This knowledge is combined with features that describe the impact of the mutation on the function of the protein it affects via a set of heuristic rules to predict the effect of the mutations of uncertain significance.

## Cancer Biomarkers Database

The cancer biomarkers db integrates manually collected genomic biomarkers of drug sensitivity, resistance and severe toxicity. These biomarkers are classified by the cancer type in which they have been described according to different levels of clinical evidence supporting the association. The database is available for access and feedback by the community at www.cancergenomeinterpreter.org/biomarkers. The aggregation, curation and interpretation of the biomarkers follow the standard operating procedures developed under the umbrella of the H2020 MedBioinformatics project, thus ensuring the mid-term maintenance of these resources. The feedback from the community is also facilitated through the CGI web interface. Nevertheless, access to this type of data is both crucial for the advance of cancer precision medicine and highly complex to be comprehensively covered and updated by a single institution. This is why the [Variant Interpretation for Cancer Consortium](https://www.ga4gh.org/#/vicc), under the Global Alliance for Genomics & Health framework (Global Alliance for Genomics and Health et al. 2016)⁠, has recently been launched with the aim to unify the curation efforts in several institutes, including ours.

Information from https://www.cancergenomeinterpreter.org/faq

