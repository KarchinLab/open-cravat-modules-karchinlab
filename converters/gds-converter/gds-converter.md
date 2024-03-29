### <span style="color: red;">Warning: This converter only works on MacOS and Linux and will fail if used on a Window based device.</span>

This is a file converter that allows OpenCravat to analyze Genomic Data Structure (GDS) files. 

The GDS file format was developed by Dr. Xiuwen Zheng and is a flexible and portable data container with hierarchical structure to store multiple scalable array-oriented data sets.
GDS is suited for large-scale datasets, especially for data which are much larger than the available random-access memory. This makes it a suitable file type for storing large 
amounts of genomic information. The file is compressed to reduce file size but still retains many of the same benefits as the VCF file format. More information on the file format can be found [here](https://bioconductor.org/packages/release/bioc/vignettes/SeqArray/inst/doc/SeqArrayTutorial.html).

Requirments: 
- OS: *MacOS* or *Linux*. Will not work on Windows
- Programming Languange *Python3*
- Programming Languange *R*
- Python Library *rpy2*
- R Package *SeqArray*

Installation:
 1. Installing R: Further installation link and instructions can be found at [http://lib.stat.cmu.edu/R/CRAN/](http://lib.stat.cmu.edu/R/CRAN/)
 2. Installing rpy2: Call `pip install rpy2` in terminal. Note: this assumes that python and pip are already installed.
 3. Installing the R Package SeqArray:
    - We will be installing this through python and the rpy2 library. It MUST be installed through the rpy2 library. Installing the R Package directly could install it to a directory inaccessable to python. First, run python in terminal by calling `python` or `python3`.
    - In python you can call the following short script and this will download and install the necessary packages.
    
    ```
    from rpy2.robjects.packages import importr
    import rpy2.robjects.packages as rpackages
    rpackages.importr('utils').chooseCRANmirror(ind=1)
    rpackages.importr('utils').install_packages('BiocManager')
    importr('BiocManager').install('SeqArray')
    ```
