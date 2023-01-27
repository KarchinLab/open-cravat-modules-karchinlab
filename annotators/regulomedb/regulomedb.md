# RegulomeDB

RegulomeDB is a database that annotates SNPs with known and predicted regulatory elements in the intergenic regions of the H. sapiens genome. Known and predicted regulatory DNA elements include regions of DNase hypersensitivity, binding sites oftranscription factors, and promoter regions that have been biochemically characterized to regulation transcription. Sources of these data include public datasets from GEO, the ENCODE project, and published literature.

## Rank
|Score| Supporting data|
|-----|:----------------|
|1a|	eQTL + TF binding + matched TF motif + matched DNase Footprint + DNase peak|
|1b|	eQTL + TF binding + any motif + DNase Footprint + DNase peak|
|1c|	eQTL + TF binding + matched TF motif + DNase peak|
|1d|	eQTL + TF binding + any motif + DNase peak|
|1e|	eQTL + TF binding + matched TF motif|
|1f|	eQTL + TF binding / DNase peak|
|2a|	TF binding + matched TF motif + matched DNase Footprint + DNase peak|
|2b|	TF binding + any motif + DNase Footprint + DNase peak|
|2c|	TF binding + matched TF motif + DNase peak|
|3a|	TF binding + any motif + DNase peak|
|3b|	TF binding + matched TF motif|
|4|	TF binding + DNase peak|
|5|	TF binding or DNase peak|
|6|	Motif hit|
|7|	Other|

Information from https://www.regulomedb.org/regulome-help/