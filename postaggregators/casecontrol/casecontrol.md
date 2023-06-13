# Read the installation section. This module requires the python package `scipy`

# Case-Control Analysis

OpenCRAVAT can perform basic comparisons between case and control cohorts in a study. The Case/Control feature allows users to (1) count samples in case and control groups with particular genotypes, (2) compute the one-sided p-value using Fisher’s Exact Test. Case and control sets are defined by a separate input file.

## Installing

Case/Control uses the python package scipy for statistical tests. On most systems, this can be installed with 

```
pip3 install scipy
```

If this does not work, consult the [scipy website](https://www.scipy.org/install.html) for more options.

Install the `casecontrol` module.

```bash
oc module install casecontrol
```



## Running

Case-Control may be run from the command line and from the GUI in versions above 2.2.0.

Both methods will require a text file which assigns samples to a cohort. The file contains two columns, with whitespace as the delimiter.

```
sample_0    case
sample_1    control
```

Samples which are not in the cohorts file, or are assigned a cohort other than case or control, will not be included in the analysis.

You will be notified if samples in the cohorts file cannot be found in the job. In some cases, this is because multiple input files were used. In that situation, the sample ID must be prefixed with the filename of the input it came from, and a double underscore. For example, a sample called `sample_0` from file `input.vcf` would become `input.vcf__sample_0`.

### Command line

Run casecontrol in the command line by pointing the module to the cohorts file.

```bash
oc run input --module-option casecontrol.cohorts=cohorts.txt
```

### GUI

Run casecontrol in the GUI by scrolling to the bottom of the left hand panel in the submit page, to the section called "Additional Analysis". Then, click the "Case-Control cohorts" button to select your cohorts file.

## Interpreting results

There will be nine output columns. The three columns shown by default are p-values of the likelihood that a variant occurs more in case samples under three different inheritance models. Six hidden columns include counts of homozygous, heterozygous and reference variants across the cohorts.

## P-value calculation for inheritance models

The three inheritance models create different contingency tables depending on the zygosity of the variant.

The dominant model counts a variant as an alt genotype if the variant is heterozygous or homozygous. The recessive model counts a variant as alt only if it is homozygous. The allelic model counts each chromosome separately, counting homozygous as 2 alt genotypes, reference as 2 ref genotypes, and heterozygous as 1 ref genotype and 1 alt genotype.

For example, consider a single case sample's contribution to the contingency table. The contingency tables would depend on zygosity of the allele as follows.

### Heterozygous

Dominant model

|         | Alt | Ref |
|---------|-----|-----|
| Case    |  1  |  0  |
| Control |  0  |  0  |

Recessive model

|         | Alt | Ref |
|---------|-----|-----|
| Case    |  0  |  1  |
| Control |  0  |  0  |

Allelic model

|         | Alt | Ref |
|---------|-----|-----|
| Case    |  1  |  1  |
| Control |  0  |  0  |

### Homozygous

Dominant model

|         | Alt | Ref |
|---------|-----|-----|
| Case    |  1  |  0  |
| Control |  0  |  0  |

Recessive model

|         | Alt | Ref |
|---------|-----|-----|
| Case    |  1  |  0  |
| Control |  0  |  0  |

Allelic model

|         | Alt | Ref |
|---------|-----|-----|
| Case    |  2  |  0  |
| Control |  0  |  0  |

### Reference

Dominant model

|         | Alt | Ref |
|---------|-----|-----|
| Case    |  0  |  1  |
| Control |  0  |  0  |

Recessive model

|         | Alt | Ref |
|---------|-----|-----|
| Case    |  0  |  1  |
| Control |  0  |  0  |

Allelic model

|         | Alt | Ref |
|---------|-----|-----|
| Case    |  0  |  2  |
| Control |  0  |  0  |