from rpy2.robjects.packages import importr
import rpy2.robjects as robjects
from rpy2.robjects.vectors import StrVector
import rpy2.rinterface as ri
from cravat import BaseConverter
import os

class CravatConverter(BaseConverter):
    def __init__(self):
        self.format_name = 'gds'
        self.addl_cols = [
            {'name':'zygosity','title':'Zygosity','type':'string'}
        ]

    def check_format(self, f):
        file = open(os.path.realpath(f.name), 'rb')
        file_head = file.read(9)
        return file_head.decode() == 'COREARRAY'

    def setup(self, f):
        pass

    #intentional lack of implementation for the convert_line function as gds is a binary file format

    def convert_file(self, f, exc_handler = None, buffsize = 10000):
        SeqArray = importr("SeqArray")
        file = SeqArray.seqOpen(os.path.realpath(f.name))
        sample = SeqArray.seqGetData(file, "sample.id")
        robjects.r('sampleID = {sample}'.format(sample = sample.r_repr()))
        numOfVariants = SeqArray.seqSummary(file, varname = "variant.id")[0]

        robjects.r('''
        output <- function(data) {
        lines <- matrix(, nrow = 0, ncol = 6)
        chrom = data[[1]]
        pos = data[[2]]
        alleles <- c(strsplit(data[[3]][1], ",")[[1]], ".")
        genotype = data[[4]]
        
        internalWrite <- function(alt, hom_het, id) {
            lines <<- rbind(lines, c(chrom, pos, alleles[1], alt, hom_het, id))
        }
        
        genotype[is.na(genotype)] = length(alleles) - 1
        
        for (col in 1:ncol(genotype)) {
            num1 = genotype[1, col] + 1
            num2 = genotype[2, col] + 1
            id = sampleID[col]
            
            if (num1 == 1 & num2 == 1) {
            #nothing to print
            }
            else if (num1 != 1 & num2 == 1) {
            internalWrite(alleles[num1], "het", id)
            }
            else if (num1 == 1 & num2 != 1) {
            internalWrite(alleles[num2], "het", id)
            }
            else if (num1 == num2) {
            internalWrite(alleles[num1], "hom", id)
            }
            else {
            internalWrite(alleles[num1], "het", id)
            internalWrite(alleles[num2], "het", id)
            }
        }
        return(lines)
        }
        ''')
        output = robjects.globalenv['output']

        @ri.rternalize
        def printWithStops(data):
            result = []
            lines = output(data)
            rows = len(lines) // 6

            for line in range(rows):
                result.append(" ".join([lines[line], lines[line+ rows], lines[line+ (2* rows)], lines[line+ (3* rows)], lines[line+ (4* rows)], lines[line+ (5* rows)]]))
            return StrVector(result)

        #returns pairs (a,b) such that the first a is equal to i, the last b is equal to n+1. If we look at all a's inclusively and all b's
        #exclusively then this generates intervals that partition the set of numbers from 1 to n (inclusively) such that all intervals
        #contain a buff amount of numbers except for possibly the last interval 
        def inclusiveRanges(i, n, buff):
            while i <= n:
                if i + buff > n+1:
                    buff -= i + buff - n-1
                yield [i, i+buff]
                i += buff 
        
        for start, end in inclusiveRanges(1, numOfVariants, buffsize):
            try:
                robjects.r('array = c({previous}:{next})'.format(previous = start, next = end - 1))
                SeqArray.seqSetFilter(file, variant_sel = robjects.globalenv['array'], verbose = False)

                result = SeqArray.seqApply(file, StrVector(["chromosome", "position", "allele", "genotype"]), FUN= printWithStops, margin="by.variant", as_is="list")

                for variant in result:
                    for charLine in variant:
                        try:
                            line = charLine.split()
                            if line[3] == '.':
                                continue
                            result = [{
                            'chrom': line[0],
                            'pos': line[1],
                            'ref_base': line[2],
                            'alt_base': line[3],
                            'tags': None,
                            'sample_id': line[5],
                            'zygosity': line[4]
                            }]
                            yield 0,line, result
                        except Exception as e:
                            if exc_handler:
                                exc_handler(0,"",e)
                                continue
                            else:
                                raise e
            except Exception as e:
                if exc_handler:
                    exc_handler(0,"",e)
                    continue
                else:
                    raise e


        #closes the embedded R subprocess and deletes rpy2 objects
        ri.endr(0)
        del file, output, printWithStops, sample, variant