#GDS Converter

This is a file converter that allows OpenCravat to analyze Genomic Data Structure (GDS) files. 

The GDS file format was developed by Dr. Xiuwen Zheng and is a flexible and portable data container with hierarchical structure to store multiple scalable array-oriented data sets.
GDS is suited for large-scale datasets, especially for data which are much larger than the available random-access memory. This makes it a suitable file type for storing large 
amounts of genomic information. The file is compressed to reduce file size but still retains many of the same benefits as the VCF file format.

Requirments: 
OS: Mac OS or Linux
Python: >= 3.9.7
Python Library rpy2: >= 3.4.5
R: >= 4.1.1
R Package SeqArray: >= 1.32.0

Installation:
 1. Installing rpy2: Call "pip install rpy2" in terminal. Note: this assumes that python and pip are already installed.
 2. Installing R: Further installation link and instructions can be found at http://lib.stat.cmu.edu/R/CRAN/
 3. Installing the R Package SeqArray:
    A. We will be installing this through python and the rpy2 library. First, run python in terminal by calling "python" or "python3".
    B. In python you can call the following short script and this will download and install the necessary packages.
    "from rpy2.robjects.packages import importr
    import rpy2.robjects.packages as rpackages
    rpackages.importr('utils').chooseCRANmirror(ind=1)
    rpackages.importr('utils').install_packages('BiocManager')
    importr('BiocManager').install('SeqArray')"
