# About MutPred

MutPred2 is a machine learning-based method and software package that integrates genetic and molecular data to reason probabilistically about the pathogenicity of amino acid substitutions. This is achieved by providing (1) a general pathogenicity prediction, and (2) a ranked list of specific molecular alterations potentially affecting the phenotype. It is trained on a set of 53,180 pathogenic and 206,946 unlabeled (putatively neutral) variants obtained from the Human Gene Mutation Database (HGMD) [1], SwissVar [2], dbSNP [3] and inter-species pairwise alignment. The MutPred2 model is a bagged ensemble of 30 feed-forward neural networks, each trained on a balanced subset of pathogenic and unlabeled variants.

MutPred2 was developed by Vikas Pejaver at Indiana University, Bloomington, and was a joint project of the Mooney group at the University of Washington and the Radivojac group at Indiana University. The Iakoucheva and Sebat groups at the University of California, San Diego provided additional validation and support. More information on the method and detailed instructions can be seen in the help page.

# Supported By

The work is funded by:
- NIH R01LM009722 (PI: Mooney)
- NIH R01MH105524 (PI: Iakoucheva and Radivojac)
- NIH R01MH104766 (PI: Iakoucheva)
- NIH R01MH076431 (PI: Sebat)
- Indiana University Precision Health Initiative (PI: Radivojac)
- NIH K99LM012992 (PI: Pejaver)

# References

1. Stenson PD, Mort M, Ball EV, Evans K, Hayden M, Heywood S, Hussain M, Phillips AD, Cooper DN. The Human Gene Mutation Database: towards a comprehensive repository of inherited mutation data for medical research, genetic diagnosis and next-generation sequencing studies. Hum Genet (2017)
2. Mottaz A, David FP, Veuthey AL, Yip YL. Easy retrieval of single amino-acid polymorphisms and phenotype information using SwissVar. Bioinformatics (2010) 26(6):851-852
3. Sherry ST, Ward MH, Kholodov M, Baker J, Phan L, Smigielski EM, Sirotkin K. dbSNP: the NCBI database of genetic variation. Nucleic Acids Res (2001) 29(1):308-311

# Disclaimer

The purpose of this resource is to distribute functional prediction of mutation data. The data is meant to be used for basic research. Do not use this data to make clinical decisions. 

