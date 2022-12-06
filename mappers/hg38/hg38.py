# cython: profile=False
import os
import pickle
import time
import json
import glob
import cravat

# bases
ADENINENUM = 0
THYMINENUM = 1
GUANINENUM = 2
CYTOSINENUM = 3
NBASENUM = 0b10000000
ADENINECHAR = "A"
THYMINECHAR = "T"
GUANINECHAR = "G"
CYTOSINECHAR = "C"
NBASECHAR = "N"
ADENINECHARORD = ord(ADENINECHAR)
THYMINECHARORD = ord(THYMINECHAR)
GUANINECHARORD = ord(GUANINECHAR)
CYTOSINECHARORD = ord(CYTOSINECHAR)
NBASECHARORD = ord(NBASECHAR)
# crx column nos
MAPPING_UNIPROT_I = 0
MAPPING_ACHANGE_I = 1
MAPPING_SO_I = 2
MAPPING_TR_I = 3
MAPPING_CCHANGE_I = 4
MAPPING_AALEN_I = 5
MAPPING_GENENAME_I = 6
MAPPING_CODING_I = 7
MAPPING_MANESELECT_I = 8


def basenum_to_base(n):
    if n == ADENINENUM:
        return ADENINECHAR
    elif n == THYMINENUM:
        return THYMINECHAR
    elif n == GUANINENUM:
        return GUANINECHAR
    elif n == CYTOSINENUM:
        return CYTOSINECHAR
    elif n == NBASENUM:
        return NBASECHAR
    else:
        return None


def base_to_basenum(c):
    if c == ADENINECHAR:
        return ADENINENUM
    elif c == THYMINECHAR:
        return THYMINENUM
    elif c == GUANINECHAR:
        return GUANINENUM
    elif c == CYTOSINECHAR:
        return CYTOSINENUM
    elif c == NBASECHAR:
        return NBASENUM
    else:
        return None


def _compare_mapping(m2, m1):
    m1sos = m1[MAPPING_SO_I]
    m2sos = m2[MAPPING_SO_I]
    # Prefer protein coding genes
    minm1so = min(m1sos)
    minm2so = min(m2sos)
    if minm2so < 0 and minm1so > 0:
        return -1
    elif minm1so < 0 and minm2so > 0:
        return 1
    # Prefer more severe sequence ontology
    m1so = max(m1sos)
    m2so = max(m2sos)
    if m1so > m2so:
        return -1
    elif m1so < m2so:
        return 1
    else: # m1so == m2so
        # Prefer MANE select transcripts
        m1mane = m1[MAPPING_MANESELECT_I]
        m2mane = m2[MAPPING_MANESELECT_I]
        if m1mane and not m2mane:
            return -1
        if m2mane and not m1mane:
            return 1
        # Prefer longer genes
        m1aalen = m1[MAPPING_AALEN_I]
        m2aalen = m2[MAPPING_AALEN_I]
        if m1aalen > m2aalen:
            return -1
        else:
            return 1


def convert_codon_to_codonnum(codon):
    codonnum = 0
    codonnum = codonnum | (base_to_basenum(codon[0]) << 4)
    codonnum = codonnum | (base_to_basenum(codon[1]) << 2)
    codonnum = codonnum | base_to_basenum(codon[2])
    return codonnum


# strands
PLUSSTRAND = 1
MINUSSTRAND = -1
rev_bases = {"A": "T", "T": "A", "G": "C", "C": "G", "-": "-"}
# frag kind
FRAG_FLAG_2K = 0b00000010
FRAG_FLAG_UTR = 0b00000100
FRAG_FLAG_CDS = 0b00001000
FRAG_FLAG_INTRON = 0b00010000
FRAG_FLAG_IG = 0b00100000  # intergenic
FRAG_UPIG = FRAG_FLAG_IG | 0b0
FRAG_DNIG = FRAG_FLAG_IG | 0b1
FRAG_UP2K = FRAG_FLAG_2K | 0b0
FRAG_DN2K = FRAG_FLAG_2K | 0b1
FRAG_UTR5 = FRAG_FLAG_UTR | 0b0
FRAG_UTR3 = FRAG_FLAG_UTR | 0b1
FRAG_CDS = FRAG_FLAG_CDS | 0b0
FRAG_NCRNA = FRAG_FLAG_CDS | 0b1
FRAG_UTR5INTRON = FRAG_FLAG_INTRON | FRAG_UTR5
FRAG_UTR3INTRON = FRAG_FLAG_INTRON | FRAG_UTR3
FRAG_CDSINTRON = FRAG_FLAG_INTRON | FRAG_CDS
FRAG_NCRNAINTRON = FRAG_FLAG_INTRON | FRAG_NCRNA
# variant kind
SNV = 21
INS = 22
DEL = 23
COM = 24
# sequence ontology
SO_NSO = -44
SO_PTR = -43  # processed_transcript
SO_TU1 = -42  # transcribed_unprocessed_pseudogene
SO_UNP = -41  # unprocessed_pseudogene
SO_MIR = -40  # miRNA
SO_LNC = -39  # lncRNA_gene
SO_PPS = -38  # processed_pseudogene
SO_SNR = -37  # snRNA
SO_TPR = -36  # transcribed_processed_pseudogene
SO_RTI = -35  # pseudogenic_transcript_with_retained_intron
SO_NMD = -34  # NMD_polymorphic_pseudogene_transcript
SO_MCR = -33  # misc_RNA
SO_UNT = -32  # unconfirmed_transcript
SO_PSE = -31  # pseudogene
SO_TU2 = -30  # transcribed_unitary_pseudogene
SO_NSD = -29
SO_SNO = -28
SO_SCA = -27
SO_PRR = -26
SO_UPG = -25
SO_PPG = -24
SO_RRN = -23
SO_IVP = -22
SO_RIB = -21
SO_SRN = -20
SO_TVG = -19
SO_TVP = -18
SO_TDG = -17
SO_TJG = -16
SO_TCG = -15
SO_TJP = -14
SO_ICG = -13
SO_ICP = -12
SO_IJG = -11
SO_IJP = -10
SO_IDG = -9
SO_IVG = -8
SO_IGP = -7
SO_TPP = -6
SO_SCR = -5
SO_VLR = -4
SO_TUP = -3
SO_MTR = -2
SO_MRR = -1
SO_2KD = 31
SO_2KU = 32
SO_UT3 = 33
SO_UT5 = 34
SO_INT = 35
SO_UNK = 36
SO_SYN = 37
SO_MRT = 38  # start_retained_variant
SO_STR = 39  # stop_retained_variant
SO_MIS = 40
SO_CSS = 41
SO_IND = 42
SO_INI = 43
SO_STL = 44
SO_SPL = 45
SO_STG = 46
SO_FSD = 47
SO_FSI = 48
SO_EXL = 49  # exon_loss_variant
SO_MLO = 50  # start_lost
SO_TAB = 51  # transcript_ablation
# coding column
CODING = 60
NONCODING = 61
transcripttype_to_so = {
    "processed_transcript": SO_PTR,
    "transcribed_unprocessed_pseudogene": SO_TU1,
    "unprocessed_pseudogene": SO_UNP,
    "miRNA": SO_MIR,
    "lncRNA": SO_LNC,
    "processed_pseudogene": SO_PPS,
    "snRNA": SO_SNR,
    "transcribed_processed_pseudogene": SO_TPR,
    "retained_intron": SO_RTI,
    "nonsense_mediated_decay": SO_NMD,
    "misc_RNA": SO_MCR,
    "TEC": SO_UNT,
    "pseudogene": SO_PSE,
    "transcribed_unitary_pseudogene": SO_TU2,
    "non_stop_decay": SO_NSD,
    "snoRNA": SO_SNO,
    "scaRNA": SO_SCA,
    "rRNA_pseudogene": SO_PRR,
    "unitary_pseudogene": SO_UPG,
    "polymorphic_pseudogene": SO_PPG,
    "rRNA": SO_RRN,
    "IG_V_pseudogene": SO_IVP,
    "ribozyme": SO_RIB,
    "sRNA": SO_SRN,
    "TR_V_gene": SO_TVG,
    "TR_V_pseudogene": SO_TVP,
    "TR_D_gene": SO_TDG,
    "TR_J_gene": SO_TJG,
    "TR_C_gene": SO_TCG,
    "TR_J_pseudogene": SO_TJP,
    "IG_C_gene": SO_ICG,
    "IG_C_pseudogene": SO_ICP,
    "IG_J_gene": SO_IJG,
    "IG_J_pseudogene": SO_IJP,
    "IG_D_gene": SO_IDG,
    "IG_V_gene": SO_IVG,
    "IG_pseudogene": SO_IGP,
    "translated_processed_pseudogene": SO_TPP,
    "scRNA": SO_SCR,
    "vaultRNA": SO_VLR,
    "translated_unprocessed_pseudogene": SO_TUP,
    "Mt_tRNA": SO_MTR,
    "Mt_rRNA": SO_MRR,
}
sonum_to_so = {
    SO_NSO: "",
    SO_PTR: "PTR",
    SO_TU1: "TU1",
    SO_UNP: "UNP",
    SO_MIR: "MIR",
    SO_LNC: "LNC",
    SO_PPS: "PPS",
    SO_SNR: "SNR",
    SO_TPR: "TPR",
    SO_RTI: "RTI",
    SO_NMD: "NMD",
    SO_MCR: "MCR",
    SO_UNT: "UNT",
    SO_PSE: "PSE",
    SO_TU2: "TU2",
    SO_NSD: "NSD",
    SO_SNO: "SNO",
    SO_SCA: "SCA",
    SO_PRR: "PRR",
    SO_UPG: "UPG",
    SO_PPG: "PPG",
    SO_RRN: "RRN",
    SO_IVP: "IVP",
    SO_RIB: "RIB",
    SO_SRN: "SRN",
    SO_TVG: "TVG",
    SO_TVP: "TVP",
    SO_TDG: "TDG",
    SO_TJG: "TJG",
    SO_TCG: "TCG",
    SO_TJP: "TJP",
    SO_ICG: "ICG",
    SO_ICP: "ICP",
    SO_IJG: "IJG",
    SO_IJP: "IJP",
    SO_IDG: "IDG",
    SO_IVG: "IVG",
    SO_IGP: "IGP",
    SO_TPP: "TPP",
    SO_SCR: "SCR",
    SO_VLR: "VLR",
    SO_TUP: "TUP",
    SO_MTR: "MTR",
    SO_MRR: "MRR",
    SO_2KD: "2KD",
    SO_2KU: "2KU",
    SO_UT3: "UT3",
    SO_UT5: "UT5",
    SO_INT: "INT",
    SO_UNK: "UNK",
    SO_SYN: "SYN",
    SO_MRT: "MRT",
    SO_STR: "STR",
    SO_MIS: "MIS",
    SO_CSS: "CSS",
    SO_IND: "IND",
    SO_INI: "INI",
    SO_STL: "STL",
    SO_SPL: "SPL",
    SO_STG: "STG",
    SO_FSD: "FSD",
    SO_FSI: "FSI",
    SO_EXL: "EXL",
    SO_MLO: "MLO",
    SO_TAB: "TAB",
}
so_to_sonum = {}
for sonum in sonum_to_so:
    so_to_sonum[sonum_to_so[sonum]] = sonum
# aa
NDA = 32
NOA = 95
XAA = 63  # unknown aa
TER = 42
ALA = 65
CYS = 67
ASP = 68
GLU = 69
PHE = 70
GLY = 71
HIS = 72
ILE = 73
LYS = 75
LEU = 76
MET = 77
ASN = 78
PRO = 80
GLN = 81
ARG = 82
SER = 83
THR = 84
VAL = 86
TRP = 87
TYR = 89
aa_to_num = {
    "A": ALA,
    "C": CYS,
    "D": ASP,
    "E": GLU,
    "F": PHE,
    "G": GLY,
    "H": HIS,
    "I": ILE,
    "K": LYS,
    "L": LEU,
    "M": MET,
    "N": ASN,
    "P": PRO,
    "Q": GLN,
    "R": ARG,
    "S": SER,
    "T": THR,
    "V": VAL,
    "W": TRP,
    "Y": TYR,
    "*": TER,
    NOA: "_",
    XAA: "?",
    NDA: " ",
}
aanum_to_aa1 = {
    ALA: "A",
    CYS: "C",
    ASP: "D",
    GLU: "E",
    PHE: "F",
    GLY: "G",
    HIS: "H",
    ILE: "I",
    LYS: "K",
    LEU: "L",
    MET: "M",
    ASN: "N",
    PRO: "P",
    GLN: "Q",
    ARG: "R",
    SER: "S",
    THR: "T",
    VAL: "V",
    TRP: "W",
    TYR: "Y",
    TER: "*",
    NOA: "_",
    XAA: "?",
    NDA: " ",
}
aanum_to_aa = {
    ALA: "Ala",
    CYS: "Cys",
    ASP: "Asp",
    GLU: "Glu",
    PHE: "Phe",
    GLY: "Gly",
    HIS: "His",
    ILE: "Ile",
    LYS: "Lys",
    LEU: "Leu",
    MET: "Met",
    ASN: "Asn",
    PRO: "Pro",
    GLN: "Gln",
    ARG: "Arg",
    SER: "Ser",
    THR: "Thr",
    VAL: "Val",
    TRP: "Trp",
    TYR: "Tyr",
    TER: "Ter",
    NOA: "???",
    XAA: "???",
    NDA: "???",
}
codon_to_codonnum = {
    "AAA": convert_codon_to_codonnum("AAA"),
    "AAT": convert_codon_to_codonnum("AAT"),
    "AAG": convert_codon_to_codonnum("AAG"),
    "AAC": convert_codon_to_codonnum("AAC"),
    "ATA": convert_codon_to_codonnum("ATA"),
    "ATT": convert_codon_to_codonnum("ATT"),
    "ATG": convert_codon_to_codonnum("ATG"),
    "ATC": convert_codon_to_codonnum("ATC"),
    "AGA": convert_codon_to_codonnum("AGA"),
    "AGT": convert_codon_to_codonnum("AGT"),
    "AGG": convert_codon_to_codonnum("AGG"),
    "AGC": convert_codon_to_codonnum("AGC"),
    "ACA": convert_codon_to_codonnum("ACA"),
    "ACT": convert_codon_to_codonnum("ACT"),
    "ACG": convert_codon_to_codonnum("ACG"),
    "ACC": convert_codon_to_codonnum("ACC"),
    "TAA": convert_codon_to_codonnum("TAA"),
    "TAT": convert_codon_to_codonnum("TAT"),
    "TAG": convert_codon_to_codonnum("TAG"),
    "TAC": convert_codon_to_codonnum("TAC"),
    "TTA": convert_codon_to_codonnum("TTA"),
    "TTT": convert_codon_to_codonnum("TTT"),
    "TTG": convert_codon_to_codonnum("TTG"),
    "TTC": convert_codon_to_codonnum("TTC"),
    "TGA": convert_codon_to_codonnum("TGA"),
    "TGT": convert_codon_to_codonnum("TGT"),
    "TGG": convert_codon_to_codonnum("TGG"),
    "TGC": convert_codon_to_codonnum("TGC"),
    "TCA": convert_codon_to_codonnum("TCA"),
    "TCT": convert_codon_to_codonnum("TCT"),
    "TCG": convert_codon_to_codonnum("TCG"),
    "TCC": convert_codon_to_codonnum("TCC"),
    "GAA": convert_codon_to_codonnum("GAA"),
    "GAT": convert_codon_to_codonnum("GAT"),
    "GAG": convert_codon_to_codonnum("GAG"),
    "GAC": convert_codon_to_codonnum("GAC"),
    "GTA": convert_codon_to_codonnum("GTA"),
    "GTT": convert_codon_to_codonnum("GTT"),
    "GTG": convert_codon_to_codonnum("GTG"),
    "GTC": convert_codon_to_codonnum("GTC"),
    "GGA": convert_codon_to_codonnum("GGA"),
    "GGT": convert_codon_to_codonnum("GGT"),
    "GGG": convert_codon_to_codonnum("GGG"),
    "GGC": convert_codon_to_codonnum("GGC"),
    "GCA": convert_codon_to_codonnum("GCA"),
    "GCT": convert_codon_to_codonnum("GCT"),
    "GCG": convert_codon_to_codonnum("GCG"),
    "GCC": convert_codon_to_codonnum("GCC"),
    "CAA": convert_codon_to_codonnum("CAA"),
    "CAT": convert_codon_to_codonnum("CAT"),
    "CAG": convert_codon_to_codonnum("CAG"),
    "CAC": convert_codon_to_codonnum("CAC"),
    "CTA": convert_codon_to_codonnum("CTA"),
    "CTT": convert_codon_to_codonnum("CTT"),
    "CTG": convert_codon_to_codonnum("CTG"),
    "CTC": convert_codon_to_codonnum("CTC"),
    "CGA": convert_codon_to_codonnum("CGA"),
    "CGT": convert_codon_to_codonnum("CGT"),
    "CGG": convert_codon_to_codonnum("CGG"),
    "CGC": convert_codon_to_codonnum("CGC"),
    "CCA": convert_codon_to_codonnum("CCA"),
    "CCT": convert_codon_to_codonnum("CCT"),
    "CCG": convert_codon_to_codonnum("CCG"),
    "CCC": convert_codon_to_codonnum("CCC"),
}
codonnum_to_codon = {
    convert_codon_to_codonnum("AAA"): "AAA",
    convert_codon_to_codonnum("AAT"): "AAT",
    convert_codon_to_codonnum("AAG"): "AAG",
    convert_codon_to_codonnum("AAC"): "AAC",
    convert_codon_to_codonnum("ATA"): "ATA",
    convert_codon_to_codonnum("ATT"): "ATT",
    convert_codon_to_codonnum("ATG"): "ATG",
    convert_codon_to_codonnum("ATC"): "ATC",
    convert_codon_to_codonnum("AGA"): "AGA",
    convert_codon_to_codonnum("AGT"): "AGT",
    convert_codon_to_codonnum("AGG"): "AGG",
    convert_codon_to_codonnum("AGC"): "AGC",
    convert_codon_to_codonnum("ACA"): "ACA",
    convert_codon_to_codonnum("ACT"): "ACT",
    convert_codon_to_codonnum("ACG"): "ACG",
    convert_codon_to_codonnum("ACC"): "ACC",
    convert_codon_to_codonnum("TAA"): "TAA",
    convert_codon_to_codonnum("TAT"): "TAT",
    convert_codon_to_codonnum("TAG"): "TAG",
    convert_codon_to_codonnum("TAC"): "TAC",
    convert_codon_to_codonnum("TTA"): "TTA",
    convert_codon_to_codonnum("TTT"): "TTT",
    convert_codon_to_codonnum("TTG"): "TTG",
    convert_codon_to_codonnum("TTC"): "TTC",
    convert_codon_to_codonnum("TGA"): "TGA",
    convert_codon_to_codonnum("TGT"): "TGT",
    convert_codon_to_codonnum("TGG"): "TGG",
    convert_codon_to_codonnum("TGC"): "TGC",
    convert_codon_to_codonnum("TCA"): "TCA",
    convert_codon_to_codonnum("TCT"): "TCT",
    convert_codon_to_codonnum("TCG"): "TCG",
    convert_codon_to_codonnum("TCC"): "TCC",
    convert_codon_to_codonnum("GAA"): "GAA",
    convert_codon_to_codonnum("GAT"): "GAT",
    convert_codon_to_codonnum("GAG"): "GAG",
    convert_codon_to_codonnum("GAC"): "GAC",
    convert_codon_to_codonnum("GTA"): "GTA",
    convert_codon_to_codonnum("GTT"): "GTT",
    convert_codon_to_codonnum("GTG"): "GTG",
    convert_codon_to_codonnum("GTC"): "GTC",
    convert_codon_to_codonnum("GGA"): "GGA",
    convert_codon_to_codonnum("GGT"): "GGT",
    convert_codon_to_codonnum("GGG"): "GGG",
    convert_codon_to_codonnum("GGC"): "GGC",
    convert_codon_to_codonnum("GCA"): "GCA",
    convert_codon_to_codonnum("GCT"): "GCT",
    convert_codon_to_codonnum("GCG"): "GCG",
    convert_codon_to_codonnum("GCC"): "GCC",
    convert_codon_to_codonnum("CAA"): "CAA",
    convert_codon_to_codonnum("CAT"): "CAT",
    convert_codon_to_codonnum("CAG"): "CAG",
    convert_codon_to_codonnum("CAC"): "CAC",
    convert_codon_to_codonnum("CTA"): "CTA",
    convert_codon_to_codonnum("CTT"): "CTT",
    convert_codon_to_codonnum("CTG"): "CTG",
    convert_codon_to_codonnum("CTC"): "CTC",
    convert_codon_to_codonnum("CGA"): "CGA",
    convert_codon_to_codonnum("CGT"): "CGT",
    convert_codon_to_codonnum("CGG"): "CGG",
    convert_codon_to_codonnum("CGC"): "CGC",
    convert_codon_to_codonnum("CCA"): "CCA",
    convert_codon_to_codonnum("CCT"): "CCT",
    convert_codon_to_codonnum("CCG"): "CCG",
    convert_codon_to_codonnum("CCC"): "CCC",
}
codonnum_to_aanum = {
    convert_codon_to_codonnum("ATG"): aa_to_num["M"],
    convert_codon_to_codonnum("GCT"): aa_to_num["A"],
    convert_codon_to_codonnum("GCC"): aa_to_num["A"],
    convert_codon_to_codonnum("GCA"): aa_to_num["A"],
    convert_codon_to_codonnum("GCG"): aa_to_num["A"],
    convert_codon_to_codonnum("TGT"): aa_to_num["C"],
    convert_codon_to_codonnum("TGC"): aa_to_num["C"],
    convert_codon_to_codonnum("GAT"): aa_to_num["D"],
    convert_codon_to_codonnum("GAC"): aa_to_num["D"],
    convert_codon_to_codonnum("GAA"): aa_to_num["E"],
    convert_codon_to_codonnum("GAG"): aa_to_num["E"],
    convert_codon_to_codonnum("TTT"): aa_to_num["F"],
    convert_codon_to_codonnum("TTC"): aa_to_num["F"],
    convert_codon_to_codonnum("GGT"): aa_to_num["G"],
    convert_codon_to_codonnum("GGC"): aa_to_num["G"],
    convert_codon_to_codonnum("GGA"): aa_to_num["G"],
    convert_codon_to_codonnum("GGG"): aa_to_num["G"],
    convert_codon_to_codonnum("CAT"): aa_to_num["H"],
    convert_codon_to_codonnum("CAC"): aa_to_num["H"],
    convert_codon_to_codonnum("ATT"): aa_to_num["I"],
    convert_codon_to_codonnum("ATC"): aa_to_num["I"],
    convert_codon_to_codonnum("ATA"): aa_to_num["I"],
    convert_codon_to_codonnum("AAA"): aa_to_num["K"],
    convert_codon_to_codonnum("AAG"): aa_to_num["K"],
    convert_codon_to_codonnum("TTA"): aa_to_num["L"],
    convert_codon_to_codonnum("TTG"): aa_to_num["L"],
    convert_codon_to_codonnum("CTT"): aa_to_num["L"],
    convert_codon_to_codonnum("CTC"): aa_to_num["L"],
    convert_codon_to_codonnum("CTA"): aa_to_num["L"],
    convert_codon_to_codonnum("CTG"): aa_to_num["L"],
    convert_codon_to_codonnum("AAT"): aa_to_num["N"],
    convert_codon_to_codonnum("AAC"): aa_to_num["N"],
    convert_codon_to_codonnum("CCT"): aa_to_num["P"],
    convert_codon_to_codonnum("CCC"): aa_to_num["P"],
    convert_codon_to_codonnum("CCA"): aa_to_num["P"],
    convert_codon_to_codonnum("CCG"): aa_to_num["P"],
    convert_codon_to_codonnum("CAA"): aa_to_num["Q"],
    convert_codon_to_codonnum("CAG"): aa_to_num["Q"],
    convert_codon_to_codonnum("TCT"): aa_to_num["S"],
    convert_codon_to_codonnum("TCC"): aa_to_num["S"],
    convert_codon_to_codonnum("TCA"): aa_to_num["S"],
    convert_codon_to_codonnum("TCG"): aa_to_num["S"],
    convert_codon_to_codonnum("AGT"): aa_to_num["S"],
    convert_codon_to_codonnum("AGC"): aa_to_num["S"],
    convert_codon_to_codonnum("ACT"): aa_to_num["T"],
    convert_codon_to_codonnum("ACC"): aa_to_num["T"],
    convert_codon_to_codonnum("ACA"): aa_to_num["T"],
    convert_codon_to_codonnum("ACG"): aa_to_num["T"],
    convert_codon_to_codonnum("CGT"): aa_to_num["R"],
    convert_codon_to_codonnum("CGC"): aa_to_num["R"],
    convert_codon_to_codonnum("CGA"): aa_to_num["R"],
    convert_codon_to_codonnum("CGG"): aa_to_num["R"],
    convert_codon_to_codonnum("AGA"): aa_to_num["R"],
    convert_codon_to_codonnum("AGG"): aa_to_num["R"],
    convert_codon_to_codonnum("GTT"): aa_to_num["V"],
    convert_codon_to_codonnum("GTC"): aa_to_num["V"],
    convert_codon_to_codonnum("GTA"): aa_to_num["V"],
    convert_codon_to_codonnum("GTG"): aa_to_num["V"],
    convert_codon_to_codonnum("TGG"): aa_to_num["W"],
    convert_codon_to_codonnum("TAT"): aa_to_num["Y"],
    convert_codon_to_codonnum("TAC"): aa_to_num["Y"],
    convert_codon_to_codonnum("TGA"): aa_to_num["*"],
    convert_codon_to_codonnum("TAA"): aa_to_num["*"],
    convert_codon_to_codonnum("TAG"): aa_to_num["*"],
}
codonnum_to_aa = {
    convert_codon_to_codonnum("ATG"): "M",
    convert_codon_to_codonnum("GCT"): "A",
    convert_codon_to_codonnum("GCC"): "A",
    convert_codon_to_codonnum("GCA"): "A",
    convert_codon_to_codonnum("GCG"): "A",
    convert_codon_to_codonnum("TGT"): "C",
    convert_codon_to_codonnum("TGC"): "C",
    convert_codon_to_codonnum("GAT"): "D",
    convert_codon_to_codonnum("GAC"): "D",
    convert_codon_to_codonnum("GAA"): "E",
    convert_codon_to_codonnum("GAG"): "E",
    convert_codon_to_codonnum("TTT"): "F",
    convert_codon_to_codonnum("TTC"): "F",
    convert_codon_to_codonnum("GGT"): "G",
    convert_codon_to_codonnum("GGC"): "G",
    convert_codon_to_codonnum("GGA"): "G",
    convert_codon_to_codonnum("GGG"): "G",
    convert_codon_to_codonnum("CAT"): "H",
    convert_codon_to_codonnum("CAC"): "H",
    convert_codon_to_codonnum("ATT"): "I",
    convert_codon_to_codonnum("ATC"): "I",
    convert_codon_to_codonnum("ATA"): "I",
    convert_codon_to_codonnum("AAA"): "K",
    convert_codon_to_codonnum("AAG"): "K",
    convert_codon_to_codonnum("TTA"): "L",
    convert_codon_to_codonnum("TTG"): "L",
    convert_codon_to_codonnum("CTT"): "L",
    convert_codon_to_codonnum("CTC"): "L",
    convert_codon_to_codonnum("CTA"): "L",
    convert_codon_to_codonnum("CTG"): "L",
    convert_codon_to_codonnum("AAT"): "N",
    convert_codon_to_codonnum("AAC"): "N",
    convert_codon_to_codonnum("CCT"): "P",
    convert_codon_to_codonnum("CCC"): "P",
    convert_codon_to_codonnum("CCA"): "P",
    convert_codon_to_codonnum("CCG"): "P",
    convert_codon_to_codonnum("CAA"): "Q",
    convert_codon_to_codonnum("CAG"): "Q",
    convert_codon_to_codonnum("TCT"): "S",
    convert_codon_to_codonnum("TCC"): "S",
    convert_codon_to_codonnum("TCA"): "S",
    convert_codon_to_codonnum("TCG"): "S",
    convert_codon_to_codonnum("AGT"): "S",
    convert_codon_to_codonnum("AGC"): "S",
    convert_codon_to_codonnum("ACT"): "T",
    convert_codon_to_codonnum("ACC"): "T",
    convert_codon_to_codonnum("ACA"): "T",
    convert_codon_to_codonnum("ACG"): "T",
    convert_codon_to_codonnum("CGT"): "R",
    convert_codon_to_codonnum("CGC"): "R",
    convert_codon_to_codonnum("CGA"): "R",
    convert_codon_to_codonnum("CGG"): "R",
    convert_codon_to_codonnum("AGA"): "R",
    convert_codon_to_codonnum("AGG"): "R",
    convert_codon_to_codonnum("GTT"): "V",
    convert_codon_to_codonnum("GTC"): "V",
    convert_codon_to_codonnum("GTA"): "V",
    convert_codon_to_codonnum("GTG"): "V",
    convert_codon_to_codonnum("TGG"): "W",
    convert_codon_to_codonnum("TAT"): "Y",
    convert_codon_to_codonnum("TAC"): "Y",
    convert_codon_to_codonnum("TGA"): "*",
    convert_codon_to_codonnum("TAA"): "*",
    convert_codon_to_codonnum("TAG"): "*",
}
codon_to_aanum = {
    "ATG": MET,
    "GCT": ALA,
    "GCC": ALA,
    "GCA": ALA,
    "GCG": ALA,
    "TGT": CYS,
    "TGC": CYS,
    "GAT": ASP,
    "GAC": ASP,
    "GAA": GLU,
    "GAG": GLU,
    "TTT": PHE,
    "TTC": PHE,
    "GGT": GLY,
    "GGC": GLY,
    "GGA": GLY,
    "GGG": GLY,
    "CAT": HIS,
    "CAC": HIS,
    "ATT": ILE,
    "ATC": ILE,
    "ATA": ILE,
    "AAA": LYS,
    "AAG": LYS,
    "TTA": LEU,
    "TTG": LEU,
    "CTT": LEU,
    "CTC": LEU,
    "CTA": LEU,
    "CTG": LEU,
    "AAT": ASN,
    "AAC": ASN,
    "CCT": PRO,
    "CCC": PRO,
    "CCA": PRO,
    "CCG": PRO,
    "CAA": GLN,
    "CAG": GLN,
    "TCT": SER,
    "TCC": SER,
    "TCA": SER,
    "TCG": SER,
    "AGT": SER,
    "AGC": SER,
    "ACT": THR,
    "ACC": THR,
    "ACA": THR,
    "ACG": THR,
    "CGT": ARG,
    "CGC": ARG,
    "CGA": ARG,
    "CGG": ARG,
    "AGA": ARG,
    "AGG": ARG,
    "GTT": VAL,
    "GTC": VAL,
    "GTA": VAL,
    "GTG": VAL,
    "TGG": TRP,
    "TAT": TYR,
    "TAC": TYR,
    "TGA": TER,
    "TAA": TER,
    "TAG": TER,
}
codon_to_aa = {
    "ATG": "M",
    "GCT": "A",
    "GCC": "A",
    "GCA": "A",
    "GCG": "A",
    "TGT": "C",
    "TGC": "C",
    "GAT": "D",
    "GAC": "D",
    "GAA": "E",
    "GAG": "E",
    "TTT": "F",
    "TTC": "F",
    "GGT": "G",
    "GGC": "G",
    "GGA": "G",
    "GGG": "G",
    "CAT": "H",
    "CAC": "H",
    "ATT": "I",
    "ATC": "I",
    "ATA": "I",
    "AAA": "K",
    "AAG": "K",
    "TTA": "L",
    "TTG": "L",
    "CTT": "L",
    "CTC": "L",
    "CTA": "L",
    "CTG": "L",
    "AAT": "N",
    "AAC": "N",
    "CCT": "P",
    "CCC": "P",
    "CCA": "P",
    "CCG": "P",
    "CAA": "Q",
    "CAG": "Q",
    "TCT": "S",
    "TCC": "S",
    "TCA": "S",
    "TCG": "S",
    "AGT": "S",
    "AGC": "S",
    "ACT": "T",
    "ACC": "T",
    "ACA": "T",
    "ACG": "T",
    "CGT": "R",
    "CGC": "R",
    "CGA": "R",
    "CGG": "R",
    "AGA": "R",
    "AGG": "R",
    "GTT": "V",
    "GTC": "V",
    "GTA": "V",
    "GTG": "V",
    "TGG": "W",
    "TAT": "Y",
    "TAC": "Y",
    "TGA": "*",
    "TAA": "*",
    "TAG": "*",
}
# misc
NO_NEXT_TER = -1
CCHANGE_EXONIC = 1
CCHANGE_NONEXONIC = 0
TR_INFO_ALEN_I = 3
TR_INFO_TLEN_I = 4
TRUE = 1
FALSE = 0
GENETYPENO_PROTEIN_CODING = None
TRANSCRIPTTYPENO_PROTEIN_CODING = None
TRANSCRIPTCLASSNO_CODING = None
TRANSCRIPTTYPENO_NMD = None
NO_VALUE = -1
SO_TO_DISCARD = -999


def _get_base_str(tr_base, lenbase):
    tr_base_str = ""
    for i in range(lenbase):
        tr_base_str += chr(tr_base[i])
    return tr_base_str


class Mapper(cravat.BaseMapper):
    def map(self, crv_data):
        tr_info = self.tr_info
        chrom = crv_data["chrom"]
        if chrom.startswith('chrK') or chrom.startswith('chrG') or chrom.startswith('chrJ'):
            chrom_nover = chrom[3:].split('.')[0]
            q = f'select chrom from chroms where substr(chrom, instr(chrom, "_") + 1, instr(chrom, "v") - instr(chrom, "_") - 1) like "{chrom_nover}%"'
            self.c.execute(q)
            r = self.c.fetchone()
            if r is not None:
                chrom = r[0]
        gpos = crv_data["pos"]
        ref_base_str = crv_data["ref_base"]
        alt_base_str = crv_data["alt_base"]
        if ref_base_str is None:
            ref_base_str = "-"
        if alt_base_str is None:
            alt_base_str = "-"
        lenref = len(ref_base_str)
        lenalt = len(alt_base_str)
        tr_ref_base_plus = ""
        for i in range(lenref):
            tr_ref_base_plus += ref_base_str[i]
        tr_alt_base_plus = ""
        for i in range(lenalt):
            tr_alt_base_plus += alt_base_str[i]
        tr_ref_base_minus = ""
        for i in range(lenref):
            j = lenref - 1 - i
            tr_ref_base_minus += rev_bases[ref_base_str[j]]
        tr_alt_base_minus = ""
        for i in range(lenalt):
            j = lenalt - 1 - i
            tr_alt_base_minus += rev_bases[alt_base_str[j]]
        if ref_base_str == "-" and alt_base_str != "-" and lenalt >= 1:
            var_type = INS
        elif alt_base_str == "-" and ref_base_str != "-" and lenref >= 1:
            var_type = DEL
        elif (
            ref_base_str != "-" and alt_base_str != "-" and lenref == 1 and lenalt == 1
        ):
            var_type = SNV
        else:
            var_type = COM
        tr_map_starts = self._get_tr_map_data(chrom, gpos)
        if var_type == DEL or var_type == COM:
            tr_map_start_by_tid = {}
            tr_map_end_by_tid = {}
            if lenref == 1:
                gposend = gpos
                for tr_map_start in tr_map_starts:
                    tid = tr_map_start[0]
                    tr_map_start_by_tid[tid] = tr_map_start
                    tr_map_end_by_tid[tid] = tr_map_start
            else:
                gposend = gpos + lenref - 1
                for tr_map_start in tr_map_starts:
                    tr_map_start_by_tid[tr_map_start[0]] = tr_map_start
                tr_map_ends = self._get_tr_map_data(chrom, gposend)
                for tr_map_end in tr_map_ends:
                    tr_map_end_by_tid[tr_map_end[0]] = tr_map_end
                for tid in tr_map_start_by_tid:
                    if tid not in tr_map_end_by_tid:
                        tr_map_end_by_tid[tid] = (
                            tid,
                            -1,
                            -1,
                            -1,
                            FRAG_FLAG_IG,
                            -1,
                            -1,
                            -1,
                            -1,
                            -1,
                            -1,
                        )
                for tid in tr_map_end_by_tid:
                    if tid not in tr_map_start_by_tid:
                        tr_map_start_by_tid[tid] = (
                            tid,
                            -1,
                            -1,
                            -1,
                            FRAG_FLAG_IG,
                            -1,
                            -1,
                            -1,
                            -1,
                            -1,
                            -1,
                        )
        else:
            gposend = gpos
        all_mappings = {}
        coding = NONCODING
        for tr_map_start in tr_map_starts:
            (
                tid,
                fragno,
                start,
                end,
                kind,
                exonno,
                tstart,
                cstart,
                binno,
                prevcont,
                nextcont,
            ) = tr_map_start
            (
                tr,
                strand,
                uniprot,
                alen,
                tlen,
                genename,
                tposcposoffset,
                genetypeno,
                transcripttypeno,
                transcriptclassno,
            ) = tr_info[tid]
            if (
                (genetypeno == GENETYPENO_PROTEIN_CODING)
                and (
                    transcripttypeno == TRANSCRIPTTYPENO_PROTEIN_CODING
                    or transcripttypeno == TRANSCRIPTTYPENO_NMD
                )
                and transcriptclassno == TRANSCRIPTCLASSNO_CODING
            ):
                if strand == MINUSSTRAND and gposend != gpos:
                    strand_gpos = gposend
                    strand_gposend = gpos
                    (
                        tid,
                        fragno,
                        start,
                        end,
                        kind,
                        exonno,
                        tstart,
                        cstart,
                        binno,
                        prevcont,
                        nextcont,
                    ) = tr_map_end_by_tid[tid]
                    if var_type == DEL or var_type == COM:
                        tr_map_end = tr_map_start
                else:
                    strand_gpos = gpos
                    strand_gposend = gposend
                    if var_type == DEL or var_type == COM:
                        tr_map_end = tr_map_end_by_tid[tid]
                if strand == PLUSSTRAND:
                    tr_ref_base = tr_ref_base_plus
                    tr_alt_base = tr_alt_base_plus
                    gdist = strand_gpos - start
                elif strand == MINUSSTRAND:
                    tr_ref_base = tr_ref_base_minus
                    tr_alt_base = tr_alt_base_minus
                    gdist = end - strand_gpos
                # tpos, cpos, apos
                tpos = -1
                if kind == FRAG_CDS or kind == FRAG_NCRNA:
                    cpos = cstart + gdist
                    tpos = tstart + gdist
                    apos = int((cpos - 1) / 3) + 1
                elif kind == FRAG_CDSINTRON:
                    tpos = tstart
                    cpos = cstart
                    apos = int((cpos - 1) / 3) + 1
                elif kind == FRAG_UTR5 or kind == FRAG_UTR3:
                    tpos = gdist + tstart
                    cpos = gdist + cstart
                    apos = -1
                elif kind == FRAG_UP2K or kind == FRAG_DN2K:
                    tpos = gdist + tstart
                    cpos = gdist + cstart
                    apos = -1
                elif kind == FRAG_UTR5INTRON or kind == FRAG_UTR3INTRON:
                    tpos = tstart
                    cpos = cstart
                    apos = -1
                elif kind == FRAG_UP2K or kind == FRAG_DN2K:
                    tpos = gdist + tstart
                    cpos = gdist + cstart
                    apos = -1
                elif kind == FRAG_FLAG_IG:
                    tpos = -1
                    cpos = -1
                    apos = -1
                # so, refaa, altaa
                if var_type == SNV:
                    so, achange, cchange, coding = self._get_snv_map_data(
                        tid,
                        cpos,
                        cstart,
                        tpos,
                        tstart,
                        tr_ref_base,
                        tr_alt_base,
                        strand,
                        kind,
                        apos,
                        strand_gpos,
                        start,
                        end,
                        chrom,
                        fragno,
                        lenref,
                        lenalt,
                        prevcont,
                        nextcont,
                        exonno,
                    )
                elif var_type == INS:
                    so, achange, cchange, coding = self._get_ins_map_data(
                        tid,
                        cpos,
                        cstart,
                        tpos,
                        tstart,
                        tr_ref_base,
                        tr_alt_base,
                        strand,
                        kind,
                        apos,
                        strand_gpos,
                        start,
                        end,
                        chrom,
                        fragno,
                        lenref,
                        lenalt,
                        prevcont,
                        nextcont,
                        exonno,
                        alen,
                        tposcposoffset
                    )
                elif var_type == DEL:
                    so, achange, cchange, coding = self._get_del_map_data(
                        tid,
                        cpos,
                        cstart,
                        tpos,
                        tstart,
                        tr_ref_base,
                        tr_alt_base,
                        strand,
                        kind,
                        apos,
                        strand_gpos,
                        start,
                        end,
                        chrom,
                        strand_gposend,
                        fragno,
                        lenref,
                        lenalt,
                        prevcont,
                        nextcont,
                        alen,
                        tlen,
                        exonno,
                        tr_map_end,
                        tposcposoffset,
                    )
                elif var_type == COM:
                    so, achange, cchange, coding = self._get_com_map_data(
                        tid,
                        cpos,
                        cstart,
                        tpos,
                        tstart,
                        tr_ref_base,
                        tr_alt_base,
                        strand,
                        kind,
                        apos,
                        strand_gpos,
                        start,
                        end,
                        chrom,
                        strand_gposend,
                        fragno,
                        lenref,
                        lenalt,
                        prevcont,
                        nextcont,
                        alen,
                        tlen,
                        exonno,
                        tr_map_end,
                        tposcposoffset,
                        tr_alt_base_plus,
                        tr_alt_base_minus,
                        var_type,
                    )
                if SO_TO_DISCARD in so:
                    continue
                if transcripttypeno == TRANSCRIPTTYPENO_NMD:
                    so += (SO_NMD,)
                primarytr = genename in self.primary_transcript and tr.split(".")[0] == self.primary_transcript[genename]
                mapping = (uniprot, achange, so, tr, cchange, alen, genename, coding, primarytr)
                if genename not in all_mappings:
                    all_mappings[genename] = []
                all_mappings[genename].append(mapping)
            else:
                ttype = self.transcripttypes[transcripttypeno]
                if ttype in transcripttype_to_so:
                    so = (transcripttype_to_so[ttype],)
                else:
                    gtype = self.genetypes[genetypeno]
                    if gtype in transcripttype_to_so:
                        so = (transcripttype_to_so[gtype],)
                    else:
                        so = (SO_UNK,)
                if kind & FRAG_FLAG_INTRON == FRAG_FLAG_INTRON:
                    so += (SO_INT,)
                elif kind == FRAG_UTR5:
                    so += (SO_UT5,)
                elif kind == FRAG_UTR3:
                    so += (SO_UT3,)
                elif kind == FRAG_UP2K:
                    so += (SO_2KU,)
                elif kind == FRAG_DN2K:
                    so += (SO_2KD,)
                if so is None:
                    continue
                uniprot = ""
                achange = ""
                cchange = ""
                coding = NONCODING
                primarytr = genename in self.primary_transcript and tr.split(".")[0] == self.primary_transcript[genename]
                mapping = (uniprot, achange, so, tr, cchange, alen, genename, coding, primarytr)
                if genename not in all_mappings:
                    all_mappings[genename] = []
                all_mappings[genename].append(mapping)
        primary_mapping = self._get_primary_mapping(all_mappings)
        crx_data = {x["name"]: "" for x in cravat.constants.crx_def}
        crx_data.update(crv_data)
        crx_data["hugo"] = primary_mapping[MAPPING_GENENAME_I]
        crx_data["coding"] = "Y" if primary_mapping[MAPPING_CODING_I] == CODING else ""
        crx_data["transcript"] = primary_mapping[MAPPING_TR_I]
        minso = min(primary_mapping[MAPPING_SO_I])
        if minso < 0:
            crx_data["so"] = sonum_to_so[minso]
        else:
            crx_data["so"] = sonum_to_so[max(primary_mapping[MAPPING_SO_I])]
        crx_data["achange"] = primary_mapping[MAPPING_ACHANGE_I]
        crx_data["cchange"] = primary_mapping[MAPPING_CCHANGE_I]
        amd = {}
        for genename in sorted(all_mappings.keys()):
            amd[genename] = []
            for mapping in all_mappings[genename]:
                amd[genename].append(
                    (
                        mapping[MAPPING_UNIPROT_I],
                        mapping[MAPPING_ACHANGE_I],
                        ",".join(
                            sorted([sonum_to_so[v] for v in mapping[MAPPING_SO_I]])
                        ),
                        mapping[MAPPING_TR_I],
                        mapping[MAPPING_CCHANGE_I],
                    )
                )
        crx_data["all_mappings"] = json.dumps(amd)
        return crx_data

    def _get_snv_map_data(
        self,
        tid,
        cpos,
        cstart,
        tpos,
        tstart,
        tr_ref_base,
        tr_alt_base,
        strand,
        kind,
        apos,
        gpos,
        start,
        end,
        chrom,
        fragno,
        lenref,
        lenalt,
        prevcont,
        nextcont,
        exonno,
    ):
        if kind == FRAG_CDS:
            so, ref_aanum, alt_aanum = self._get_svn_cds_so(
                tid, cpos, cstart, tpos, tstart, tr_alt_base, apos
            )
            ref_aa = aanum_to_aa[ref_aanum]
            alt_aa = aanum_to_aa[alt_aanum]
            if ref_aanum == alt_aanum:
                achange = f"p.{ref_aa}{apos}="
            else:
                if apos == 1:
                    so += (SO_MLO,)
                    achange = f"p.{ref_aa}{apos}?"
                else:
                    if ref_aanum != TER:
                        achange = f"p.{ref_aa}{apos}{alt_aa}"
                    else:
                        cpos_codonstart = int((cpos - 1) / 3) * 3 + 1
                        next_stp_apos = self._find_next_stp_apos(
                            tid, cpos_codonstart + 3 - cstart + tstart
                        )
                        if next_stp_apos == NO_NEXT_TER:
                            achange = f"p.{ref_aa}{apos}{alt_aa}ext{aanum_to_aa[TER]}?"
                        else:
                            achange = f"p.{ref_aa}{apos}{alt_aa}ext{aanum_to_aa[TER]}{next_stp_apos}"
            cchange = f"c.{cpos}{tr_ref_base}>{tr_alt_base}"
            coding = CODING
        elif kind == FRAG_UTR5:
            so = (SO_UT5,)
            achange = ""
            cchange = f"c.{cpos}{tr_ref_base}>{tr_alt_base}"
            coding = NONCODING
        elif kind == FRAG_UTR3:
            so = (SO_UT3,)
            achange = ""
            cchange = f"c.*{cpos}{tr_ref_base}>{tr_alt_base}"
            coding = NONCODING
        elif kind & FRAG_FLAG_INTRON == FRAG_FLAG_INTRON:
            coding = NONCODING
            achange = ""
            if gpos == start or gpos == start + 1:
                if (prevcont == 1 and strand == PLUSSTRAND) or (
                    nextcont == 1 and strand == MINUSSTRAND
                ):
                    so = (SO_INT,)
                else:
                    so = (SO_SPL, SO_INT)
                    offset = gpos - start + 1
            elif gpos == end or gpos == end - 1:
                if (nextcont == 1 and strand == PLUSSTRAND) or (
                    prevcont == 1 and strand == MINUSSTRAND
                ):
                    so = (SO_INT,)
                else:
                    so = (SO_SPL, SO_INT)
                    offset = end - gpos + 1
            else:
                so = (SO_INT,)
            if SO_INT in so:
                if prevcont != 0:
                    intron_start = self._get_exon_start(
                        chrom, tid, exonno, kind, strand
                    )
                else:
                    if strand == PLUSSTRAND:
                        intron_start = start
                    else:
                        intron_start = end
                if nextcont != 0:
                    intron_end = self._get_exon_end(chrom, tid, exonno, kind, strand)
                else:
                    if strand == PLUSSTRAND:
                        intron_end = end
                    else:
                        intron_end = start
                midpoint = (intron_start + intron_end) / 2
                if gpos < midpoint:
                    if strand == PLUSSTRAND:
                        diff = gpos - intron_start + 1
                        cchange = f"{cstart}+{diff}{tr_ref_base}>{tr_alt_base}"
                    else:
                        diff = gpos - intron_end + 1
                        cchange = f"{cstart + 1}-{diff}{tr_ref_base}>{tr_alt_base}"
                else:
                    if strand == PLUSSTRAND:
                        diff = intron_end - gpos + 1
                        cchange = f"{cstart + 1}-{diff}{tr_ref_base}>{tr_alt_base}"
                    else:
                        diff = intron_start - gpos + 1
                        cchange = f"{cstart}+{diff}{tr_ref_base}>{tr_alt_base}"
                if kind == FRAG_UTR3INTRON:
                    cchange = "c.*" + cchange
                else:
                    cchange = "c." + cchange
        elif kind == FRAG_NCRNA:
            so = (SO_UNK,)
            achange = ""
            cchange = ""
            coding = NONCODING
        elif kind == FRAG_UP2K:
            so = (SO_2KU,)
            achange = ""
            cchange = f"c.{cpos}{tr_ref_base}>{tr_alt_base}"
            coding = NONCODING
        elif kind == FRAG_DN2K:
            so = (SO_2KD,)
            achange = ""
            cchange = f"c.*{cpos}{tr_ref_base}>{tr_alt_base}"
            coding = NONCODING
        return so, achange, cchange, coding

    def _get_ins_map_data(
        self,
        tid,
        cpos,
        cstart,
        tpos,
        tstart,
        tr_ref_base,
        tr_alt_base,
        strand,
        kind,
        apos,
        gpos,
        start,
        end,
        chrom,
        fragno,
        lenref,
        lenalt,
        prevcont,
        nextcont,
        exonno,
        alen,
        tposcposoffset
    ):
        coding = NONCODING
        achange = ""
        cchange = ""
        cpos_ter_end = alen * 3 + 3
        if kind == FRAG_CDS:
            if cpos == 1 and strand == PLUSSTRAND:
                fragkind = self._get_gpos_fragkind(tid, chrom, gpos - 1)
                if fragkind == FRAG_UTR5:
                    so = (SO_UT5,)
                elif fragkind == FRAG_UP2K:
                    so = (SO_2KU,)
                elif fragkind & FRAG_FLAG_INTRON == FRAG_FLAG_INTRON:
                    so = (SO_UT5,)
                else:
                    so = (SO_NSO,)
            elif cpos == cpos_ter_end and strand == MINUSSTRAND:
                fragkind = self._get_gpos_fragkind(tid, chrom, gpos - 1)
                if fragkind == FRAG_UTR3:
                    so = (SO_UT3,)
                elif fragkind == FRAG_DN2K:
                    so = (SO_2KD,)
                elif fragkind & FRAG_FLAG_INTRON == FRAG_FLAG_INTRON:
                    so = (SO_UT3,)
                else:
                    so = (SO_NSO,)
            else:
                so, achange = self._get_ins_cds_data(
                    tid,
                    cpos,
                    cstart,
                    tpos,
                    tstart,
                    tr_alt_base,
                    chrom,
                    strand,
                    lenalt,
                    apos,
                    gpos,
                    tposcposoffset,
                )
                coding = CODING
        elif kind == FRAG_UTR5:
            so = (SO_UT5,)
        elif kind == FRAG_UTR3:
            so = (SO_UT3,)
        elif kind & FRAG_FLAG_INTRON == FRAG_FLAG_INTRON:
            if gpos == start:
                if (prevcont == 1 and strand == PLUSSTRAND) or (
                    nextcont == 1 and strand == MINUSSTRAND
                ):
                    so = (SO_INT,)
                else:
                    if strand == PLUSSTRAND:
                        q = f"select kind, start, end, tstart, cstart from transcript_frags_{chrom} where tid={tid} and fragno={fragno - 1}"
                        self.c2.execute(q)
                        (kind, start, end, tstart, cstart) = self.c2.fetchone()
                        if kind == FRAG_UTR5:
                            cpos = end - start + cstart
                            tpos = end - start + tstart
                            apos = -1
                            so = (SO_UT5,)
                        elif kind == FRAG_CDS:
                            cpos = end - start + cstart + 1
                            tpos = end - start + tstart + 1
                            apos = int((cpos - 1) / 3) + 1
                            gpos = end + 1
                            so, achange = self._get_ins_cds_data(
                                tid,
                                cpos,
                                cstart,
                                tpos,
                                tstart,
                                tr_alt_base,
                                chrom,
                                strand,
                                lenalt,
                                apos,
                                gpos,
                                tposcposoffset,
                            )
                            coding = CODING
                        elif kind == FRAG_UTR3:
                            cpos = end - start + cstart
                            tpos = end - start + tstart
                            apos = -1
                            so = (SO_UT3,)
                    else:
                        q = f"select kind, start, end, tstart, cstart from transcript_frags_{chrom} where tid={tid} and fragno={fragno + 1}"
                        self.c2.execute(q)
                        (kind, start, end, tstart, cstart) = self.c2.fetchone()
                        if kind == FRAG_UTR5:
                            cpos = cstart
                            tpos = tstart
                            apos = -1
                            so = (SO_UT5,)
                        elif kind == FRAG_CDS:
                            cpos = cstart - 1
                            tpos = tstart - 1
                            apos = int((cpos - 1) / 3) + 1
                            gpos = end + 1
                            so, achange = self._get_ins_cds_data(
                                tid,
                                cpos,
                                cstart,
                                tpos,
                                tstart,
                                tr_alt_base,
                                chrom,
                                strand,
                                lenalt,
                                apos,
                                gpos,
                                tposcposoffset,
                            )
                            coding = CODING
                        elif kind == FRAG_UTR3:
                            cpos = cstart
                            tpos = tstart
                            apos = -1
                            so = (SO_UT3,)
            elif gpos == start + 1:
                if (prevcont == 1 and strand == PLUSSTRAND) or (
                    nextcont == 1 and strand == MINUSSTRAND
                ):
                    so = (SO_INT,)
                else:
                    so = (SO_SPL, SO_INT)
            elif gpos == end:
                if (nextcont == 1 and strand == PLUSSTRAND) or (
                    prevcont == 1 and strand == MINUSSTRAND
                ):
                    so = (SO_INT,)
                else:
                    so = (SO_SPL, SO_INT)
            else:
                so = (SO_INT,)
        elif kind == FRAG_NCRNA:
            so = (SO_UNK,)
        elif kind == FRAG_UP2K:
            so = (SO_2KU,)
        elif kind == FRAG_DN2K:
            so = (SO_2KD,)
        else:
            print(f"@ error. kind={kind:0b}")
        # hgvs c.
        if strand == PLUSSTRAND:
            prev_ref_start = gpos - lenalt
            prev_ref_end = gpos - 1
            prev_ref = self.hg38reader.get_bases(
                chrom, prev_ref_start, prev_ref_end
            ).upper()
            next_ref_start = gpos
            next_ref_end = gpos + lenalt - 1 + lenalt - 1
            next_ref = self.hg38reader.get_bases(
                chrom, next_ref_start, next_ref_end
            ).upper()
        else:
            gpos -= 1
            tpos += 1
            cpos += 1
            prev_ref_start = gpos + lenalt
            prev_ref_end = gpos + 1
            prev_ref = self.hg38reader.get_bases(
                chrom, prev_ref_end, prev_ref_start, strand="-"
            ).upper()
            next_ref_start = gpos
            next_ref_end = gpos - lenalt + 1 - lenalt + 1
            next_ref = self.hg38reader.get_bases(
                chrom, next_ref_end, next_ref_start, strand="-"
            ).upper()
        search_bases = prev_ref + tr_alt_base + next_ref
        dup_found = FALSE
        max_gpos_q_start = None
        for i in range(lenalt * 3):
            scan_frag = search_bases[i : i + lenalt]
            if scan_frag == search_bases[i + lenalt : i + lenalt + lenalt] and (
                i <= lenalt or scan_frag[lenalt - i :] == search_bases[lenalt:i]
            ):
                dup_found = TRUE
                if strand == PLUSSTRAND:
                    gpos_q_start = gpos - lenalt + i
                    if max_gpos_q_start is None or gpos_q_start > max_gpos_q_start:
                        max_gpos_q_start = gpos_q_start
                    while TRUE:
                        gpos_q_f = gpos_q_start + lenalt
                        base_q_f = self.hg38reader.get_bases(
                            chrom, gpos_q_f, gpos_q_f + lenalt - 1
                        ).upper()
                        if base_q_f == scan_frag:
                            gpos_q_start = gpos_q_f
                            if gpos_q_start > max_gpos_q_start:
                                max_gpos_q_start = gpos_q_start
                            gpos_q_f = gpos_q_start + lenalt
                        else:
                            break
                else:
                    gpos_q_start = gpos + lenalt - i
                    if max_gpos_q_start is None or gpos_q_start < max_gpos_q_start:
                        max_gpos_q_start = gpos_q_start
                    while TRUE:
                        gpos_q_f = gpos_q_start - lenalt
                        base_q_f = self.hg38reader.get_bases(
                            chrom, gpos_q_f - lenalt + 1, gpos_q_f, strand=strand
                        ).upper()
                        if base_q_f == scan_frag:
                            gpos_q_start = gpos_q_f
                            if gpos_q_start < max_gpos_q_start:
                                max_gpos_q_start = gpos_q_start
                            gpos_q_f = gpos_q_start - lenalt
                        else:
                            break
        if dup_found:
            if lenalt == 1:
                hgvs_start = self._get_hgvs_cpos(
                    tid,
                    kind,
                    start,
                    end,
                    cstart,
                    max_gpos_q_start,
                    chrom,
                    strand,
                    prevcont,
                    nextcont,
                    exonno,
                )
                cchange = f"c.{hgvs_start}dup"
            else:
                if strand == PLUSSTRAND:
                    hgvs_start = self._get_hgvs_cpos(
                        tid,
                        kind,
                        start,
                        end,
                        cstart,
                        max_gpos_q_start,
                        chrom,
                        strand,
                        prevcont,
                        nextcont,
                        exonno,
                    )
                    hgvs_end = self._get_hgvs_cpos(
                        tid,
                        kind,
                        start,
                        end,
                        cstart,
                        max_gpos_q_start + lenalt - 1,
                        chrom,
                        strand,
                        prevcont,
                        nextcont,
                        exonno,
                    )
                else:
                    hgvs_start = self._get_hgvs_cpos(
                        tid,
                        kind,
                        start,
                        end,
                        cstart,
                        max_gpos_q_start,
                        chrom,
                        strand,
                        prevcont,
                        nextcont,
                        exonno,
                    )
                    hgvs_end = self._get_hgvs_cpos(
                        tid,
                        kind,
                        start,
                        end,
                        cstart,
                        max_gpos_q_start - lenalt + 1,
                        chrom,
                        strand,
                        prevcont,
                        nextcont,
                        exonno,
                    )
                cchange = f"c.{hgvs_start}_{hgvs_end}dup"
        else:
            for i in range(lenalt):
                if tr_alt_base[i] != next_ref[i]:
                    if strand == PLUSSTRAND:
                        gpos = gpos + i
                    else:
                        gpos = gpos - i
                    tr_alt_base = tr_alt_base[i:] + next_ref[:i]
                    break
            if strand == PLUSSTRAND:
                hgvs_start = self._get_hgvs_cpos(
                    tid,
                    kind,
                    start,
                    end,
                    cstart,
                    gpos - 1,
                    chrom,
                    strand,
                    prevcont,
                    nextcont,
                    exonno,
                )
                hgvs_end = self._get_hgvs_cpos(
                    tid,
                    kind,
                    start,
                    end,
                    cstart,
                    gpos,
                    chrom,
                    strand,
                    prevcont,
                    nextcont,
                    exonno,
                )
            else:
                hgvs_start = self._get_hgvs_cpos(
                    tid,
                    kind,
                    start,
                    end,
                    cstart,
                    gpos + 1,
                    chrom,
                    strand,
                    prevcont,
                    nextcont,
                    exonno,
                )
                hgvs_end = self._get_hgvs_cpos(
                    tid,
                    kind,
                    start,
                    end,
                    cstart,
                    gpos,
                    chrom,
                    strand,
                    prevcont,
                    nextcont,
                    exonno,
                )
            cchange = f"c.{hgvs_start}_{hgvs_end}ins{tr_alt_base}"
        return so, achange, cchange, coding

    def _get_del_map_data(
        self,
        tid,
        cpos,
        cstart,
        tpos,
        tstart,
        tr_ref_base,
        tr_alt_base,
        strand,
        kind,
        apos,
        gpos,
        gstart,
        gend,
        chrom,
        gposend,
        fragno,
        lenref,
        lenalt,
        prevcont,
        nextcont,
        alen,
        tlen,
        exonno,
        tr_map_end,
        tposcposoffset,
    ):
        (
            dummy,
            gposend_fragno,
            gposend_gstart,
            gposend_gend,
            gposend_kind,
            gposend_exonno,
            gposend_tstart,
            gposend_cstart,
            dummy,
            gposend_prevcont,
            gposend_nextcont,
        ) = tr_map_end
        if gposend == gpos:
            tpos_end = tpos
            cpos_end = cpos
            apos_end = apos
        else:
            if strand == PLUSSTRAND:
                gposend_gdist = gposend - gposend_gstart
            else:
                gposend_gdist = gposend_gend - gposend
            if gposend_kind == FRAG_CDS:
                tpos_end = gposend_gdist + gposend_tstart
                cpos_end = gposend_gdist + gposend_cstart
                apos_end = int((cpos_end - 1) / 3) + 1
            elif gposend_kind == FRAG_CDSINTRON:
                tpos_end = gposend_tstart
                cpos_end = gposend_cstart
                apos_end = int((cpos_end - 1) / 3) + 1
            elif gposend_kind == FRAG_UTR5 or gposend_kind == FRAG_UTR3:
                tpos_end = gposend_gdist + gposend_tstart
                cpos_end = -1
                apos_end = -1
            elif gposend_kind == FRAG_UP2K or gposend_kind == FRAG_DN2K:
                tpos_end = -1
                cpos_end = -1
                apos_end = -1
            elif gposend_kind == FRAG_UTR5INTRON or gposend_kind == FRAG_UTR3INTRON:
                tpos_end = gposend_tstart
                cpos_end = -1
                apos_end = -1
            elif gposend_kind == FRAG_UP2K or gposend_kind == FRAG_DN2K:
                tpos_end = -1
                cpos_end = -1
                apos_end = -1
            elif gposend_kind == FRAG_FLAG_IG:
                tpos_end = -1
                cpos_end = -1
                apos_end = -1
        coding = NONCODING
        cchange = ""
        achange = ""
        if kind == FRAG_UP2K:
            if gposend_kind == FRAG_UP2K:
                so = (SO_2KU,)
            elif gposend_kind == FRAG_DN2K:  # no transcript
                so = (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3, SO_2KD)
                coding = CODING
            elif gposend_kind == FRAG_UTR5:
                so = (SO_2KU, SO_UT5)
            elif gposend_kind == FRAG_UTR3:  # no transcript
                so = (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3)
                coding = CODING
            elif gposend_kind == FRAG_CDS:  # no transcript
                so = (SO_TAB, SO_2KU, SO_UT5, SO_MLO)
                coding = CODING
            elif gposend_kind == FRAG_NCRNA:
                so = (SO_2KU, SO_UNK)
            elif gposend_kind == FRAG_UTR5INTRON:
                so = (SO_2KU, SO_UT5)
            elif gposend_kind == FRAG_UTR3INTRON:  # no transcript
                so = (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3)
                coding = CODING
            elif gposend_kind == FRAG_CDSINTRON:  # no transcript
                so = (SO_TAB, SO_2KU, SO_UT5, SO_MLO)
                coding = CODING
            elif gposend_kind == FRAG_NCRNAINTRON:
                so = (SO_2KU, SO_UNK)
            elif gposend_kind == FRAG_FLAG_IG:
                if strand == PLUSSTRAND:
                    if gposend > gpos:
                        so = (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3, SO_2KD)
                    else:
                        so = (SO_2KU,)
                else:
                    if gposend < gpos:
                        so = (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3, SO_2KD)
                    else:
                        so = (SO_2KU,)
        elif kind == FRAG_DN2K:
            if gposend_kind == FRAG_UP2K:  # no transcript
                so = (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3, SO_2KD)
                coding = CODING
            elif gposend_kind == FRAG_DN2K:
                so = (SO_2KD,)
            elif gposend_kind == FRAG_UTR5:  # no transcript
                so = (SO_MLO, SO_2KD, SO_UT5)
                coding = CODING
            elif gposend_kind == FRAG_UTR3:
                so = (SO_2KD, SO_UT3)
            elif gposend_kind == FRAG_CDS:
                if apos == alen:
                    so = (SO_STL, SO_UT3, SO_2KU)
                elif apos == 1:
                    so = (SO_MLO, SO_STL, SO_UT3, SO_2KD)
                else:
                    so = (SO_UT3, SO_2KD)
                so = (SO_2KD, SO_STL)
                achange = ""
                coding = CODING
            elif gposend_kind == FRAG_NCRNA:
                so = (SO_2KU, SO_UNK)
            elif gposend_kind == FRAG_UTR5INTRON:
                so = (SO_MLO, SO_2KU, SO_UT5)
                coding = CODING
            elif gposend_kind == FRAG_UTR3INTRON:
                so = (SO_2KU, SO_UT3)
            elif gposend_kind == FRAG_CDSINTRON:
                so = (SO_UT3, SO_2KD, SO_INT, SO_STL)
                achange = ""
                coding = CODING
            elif gposend_kind == FRAG_NCRNAINTRON:
                so = (SO_2KU, SO_UNK)
            elif gposend_kind == FRAG_FLAG_IG:
                if strand == PLUSSTRAND:
                    if gposend > gpos:
                        so = (SO_2KD,)
                    else:
                        so = (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3, SO_2KD)
                else:
                    if gposend < gpos:
                        so = (SO_2KD,)
                    else:
                        so = (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3, SO_2KD)
        elif kind == FRAG_UTR5:
            if gposend_kind == FRAG_UP2K:
                so = (SO_2KU, SO_UT5)
            elif gposend_kind == FRAG_DN2K:
                so = (SO_MLO, SO_UT5, SO_2KD)
                coding = CODING
            elif gposend_kind == FRAG_UTR5:
                so = (SO_UT5,)
            elif gposend_kind == FRAG_UTR3:
                so = (SO_MLO, SO_UT5, SO_UT3)
                coding = CODING
            elif gposend_kind == FRAG_CDS:
                so = (SO_UT5,)
                so_addl, achange = self._get_del_utr5_cds_data(
                    chrom, gpos, gposend, cpos_end, apos_end, strand
                )
                so = so + so_addl
                coding = CODING
            elif gposend_kind == FRAG_NCRNA:
                so = (SO_UT5, SO_UNK)
            elif gposend_kind == FRAG_UTR5INTRON:
                so = (SO_UT5,)
            elif gposend_kind == FRAG_UTR3INTRON:
                so = (SO_MLO, SO_UT5, SO_UT3)
                coding = CODING
            elif gposend_kind == FRAG_CDSINTRON:
                so = (SO_MLO, SO_UT5, SO_INT)
                achange = ""
                coding = CODING
            elif gposend_kind == FRAG_NCRNAINTRON:
                so = (SO_UT5, SO_UNK)
            elif gposend_kind == FRAG_FLAG_IG:
                if strand == PLUSSTRAND:
                    if gposend > gpos:
                        so = (SO_UT5, SO_MLO, SO_STL, SO_UT3, SO_2KD)
                    else:
                        so = (SO_2KU, SO_UT5)
                else:
                    if gposend < gpos:
                        so = (SO_UT5, SO_MLO, SO_STL, SO_UT3, SO_2KD)
                    else:
                        so = (SO_2KU, SO_UT5)
        elif kind == FRAG_UTR3:
            if gposend_kind == FRAG_UP2K:
                so = (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3)
                coding = CODING
            elif gposend_kind == FRAG_DN2K:
                so = (SO_UT3, SO_2KD)
            elif gposend_kind == FRAG_UTR5:
                so = (SO_MLO, SO_UT5, SO_UT3)
                coding = CODING
            elif gposend_kind == FRAG_UTR3:
                so = (SO_UT3,)
            elif gposend_kind == FRAG_CDS:
                so = (SO_UT3, SO_STL)
                achange = ""
                coding = CODING
            elif gposend_kind == FRAG_NCRNA:
                so = (SO_UT3, SO_UNK)
            elif gposend_kind == FRAG_UTR5INTRON:
                so = (SO_MLO, SO_UT5, SO_UT3)
                coding = CODING
            elif gposend_kind == FRAG_UTR3INTRON:
                so = (SO_UT3,)
            elif gposend_kind == FRAG_CDSINTRON:
                so = (SO_STL, SO_UT3, SO_INT)
                achange = ""
                coding = CODING
            elif gposend_kind == FRAG_NCRNAINTRON:
                so = (SO_UT3, SO_UNK)
            elif gposend_kind == FRAG_FLAG_IG:
                if strand == PLUSSTRAND:
                    if gposend > gpos:
                        so = (SO_UT3, SO_2KD)
                    else:
                        so = (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3)
                else:
                    if gposend < gpos:
                        so = (SO_UT3, SO_2KD)
                    else:
                        so = (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3)
        elif kind == FRAG_CDS:
            if gposend_kind == FRAG_UP2K:
                so = (SO_TAB, SO_2KU, SO_UT5, SO_MLO)
                coding = CODING
            elif gposend_kind == FRAG_DN2K:
                so = (SO_STL, SO_2KD)
                achange = ""
                coding = CODING
            elif gposend_kind == FRAG_UTR5:
                so = (SO_MLO, SO_UT5)
                coding = CODING
            elif gposend_kind == FRAG_UTR3:
                so, achange = self._get_del_cds_utr3_data(
                    cpos, tpos, tid, tpos_end, apos, tlen, lenref, tstart, cstart, alen
                )
                coding = CODING
            elif gposend_kind == FRAG_CDS:
                so, achange = self._get_del_cds_cds_data(
                    tid,
                    cpos,
                    cstart,
                    tpos,
                    tstart,
                    chrom,
                    strand,
                    lenalt,
                    apos,
                    lenref,
                    alen,
                    cpos_end,
                    tpos_end,
                    tlen,
                )
                coding = CODING
            elif gposend_kind == FRAG_NCRNA:
                so = (SO_UNK,)
                coding = CODING
            elif gposend_kind == FRAG_UTR5INTRON:
                so = (SO_MLO, SO_UT5)
                coding = CODING
            elif gposend_kind == FRAG_UTR3INTRON:
                so = (SO_STL, SO_UT3)
                achange = ""
                coding = CODING
            elif gposend_kind == FRAG_CDSINTRON:
                so = (SO_INT,)
                so_addl, achange = self._get_del_cds_cdsintron_data(
                    chrom,
                    tid,
                    strand,
                    gpos,
                    cpos,
                    tpos,
                    apos,
                    cstart,
                    tstart,
                    prevcont,
                    nextcont,
                    gposend_prevcont,
                    gposend_nextcont,
                    exonno,
                    gposend_exonno,
                    gstart,
                    gend,
                    gposend_gstart,
                    gposend_gend,
                    gposend,
                    tposcposoffset,
                    alen,
                    kind,
                )
                so += so_addl
                coding = CODING
            elif gposend_kind == FRAG_NCRNAINTRON:
                so = (SO_UNK,)
                coding = CODING
            elif gposend_kind == FRAG_FLAG_IG:
                if strand == PLUSSTRAND:
                    if gposend > gpos:
                        so = (SO_STL, SO_UT3, SO_2KD)
                    else:
                        so = (SO_TAB, SO_2KU, SO_UT5, SO_MLO)
                else:
                    if gposend < gpos:
                        so = (SO_STL, SO_UT3, SO_2KD)
                    else:
                        so = (SO_TAB, SO_2KU, SO_UT5, SO_MLO)
        elif kind == FRAG_NCRNA:
            so = (SO_UNK,)
        elif kind == FRAG_UTR5INTRON:
            if gposend_kind == FRAG_UP2K:
                so = (SO_UT5, SO_2KU)
            elif gposend_kind == FRAG_DN2K:
                so = (SO_MLO,)
                coding = CODING
            elif gposend_kind == FRAG_UTR5:
                so = (SO_UT5,)
            elif gposend_kind == FRAG_UTR3:
                so = (SO_MLO, SO_UT5, SO_UT3)
                coding = CODING
            elif gposend_kind == FRAG_CDS:
                so = (SO_MLO, SO_UT5)
                coding = CODING
            elif gposend_kind == FRAG_NCRNA:
                so = (SO_UNK,)
            elif gposend_kind == FRAG_UTR5INTRON:
                so = (SO_UT5,)
            elif gposend_kind == FRAG_UTR3INTRON:
                so = (SO_MLO,)
                coding = CODING
            elif gposend_kind == FRAG_CDSINTRON:
                so = (SO_MLO, SO_INT)
                achange = ""
                coding = CODING
            elif gposend_kind == FRAG_NCRNAINTRON:
                so = (SO_UNK,)
            elif gposend_kind == FRAG_FLAG_IG:
                if strand == PLUSSTRAND:
                    if gposend > gpos:
                        so = (SO_UT5, SO_MLO, SO_STL, SO_UT3, SO_2KD)
                    else:
                        so = (SO_2KU, SO_UT5)
                else:
                    if gposend < gpos:
                        so = (SO_UT5, SO_MLO, SO_STL, SO_UT3, SO_2KD)
                    else:
                        so = (SO_2KU, SO_UT5)
        elif kind == FRAG_UTR3INTRON:
            if gposend_kind == FRAG_UP2K:
                so = (SO_UT5, SO_2KU)
            elif gposend_kind == FRAG_DN2K:
                so = (SO_MLO,)
                coding = CODING
            elif gposend_kind == FRAG_UTR5:
                so = (SO_MLO, SO_UT5, SO_UT3)
                coding = CODING
            elif gposend_kind == FRAG_UTR3:
                so = (SO_UT3,)
            elif gposend_kind == FRAG_CDS:
                so = (SO_MLO, SO_UT5)
                coding = CODING
            elif gposend_kind == FRAG_NCRNA:
                so = (SO_UNK,)
            elif gposend_kind == FRAG_UTR5INTRON:
                so = (SO_MLO, SO_UT5, SO_UT3)
                coding = CODING
            elif gposend_kind == FRAG_UTR3INTRON:
                so = (SO_UT3,)
            elif gposend_kind == FRAG_CDSINTRON:
                so = (SO_STL, SO_INT)
                achange = ""
                coding = CODING
            elif gposend_kind == FRAG_NCRNAINTRON:
                so = (SO_UNK,)
            elif gposend_kind == FRAG_FLAG_IG:
                if strand == PLUSSTRAND:
                    if gposend > gpos:
                        so = (SO_UT3, SO_2KD)
                    else:
                        so = (SO_TAB, SO_UT5, SO_MLO, SO_STL, SO_UT3)
                else:
                    if gposend < gpos:
                        so = (SO_UT3, SO_2KD)
                    else:
                        so = (SO_TAB, SO_UT5, SO_MLO, SO_STL, SO_UT3)
        elif kind == FRAG_CDSINTRON:
            if gposend_kind == FRAG_UP2K:
                so = (SO_MLO, SO_UT5, SO_2KU)
                coding = CODING
            elif gposend_kind == FRAG_DN2K:
                so = (SO_STL, SO_UT3, SO_2KD)
                coding = CODING
            elif gposend_kind == FRAG_UTR5:
                so = (
                    SO_MLO,
                    SO_UT5,
                )
                coding = CODING
            elif gposend_kind == FRAG_UTR3:
                so = (SO_STL, SO_UT3)
                coding = CODING
            elif gposend_kind == FRAG_CDS:
                so, achange = self._get_del_cdsintron_cds_data(
                    tid,
                    cpos,
                    cstart,
                    tpos,
                    tstart,
                    chrom,
                    strand,
                    lenalt,
                    apos,
                    gpos,
                    lenref,
                    alen,
                    gposend_kind,
                    gposend_fragno,
                    gposend_cstart,
                    gposend_tstart,
                    gposend,
                    cpos_end,
                    tpos_end,
                    tlen,
                    fragno,
                    apos_end,
                    gstart,
                    gend,
                    gposend_gstart,
                    gposend_gend,
                    exonno,
                    gposend_exonno,
                )
                coding = CODING
            elif gposend_kind == FRAG_NCRNA:
                so = (SO_UNK,)
            elif gposend_kind == FRAG_UTR5INTRON:
                so = (
                    SO_MLO,
                    SO_UT5,
                )
                coding = CODING
            elif gposend_kind == FRAG_UTR3INTRON:
                so = (SO_STL, SO_UT3)
            elif gposend_kind == FRAG_CDSINTRON:
                so, achange = self._get_del_cdsintron_cdsintron_data(
                    tid,
                    cpos,
                    cstart,
                    tpos,
                    tstart,
                    tr_alt_base,
                    chrom,
                    strand,
                    lenalt,
                    apos,
                    gpos,
                    lenref,
                    alen,
                    gposend_kind,
                    gposend_fragno,
                    gposend_cstart,
                    gposend_tstart,
                    gposend,
                    cpos_end,
                    tpos_end,
                    tlen,
                    fragno,
                    apos_end,
                    gstart,
                    gend,
                    gposend_gstart,
                    gposend_gend,
                    exonno,
                    gposend_exonno,
                )
                if (
                    (SO_EXL in so)
                    or (SO_SPL in so)
                    or (SO_IND in so)
                    or (SO_FSD in so)
                    or (SO_MLO in so)
                ):
                    coding = CODING
            elif gposend_kind == FRAG_NCRNAINTRON:
                so = (SO_UNK,)
            elif gposend_kind == FRAG_FLAG_IG:
                if strand == PLUSSTRAND:
                    if gposend > gpos:
                        so = (SO_STL, SO_UT3, SO_2KD)
                    else:
                        so = (SO_2KU, SO_UT5, SO_MLO)
                else:
                    if gposend < gpos:
                        so = (SO_STL, SO_UT3, SO_2KD)
                    else:
                        so = (SO_2KU, SO_UT5, SO_MLO)
        elif kind == FRAG_NCRNAINTRON:
            if gposend_kind == FRAG_UP2K:
                so = (SO_2KU, SO_UNK)
            elif gposend_kind == FRAG_DN2K:
                so = (SO_2KD, SO_UNK)
            elif gposend_kind == FRAG_UTR5:
                so = (SO_UT5, SO_UNK)
            elif gposend_kind == FRAG_UTR3:
                so = (SO_UT3, SO_UNK)
            elif gposend_kind == FRAG_CDS:
                so = (SO_UNK,)
            elif gposend_kind == FRAG_NCRNA:
                so = (SO_UNK,)
            elif gposend_kind == FRAG_UTR5INTRON:
                so = (SO_UT5, SO_UNK)
            elif gposend_kind == FRAG_UTR3INTRON:
                so = (SO_UT3, SO_UNK)
            elif gposend_kind == FRAG_CDSINTRON:
                so = (SO_UNK,)
            elif gposend_kind == FRAG_NCRNAINTRON:
                so = (SO_UNK,)
            elif gposend_kind == FRAG_FLAG_IG:
                so = (SO_UNK,)
        elif kind == FRAG_FLAG_IG:
            if gposend_kind == FRAG_UP2K:
                if strand == PLUSSTRAND:
                    if gposend > gpos:
                        so = (SO_2KU,)
                    else:
                        so = (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3, SO_2KD)
                else:
                    if gposend < gpos:
                        so = (SO_2KU,)
                    else:
                        so = (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3, SO_2KD)
            elif gposend_kind == FRAG_DN2K:
                if strand == PLUSSTRAND:
                    if gposend > gpos:
                        so = (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3, SO_2KD)
                    else:
                        so = (SO_2KD,)
                else:
                    if gposend < gpos:
                        so = (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3, SO_2KD)
                    else:
                        so = (SO_2KD,)
            elif gposend_kind == FRAG_UTR5:
                if strand == PLUSSTRAND:
                    if gposend > gpos:
                        so = (SO_UT5, SO_2KU)
                    else:
                        so = (SO_MLO, SO_UT5, SO_UT3, SO_2KD)
                else:
                    if gposend < gpos:
                        so = (SO_UT5, SO_2KU)
                    else:
                        so = (SO_MLO, SO_UT5, SO_UT3, SO_2KD)
            elif gposend_kind == FRAG_UTR3:
                if strand == PLUSSTRAND:
                    if gposend > gpos:
                        so = (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3)
                    else:
                        so = (SO_UT3, SO_2KD)
                else:
                    if gposend < gpos:
                        so = (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3)
                    else:
                        so = (SO_UT3, SO_2KD)
            elif gposend_kind == FRAG_CDS:
                if strand == PLUSSTRAND:
                    if gposend > gpos:
                        so = (SO_2KU, SO_UT5, SO_MLO)
                    else:
                        so = (SO_STL, SO_UT3, SO_2KD)
                else:
                    if gposend < gpos:
                        so = (SO_2KU, SO_UT5, SO_MLO)
                    else:
                        so = (SO_STL, SO_UT3, SO_2KD)
            elif gposend_kind == FRAG_NCRNA:
                if strand == PLUSSTRAND:
                    if gposend > gpos:
                        so = (SO_TAB, SO_UNK)
                    else:
                        so = (SO_UNK,)
                else:
                    if gposend < gpos:
                        so = (SO_TAB, SO_UNK)
                    else:
                        so = (SO_UNK,)
            elif gposend_kind == FRAG_UTR5INTRON:
                if strand == PLUSSTRAND:
                    if gposend > gpos:
                        so = (SO_TAB, SO_2KU, SO_UT5)
                    else:
                        so = (SO_UT5, SO_MLO, SO_STL, SO_UT3, SO_2KD)
                else:
                    if gposend < gpos:
                        so = (SO_TAB, SO_2KU, SO_UT5)
                    else:
                        so = (SO_UT5, SO_MLO, SO_STL, SO_UT3, SO_2KD)
            elif gposend_kind == FRAG_UTR3INTRON:
                if strand == PLUSSTRAND:
                    if gposend > gpos:
                        so = (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3)
                    else:
                        so = (SO_UT3, SO_2KD)
                else:
                    if gposend < gpos:
                        so = (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3)
                    else:
                        so = (SO_UT3, SO_2KD)
            elif gposend_kind == FRAG_CDSINTRON:
                if strand == PLUSSTRAND:
                    if gposend > gpos:
                        #TODO: MLO should be separately determined.
                        so = (SO_TAB, SO_2KU, SO_UT5)
                    else:
                        #TODO: MLO should be separately determined.
                        so = (SO_STL, SO_UT3, SO_2KD)
                else:
                    if gposend < gpos:
                        #TODO: MLO should be separately determined.
                        so = (SO_TAB, SO_2KU, SO_UT5)
                    else:
                        #TODO: MLO should be separately determined.
                        so = (SO_STL, SO_UT3, SO_2KD)
            elif gposend_kind == FRAG_NCRNAINTRON:
                if strand == PLUSSTRAND:
                    if gposend > gpos:
                        so = (SO_TAB, SO_2KU, SO_UT5, SO_UNK)
                    else:
                        so = (SO_UNK,)
                else:
                    if gposend < gpos:
                        so = (SO_TAB, SO_2KU, SO_UT5, SO_UNK)
                    else:
                        so = (SO_UNK,)
            elif gposend_kind == FRAG_FLAG_IG:
                #TODO: whole gene deletion should be separately determined.
                so = (SO_NSO,)
        # hgvs c.
        if kind == FRAG_CDS and gposend_kind == FRAG_CDS:
            _get_bases_tpos = self._get_bases_tpos
            tpos_diff_start = None
            exon_tend = gend - gstart + tstart
            dup_found = FALSE
            tpos_q = tpos_end + 1
            tpos_q_start = tpos_end + 1
            tpos_q_until = exon_tend
            if tpos_q_start < tpos_q_until:
                for tpos_q in range(tpos_q_start, tpos_q_until):
                    early_base = _get_bases_tpos(tid, tpos_q - lenref).upper()
                    late_base = _get_bases_tpos(tid, tpos_q).upper()
                    if early_base != late_base:
                        tpos_diff_start = tpos_q
                        dup_found = TRUE
                        break
                if dup_found == FALSE:
                    tpos_diff_start = exon_tend - lenref + 1
            else:
                tpos_diff_start = tpos_end + 1
            cpos_diff_start = tpos_diff_start - tposcposoffset - lenref
            if gpos == gposend:
                cchange = f"c.{cpos_diff_start}del"
            else:
                cpos_ter_end = alen * 3 + 3
                if cpos_diff_start > cpos_ter_end:
                    hgvs_start = f"{aanum_to_aa[TER]}{cpos_diff_start - cpos_ter_end}"
                else:
                    hgvs_start = f"{cpos_diff_start}"
                cpos_diff_end = cpos_diff_start + lenref - 1
                if cpos_diff_end > cpos_ter_end:
                    hgvs_end = f"{aanum_to_aa[TER]}{cpos_diff_end - cpos_ter_end}"
                else:
                    hgvs_end = f"{cpos_diff_end}"
                cchange = f"c.{hgvs_start}_{hgvs_end}del"
        else:
            get_bases = self.hg38reader.get_bases
            _get_hgvs_cpos = self._get_hgvs_cpos
            if strand == PLUSSTRAND:
                gpos_q = gposend + 1
                gpos_diff_start = None
                while TRUE:
                    late_base = get_bases(chrom, gpos_q).upper()
                    early_base = get_bases(chrom, gpos_q - lenref).upper()
                    if early_base != late_base:
                        gpos_diff_start = gpos_q - lenref
                        break
                    else:
                        gpos_q += 1
                hgvs_start = _get_hgvs_cpos(
                    tid,
                    kind,
                    gstart,
                    gend,
                    cstart,
                    gpos_diff_start,
                    chrom,
                    strand,
                    prevcont,
                    nextcont,
                    exonno,
                )
                if gpos == gposend:
                    cchange = f"c.{hgvs_start}del"
                else:
                    hgvs_end = _get_hgvs_cpos(
                        tid,
                        gposend_kind,
                        gposend_gstart,
                        gposend_gend,
                        gposend_cstart,
                        gpos_diff_start + lenref - 1,
                        chrom,
                        strand,
                        gposend_prevcont,
                        gposend_nextcont,
                        gposend_exonno,
                    )
                    cchange = f"c.{hgvs_start}_{hgvs_end}del"
            else:
                gpos_q = gposend - 1
                gpos_diff_start = None
                while TRUE:
                    late_base = get_bases(chrom, gpos_q).upper()
                    early_base = get_bases(chrom, gpos_q + lenref).upper()
                    if early_base != late_base:
                        gpos_diff_start = gpos_q + lenref
                        break
                    else:
                        gpos_q -= 1
                hgvs_start = _get_hgvs_cpos(
                    tid,
                    kind,
                    gstart,
                    gend,
                    cstart,
                    gpos_diff_start,
                    chrom,
                    strand,
                    prevcont,
                    nextcont,
                    exonno,
                )
                if gpos == gposend:
                    cchange = f"c.{hgvs_start}del"
                else:
                    hgvs_end = _get_hgvs_cpos(
                        tid,
                        kind,
                        gstart,
                        gend,
                        cstart,
                        gpos_diff_start - lenref + 1,
                        chrom,
                        strand,
                        prevcont,
                        nextcont,
                        exonno,
                    )
                    cchange = f"c.{hgvs_start}_{hgvs_end}del"
        return so, achange, cchange, coding

    def _get_com_map_data(
        self,
        tid,
        cpos,
        cstart,
        tpos,
        tstart,
        tr_ref_base,
        tr_alt_base,
        strand,
        kind,
        apos,
        gpos,
        gstart,
        gend,
        chrom,
        gposend,
        fragno,
        lenref,
        lenalt,
        prevcont,
        nextcont,
        alen,
        tlen,
        exonno,
        tr_map_end,
        tposcposoffset,
        tr_alt_base_plus,
        tr_alt_base_minus,
        var_type,
    ):
        (
            dummy,
            gposend_fragno,
            gposend_gstart,
            gposend_gend,
            gposend_kind,
            gposend_exonno,
            gposend_tstart,
            gposend_cstart,
            dummy,
            gposend_prevcont,
            gposend_nextcont,
        ) = tr_map_end
        if gposend == gpos:
            tpos_end = tpos
            cpos_end = cpos
            apos_end = apos
        else:
            if strand == PLUSSTRAND:
                gposend_gdist = gposend - gposend_gstart
            else:
                gposend_gdist = gposend_gend - gposend
            if gposend_kind == FRAG_CDS:
                tpos_end = gposend_gdist + gposend_tstart
                cpos_end = gposend_gdist + gposend_cstart
                apos_end = int((cpos_end - 1) / 3) + 1
            elif gposend_kind == FRAG_CDSINTRON:
                tpos_end = gposend_tstart
                cpos_end = gposend_cstart
                apos_end = int((cpos_end - 1) / 3) + 1
            elif gposend_kind == FRAG_UTR5 or gposend_kind == FRAG_UTR3:
                tpos_end = gposend_gdist + gposend_tstart
                cpos_end = -1
                apos_end = -1
            elif gposend_kind == FRAG_UP2K or gposend_kind == FRAG_DN2K:
                tpos_end = -1
                cpos_end = -1
                apos_end = -1
            elif gposend_kind == FRAG_UTR5INTRON or gposend_kind == FRAG_UTR3INTRON:
                tpos_end = gposend_tstart
                cpos_end = -1
                apos_end = -1
            elif gposend_kind == FRAG_UP2K or gposend_kind == FRAG_DN2K:
                tpos_end = -1
                cpos_end = -1
                apos_end = -1
            elif gposend_kind == FRAG_FLAG_IG:
                tpos_end = -1
                cpos_end = -1
                apos_end = -1
        coding = NONCODING
        cchange = ""
        achange = ""
        so = ()
        if kind == FRAG_UP2K:
            so += (SO_2KU,)
            if gposend_kind == FRAG_UP2K:
                pass
            elif gposend_kind == FRAG_DN2K:
                so += (SO_TAB, SO_UT5, SO_MLO, SO_STL, SO_UT3, SO_2KD)
                coding = CODING
            elif gposend_kind == FRAG_UTR5:
                #TODO: SO_TAB should be separately determined.
                so += (SO_UT5,)
            elif gposend_kind == FRAG_UTR3:
                so += (SO_TAB, SO_UT5, SO_MLO, SO_STL, SO_UT3)
                coding = CODING
            elif gposend_kind == FRAG_CDS:
                #TODO: SO_MLO should be separately determined.
                so += (SO_TAB, SO_UT5, SO_MLO)
                coding = CODING
            elif gposend_kind == FRAG_NCRNA:
                so += (SO_TAB, SO_UT5, SO_UNK)
            elif gposend_kind == FRAG_UTR5INTRON:
                #TODO: SO_TAB should be separately determined.
                so += (SO_UT5,)
            elif gposend_kind == FRAG_UTR3INTRON:
                so += (SO_TAB, SO_UT5, SO_MLO, SO_STL, SO_UT3)
                coding = CODING
            elif gposend_kind == FRAG_CDSINTRON:
                if (
                    self._check_splice_site(
                        chrom, tid, exonno, kind, gpos, var_type, strand
                    )
                    == TRUE
                ):
                    so += (SO_SPL,)
                    coding = CODING
                else:
                    so += (SO_INT,)
                so += (SO_TAB, SO_UT5, SO_MLO)
                coding = CODING
            elif gposend_kind == FRAG_NCRNAINTRON:
                so += (SO_TAB, SO_UNK)
            elif gposend_kind == FRAG_FLAG_IG:
                if strand == PLUSSTRAND:
                    if gposend > gpos:
                        so += (SO_TAB, SO_UT5, SO_MLO, SO_STL, SO_UT3, SO_2KD)
                        coding = CODING
                    else:
                        so += (SO_2KU,)
                else:
                    if gposend < gpos:
                        so += (SO_TAB, SO_UT5, SO_MLO, SO_STL, SO_UT3, SO_2KD)
                        coding = CODING
                    else:
                        so += (SO_2KU,)
        elif kind == FRAG_DN2K:
            so += (SO_2KD,)
            if gposend_kind == FRAG_UP2K:
                so += (SO_TAB, SO_UT3, SO_STL, SO_MLO, SO_UT5, SO_2KU)
                coding = CODING
            elif gposend_kind == FRAG_DN2K:
                pass
            elif gposend_kind == FRAG_UTR5:
                so += (SO_UT3, SO_STL, SO_MLO, SO_UT5)
                coding = CODING
            elif gposend_kind == FRAG_UTR3:
                so += (SO_UT3,)
            elif gposend_kind == FRAG_CDS:
                so += (SO_UT3, SO_STL)
                coding = CODING
                if apos == 1:
                    so += (SO_MLO,)
            elif gposend_kind == FRAG_NCRNA:
                so += (SO_UNK,)
            elif gposend_kind == FRAG_UTR5INTRON:
                so += (SO_UT3, SO_STL, SO_MLO, SO_UT5)
                coding = CODING
            elif gposend_kind == FRAG_UTR3INTRON:
                so += (SO_UT3,)
            elif gposend_kind == FRAG_CDSINTRON:
                if (
                    self._check_splice_site(
                        chrom, tid, exonno, kind, gpos, var_type, strand
                    )
                    == TRUE
                ):
                    so += (SO_SPL,)
                    coding = CODING
                else:
                    so += (SO_INT,)
                so += (SO_UT3, SO_STL)
                coding = CODING
            elif gposend_kind == FRAG_NCRNAINTRON:
                so += (SO_UNK,)
            elif gposend_kind == FRAG_FLAG_IG:
                if strand == PLUSSTRAND:
                    if gposend > gpos:
                        pass
                    else:
                        so += (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3)
                        coding = CODING
                else:
                    if gposend < gpos:
                        pass
                    else:
                        so += (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3)
                        coding = CODING
        elif kind == FRAG_UTR5:
            so += (SO_UT5,)
            if gposend_kind == FRAG_UP2K:
                so += (SO_2KU,)
            elif gposend_kind == FRAG_DN2K:
                so += (SO_MLO, SO_STL, SO_UT3, SO_2KD)
                coding = CODING
            elif gposend_kind == FRAG_UTR5:
                pass
            elif gposend_kind == FRAG_UTR3:
                so += (SO_MLO, SO_STL, SO_UT3)
                coding = CODING
            elif gposend_kind == FRAG_CDS:
                if apos <= 1 and apos_end >= 1:
                    so += (SO_MLO,)
                if apos <= alen + 1 and apos_end >= alen + 1:
                    so += (SO_STL,)
                coding = CODING
            elif gposend_kind == FRAG_NCRNA:
                so += (SO_UNK,)
            elif gposend_kind == FRAG_UTR5INTRON:
                pass
            elif gposend_kind == FRAG_UTR3INTRON:
                so += (SO_MLO, SO_STL, SO_UT3)
                coding = CODING
            elif gposend_kind == FRAG_CDSINTRON:
                if (
                    self._check_splice_site(
                        chrom, tid, exonno, kind, gpos, var_type, strand
                    )
                    == TRUE
                ):
                    so += (SO_SPL,)
                    coding = CODING
                else:
                    so += (SO_INT,)
                so += (SO_MLO,)
                coding = CODING
            elif gposend_kind == FRAG_NCRNAINTRON:
                so += (SO_UNK,)
            elif gposend_kind == FRAG_FLAG_IG:
                if strand == PLUSSTRAND:
                    if gposend > gpos:
                        so += (SO_MLO, SO_STL, SO_UT3, SO_2KD)
                        coding = CODING
                    else:
                        so += (SO_2KU,)
                else:
                    if gposend < gpos:
                        so += (SO_MLO, SO_STL, SO_UT3, SO_2KD)
                        coding = CODING
                    else:
                        so += (SO_2KU,)
        elif kind == FRAG_UTR3:
            so += (SO_UT3,)
            if gposend_kind == FRAG_UP2K:
                so += (SO_TAB, SO_STL, SO_MLO, SO_UT5, SO_2KU)
                coding = CODING
            elif gposend_kind == FRAG_DN2K:
                so += (SO_2KD,)
            elif gposend_kind == FRAG_UTR5:
                so += (SO_STL, SO_MLO, SO_UT5)
                coding = CODING
            elif gposend_kind == FRAG_UTR3:
                pass
            elif gposend_kind == FRAG_CDS:
                so += (SO_STL,)
                coding = CODING
            elif gposend_kind == FRAG_NCRNA:
                so += (SO_UNK,)
            elif gposend_kind == FRAG_UTR5INTRON:
                so += (SO_STL, SO_MLO, SO_UT5)
                coding = CODING
            elif gposend_kind == FRAG_UTR3INTRON:
                pass
            elif gposend_kind == FRAG_CDSINTRON:
                if (
                    self._check_splice_site(
                        chrom, tid, exonno, kind, gpos, var_type, strand
                    )
                    == TRUE
                ):
                    so += (SO_SPL,)
                    coding = CODING
                else:
                    so += (SO_INT,)
                so += (SO_STL,)
                coding = CODING
            elif gposend_kind == FRAG_NCRNAINTRON:
                so += (SO_UNK,)
            elif gposend_kind == FRAG_FLAG_IG:
                if strand == PLUSSTRAND:
                    if gposend > gpos:
                        so += (SO_2KD,)
                    else:
                        so += (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL)
                        coding = CODING
                else:
                    if gposend < gpos:
                        so += (SO_2KD,)
                    else:
                        so += (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL)
                        coding = CODING
        elif kind == FRAG_CDS:
            coding = CODING
            if gposend_kind == FRAG_UP2K:
                so += (SO_TAB, SO_MLO, SO_UT5, SO_2KU)
            elif gposend_kind == FRAG_DN2K:
                so += (SO_STL, SO_UT3, SO_2KD)
            elif gposend_kind == FRAG_UTR5:
                so += (SO_MLO, SO_UT5)
            elif gposend_kind == FRAG_UTR3:
                so += (SO_STL, SO_UT3)
            elif gposend_kind == FRAG_CDS:
                so, achange = self._get_com_cds_cds_data(
                    tid,
                    tpos,
                    cpos,
                    apos,
                    lenref,
                    lenalt,
                    bytearray(tr_alt_base, "ascii"),
                    tposcposoffset,
                    alen,
                )
            elif gposend_kind == FRAG_NCRNA:
                so += (SO_UNK,)
                coding = NONCODING
            elif gposend_kind == FRAG_UTR5INTRON:
                so += (SO_MLO, SO_UT5)
            elif gposend_kind == FRAG_UTR3INTRON:
                so += (SO_STL, SO_UT3)
            elif gposend_kind == FRAG_CDSINTRON:
                if (
                    self._check_splice_site(
                        chrom, tid, exonno, kind, gpos, var_type, strand
                    )
                    == TRUE
                ):
                    so += (SO_SPL,)
                    coding = CODING
                else:
                    so += (SO_INT,)
            elif gposend_kind == FRAG_NCRNAINTRON:
                so += (SO_UNK,)
                coding = NONCODING
            elif gposend_kind == FRAG_FLAG_IG:
                if strand == PLUSSTRAND:
                    if gposend > gpos:
                        so += (SO_STL, SO_UT3, SO_2KD)
                    else:
                        so += (SO_2KU, SO_UT5, SO_MLO)
                else:
                    if gposend < gpos:
                        so += (SO_STL, SO_UT3, SO_2KD)
                    else:
                        so += (SO_2KU, SO_UT5, SO_MLO)
        elif kind == FRAG_NCRNA:
            so += (SO_UNK,)
        elif kind == FRAG_UTR5INTRON:
            so += (SO_UT5,)
            if gposend_kind == FRAG_UP2K:
                so += (SO_2KU,)
            elif gposend_kind == FRAG_DN2K:
                so += (SO_MLO, SO_STL, SO_UT3, SO_2KD)
                coding = CODING
            elif gposend_kind == FRAG_UTR5:
                pass
            elif gposend_kind == FRAG_UTR3:
                so += (SO_MLO, SO_STL, SO_UT3)
                coding = CODING
            elif gposend_kind == FRAG_CDS:
                so += (SO_MLO,)
                coding = CODING
            elif gposend_kind == FRAG_NCRNA:
                so += (SO_UNK,)
            elif gposend_kind == FRAG_UTR5INTRON:
                pass
            elif gposend_kind == FRAG_UTR3INTRON:
                so += (SO_MLO, SO_STL, SO_UT3)
                coding = CODING
            elif gposend_kind == FRAG_CDSINTRON:
                if (
                    self._check_splice_site(
                        chrom, tid, exonno, kind, gpos, var_type, strand
                    )
                    == TRUE
                ):
                    so += (SO_SPL,)
                    coding = CODING
                else:
                    so += (SO_INT,)
                so += (SO_MLO,)
                coding = CODING
            elif gposend_kind == FRAG_NCRNAINTRON:
                so += (SO_UNK,)
            elif gposend_kind == FRAG_FLAG_IG:
                if strand == PLUSSTRAND:
                    if gposend > gpos:
                        so += (SO_MLO, SO_STL, SO_UT3, SO_2KD)
                        coding = CODING
                    else:
                        so += (SO_2KU,)
                else:
                    if gposend < gpos:
                        so += (SO_MLO, SO_STL, SO_UT3, SO_2KD)
                        coding = CODING
                    else:
                        so += (SO_2KU,)
        elif kind == FRAG_UTR3INTRON:
            so += (SO_UT3,)
            if gposend_kind == FRAG_UP2K:
                so += (SO_STL, SO_MLO, SO_UT5, SO_2KU)
                coding = CODING
            elif gposend_kind == FRAG_DN2K:
                so += (SO_2KD,)
            elif gposend_kind == FRAG_UTR5:
                so += (SO_STL, SO_MLO, SO_UT5)
                coding = CODING
            elif gposend_kind == FRAG_UTR3:
                pass
            elif gposend_kind == FRAG_CDS:
                so += (SO_STL,)
                coding = CODING
            elif gposend_kind == FRAG_NCRNA:
                so += (SO_UNK,)
            elif gposend_kind == FRAG_UTR5INTRON:
                so += (SO_STL, SO_MLO, SO_UT5)
                coding = CODING
            elif gposend_kind == FRAG_UTR3INTRON:
                pass
            elif gposend_kind == FRAG_CDSINTRON:
                if (
                    self._check_splice_site(
                        chrom, tid, exonno, kind, gpos, var_type, strand
                    )
                    == TRUE
                ):
                    so += (SO_SPL,)
                    coding = CODING
                else:
                    so += (SO_INT,)
                so += (SO_STL,)
                coding = CODING
            elif gposend_kind == FRAG_NCRNAINTRON:
                so += (SO_UNK,)
            elif gposend_kind == FRAG_FLAG_IG:
                if strand == PLUSSTRAND:
                    if gposend > gpos:
                        so += (SO_2KD,)
                    else:
                        so += (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL)
                        coding = CODING
                else:
                    if gposend < gpos:
                        so += (SO_2KD,)
                    else:
                        so += (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL)
                        coding = CODING
        elif kind == FRAG_CDSINTRON:
            if (
                self._check_splice_site(
                    chrom, tid, exonno, kind, gpos, var_type, strand
                )
                == TRUE
            ):
                so += (SO_SPL,)
                coding = CODING
            else:
                so += (SO_INT,)
            if gposend_kind == FRAG_UP2K:
                so += (SO_TAB, SO_2KU, SO_UT5, SO_MLO)
                coding = CODING
            elif gposend_kind == FRAG_DN2K:
                so += (SO_STL, SO_UT3, SO_2KD)
                coding = CODING
            elif gposend_kind == FRAG_UTR5:
                #TODO: what if cds - stp - ut3 - 2kd - ig - 2ku - ut5 change?
                so += (SO_MLO, SO_UT5)
                coding = CODING
            elif gposend_kind == FRAG_UTR3:
                so += (SO_STL, SO_UT3)
                coding = CODING
            elif gposend_kind == FRAG_CDS:
                pass
            elif gposend_kind == FRAG_NCRNA:
                so += (SO_UNK,)
                coding = NONCODING
            elif gposend_kind == FRAG_UTR5INTRON:
                so += (SO_MLO, SO_UT5)
                coding = CODING
            elif gposend_kind == FRAG_UTR3INTRON:
                so += (SO_STL, SO_UT3)
                coding = CODING
            elif gposend_kind == FRAG_CDSINTRON:
                if exonno != gposend_exonno:
                    so += (SO_EXL,)
                    coding = CODING
            elif gposend_kind == FRAG_NCRNAINTRON:
                so += (SO_UNK,)
                coding = NONCODING
            elif gposend_kind == FRAG_FLAG_IG:
                if strand == PLUSSTRAND:
                    if gposend > gpos:
                        so += (SO_STL, SO_UT3, SO_2KD)
                        coding = CODING
                    else:
                        so += (SO_2KU, SO_UT5, SO_MLO)
                        coding = CODING
                else:
                    if gposend < gpos:
                        so += (SO_STL, SO_UT3, SO_2KD)
                        coding = CODING
                    else:
                        so += (SO_2KU, SO_UT5, SO_MLO)
                        coding = CODING
        elif kind == FRAG_NCRNAINTRON:
            so += (SO_UNK,)
        elif kind == FRAG_FLAG_IG:
            if gposend_kind == FRAG_UP2K:
                if strand == PLUSSTRAND:
                    if gpos < gposend:
                        so += (SO_2KU,)
                    else:
                        so += (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3, SO_2KD)
                        coding = CODING
                else:
                    if gposend < gpos:
                        so += (SO_2KU,)
                    else:
                        so += (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3, SO_2KD)
                        coding = CODING
            elif gposend_kind == FRAG_DN2K:
                if strand == PLUSSTRAND:
                    if gpos < gposend:
                        so += (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3, SO_2KD)
                        coding = CODING
                    else:
                        so += (SO_2KD,)
                else:
                    if gposend < gpos:
                        so += (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3, SO_2KD)
                        coding = CODING
                    else:
                        so += (SO_2KD,)
            elif gposend_kind == FRAG_UTR5:
                if strand == PLUSSTRAND:
                    if gpos < gposend:
                        so += (SO_2KU, SO_UT5)
                    else:
                        so += (SO_UT5, SO_MLO, SO_STL, SO_UT3, SO_2KD)
                        coding = CODING
                else:
                    if gposend < gpos:
                        so += (SO_2KU, SO_UT5)
                    else:
                        so += (SO_2KD, SO_UT3, SO_STL, SO_MLO, SO_UT5)
                        coding = CODING
            elif gposend_kind == FRAG_UTR3:
                if strand == PLUSSTRAND:
                    if gpos < gposend:
                        so += (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3)
                        coding = CODING
                    else:
                        so += (SO_UT3, SO_2KD)
                else:
                    if gposend < gpos:
                        so += (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3)
                        coding = CODING
                    else:
                        so += (SO_UT3, SO_2KD)
            elif gposend_kind == FRAG_CDS:
                if strand == PLUSSTRAND:
                    if gpos < gposend:
                        so += (SO_2KU, SO_UT5, SO_MLO)
                        coding = CODING
                    else:
                        so += (SO_STL, SO_UT3, SO_2KD)
                        coding = CODING
                else:
                    if gposend < gpos:
                        so += (SO_2KU, SO_UT5, SO_MLO)
                        coding = CODING
                    else:
                        so += (SO_STL, SO_UT3, SO_2KD)
                        coding = CODING
            elif gposend_kind == FRAG_NCRNA:
                if strand == PLUSSTRAND:
                    if gpos < gposend:
                        so += (SO_TAB, SO_2KU, SO_UNK)
                    else:
                        so += (SO_UNK,)
                else:
                    if gposend < gpos:
                        so += (SO_TAB, SO_2KU, SO_UNK)
                    else:
                        so += (SO_UNK,)
            elif gposend_kind == FRAG_UTR5INTRON:
                if strand == PLUSSTRAND:
                    if gpos < gposend:
                        so += (SO_TAB, SO_2KU, SO_UT5)
                        coding = CODING
                    else:
                        so += (SO_UT5, SO_MLO, SO_STL, SO_UT3, SO_2KD)
                        coding = CODING
                else:
                    if gposend < gpos:
                        so += (SO_TAB, SO_2KU, SO_UT5)
                        coding = CODING
                    else:
                        so += (SO_UT5, SO_MLO, SO_STL, SO_UT3, SO_2KD)
                        coding = CODING
            elif gposend_kind == FRAG_UTR3INTRON:
                if strand == PLUSSTRAND:
                    if gpos < gposend:
                        so += (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3)
                        coding = CODING
                    else:
                        so += (SO_UT3, SO_2KD)
                else:
                    if gposend < gpos:
                        so += (SO_TAB, SO_2KU, SO_UT5, SO_MLO, SO_STL, SO_UT3)
                        coding = CODING
                    else:
                        so += (SO_UT3, SO_2KD)
            elif gposend_kind == FRAG_CDSINTRON:
                if (
                    self._check_splice_site(
                        chrom, tid, exonno, kind, gpos, var_type, strand
                    )
                    == TRUE
                ):
                    so += (SO_SPL,)
                    coding = CODING
                else:
                    so += (SO_INT,)
                if strand == PLUSSTRAND:
                    if gpos < gposend:
                        so += (SO_TAB, SO_2KU, SO_UT5, SO_MLO)
                        coding = CODING
                    else:
                        so += (SO_STL, SO_UT3, SO_2KD)
                        coding = CODING
                else:
                    if gposend < gpos:
                        so += (SO_TAB, SO_2KU, SO_UT5, SO_MLO)
                        coding = CODING
                    else:
                        so += (SO_STL, SO_UT3, SO_2KD)
                        coding = CODING
            elif gposend_kind == FRAG_NCRNAINTRON:
                if strand == PLUSSTRAND:
                    if gposend > gpos:
                        so += (SO_TAB, SO_UNK)
                    else:
                        so += (SO_UNK,)
                else:
                    if gposend < gpos:
                        so += (SO_TAB, SO_UNK)
                    else:
                        so += (SO_UNK,)
            elif gposend_kind == FRAG_FLAG_IG:
                so = (SO_NSO,)
        # hgvs c.
        get_bases = self.hg38reader.get_bases
        _get_hgvs_cpos = self._get_hgvs_cpos
        if strand == PLUSSTRAND:
            hgvs_start = _get_hgvs_cpos(
                tid,
                kind,
                gstart,
                gend,
                cstart,
                gpos,
                chrom,
                strand,
                prevcont,
                nextcont,
                exonno,
            )
            if gpos == gposend:
                cchange = f"c.{hgvs_start}delins{tr_alt_base}"
            else:
                hgvs_end = _get_hgvs_cpos(
                    tid,
                    gposend_kind,
                    gposend_gstart,
                    gposend_gend,
                    gposend_cstart,
                    gposend,
                    chrom,
                    strand,
                    gposend_prevcont,
                    gposend_nextcont,
                    gposend_exonno,
                )
                cchange = f"c.{hgvs_start}_{hgvs_end}delins{tr_alt_base}"
        else:
            hgvs_start = _get_hgvs_cpos(
                tid,
                kind,
                gstart,
                gend,
                cstart,
                gpos,
                chrom,
                strand,
                prevcont,
                nextcont,
                exonno,
            )
            if gpos == gposend:
                cchange = f"c.{hgvs_start}delins{tr_alt_base}"
            else:
                hgvs_end = _get_hgvs_cpos(
                    tid,
                    kind,
                    gstart,
                    gend,
                    cstart,
                    gposend,
                    chrom,
                    strand,
                    prevcont,
                    nextcont,
                    exonno,
                )
                cchange = f"c.{hgvs_start}_{hgvs_end}delins{tr_alt_base}"
        return so, achange, cchange, coding

    def _check_splice_site(self, chrom, tid, exonno, kind, gpos, var_type, strand):
        exon_start = self._get_exon_start(chrom, tid, exonno, kind, strand)
        exon_end = self._get_exon_end(chrom, tid, exonno, kind, strand)
        splice = FALSE
        if var_type == INS:
            if strand == PLUSSTRAND and (gpos == exon_start + 1 or gpos == exon_end):
                splice = TRUE
            elif strand == MINUSSTRAND and (gpos == exon_start or gpos == exon_end - 1):
                splice = TRUE
        elif (
            gpos == exon_start
            or gpos == exon_start + 1
            or gpos == exon_end
            or gpos == exon_end - 1
        ):
            splice = TRUE
        return splice

    def _get_exon_start(self, chrom, tid, exonno, kind, strand):
        if strand == PLUSSTRAND:
            q = f"select start from transcript_frags_{chrom} where tid={tid} and exonno={exonno} and kind={kind} and prevcont=0"
        else:
            q = f"select end from transcript_frags_{chrom} where tid={tid} and exonno={exonno} and kind={kind} and prevcont=0"
        self.c2.execute(q)
        return self.c2.fetchone()[0]

    def _get_exon_end(self, chrom, tid, exonno, kind, strand):
        if strand == PLUSSTRAND:
            q = f"select end from transcript_frags_{chrom} where tid={tid} and exonno={exonno} and kind={kind} and nextcont=0"
        else:
            q = f"select start from transcript_frags_{chrom} where tid={tid} and exonno={exonno} and kind={kind} and nextcont=0"
        self.c2.execute(q)
        return self.c2.fetchone()[0]

    @staticmethod
    def _get_new_pseq(mrna, tlen, tposcposoffset, source_pseq):
        source_pseq_len = len(source_pseq)
        max_alen = int(tlen / 3)
        pseq = bytearray(max_alen)
        tpos_q = 0
        ter_found = FALSE
        for tpos_q in range(tposcposoffset, tlen - 2, 3):
            aanum = codon_to_aanum[mrna[tpos_q : tpos_q + 3].decode().upper()]
            apos = int((tpos_q - tposcposoffset) / 3) + 1
            pseq[apos - 1] = aanum
            if apos <= source_pseq_len:
                source_aa = source_pseq[apos - 1]
                if apos < source_pseq_len and source_aa == aanum:
                    continue
            if aanum == TER:
                alen = apos
                pseq = pseq[:alen]
                ter_found = TRUE
                break
        if ter_found == FALSE:
            if 0 in pseq:
                alen = pseq.index(0)
                pseq = pseq[:alen]
            else:
                alen = len(pseq)
        return pseq, alen, ter_found

    def _get_com_cds_cds_data(
        self, tid, tpos, cpos, apos, lendel, lenins, ins_base, tposcposoffset, alen
    ):
        so = (SO_CSS,)
        cpos_end = cpos + lendel - 1
        apos_end = int((cpos_end - 1) / 3) + 1
        lendifrem = abs(lendel - lenins) % 3
        if lendel > lenins:
            if lendifrem == 0:
                so += (SO_IND,)
            else:
                so += (SO_FSD,)
        elif lendel < lenins:
            if lendifrem == 0:
                so += (SO_INI,)
            else:
                so += (SO_FSI,)
        pseq = self.prots[tid]
        if pseq is None:
            achange = ""
            return so, achange
        len_pseq = len(pseq)
        tlen = self.tr_info[tid][TR_INFO_TLEN_I]
        mrna = bytearray(tlen)
        self._fill_full_mrna_seq(tid, mrna)
        mrna_lastcodon_tpos = tposcposoffset + alen * 3
        mrna_lastcodon = mrna[mrna_lastcodon_tpos : mrna_lastcodon_tpos + 3].decode()
        if (
            mrna_lastcodon != "TAA"
            and mrna_lastcodon != "TAG"
            and mrna_lastcodon != "TGA"
        ):
            so = (SO_TO_DISCARD,)
            achange = ""
            return so, achange
        new_mrna = bytearray(tlen - lendel + lenins)
        new_mrna = mrna[: tpos - 1] + ins_base + mrna[tpos + lendel - 1 :]
        new_pseq, len_new_pseq, ter_found = Mapper._get_new_pseq(
            new_mrna, len(new_mrna), tposcposoffset, pseq
        )
        if new_pseq[0] != MET:
            so += (SO_MLO,)
            if MET in new_pseq:
                so += (SO_MRT,)
                new_pseq = new_pseq[new_pseq.index(MET) :]
            else:
                achange = ""
                return so, achange
        apos_ter = alen + 1
        if apos <= apos_ter and apos_end >= apos_ter:
            so += (SO_STL,)
            if TER in new_pseq[apos - 1 : apos_end]:
                so += (SO_STR,)
        pseq_frag = pseq[apos - 1 :]
        new_pseq_frag = new_pseq[apos - 1 :]
        lenpseqfrag = len(pseq_frag)
        lennewpseqfrag = len(new_pseq_frag)
        min_pseq_frag_len = min(lenpseqfrag, lennewpseqfrag)
        apos_n_diff = NO_VALUE
        for i in range(min_pseq_frag_len):
            if pseq_frag[i] != new_pseq_frag[i]:
                apos_n_diff = apos + i
                pseq_frag = pseq_frag[i:]
                new_pseq_frag = new_pseq_frag[i:]
                break
        if apos_n_diff == NO_VALUE:
            pseq_frag = []
            new_pseq_frag = []
        else:
            if lendifrem != 0:  # frameshift
                if TER in new_pseq_frag:
                    n = new_pseq_frag.index(TER) + 1
                else:
                    n = "?"
                if n == 1:
                    achange = f"p.{aanum_to_aa[pseq[apos_n_diff - 1]]}{apos_n_diff}{aanum_to_aa[new_pseq_frag[0]]}"
                else:
                    achange = f"p.{aanum_to_aa[pseq[apos_n_diff - 1]]}{apos_n_diff}{aanum_to_aa[new_pseq_frag[0]]}fs{aanum_to_aa[TER]}{n}"
                return so, achange
            aa1ter = aanum_to_aa1[TER]
            if aanum_to_aa1[new_pseq_frag[0]] == aa1ter:
                if aanum_to_aa1[pseq_frag[0]] == aa1ter:
                    so += (SO_SYN,)
                    achange = f"p.{aanum_to_aa[pseq[apos_n_diff - 1]]}{apos_n_diff}="
                    return so, achange
                else:
                    so += (SO_STG,)
                    achange = f"p.{aanum_to_aa[pseq[apos_n_diff - 1]]}{apos_n_diff}{aanum_to_aa[TER]}"
                    return so, achange
        lenpseqfrag = len(pseq_frag)
        lennewpseqfrag = len(new_pseq_frag)
        min_pseq_frag_len = min(lenpseqfrag, lennewpseqfrag)
        apos_c_diff = NO_VALUE
        for i in range(min_pseq_frag_len):
            sp = -i - 1
            if pseq_frag[sp] != new_pseq_frag[sp]:
                apos_c_diff = apos_n_diff + lenpseqfrag + sp
                pseq_frag = pseq_frag[: lenpseqfrag - i]
                new_pseq_frag = new_pseq_frag[: lennewpseqfrag - i]
                break
        lenpseqfrag = len(pseq_frag)
        lennewpseqfrag = len(new_pseq_frag)
        if apos_c_diff == NO_VALUE:
            if lenpseqfrag > lennewpseqfrag:
                diff = lenpseqfrag - lennewpseqfrag
                apos_c_diff = apos_n_diff + diff - 1
                pseq_frag = pseq_frag[:diff]
                new_pseq_frag = []
            elif lenpseqfrag < lennewpseqfrag:
                diff = lennewpseqfrag - lenpseqfrag
                apos_c_diff = apos_n_diff
                apos_n_diff -= 1
                pseq_frag = []
                new_pseq_frag = new_pseq_frag[:diff]
            else:
                apos_c_diff = apos_n_diff
                pseq_frag = []
                new_pseq_frag = []
        lenpseqfrag = len(pseq_frag)
        lennewpseqfrag = len(new_pseq_frag)
        if apos_n_diff == NO_VALUE:
            so += (SO_SYN,)
            achange = f"p.{aanum_to_aa[pseq[apos - 1]]}{apos}="
        elif apos_n_diff == 1 and apos_c_diff == 1:
            so += (SO_MLO,)
            achange = f"p.{aanum_to_aa[MET]}1?"
        elif apos_n_diff > 1 and apos_c_diff <= alen + 1:  # middle aas
            if lendifrem == 0:  # inframe
                if lenpseqfrag == 1:
                    if lennewpseqfrag == 1:
                        if new_pseq_frag[0] == TER:
                            so += (SO_STG,)
                            achange = f"p.{aanum_to_aa[pseq[apos_n_diff - 1]]}{apos_n_diff}{aanum_to_aa[TER]}"
                        else:
                            so += (SO_MIS,)
                            achange = f"p.{aanum_to_aa[pseq[apos_n_diff - 1]]}{apos_n_diff}{aanum_to_aa[new_pseq_frag[0]]}"
                    elif lennewpseqfrag > 1:
                        if TER in new_pseq_frag:
                            idx = new_pseq_frag.index(TER)
                            so += (SO_STG,)
                            achange = f'p.{aanum_to_aa[pseq_frag[0]]}{apos_n_diff}delins{"".join([aanum_to_aa[aanum] for aanum in new_pseq_frag[:idx + 1]])}'
                        else:
                            achange = f'p.{aanum_to_aa[pseq_frag[0]]}{apos_n_diff}delins{"".join([aanum_to_aa[aanum] for aanum in new_pseq_frag])}'
                    else:
                        achange = f"p.{aanum_to_aa[pseq_frag[0]]}{apos_n_diff}del"
                elif lenpseqfrag > 1:
                    if lennewpseqfrag == 1:
                        if new_pseq_frag[0] == TER:
                            so += (SO_STG,)
                            achange = f"p.{aanum_to_aa[pseq_frag[0]]}{apos_n_diff}_{aanum_to_aa[pseq_frag[-1]]}{apos_c_diff}delins{aanum_to_aa[TER]}"
                        else:
                            so += (SO_MIS,)
                            achange = f"p.{aanum_to_aa[pseq_frag[0]]}{apos_n_diff}_{aanum_to_aa[pseq_frag[-1]]}{apos_c_diff}delins{aanum_to_aa[new_pseq_frag[0]]}"
                    elif lennewpseqfrag > 1:
                        if TER in new_pseq_frag:
                            idx = new_pseq_frag.index(TER)
                            so += (SO_STG,)
                            achange = f'p.{aanum_to_aa[pseq_frag[0]]}{apos_n_diff}_{aanum_to_aa[pseq_frag[-1]]}{apos_c_diff}delins{"".join([aanum_to_aa[aanum] for aanum in new_pseq_frag[:idx + 1]])}'
                        else:
                            achange = f'p.{aanum_to_aa[pseq_frag[0]]}{apos_n_diff}_{aanum_to_aa[pseq_frag[-1]]}{apos_c_diff}delins{"".join([aanum_to_aa[aanum] for aanum in new_pseq_frag])}'
                    else:
                        achange = f"p.{aanum_to_aa[pseq_frag[0]]}{apos_n_diff}_{aanum_to_aa[pseq_frag[-1]]}{apos_c_diff}del"
                else:  # insertion
                    if lennewpseqfrag == 1:
                        alt_aa = aanum_to_aa[new_pseq_frag[0]]
                        prev_ref_aa = aanum_to_aa[pseq[apos_n_diff - 1]]
                        if alt_aa == prev_ref_aa:
                            achange = f"p.{prev_ref_aa}{apos_n_diff}dup"
                        else:
                            achange = f"p.{aanum_to_aa[pseq[apos_n_diff - 1]]}{apos_n_diff}_{prev_ref_aa}{apos_c_diff}ins{alt_aa}"
                    elif lennewpseqfrag > 1:
                        alt_aas = "".join(
                            [aanum_to_aa[aanum] for aanum in new_pseq_frag]
                        )
                        prev_ref_aas = "".join(
                            [
                                aanum_to_aa[aanum]
                                for aanum in pseq[
                                    apos_n_diff - lennewpseqfrag : apos_n_diff
                                ]
                            ]
                        )
                        if alt_aas == prev_ref_aas:
                            achange = f"p.{aanum_to_aa[pseq[apos_n_diff - lennewpseqfrag]]}{apos_n_diff - lennewpseqfrag + 1}_{aanum_to_aa[pseq[apos_n_diff - 1]]}{apos_n_diff}dup"
                        else:
                            achange = f'p.{aanum_to_aa[pseq[apos_n_diff - 1]]}{apos_n_diff}_{aanum_to_aa[pseq[apos_c_diff - 1]]}{apos_c_diff}ins{"".join([aanum_to_aa[aanum] for aanum in new_pseq_frag])}'
                    else:
                        achange = (
                            f"p.{aanum_to_aa[pseq[apos_n_diff - 1]]}{apos_n_diff}="
                        )
            else:  # frameshift
                if lennewpseqfrag == 0 and lenpseqfrag > 0:  # deletion
                    if lenpseqfrag == 1:
                        achange = (
                            f"p.{aanum_to_aa[pseq[apos_n_diff - 1]]}{apos_n_diff}del"
                        )
                    else:
                        achange = f"p.{aanum_to_aa[pseq[apos_n_diff - 1]]}{apos_n_diff}_{aanum_to_aa[pseq[apos_c_diff - 1]]}{apos_c_diff}del"
                else:
                    if lenpseqfrag == 0 or pseq_frag[-1] != TER:  # has TER on new frag
                        n = lennewpseqfrag + 1
                    else:
                        n = "?"
                    achange = f"p.{aanum_to_aa[pseq[apos_n_diff - 1]]}{apos_n_diff}{aanum_to_aa[new_pseq_frag[0]]}fs{aanum_to_aa[TER]}{n}"
        return so, achange

    def _get_del_cds_utr3_data(
        self, cpos, tpos, tid, tpos_end, apos, tlen, lenref, tstart, cstart, alen
    ):
        pseq = memoryview(self.prots[tid])
        _get_bases_tpos = self._get_bases_tpos
        so = (SO_UT3, SO_STL)
        ref_codonpos_start = cpos % 3
        if ref_codonpos_start == 0:
            ref_cpos_start = cpos - 2
            ref_tpos_start = tpos - 2
        elif ref_codonpos_start == 1:
            ref_cpos_start = cpos
            ref_tpos_start = tpos
        elif ref_codonpos_start == 2:
            ref_cpos_start = cpos - 1
            ref_tpos_start = tpos - 1
        ref_codon_start = codonnum_to_codon[self._get_codonnum(tid, ref_tpos_start)]
        ref_aanum_start = codon_to_aanum[ref_codon_start]
        if ref_codonpos_start == 1:
            new_ref_codon = _get_bases_tpos(tid, tpos_end + 1, tpos_end + 3)
            ref_tpos_after_new_codon = tpos_end + 4
            so += (SO_IND,)
        elif ref_codonpos_start == 2:
            new_ref_codon = ref_codon_start[0] + _get_bases_tpos(
                tid, tpos_end + 1, tpos_end + 2
            )
            ref_tpos_after_new_codon = tpos_end + 3
            so += (SO_FSD,)
        elif ref_codonpos_start == 0:
            new_ref_codon = ref_codon_start[:2] + _get_bases_tpos(tid, tpos_end + 1)
            ref_tpos_after_new_codon = tpos_end + 2
            so += (SO_FSD,)
        new_aanum_start = codon_to_aanum[new_ref_codon]
        altered_apos = None
        if ref_aanum_start != new_aanum_start:
            new_aanum = new_aanum_start
            altered_apos = apos
            altered_tpos = ref_tpos_after_new_codon
        elif apos == alen + 1 and new_aanum_start == TER:
            so += (SO_STR,)
        else:
            new_aanum = None
            for tpos_q in range(ref_tpos_after_new_codon, tlen - 2, 3):
                aanum_q = codon_to_aanum[_get_bases_tpos(tid, tpos_q, tpos_q + 2)]
                real_cpos = tpos_q - lenref - tstart + cstart
                apos_q = int((real_cpos - 1) / 3) + 1
                if aanum_q != pseq[apos_q - 1]:
                    new_aanum = aanum_q
                    altered_apos = apos_q
                    altered_tpos = tpos_q
                    break
                else:
                    if aanum_q == TER:
                        break
        if altered_apos is None:
            if SO_STR not in so:
                so += (SO_SYN,)
            ref_aa_start = aanum_to_aa[ref_aanum_start]
            achange = f"p.{ref_aa_start}{apos}="
        else:
            if altered_apos <= 1:
                so += (SO_MLO,)
            elif pseq[altered_apos - 1] is TER and new_aanum == TER:
                so += (SO_STR,)
            elif new_aanum == TER:
                so += (SO_STG,)
            if SO_MLO in so:
                achange = ""
            elif SO_STG in so:
                achange = f"p.{aanum_to_aa[pseq[altered_apos - 1]]}{altered_apos}{aanum_to_aa[new_aanum]}"
            else:
                if SO_IND in so:
                    achange = f"p.{aanum_to_aa[pseq[altered_apos - 1]]}{altered_apos}_{aanum_to_aa[TER]}{alen + 1}del"
                elif SO_FSD in so:
                    achange = f"p.{aanum_to_aa[pseq[altered_apos - 1]]}{altered_apos}{aanum_to_aa[new_aanum]}fs"
                ter_found = FALSE
                apos_nextter = 0
                for tpos_q in range(altered_tpos + lenref - 1, tlen - 2, 3):
                    apos_nextter += 1
                    codon = _get_bases_tpos(tid, tpos_q, tpos_q + 2)
                    aanum = codon_to_aanum[codon]
                    if aanum == TER:
                        achange += f"{aanum_to_aa[TER]}{apos_nextter}"
                        ter_found = TRUE
                        break
                if ter_found == FALSE:
                    achange += f"{aanum_to_aa[TER]}?"
        return so, achange

    def _get_del_cdsintron_cds_data(
        self,
        tid,
        cpos,
        cstart,
        tpos,
        tstart,
        chrom,
        strand,
        lenalt,
        apos,
        gpos,
        lenref,
        alen,
        gposend_kind,
        gposend_fragno,
        gposend_cstart,
        gposend_tstart,
        gposend,
        cpos_end,
        tpos_end,
        tlen,
        fragno,
        apos_end,
        gstart,
        gend,
        gposend_gstart,
        gposend_gend,
        exonno,
        gposend_exonno,
    ):
        so = ()
        if exonno != gposend_exonno - 1:
            so += (SO_EXL,)
        if strand == PLUSSTRAND and gpos == gend - 1:
            if self.hg38reader.get_bases(chrom, gposend + 1, gposend + 2) == "AG":
                if SO_EXL in so:
                    q = f"select tstart, cstart from transcript_frags_{chrom} where tid={tid} and kind={FRAG_CDS} and exonno={exonno + 1}"
                    self.c2.execute(q)
                    (tstart, cstart) = self.c2.fetchone()
                    tpos = tstart
                    cpos = cstart
                else:
                    tpos = gposend_tstart
                    cpos = gposend_cstart
                    tstart = gposend_tstart
                    cstart = gposend_cstart
                    gpos = gposend_gstart
                kind = FRAG_CDS
                gposend_tpos = gposend - gposend_gstart + gposend_tstart
                lenref = gposend_tpos + 2 - tpos + 1
                lenalt = 0
                apos = int((cpos - 1) / 3) + 1
                gposend = gposend + 2
                cpos_end += 2
                tpos_end += 2
                so, achange = self._get_del_cds_cds_data(
                    tid,
                    cpos,
                    cstart,
                    tpos,
                    tstart,
                    chrom,
                    strand,
                    lenalt,
                    apos,
                    lenref,
                    alen,
                    cpos_end,
                    tpos_end,
                    tlen,
                )
            else:
                so += (SO_SPL,)
                achange = ""
        elif strand == PLUSSTRAND and gpos == gend:
            if self.hg38reader.get_bases(chrom, gposend + 1) == "G":
                if SO_EXL in so:
                    q = f"select tstart, cstart from transcript_frags_{chrom} where tid={tid} and kind={FRAG_CDS} and exonno={exonno + 1}"
                    self.c2.execute(q)
                    (tstart, cstart) = self.c2.fetchone()
                    tpos = tstart
                    cpos = cstart
                else:
                    tpos = gposend_tstart
                    cpos = gposend_cstart
                    tstart = gposend_tstart
                    cstart = gposend_cstart
                    gpos = gposend_gstart
                kind = FRAG_CDS
                gposend_tpos = gposend - gposend_gstart + gposend_tstart
                lenref = gposend_tpos + 1 - tpos + 1
                lenalt = 0
                apos = int((cpos - 1) / 3) + 1
                gposend = gposend + 1
                cpos_end += 1
                tpos_end += 1
                so, achange = self._get_del_cds_cds_data(
                    tid,
                    cpos,
                    cstart,
                    tpos,
                    tstart,
                    chrom,
                    strand,
                    lenalt,
                    apos,
                    lenref,
                    alen,
                    cpos_end,
                    tpos_end,
                    tlen,
                )
            else:
                so += (SO_SPL,)
                achange = ""
        elif strand == MINUSSTRAND and gpos == gstart + 1:
            if (
                self.hg38reader.get_bases(
                    chrom, gposend - 2, gposend - 1, strand=strand
                )
                == "AG"
            ):
                if SO_EXL in so:
                    q = f"select tstart, cstart, end from transcript_frags_{chrom} where tid={tid} and kind={FRAG_CDS} and exonno={exonno + 1}"
                    self.c2.execute(q)
                    (tstart, cstart, gpos) = self.c2.fetchone()
                    tpos = tstart
                    cpos = cstart
                else:
                    tpos = tstart + 1
                    cpos = cstart + 1
                    gpos = gstart - 1
                kind = FRAG_CDS
                gposend = gposend - 1
                gposend_tpos = gposend_gend - gposend + gposend_tstart
                lenref = tpos - gposend_tpos + 2 + 1
                lenalt = 0
                apos = int((cpos - 1) / 3) + 1
                cpos_end += 2
                tpos_end += 2
                so, achange = self._get_del_cds_cds_data(
                    tid,
                    cpos,
                    cstart,
                    tpos,
                    tstart,
                    chrom,
                    strand,
                    lenalt,
                    apos,
                    lenref,
                    alen,
                    cpos_end,
                    tpos_end,
                    tlen,
                )
            else:
                so += (SO_SPL,)
                achange = ""
        elif strand == MINUSSTRAND and gpos == gstart:
            if (
                self.hg38reader.get_bases(
                    chrom, gposend - 1, gposend - 1, strand=strand
                )
                == "G"
            ):
                if SO_EXL in so:
                    q = f"select tstart, cstart, end from transcript_frags_{chrom} where tid={tid} and kind={FRAG_CDS} and exonno={exonno + 1}"
                    self.c2.execute(q)
                    (tstart, cstart, gpos) = self.c2.fetchone()
                    tpos = tstart
                    cpos = cstart
                else:
                    tpos = tstart + 1
                    cpos = cstart + 1
                    gpos = gstart - 1
                kind = FRAG_CDS
                gposend = gposend - 1
                gposend_tpos = gposend_gend - gposend + gposend_tstart
                lenref = tpos - gposend_tpos + 1 + 1
                lenalt = 0
                apos = int((cpos - 1) / 3) + 1
                cpos_end += 1
                tpos_end += 1
                so, achange = self._get_del_cds_cds_data(
                    tid,
                    cpos,
                    cstart,
                    tpos,
                    tstart,
                    chrom,
                    strand,
                    lenalt,
                    apos,
                    lenref,
                    alen,
                    cpos_end,
                    tpos_end,
                    tlen,
                )
            else:
                so += (SO_SPL,)
                achange = ""
        elif (
            gpos == gstart
            or gpos == gstart + 1
            or gpos == gend
            or gpos == gend - 1
            or gposend == gposend_gstart
            or gposend == gposend_gstart + 1
            or gposend == gposend_gend
            or gposend == gposend_gend - 1
        ):  # splice
            so += (SO_SPL,)
            achange = ""
        else:
            so += (SO_INT,)
            achange = ""
        return so, achange

    def _get_del_cds_cdsintron_data(
        self,
        chrom,
        tid,
        strand,
        gpos,
        cpos,
        tpos,
        apos,
        cstart,
        tstart,
        prevcont,
        nextcont,
        gposend_prevcont,
        gposend_nextcont,
        exonno,
        gposend_exonno,
        gstart,
        gend,
        gposend_gstart,
        gposend_gend,
        gposend,
        tposcposoffset,
        alen,
        kind,
    ):
        so = ()
        if exonno != gposend_exonno:
            so += (SO_EXL,)
        cpos_codonpos = (cpos - 1) % 3 + 1
        if strand == PLUSSTRAND:
            if nextcont == 0:
                gpos_exon_end = gend
            else:
                gpos_exon_end = self._get_exon_end(chrom, tid, exonno, kind, strand)
            len_cds_del = gpos_exon_end - gpos + 1
            if nextcont == 0:
                gposend_exon_end = gposend_gend
            else:
                gposend_exon_end = self._get_exon_end(
                    chrom, tid, gposend_exonno, kind, strand
                )
            len_intron_ins = gposend_exon_end - gposend
            ins_base = self.hg38reader.get_bases(chrom, gposend + 1, gposend_exon_end)
        else:
            if prevcont == 0:
                gpos_exon_start = gstart
            else:
                gpos_exon_start = self._get_exon_end(chrom, tid, exonno, kind, strand)
            len_cds_del = gpos - gpos_exon_start + 1
            if prevcont == 0:
                gposend_exon_start = gposend_gstart
            else:
                gposend_exon_start = self._get_exon_start(
                    chrom, tid, gposend_exonno, kind, strand
                )
            len_intron_ins = gposend - gposend_exon_start
            ins_base = self.hg38reader.get_bases(
                chrom, gposend_exon_start, gposend - 1, strand=strand
            )
        ins_base = bytearray(ins_base, encoding="ascii")
        so, achange = self._get_com_cds_cds_data(
            tid,
            tpos,
            cpos,
            apos,
            len_cds_del,
            len_intron_ins,
            ins_base,
            tposcposoffset,
            alen,
        )
        return so, achange

    def _get_com_utr5_cds_data(
        self, chrom, gpos, gpos_end, cpos_end, apos_end, strand, tr_alt_base
    ):
        so = (SO_MLO,)
        if apos_end == 1:
            cpos_end_codonpos = (cpos_end - 1) % 3  # 0 to 2
            if cpos_end_codonpos == 0:
                if tr_alt_base[-1] == "A":
                    so += (SO_MRT,)
            elif cpos_end_codonpos == 1:
                len_tr_alt_base = len(tr_alt_base)
                if len_tr_alt_base >= 2:
                    if tr_alt_base[-2:] == "AT":
                        so += (SO_MRT,)
                elif len_tr_alt_base == 1:
                    if tr_alt_base == "T":
                        if strand == PLUSSTRAND:
                            if self.hg38reader.get_bases(chrom, gpos - 1) == "A":
                                so += (SO_MRT,)
                        else:
                            if (
                                self.hg38reader.get_bases(
                                    chrom, gpos_end + 1, gpos_end + 1, strand=strand
                                )
                                == "A"
                            ):
                                so += (SO_MRT,)
            elif cpos_end_codonpos == 2:
                len_tr_alt_base = len(tr_alt_base)
                if len_tr_alt_base >= 3:
                    if tr_alt_base[-3:] == "ATG":
                        so += (SO_MRT,)
                elif len_tr_alt_base == 2:
                    if tr_alt_base == "TG":
                        if strand == PLUSSTRAND:
                            if self.hg38reader.get_bases(chrom, gpos - 1) == "A":
                                so += (SO_MRT,)
                        else:
                            if (
                                self.hg38reader.get_bases(
                                    chrom, gpos_end + 1, gpos_end + 1, strand=strand
                                )
                                == "A"
                            ):
                                so += (SO_MRT,)
                elif len_tr_alt_base == 1:
                    if tr_alt_base == "G":
                        if strand == PLUSSTRAND:
                            if (
                                self.hg38reader.get_bases(chrom, gpos - 2, gpos - 1)
                                == "AT"
                            ):
                                so += (SO_MRT,)
                        else:
                            if (
                                self.hg38reader.get_bases(
                                    chrom, gpos_end + 1, gpos_end + 2, strand=strand
                                )
                                == "AT"
                            ):
                                so += (SO_MRT,)
        achange = ""
        return so, achange

    def _get_del_utr5_cds_data(self, chrom, gpos, gpos_end, cpos_end, apos_end, strand):
        so = (SO_MLO,)
        if apos_end == 1:
            cpos_end_codonpos = (cpos_end - 1) % 3  # 0 to 2
            if cpos_end_codonpos == 0:
                if strand == PLUSSTRAND:
                    if self.hg38reader.get_bases(chrom, gpos - 1) == "A":
                        so += (SO_MRT,)
                else:
                    if self.hg38reader.get_bases(chrom, gpos + 1) == "A":
                        so += (SO_MRT,)
            elif cpos_end_codonpos == 1:
                if strand == PLUSSTRAND:
                    if (
                        self.hg38reader.get_bases(chrom, gpos_end - 2, gpos_end - 1)
                        == "AT"
                    ):
                        so += (SO_MRT,)
                else:
                    if (
                        self.hg38reader.get_bases(
                            chrom, gpos_end + 1, gpos_end + 2, strand=strand
                        )
                        == "AT"
                    ):
                        so += (SO_MRT,)
            elif cpos_end_codonpos == 2:
                if strand == PLUSSTRAND:
                    if (
                        self.hg38reader.get_bases(chrom, gpos_end - 3, gpos_end - 1)
                        == "ATG"
                    ):
                        so += (SO_MRT,)
                else:
                    if (
                        self.hg38reader.get_bases(
                            chrom, gpos_end + 1, gpos_end + 3, strand=strand
                        )
                        == "ATG"
                    ):
                        so += (SO_MRT,)
        achange = ""
        return so, achange

    def _get_del_cdsintron_cdsintron_data(
        self,
        tid,
        cpos,
        cstart,
        tpos,
        tstart,
        tr_alt_base,
        chrom,
        strand,
        lenalt,
        apos,
        gpos,
        lenref,
        alen,
        gposend_kind,
        gposend_fragno,
        gposend_cstart,
        gposend_tstart,
        gposend,
        cpos_end,
        tpos_end,
        tlen,
        fragno,
        apos_end,
        gstart,
        gend,
        gposend_gstart,
        gposend_gend,
        exonno,
        gposend_exonno,
    ):
        so = ()
        if exonno != gposend_exonno:
            so += (SO_EXL,)
        if lenref == 2:
            if strand == PLUSSTRAND and gpos == gend - 1:
                if self.hg38reader.get_bases(chrom, gpos + 2, gpos + 3) == "AG":
                    tpos += 1
                    cpos += 1
                    tstart += 1
                    cstart += 1
                    tr_alt_base = "AG"
                    lenref = 2
                    lenalt = 0
                    apos = int((cpos - 1) / 3) + 1
                    gpos = gpos + 2
                    gposend = gpos + 3
                    gposend_kind = FRAG_CDS
                    gposend_fragno += 1
                    gposend_cstart += 1
                    gposend_tstart += 1
                    cpos_end += 1
                    tpos_end += 1
                    so, achange = self._get_del_cds_cds_data(
                        tid,
                        cpos,
                        cstart,
                        tpos,
                        tstart,
                        chrom,
                        strand,
                        lenalt,
                        apos,
                        lenref,
                        alen,
                        cpos_end,
                        tpos_end,
                        tlen,
                    )
                else:
                    so += (SO_SPL,)
                    achange = ""
            elif strand == MINUSSTRAND and gpos == gstart + 1:
                if (
                    self.hg38reader.get_bases(chrom, gpos - 3, gpos - 2, strand=strand)
                    == "AG"
                ):
                    tpos += 1
                    cpos += 1
                    tstart += 1
                    cstart += 1
                    tr_alt_base = "CT"
                    lenref = 2
                    lenalt = 0
                    apos = int((cpos - 1) / 3) + 1
                    gpos = gpos - 3
                    gposend = gpos - 2
                    gposend_kind = FRAG_CDS
                    gposend_fragno += 1
                    gposend_cstart += 1
                    gposend_tstart += 1
                    cpos_end += 1
                    tpos_end += 1
                    so, achange = self._get_del_cds_cds_data(
                        tid,
                        cpos,
                        cstart,
                        tpos,
                        tstart,
                        chrom,
                        strand,
                        lenalt,
                        apos,
                        lenref,
                        alen,
                        cpos_end,
                        tpos_end,
                        tlen,
                    )
                else:
                    so += (SO_SPL,)
                    achange = ""
            else:
                if (
                    gpos == gstart
                    or gpos == gstart + 1
                    or gpos == gend
                    or gpos == gend - 1
                    or gposend == gposend_gstart
                    or gposend == gposend_gstart + 1
                    or gposend == gposend_gend
                    or gposend == gposend_gend - 1
                ):  # splice
                    so += (SO_SPL,)
                    achange = ""
                else:
                    so += (SO_INT,)
                    achange = ""
        elif lenref == 1:
            if strand == PLUSSTRAND and gpos == gend:
                if self.hg38reader.get_bases(chrom, gpos + 1) == "G":
                    tpos += 1
                    cpos += 1
                    apos = int((cpos - 1) / 3) + 1
                    tstart += 1
                    cstart += 1
                    tr_alt_base = "G"
                    lenref = 1
                    lenalt = 0
                    gpos = gpos + 1
                    gposend = gpos + 1
                    gposend_kind = FRAG_CDS
                    gposend_fragno += 1
                    gposend_cstart += 1
                    gposend_tstart += 1
                    cpos_end += 1
                    tpos_end += 1
                    so, achange = self._get_del_cds_cds_data(
                        tid,
                        cpos,
                        cstart,
                        tpos,
                        tstart,
                        chrom,
                        strand,
                        lenalt,
                        apos,
                        lenref,
                        alen,
                        cpos_end,
                        tpos_end,
                        tlen,
                    )
                else:
                    so += (SO_SPL,)
                    achange = ""
            elif strand == MINUSSTRAND and gpos == gstart:
                if (
                    self.hg38reader.get_bases(chrom, gpos - 1, gpos - 1, strand=strand)
                    == "G"
                ):
                    tpos += 1
                    cpos += 1
                    apos = int((cpos - 1) / 3) + 1
                    tstart += 1
                    cstart += 1
                    tr_alt_base = "C"
                    lenref = 2
                    lenalt = 0
                    gpos = gpos - 1
                    gposend = gpos - 1
                    gposend_kind = FRAG_CDS
                    gposend_fragno += 1
                    gposend_cstart += 1
                    gposend_tstart += 1
                    cpos_end += 1
                    tpos_end += 1
                    so, achange = self._get_del_cds_cds_data(
                        tid,
                        cpos,
                        cstart,
                        tpos,
                        tstart,
                        chrom,
                        strand,
                        lenalt,
                        apos,
                        lenref,
                        alen,
                        cpos_end,
                        tpos_end,
                        tlen,
                    )
                else:
                    so += (SO_SPL,)
                    achange = ""
            else:
                if (
                    gpos == gstart
                    or gpos == gstart + 1
                    or gpos == gend
                    or gpos == gend - 1
                    or gposend == gposend_gstart
                    or gposend == gposend_gstart + 1
                    or gposend == gposend_gend
                    or gposend == gposend_gend - 1
                ):  # splice
                    so += (SO_SPL,)
                    achange = ""
                else:
                    so += (SO_INT,)
                    achange = ""
        else:
            if (
                gpos == gstart
                or gpos == gstart + 1
                or gpos == gend
                or gpos == gend - 1
                or gposend == gposend_gstart
                or gposend == gposend_gstart + 1
                or gposend == gposend_gend
                or gposend == gposend_gend - 1
            ):  # splice
                so += (SO_SPL,)
                achange = ""
            else:
                so += (SO_INT,)
                achange = ""
        if fragno != gposend_fragno and not (
            fragno == gposend_fragno - 1 and gposend_kind == FRAG_CDS
        ):
            cpos_codonpos = int((cstart + 1) % 3)
            cpos_end_codonpos = int((gposend_cstart + 1) % 3)
            del_start_apos = int(cstart / 3 + 1)
            del_end_apos = int((gposend_cstart - 1) / 3 + 1)
            if (
                (cpos_codonpos == 1 and cpos_end_codonpos == 2)
                or (cpos_codonpos == 2 and cpos_end_codonpos == 0)
                or (cpos_codonpos == 0 and cpos_end_codonpos == 1)
            ):
                so = (SO_EXL, SO_IND)
                prev_aanum = codonnum_to_aanum[self._get_codonnum(tid, tstart)]
                if del_start_apos == del_end_apos:
                    achange = f"p.{aanum_to_aa[prev_aanum]}{apos}del"
                else:
                    next_aanum = codonnum_to_aanum[
                        self._get_codonnum(tid, gposend_tstart + 1)
                    ]
                    if cpos_codonpos == 0:  # conservative
                        achange = f"p.{aanum_to_aa[prev_aanum]}{apos}_{aanum_to_aa[next_aanum]}{del_end_apos}del"
                    else:  # disruptive
                        achange = f"p.{aanum_to_aa[prev_aanum]}{apos}_{aanum_to_aa[next_aanum]}{del_end_apos}del"
            else:
                if del_start_apos <= 1 and del_end_apos >= 1:
                    so = (SO_EXL, SO_MLO, SO_FSD)
                else:
                    so = (SO_EXL, SO_FSD)
                aanum = codonnum_to_aanum[self._get_codonnum(tid, tstart)]
                achange = f"p.{aanum_to_aa[aanum]}{apos}fs"
        return so, achange

    def _get_del_cds_cds_data(
        self,
        tid,
        cpos,
        cstart,
        tpos,
        tstart,
        chrom,
        strand,
        lenalt,
        apos,
        lenref,
        alen,
        cpos_end,
        tpos_end,
        tlen,
    ):
        pseq = self.prots[tid]
        _get_codonnum = self._get_codonnum
        if lenref % 3 == 0:  # inframe_deletion
            ref_codonpos = cpos % 3
            if ref_codonpos == 1:  # conservative_inframe_deletion
                apos_end = int((cpos_end - 1) / 3 + 1)
                ref_aanums = pseq[apos - 1 : apos_end]
                ref_aanums_len = apos_end - apos + 1
                postdel_apos_start = apos + ref_aanums_len
                if postdel_apos_start > alen + 1:
                    max_apos_start = apos
                    max_apos_end = alen + 1
                    ref_aanums_start = pseq[max_apos_start - 1]
                    ref_aanums_end = pseq[max_apos_end - 1]
                else:
                    max_apos_start = apos
                    diff_found = False
                    for postdel_apos_q in range(postdel_apos_start, alen + 1):
                        predel_apos_q = postdel_apos_q - ref_aanums_len
                        if pseq[predel_apos_q - 1] != pseq[postdel_apos_q - 1]:
                            max_apos_start = predel_apos_q
                            ref_aanums_start = pseq[max_apos_start - 1]
                            diff_found = True
                            break
                    if not diff_found:
                        max_apos_start = alen - ref_aanums_len + 1
                        ref_aanums_start = pseq[max_apos_start - 1]
                    max_apos_end = max_apos_start + ref_aanums_len - 1
                    ref_aanums_end = pseq[max_apos_end - 1]
                if max_apos_start <= 1 and max_apos_end >= 1:  # MET deletion
                    so = (SO_MLO, SO_IND)
                    if ref_aanums_len == 1:
                        achange = (
                            f"p.{aanum_to_aa[ref_aanums_start]}{max_apos_start}del"
                        )
                    else:
                        achange = f"p.{aanum_to_aa[ref_aanums_start]}{max_apos_start}_{aanum_to_aa[ref_aanums_end]}{max_apos_end}del"
                elif (
                    max_apos_start <= alen + 1 and max_apos_end >= alen + 1
                ):  # TER deletion
                    so = (SO_STL, SO_IND)
                    if ref_aanums_len == 1:
                        achange = f"p.{aanum_to_aa[ref_aanums_start]}{max_apos_start}delext{aanum_to_aa[TER]}"
                    else:
                        achange = f"p.{aanum_to_aa[ref_aanums_start]}{max_apos_start}_{aanum_to_aa[ref_aanums_end]}{max_apos_end}delext{aanum_to_aa[TER]}"
                    ter_found = FALSE
                    max_tpos_end = max_apos_end * 3 - cstart + tstart
                    for tpos_q in range(max_tpos_end + 1, tlen + 1, 3):
                        codonnum = _get_codonnum(tid, tpos_q)
                        if codonnum is None:
                            break
                        aanum = codonnum_to_aanum[codonnum]
                        if aanum == TER:
                            apos_nextter = int((tpos_q - max_tpos_end - 1) / 3) + 1
                            achange += f"{apos_nextter:d}"
                            ter_found = TRUE
                            break
                    if ter_found == FALSE:
                        achange += "?"
                else:  # middle deletion
                    so = (SO_IND,)
                    if ref_aanums_len == 1:
                        achange = (
                            f"p.{aanum_to_aa[ref_aanums_start]}{max_apos_start}del"
                        )
                    else:
                        achange = f"p.{aanum_to_aa[ref_aanums_start]}{max_apos_start}_{aanum_to_aa[ref_aanums_end]}{max_apos_end}del"
            else:  # disruptive_inframe_deletion
                if ref_codonpos == 2:
                    ref_cpos = cpos - 1
                    ref_tpos = tpos - 1
                    num_base_from_start_codon = 1
                elif ref_codonpos == 0:
                    ref_cpos = cpos - 2
                    ref_tpos = tpos - 2
                    num_base_from_start_codon = 2
                ref_codon_start = codonnum_to_codon[_get_codonnum(tid, ref_tpos)]
                ref_aanum_start = codon_to_aanum[ref_codon_start]
                ref_codonpos_end = cpos_end % 3
                if ref_codonpos_end == 2:
                    ref_cpos_end = cpos_end - 1
                    ref_tpos_end = tpos_end - 1
                elif ref_codonpos_end == 1:
                    ref_cpos_end = cpos_end
                    ref_tpos_end = tpos_end
                elif ref_codonpos_end == 0:
                    ref_cpos_end = cpos_end - 2
                    ref_tpos_end = tpos_end - 2
                ref_codon_end = codonnum_to_codon[_get_codonnum(tid, ref_tpos_end)]
                ref_aanum_end = codon_to_aanum[ref_codon_end]
                new_codon = (
                    ref_codon_start[:num_base_from_start_codon]
                    + ref_codon_end[ref_codonpos_end:]
                )
                new_aanum = codon_to_aanum[new_codon]
                if new_aanum == TER:  # new aa starts with TER.
                    if ref_aanum_start == TER:
                        so = (SO_STR, SO_IND)
                        achange = f"p.{aanum_to_aa[TER]}{apos}="
                    else:
                        so = (SO_STG, SO_IND)
                        achange = (
                            f"p.{aanum_to_aa[ref_aanum_start]}{apos}{aanum_to_aa[TER]}"
                        )
                else:
                    if new_aanum != ref_aanum_start and new_aanum != ref_aanum_end:
                        apos_del_end = int((ref_cpos_end - 1) / 3 + 1)
                        if apos == 1:  # MET deletion
                            so = (SO_MLO, SO_IND)
                            achange = f"p.{aanum_to_aa[MET]}1{aanum_to_aa[new_aanum]}"
                        elif (
                            apos <= alen + 1 and apos_del_end >= alen + 1
                        ):  # TER deletion
                            so = (SO_STL, SO_IND)
                            achange = f"p.{aanum_to_aa[codon_to_aanum[ref_codon_start]]}{apos}_{aanum_to_aa[codon_to_aanum[ref_codon_end]]}{apos_del_end}delins{aanum_to_aa[new_aanum]}ext{aanum_to_aa[TER]}"
                            ter_found = FALSE
                            tpos_del_end = apos_del_end * 3 - cstart + tstart
                            for tpos_q in range(tpos_del_end + 1, tlen + 1, 3):
                                codonnum = _get_codonnum(tid, tpos_q)
                                if codonnum is None:
                                    break
                                aanum = codonnum_to_aanum[codonnum]
                                if aanum == TER:
                                    apos_nextter = (tpos_q - tpos_del_end - 1) / 3 + 2
                                    achange += f"{apos_nextter}"
                                    ter_found = TRUE
                            if ter_found == FALSE:
                                achange += "?"
                        else:
                            so = (SO_IND,)
                            achange = f"p.{aanum_to_aa[ref_aanum_start]}{apos}_{aanum_to_aa[ref_aanum_end]}{apos_del_end}delins{aanum_to_aa[new_aanum]}"
                    else:
                        num_aas_del = int(lenref / 3)
                        if new_aanum == ref_aanum_start:
                            if apos + num_aas_del > alen:
                                max_apos_del_start = apos
                            else:
                                for apos_q in range(apos + 1, alen + 1):
                                    predel_aanum = pseq[apos_q - 1]
                                    postdel_aanum = pseq[apos_q + num_aas_del - 1]
                                    if predel_aanum != postdel_aanum:
                                        max_apos_del_start = apos_q
                                        break
                            max_apos_del_end = max_apos_del_start + num_aas_del - 1
                        elif new_aanum == ref_aanum_end:
                            if apos + num_aas_del > alen:
                                max_apos_del_start = apos
                            else:
                                for apos_q in range(apos, alen + 1):
                                    predel_aanum = pseq[apos_q - 1]
                                    postdel_aanum = pseq[apos_q + num_aas_del - 1]
                                    if predel_aanum != postdel_aanum:
                                        max_apos_del_start = apos_q
                                        break
                            max_apos_del_end = max_apos_del_start + num_aas_del - 1
                        if (
                            max_apos_del_start <= 1 and max_apos_del_end >= 1
                        ):  # MET deletion
                            so = (
                                SO_MLO,
                                SO_IND,
                            )
                            ref_aanums_start = pseq[max_apos_del_start - 1]
                            if num_aas_del == 1:
                                achange = f"p.{aanum_to_aa[ref_aanums_start]}{max_apos_del_start}del"
                            else:
                                ref_aanums_end = pseq[max_apos_del_end - 1]
                                achange = f"p.{aanum_to_aa[ref_aanums_end]}{max_apos_del_start}_{aanum_to_aa[ref_aanums_end]}{max_apos_del_end}del"
                        elif (
                            max_apos_del_start <= alen + 1
                            and max_apos_del_end >= alen + 1
                        ):  # TER deletion
                            so = (SO_STL, SO_IND)
                            ref_aanums_start = pseq[max_apos_del_start - 1]
                            if num_aas_del == 1:
                                achange = f"p.{aanum_to_aa[ref_aanums_start]}{max_apos_del_start}delext{aanum_to_aa[TER]}"
                            else:
                                ref_aanums_end = pseq[max_apos_del_end - 1]
                                achange = f"p.{aanum_to_aa[ref_aanums_start]}{max_apos_del_start}_{aanum_to_aa[ref_aanums_end]}{max_apos_del_end}delext{aanum_to_aa[TER]}"
                            ter_found = FALSE
                            max_tpos_del_end = max_apos_del_end * 3 - cstart + tstart
                            for tpos_q in range(max_tpos_del_end + 1, tlen + 1, 3):
                                codonnum = _get_codonnum(tid, tpos_q)
                                aanum = codonnum_to_aanum[codonnum]
                                if aanum == TER:
                                    apos_nextter = (
                                        int((tpos_q - max_tpos_del_end - 1) / 3) + 1
                                    )
                                    achange += f"{apos_nextter}"
                                    ter_found = TRUE
                                    break
                            if ter_found == FALSE:
                                achange += "?"
                        else:  # middle deletion
                            so = (SO_IND,)
                            ref_aanums_start = pseq[max_apos_del_start - 1]
                            ref_aanums_end = pseq[max_apos_del_end - 1]
                            if num_aas_del == 1:
                                achange = f"p.{aanum_to_aa[ref_aanums_start]}{max_apos_del_start}del"
                            else:
                                achange = f"p.{aanum_to_aa[ref_aanums_start]}{max_apos_del_start}_{aanum_to_aa[ref_aanums_end]}{max_apos_del_end}del"
        else:  # frameshift_truncation
            _get_bases_tpos = self._get_bases_tpos
            ref_codonpos_start = cpos % 3
            if ref_codonpos_start == 0:
                ref_cpos_start = cpos - 2
                ref_tpos_start = tpos - 2
            elif ref_codonpos_start == 1:
                ref_cpos_start = cpos
                ref_tpos_start = tpos
            elif ref_codonpos_start == 2:
                ref_cpos_start = cpos - 1
                ref_tpos_start = tpos - 1
            ref_codon_start = codonnum_to_codon[self._get_codonnum(tid, ref_tpos_start)]
            ref_aanum_start = codon_to_aanum[ref_codon_start]
            ref_codonpos_end = cpos_end % 3
            if ref_codonpos_end == 0:
                ref_cpos_end = cpos_end - 2
                ref_tpos_end = tpos_end - 2
            elif ref_codonpos_end == 1:
                ref_cpos_end = cpos_end
                ref_tpos_end = tpos_end
            elif ref_codonpos_end == 2:
                ref_cpos_end = cpos_end - 1
                ref_tpos_end = tpos_end - 1
            ref_codon_end = codonnum_to_codon[self._get_codonnum(tid, ref_tpos_end)]
            if ref_codonpos_start == 1:
                new_ref_codon = _get_bases_tpos(tid, tpos_end + 1, tpos_end + 3)
                ref_tpos_after_new_codon = tpos_end + 4
            elif ref_codonpos_start == 2:
                new_ref_codon = ref_codon_start[0] + _get_bases_tpos(
                    tid, tpos_end + 1, tpos_end + 2
                )
                ref_tpos_after_new_codon = tpos_end + 3
            elif ref_codonpos_start == 0:
                new_ref_codon = ref_codon_start[:2] + _get_bases_tpos(tid, tpos_end + 1)
                ref_tpos_after_new_codon = tpos_end + 2
            new_aanum_start = codon_to_aanum[new_ref_codon]
            so = (SO_FSD,)
            altered_apos = None
            if ref_aanum_start != new_aanum_start:
                new_aanum = new_aanum_start
                altered_apos = apos
                altered_tpos = ref_tpos_after_new_codon
                apos_nextter = 1
            elif apos == alen + 1 and new_aanum_start == TER:
                so += (SO_STR,)
                apos_nextter = 0
            else:
                apos_nextter = 0
                new_aanum = None
                for tpos_q in range(ref_tpos_after_new_codon, tlen - 2, 3):
                    aanum_q = codon_to_aanum[_get_bases_tpos(tid, tpos_q, tpos_q + 2)]
                    real_cpos = tpos_q - lenref - tstart + cstart
                    apos_q = int((real_cpos - 1) / 3) + 1
                    if aanum_q != pseq[apos_q - 1]:
                        new_aanum = aanum_q
                        altered_apos = apos_q
                        altered_tpos = tpos_q
                        break
                    else:
                        if aanum_q == TER:
                            break
            if altered_apos is None:
                if SO_STR not in so:
                    so += (SO_SYN,)
                ref_aa_start = aanum_to_aa[ref_aanum_start]
                achange = f"p.{ref_aa_start}{apos}="
            else:
                if altered_apos <= 1:
                    so += (SO_MLO,)
                elif pseq[altered_apos - 1] is TER:
                    if new_aanum == TER:
                        so += (SO_STR,)
                    else:
                        so += (SO_STL,)
                elif new_aanum == TER:
                    so += (SO_STG,)
                if SO_MLO in so:
                    achange = f"p.{aanum_to_aa[pseq[altered_apos - 1]]}{altered_apos}{aanum_to_aa[new_aanum]}fs"
                elif SO_STG in so:
                    achange = f"p.{aanum_to_aa[pseq[altered_apos - 1]]}{altered_apos}{aanum_to_aa[new_aanum]}"
                else:
                    achange = f"p.{aanum_to_aa[pseq[altered_apos - 1]]}{altered_apos}{aanum_to_aa[new_aanum]}fs"
                    ter_found = FALSE
                    for tpos_q in range(altered_tpos, tlen - 2, 3):
                        apos_nextter += 1
                        codon = _get_bases_tpos(tid, tpos_q, tpos_q + 2)
                        aanum = codon_to_aanum[codon]
                        if aanum == TER:
                            achange += f"{aanum_to_aa[TER]}{apos_nextter}"
                            ter_found = TRUE
                            break
                    if ter_found == FALSE:
                        achange += f"{aanum_to_aa[TER]}?"
        return so, achange

    def _make_primary_transcripts(self):
        self.primary_transcript = {}
        if (
            self.primary_transcript_paths is None
            or len(self.primary_transcript_paths) == 0
        ):
            return
        for primary_transcript_path in self.primary_transcript_paths:
            if primary_transcript_path == "mane":
                fns = glob.glob(os.path.join(self.module_dir, "MANE.GRCh38.*.txt"))
                fns.sort()
                fn = fns[-1]
                mane_path = fn
                f = open(fn)
                toks = f.readline().split("\t")
                hugo_colno = toks.index("symbol")
                enst_colno = toks.index("Ensembl_nuc")
                for line in f:
                    toks = line[:-1].split("\t")
                    hugo = toks[hugo_colno]
                    enst = toks[enst_colno].split(".")[0]
                    if hugo not in self.primary_transcript:
                        self.primary_transcript[hugo] = enst
                f.close()
            else:
                f = open(primary_transcript_path)
                for line in f:
                    if line.startswith("#"):
                        continue
                    toks = line[:-1].split()
                    # if tokslen == 1:
                    #    self.primary_transcript += (toks[0],)
                    #    for line in f:
                    #        if line.startswith('#'):
                    #            continue
                    #        toks = line[:-1].split()
                    #        self.primary_transcript += (toks[0],)
                    if len(toks) != 2:
                        continue
                    else:
                        hugo = toks[0]
                        enst = toks[1]
                        self.primary_transcript[hugo] = enst
                f.close()

    def setup(self):
        self.module_dir = os.path.dirname(__file__)
        data_dir = os.path.join(self.module_dir, "data")
        db_path = os.path.join(data_dir, "gene_33_10000.sqlite")
        self.db = Mapper._get_db(db_path)
        self.c = self.db.cursor()
        self.c2 = self.db.cursor()
        q = 'select v from info where k="binsize"'
        self.c.execute(q)
        self.binsize = int(self.c.fetchone()[0])
        q = 'select v from info where k="gencode_ver"'
        self.c.execute(q)
        self.ver = self.c.fetchone()[0]
        mrnas_path = os.path.join(data_dir, "mrnas_33.pickle")
        f = open(mrnas_path, "rb")
        self.mrnas = pickle.load(f)
        self.prots = pickle.load(f)
        f.close()
        self.logger.info(f"mapper database: {db_path}")
        self.hg38reader = cravat.get_wgs_reader(assembly="hg38")
        self._make_tr_info()
        self._make_primary_transcripts()

    def end(self):
        self.c.close()
        self.c2.close()
        self.db.close()

    def _make_tr_info(self):
        t = time.time()
        q = """
            select
                t.tid, t.name, t.strand, t.uniprot, t.alen, t.tlen, g.desc, t.tposcposoffset,
                t.genetype, t.transcripttype, t.transcriptclass
            from transcript as t, genenames as g where t.genename=g.genename
            """
        self.c.execute(q)
        tr_info = {}
        for r in self.c.fetchall():
            (
                tid,
                name,
                strand,
                uniprot,
                alen,
                tlen,
                genename,
                tposcposoffset,
                genetype,
                transcripttype,
                transcriptclass,
            ) = r
            tr_info[tid] = (
                name,
                strand,
                uniprot,
                alen,
                tlen,
                genename,
                tposcposoffset,
                genetype,
                transcripttype,
                transcriptclass,
            )
        self.tr_info = tr_info
        q = "select genetype, desc from genetypes"
        self.c.execute(q)
        self.genetypes = {}
        self.genetypenos = {}
        for r in self.c.fetchall():
            self.genetypes[r[0]] = r[1]
            self.genetypenos[r[1]] = r[0]
        q = "select transcripttype, desc from transcripttypes"
        self.c.execute(q)
        self.transcripttypes = {}
        self.transcripttypenos = {}
        for r in self.c.fetchall():
            self.transcripttypes[r[0]] = r[1]
            self.transcripttypenos[r[1]] = r[0]
        q = "select transcriptclass, desc from transcriptclasses"
        self.c.execute(q)
        self.transcriptclasses = {}
        self.transcriptclassnos = {}
        for r in self.c.fetchall():
            self.transcriptclasses[r[0]] = r[1]
            self.transcriptclassnos[r[1]] = r[0]
        global GENETYPENO_PROTEIN_CODING
        global TRANSCRIPTTYPENO_PROTEIN_CODING
        global TRANSCRIPTTYPENO_NMD
        global TRANSCRIPTCLASSNO_CODING
        GENETYPENO_PROTEIN_CODING = self.genetypenos["protein_coding"]
        TRANSCRIPTTYPENO_PROTEIN_CODING = self.transcripttypenos["protein_coding"]
        TRANSCRIPTTYPENO_NMD = self.transcripttypenos["nonsense_mediated_decay"]
        TRANSCRIPTCLASSNO_CODING = self.transcriptclassnos["coding"]

    @staticmethod
    def _get_db(db_path):
        try:
            import sqlite3

            diskdb = sqlite3.connect(db_path)
            db = sqlite3.connect(":memory:")
            diskdb.backup(db)
        except:
            try:
                import apsw

                diskdb = apsw.Connection(db_path)
                db = apsw.Connection(":memory:")
                db.backup("main", diskdb, "main").step()
            except:
                try:
                    from supersqlite import sqlite3

                    diskdb = sqlite3.connect(db_path)
                    db = sqlite3.connect(":memory:")
                    diskdb.backup(db)
                except:
                    db = sqlite3.connect(db_path)
        return db

    def _get_gpos_fraginfo(self, tid, chrom, gpos):
        gposbin = int(gpos / self.binsize)
        q = f"select start, end, kind, cstart, exonno from transcript_frags_{chrom} where tid={tid} and binno={gposbin} and start<={gpos} and end>={gpos}"
        self.c2.execute(q)
        row = self.c2.fetchone()
        if row is None:
            return None
        else:
            return row

    def _get_gpos_fragkind(self, tid, chrom, gpos):
        gposbin = int(gpos / self.binsize)
        q = f"select kind, cstart from transcript_frags_{chrom} where tid={tid} and binno={gposbin} and start<={gpos} and end>={gpos}"
        self.c2.execute(q)
        row = self.c2.fetchone()
        if row is None:
            return None
        else:
            return row[0]

    def _fill_full_mrna_seq(self, tid, mrna):
        mrnalen = len(mrna)
        [seq, ex] = self.mrnas[tid]
        for tpos_q in range(len(seq) * 4):
            if tpos_q >= mrnalen:
                break
            if tpos_q + 1 in ex:
                base = NBASECHARORD
            else:
                seqbyteno = int(tpos_q / 4)
                seqbitno = (tpos_q % 4) * 2
                basebits = (seq[seqbyteno] >> (6 - seqbitno)) & 0b00000011
                if basebits == ADENINENUM:
                    base = ADENINECHARORD
                elif basebits == THYMINENUM:
                    base = THYMINECHARORD
                elif basebits == GUANINENUM:
                    base = GUANINECHARORD
                else:
                    base = CYTOSINECHARORD
            mrna[tpos_q] = base

    def _get_bases_tpos(self, tid, start, end=None):
        if end is None:
            end = start
        bases = ""
        [seq, ex] = self.mrnas[tid]
        for tpos_q in range(start, end + 1):
            if tpos_q in ex:
                base = NBASECHAR
            else:
                seqbyteno = int((tpos_q - 1) / 4)
                seqbitno = ((tpos_q - 1) % 4) * 2
                basebits = (seq[seqbyteno] >> (6 - seqbitno)) & 0b00000011
                if basebits == ADENINENUM:
                    base = ADENINECHAR
                elif basebits == THYMINENUM:
                    base = THYMINECHAR
                elif basebits == GUANINENUM:
                    base = GUANINECHAR
                else:
                    base = CYTOSINECHAR
            bases += base
        return bases

    def _get_intron_hgvs_cpos(
        self,
        start,
        end,
        gpos,
        cstart,
        strand,
        prevcont,
        nextcont,
        chrom,
        tid,
        exonno,
        kind,
    ):
        if prevcont != 0:
            intron_start = self._get_exon_start(chrom, tid, exonno, kind, strand)
        else:
            if strand == PLUSSTRAND:
                intron_start = start
            else:
                intron_start = end
        if nextcont != 0:
            intron_end = self._get_exon_end(chrom, tid, exonno, kind, strand)
        else:
            if strand == PLUSSTRAND:
                intron_end = end
            else:
                intron_end = start
        midpoint = (intron_start + intron_end) / 2
        if gpos < midpoint:
            if strand == PLUSSTRAND:
                diff = gpos - intron_start + 1
                hgvs_cpos = f"{cstart}+{diff}"
            else:
                diff = gpos - intron_end + 1
                hgvs_cpos = f"{cstart + 1}-{diff}"
        else:
            if strand == PLUSSTRAND:
                diff = intron_end - gpos + 1
                hgvs_cpos = f"{cstart + 1}-{diff}"
            else:
                diff = intron_start - gpos + 1
                hgvs_cpos = f"{cstart}+{diff}"
        if kind == FRAG_UTR3INTRON:
            hgvs_cpos = "*" + hgvs_cpos
        return hgvs_cpos

    def _get_hgvs_cpos(
        self,
        tid,
        kind,
        start,
        end,
        cstart,
        gpos_q,
        chrom,
        strand,
        prevcont,
        nextcont,
        exonno,
    ):
        if gpos_q >= start and gpos_q <= end:
            kind_q = kind
            start_q = start
            end_q = end
            cstart_q = cstart
        else:
            row = self._get_gpos_fraginfo(tid, chrom, gpos_q)
            if row is None:
                if strand == PLUSSTRAND:
                    if (kind == FRAG_UP2K and gpos_q < start) or (
                        kind == FRAG_DN2K and gpos_q > end
                    ):
                        return f"{cstart + gpos_q - start}"
                    elif kind == FRAG_FLAG_IG:
                        q = f"select min(start), max(end) from transcript_frags_{chrom} where tid={tid} and kind={FRAG_CDS}"
                        self.c2.execute(q)
                        (minstart, maxend) = self.c2.fetchone()
                        if gpos_q < minstart:
                            return f"{gpos_q - minstart}"
                        elif gpos_q > maxend:
                            return f"*{gpos_q - maxend}"
                    else:
                        return None
                else:
                    if (kind == FRAG_UP2K and gpos_q > end) or (
                        kind == FRAG_DN2K and gpos_q < start
                    ):
                        return f"{cstart - gpos_q + end}"
                    elif kind == FRAG_FLAG_IG:
                        q = f"select min(start), max(end) from transcript_frags_{chrom} where tid={tid} and kind={FRAG_CDS}"
                        self.c2.execute(q)
                        (minstart, maxend) = self.c2.fetchone()
                        if gpos_q < minstart:
                            return f"*{minstart - gpos_q}"
                        elif gpos_q > maxend:
                            return f"{maxend - gpos_q}"
                    else:
                        return None
            else:
                start_q, end_q, kind_q, cstart_q, exonno = row
        if kind_q & FRAG_FLAG_INTRON == FRAG_FLAG_INTRON:
            hgvs_cpos = self._get_intron_hgvs_cpos(
                start_q,
                end_q,
                gpos_q,
                cstart_q,
                strand,
                prevcont,
                nextcont,
                chrom,
                tid,
                exonno,
                kind_q,
            )
        else:
            if strand == PLUSSTRAND:
                cpos_q = gpos_q - start_q + cstart_q
                if cpos_q == 0:
                    cpos_q = -1
                hgvs_cpos = f"{cpos_q}"
            else:
                cpos_q = end_q - gpos_q + cstart_q
                if cpos_q == 0:
                    cpos_q = -1
                hgvs_cpos = f"{cpos_q}"
        if kind_q == FRAG_UTR3 or kind_q == FRAG_DN2K:
            hgvs_cpos = "*" + hgvs_cpos
        return hgvs_cpos

    def _get_tr_map_data(self, chrom, gpos):
        gposbin = int(gpos / self.binsize)
        q = f"""
            select * from transcript_frags_{chrom}
            where binno={gposbin} and start<={gpos} and end>={gpos} order by tid
            """
        try:
            self.c.execute(q)
            ret = self.c.fetchall()
        except Exception as e:
            if str(e).startswith("no such table"):
                ret = ()
            else:
                raise
        return ret

    def _get_splice_apos_prevfrag(self, tid, fragno, chrom, cpos, gpos, start, kind):
        apos = -1
        if kind == FRAG_CDSINTRON:
            prev_last_cpos = cpos
            so = (SO_SPL, SO_INT)
        elif kind == FRAG_UTR5INTRON or kind == FRAG_UTR3INTRON:
            so = (SO_INT,)
        return apos, so

    def _get_splice_apos_nextfrag(self, tid, fragno, chrom):
        apos = -1
        q = f"select max(fragno) from transcript_frags_{chrom} where tid={tid}"
        self.c2.execute(q)
        max_fragno = self.c2.fetchone()[0]
        for search_frag_no in range(fragno + 1, max_fragno + 1, 1):
            q = f"select kind, cstart from transcript_frags_{chrom} where tid={tid} and fragno={search_frag_no}"
            self.c2.execute(q)
            [kind, next_frag_cpos] = self.c2.fetchone()
            if kind == FRAG_CDS:
                next_first_cpos = next_frag_cpos
                cpos_for_apos = next_first_cpos - 1
                apos = int(cpos_for_apos / 3) + 1
                so = (SO_SPL, SO_INT)
                break
            elif (
                kind == FRAG_UTR3
                or kind == FRAG_UTR5
                or kind == FRAG_UP2K
                or kind == FRAG_DN2K
            ):
                apos = -1
                so = (SO_INT,)
                break
        return apos, so

    def _get_ins_cds_data(
        self,
        tid,
        cpos,
        cstart,
        tpos,
        tstart,
        alt_base,
        chrom,
        strand,
        lenalt,
        apos,
        gpos,
        tposcposoffset,
    ):
        if strand == MINUSSTRAND:
            cpos += 1
            tpos += 1
            gpos -= 1
            apos = int((cpos - 1) / 3 + 1)
        pseq = memoryview(self.prots[tid])
        ref_aa = pseq[apos - 1]
        if lenalt % 3 == 0:  # inframe_insertion
            ref_codonpos = cpos % 3
            if ref_codonpos == 1:  # conservative_inframe_insertion
                lenaltaas = int(lenalt / 3)
                alt_aas = bytearray(lenaltaas)
                for i in range(0, lenaltaas):
                    basei = i * 3
                    alt_aas[i] = codon_to_aanum[alt_base[basei : basei + 3]]
                if TER in alt_aas:
                    if ref_aa != TER:
                        so = (SO_INI, SO_STG)
                    else:
                        so = (SO_INI,)
                    start_idx = alt_aas.index(TER)
                    if ref_aa == TER:
                        alt_aas = alt_aas[:start_idx]
                    else:
                        alt_aas = alt_aas[: start_idx + 1]
                    ref_aa = pseq[apos - 1]
                    prev_ref_aa = pseq[apos - 2]
                    prev_ref_apos = apos - 1
                    alt_aas = "".join([aanum_to_aa[aanum] for aanum in alt_aas])
                    achange = f"p.{aanum_to_aa[pseq[apos - 2]]}{apos -1}_{aanum_to_aa[pseq[apos - 1]]}{apos}ins{alt_aas}"
                else:
                    so = (SO_INI,)
                    apos_prev_ref_start = apos - lenaltaas
                    if apos_prev_ref_start < 1:
                        apos_prev_ref_start = 1
                    prev_ref = pseq[apos_prev_ref_start - 1 : apos - 1]
                    apos_next_ref_end = apos + lenaltaas - 1
                    alen = self.tr_info[tid][TR_INFO_ALEN_I]
                    if apos_next_ref_end > alen:
                        apos_next_ref_end = alen
                    next_ref = pseq[apos - 1 : apos_next_ref_end]
                    lenaltaasrepeat = lenaltaas
                    lenprev_ref = len(prev_ref)
                    lennext_ref = len(next_ref)
                    search_pseq = bytearray(lenprev_ref + lenaltaas + lennext_ref)
                    search_pseq[:lenprev_ref] = prev_ref
                    search_pseq[lenprev_ref : lenprev_ref + lenaltaas] = alt_aas
                    search_pseq[-lennext_ref:] = next_ref
                    apos_q_start = -1
                    max_apos_q_start = None
                    dup_found = FALSE
                    for i in range(
                        len(search_pseq) - lenaltaasrepeat - lenaltaasrepeat + 1
                    ):
                        scan_frag = search_pseq[i : i + lenaltaasrepeat]
                        if (
                            scan_frag
                            == search_pseq[
                                i
                                + lenaltaasrepeat : i
                                + lenaltaasrepeat
                                + lenaltaasrepeat
                            ]
                        ):
                            dup_found = TRUE
                            apos_q_start = apos - lenaltaasrepeat + i
                            if (
                                max_apos_q_start is None
                                or apos_q_start > max_apos_q_start
                            ):
                                max_apos_q_start = apos_q_start
                            while TRUE:
                                apos_q_f = apos_q_start + lenaltaasrepeat
                                aas_q_f = pseq[
                                    apos_q_f - 1 : apos_q_f + lenaltaasrepeat - 1
                                ]
                                if aas_q_f == scan_frag:
                                    apos_q_start = apos_q_f
                                    if apos_q_start > max_apos_q_start:
                                        max_apos_q_start = apos_q_start
                                    apos_q_f = apos_q_start + lenaltaasrepeat
                                else:
                                    break
                    if dup_found:
                        if lenaltaasrepeat == 1:
                            achange = f"p.{aanum_to_aa[pseq[max_apos_q_start-1]]}{max_apos_q_start}dup"
                        else:
                            max_apos_q_end = max_apos_q_start + lenaltaasrepeat - 1
                            achange = f"p.{aanum_to_aa[pseq[max_apos_q_start-1]]}{max_apos_q_start}_{aanum_to_aa[pseq[max_apos_q_end-1]]}{max_apos_q_end}dup"
                    else:
                        for i in range(lenaltaas):
                            if alt_aas[i] != pseq[apos + i - 1]:
                                apos = apos + i
                                alt_aas = alt_aas[i:] + alt_aas[:i]
                                break
                        alt_aas = "".join([aanum_to_aa[aanum] for aanum in alt_aas])
                        achange = f"p.{aanum_to_aa[pseq[apos-2]]}{apos-1}_{aanum_to_aa[pseq[apos-1]]}{apos}ins{alt_aas}"
            else:  # disruptive_inframe_insertion
                if ref_codonpos == 2:
                    ref_cpos = cpos - 1
                elif ref_codonpos == 0:
                    ref_cpos = cpos - 2
                ref_tpos = tstart + ref_cpos - cstart
                ref_gpos = gpos + ref_cpos - cpos
                ref_codonnum = self._get_codonnum(tid, ref_tpos)
                ref_codon = codonnum_to_codon[ref_codonnum]
                if ref_codonpos == 2:
                    new_bases = ref_codon[0] + alt_base + ref_codon[1:]
                elif ref_codonpos == 0:
                    new_bases = ref_codon[:2] + alt_base + ref_codon[2]
                lennew = len(new_bases)
                lenaltaas = int(lennew / 3)
                alt_aas = bytearray(lenaltaas)
                for i in range(0, lenaltaas):
                    basei = i * 3
                    alt_aas[i] = codon_to_aanum[new_bases[basei : basei + 3]]
                if lenalt == 3:  # 1 aa insertion
                    ref_aa = pseq[apos - 1]
                    alt_aas1 = alt_aas[0]
                    alt_aas2 = alt_aas[1]
                    if apos == 1:  # ATG
                        if alt_aas1 == MET:
                            so = (SO_INI,)
                            if alt_aas2 == MET:
                                achange = f"p.{aanum_to_aa[MET]}1dup"
                            else:
                                achange = f"p.{aanum_to_aa[MET]}1_{aanum_to_aa[pseq[apos]]}{apos + 1}ins{aanum_to_aa[alt_aas2]}"
                        else:
                            if alt_aas2 == MET:
                                so = (SO_INI, SO_MRT)
                                achange = f"p.{aanum_to_aa[MET]}1="
                            else:
                                so = (SO_INI, SO_MLO)
                                alt_aas = "".join(
                                    [aanum_to_aa[aanum] for aanum in alt_aas]
                                )
                                achange = f"p.{aanum_to_aa[MET]}1delins{alt_aas}"
                    elif ref_aa == TER:  # Ter
                        if alt_aas1 == TER:
                            so = (SO_INI, SO_STR)
                            achange = f"p.{aanum_to_aa[TER]}{apos}="
                        elif alt_aas2 == TER:
                            so = (SO_INI,)
                            achange = f"p.{aanum_to_aa[pseq[apos - 2]]}{apos - 1}_{aanum_to_aa[TER]}{apos}ins{aanum_to_aa[alt_aas1]}"
                        else:
                            so = (SO_INI, SO_STL)
                            tlen = self.tr_info[tid][TR_INFO_TLEN_I]
                            tpos_q = ref_tpos + 3
                            stp_found = FALSE
                            num_addl_alt_aas = 0
                            while tpos_q <= tlen - 3:
                                codonnum = self._get_codonnum(tid, tpos_q)
                                aanum = codonnum_to_aanum[codonnum]
                                num_addl_alt_aas += 1
                                if aanum == TER:
                                    stp_found = TRUE
                                    break
                                tpos_q += 3
                            achange = f"p.{aanum_to_aa[TER]}{apos}{aanum_to_aa[alt_aas[0]]}ext"
                            if stp_found:
                                achange += f"{lenaltaas + num_addl_alt_aas - 1}"
                            else:
                                achange += "?"
                    elif alt_aas1 == TER:  # STG in middle
                        so = (SO_INI, SO_STG)
                        achange = f"p.{aanum_to_aa[ref_aa]}{apos}{aanum_to_aa[TER]}"
                    elif alt_aas2 == TER:  # STG in middle with ref change
                        so = (SO_INI, SO_STG)
                        if alt_aas1 == ref_aa:
                            achange = f"p.{aanum_to_aa[pseq[apos]]}{apos + 1}{aanum_to_aa[TER]}"
                        else:
                            alt_aas = "".join([aanum_to_aa[aanum] for aanum in alt_aas])
                            achange = f"p.{aanum_to_aa[ref_aa]}{apos}delins{alt_aas}"
                    else:
                        so = (SO_INI,)
                        alt_aa_first = alt_aas[0]
                        alt_aa_last = alt_aas[-1]
                        dup_found = FALSE
                        lenaltaasrepeat = lenaltaas - 1
                        if (
                            alt_aa_first == ref_aa and alt_aa_last != ref_aa
                        ):  # insertion after ref_aa of alt_aas[1:]
                            scan_frag = alt_aas[1:]
                            apos_next_ref_end = apos + len(scan_frag)
                            alen = self.tr_info[tid][TR_INFO_ALEN_I]
                            if apos_next_ref_end > alen:
                                apos_next_ref_end = alen
                            next_ref = pseq[apos:apos_next_ref_end]
                            if scan_frag == next_ref:
                                dup_found = TRUE
                                apos_q_start = apos + 1
                                max_apos_q_start = apos_q_start
                                while TRUE:
                                    apos_q_f = apos_q_start + lenaltaasrepeat
                                    aas_q_f = pseq[
                                        apos_q_f : apos_q_f + lenaltaasrepeat
                                    ]
                                    if aas_q_f == scan_frag:
                                        apos_q_start = apos_q_f
                                        if apos_q_start > max_apos_q_start:
                                            max_apos_q_start = apos_q_start
                                    else:
                                        break
                            if dup_found:
                                if lenaltaasrepeat == 1:
                                    achange = f"p.{aanum_to_aa[pseq[max_apos_q_start-1]]}{max_apos_q_start}dup"
                                else:
                                    max_apos_q_end = (
                                        max_apos_q_start + lenaltaasrepeat - 1
                                    )
                                    achange = f"p.{aanum_to_aa[pseq[max_apos_q_start-1]]}{max_apos_q_start}_{aanum_to_aa[pseq[max_apos_q_end-1]]}{max_apos_q_end}dup"
                            else:
                                for i in range(1, lenaltaas):
                                    if alt_aas[i] != pseq[apos + i - 1]:
                                        apos = apos + i
                                        alt_aas = alt_aas[i:] + alt_aas[1:i]
                                        break
                                alt_aas = "".join(
                                    [aanum_to_aa[aanum] for aanum in alt_aas]
                                )
                                achange = f"p.{aanum_to_aa[pseq[apos-2]]}{apos-1}_{aanum_to_aa[pseq[apos-1]]}{apos}ins{alt_aas}"
                        elif (
                            alt_aa_first != ref_aa and alt_aa_last == ref_aa
                        ):  # insertion before ref_aa of alt_aas[:-1]
                            scan_frag = alt_aas[:-1]
                            apos_prev_ref_start = apos - len(scan_frag)
                            if apos_prev_ref_start < 1:
                                apos_prev_ref_start = 1
                            prev_ref = pseq[apos_prev_ref_start - 1 : apos - 1]
                            if scan_frag == prev_ref:
                                dup_found = TRUE
                                max_apos_q_start = apos - lenaltaasrepeat
                            if dup_found:
                                if lenaltaasrepeat == 1:
                                    achange = f"p.{aanum_to_aa[pseq[max_apos_q_start-1]]}{max_apos_q_start}dup"
                                else:
                                    max_apos_q_end = (
                                        max_apos_q_start + lenaltaasrepeat - 1
                                    )
                                    achange = f"p.{aanum_to_aa[pseq[max_apos_q_start-1]]}{max_apos_q_start}_{aanum_to_aa[pseq[max_apos_q_end-1]]}{max_apos_q_end}dup"
                            else:
                                for i in range(lenaltaas - 1):
                                    if alt_aas[i] != pseq[apos + i - 1]:
                                        apos = apos + i
                                        alt_aas = alt_aas[i:-1] + alt_aas[:i]
                                        break
                                alt_aas = "".join(
                                    [aanum_to_aa[aanum] for aanum in alt_aas]
                                )
                                achange = f"p.{aanum_to_aa[pseq[apos-2]]}{apos-1}_{aanum_to_aa[pseq[apos-1]]}{apos}ins{alt_aas}"
                        elif (
                            alt_aa_first == ref_aa and alt_aa_last == ref_aa
                        ):  # window search for the most c-terminal repeat
                            apos_prev_ref_start = apos - lenaltaas + 1
                            if apos_prev_ref_start < 1:
                                apos_prev_ref_start = 1
                            prev_ref = pseq[apos_prev_ref_start - 1 : apos - 1]
                            apos_next_ref_end = apos + lenaltaas
                            alen = self.tr_info[tid][TR_INFO_ALEN_I]
                            if apos_next_ref_end > alen:
                                apos_next_ref_end = alen
                            next_ref = pseq[apos:apos_next_ref_end]
                            lenaltaasrepeat = lenaltaas - 1
                            lenprev_ref = len(prev_ref)
                            lennext_ref = len(next_ref)
                            search_pseq = bytearray(
                                lenprev_ref + lenaltaas + lennext_ref
                            )
                            search_pseq[:lenprev_ref] = prev_ref
                            search_pseq[lenprev_ref : lenprev_ref + lenaltaas] = alt_aas
                            search_pseq[-lennext_ref:] = next_ref
                            apos_q_start = -1
                            max_apos_q_start = None
                            for i in range(
                                len(search_pseq) - lenaltaasrepeat - lenaltaasrepeat + 1
                            ):
                                scan_frag = search_pseq[i : i + lenaltaasrepeat]
                                if (
                                    scan_frag
                                    == search_pseq[
                                        i
                                        + lenaltaasrepeat : i
                                        + lenaltaasrepeat
                                        + lenaltaasrepeat
                                    ]
                                ):
                                    dup_found = TRUE
                                    apos_q_start = apos - lenaltaasrepeat + 1 + i
                                    if (
                                        max_apos_q_start is None
                                        or apos_q_start > max_apos_q_start
                                    ):
                                        max_apos_q_start = apos_q_start
                                    while TRUE:
                                        apos_q_f = apos_q_start + lenaltaasrepeat
                                        aas_q_f = pseq[
                                            apos_q_f : apos_q_f + lenaltaasrepeat
                                        ]
                                        if aas_q_f == scan_frag:
                                            apos_q_start = apos_q_f
                                            if apos_q_start > max_apos_q_start:
                                                max_apos_q_start = apos_q_start
                                            apos_q_f = apos_q_start + lenaltaasrepeat
                                        else:
                                            break
                            if dup_found:
                                if lenaltaasrepeat == 1:
                                    achange = f"p.{aanum_to_aa[pseq[max_apos_q_start-1]]}{max_apos_q_start}dup"
                                else:
                                    max_apos_q_end = (
                                        max_apos_q_start + lenaltaasrepeat - 1
                                    )
                                    achange = f"p.{aanum_to_aa[pseq[max_apos_q_start-1]]}{max_apos_q_start}_{aanum_to_aa[pseq[max_apos_q_end-1]]}{max_apos_q_end}dup"
                            else:
                                for i in range(lenaltaas):
                                    if alt_aas[i] != pseq[apos + i - 1]:
                                        apos = apos + i
                                        alt_aas = alt_aas[i:] + alt_aas[:i]
                                        break
                                alt_aas = "".join(
                                    [aanum_to_aa[aanum] for aanum in alt_aas]
                                )
                                achange = f"p.{aanum_to_aa[pseq[apos-2]]}{apos-1}_{aanum_to_aa[pseq[apos-1]]}{apos}ins{alt_aas}"
                        else:  # delins
                            alt_aas = "".join([aanum_to_aa[aanum] for aanum in alt_aas])
                            achange = f"p.{aanum_to_aa[ref_aa]}{apos}delins{alt_aas}"
                else:  # multiple aa insertion
                    ref_aa = pseq[apos - 1]
                    alt_aas_first = alt_aas[0]
                    alt_aas_last = alt_aas[-1]
                    lenaltaas = len(alt_aas)
                    if apos == 1:  # ATG
                        if MET in alt_aas:
                            atg_idx = alt_aas.index(MET)
                            if atg_idx == lenaltaas - 1:
                                so = (SO_INI, SO_MRT)
                                achange = f"p.{aanum_to_aa[MET]}1="
                            else:
                                so = (SO_INI,)
                                alt_aas = alt_aas[atg_idx + 1 :]
                                if alt_aas == "M":
                                    achange = f"p.{aanum_to_aa[MET]}1dup"
                                else:
                                    alt_aas = "".join(
                                        [aanum_to_aa[aanum] for aanum in alt_aas]
                                    )
                                    achange = f"p.{aanum_to_aa[MET]}1_{aanum_to_aa[pseq[1]]}2ins{alt_aas}"
                        else:
                            so = (SO_INI, SO_MLO)
                            alt_aas = "".join([aanum_to_aa[aanum] for aanum in alt_aas])
                            achange = f"p.{aanum_to_aa[MET]}1delins{alt_aas}"
                    elif ref_aa == TER:  # Ter
                        if TER in alt_aas:
                            ter_idx = alt_aas.index(TER)
                            if ter_idx == 0:
                                so = (SO_INI, SO_STR)
                                achange = f"p.{aanum_to_aa[TER]}{apos}="
                            else:
                                so = (SO_INI,)
                                alt_aas = alt_aas[:ter_idx]
                                alt_aas = "".join(
                                    [aanum_to_aa[aanum] for aanum in alt_aas]
                                )
                                achange = f"p.{aanum_to_aa[pseq[apos - 2]]}{apos - 1}_{aanum_to_aa[TER]}{apos}ins{alt_aas}"
                        else:  # 3' extension
                            so = (SO_INI, SO_STL)
                            tlen = self.tr_info[tid][TR_INFO_TLEN_I]
                            tpos_q_start = ref_tpos + 3
                            stp_found = FALSE
                            num_addl_alt_aas = 0
                            for tpos_q in range(tpos_q_start, tlen, 3):
                                codonnum = self._get_codonnum(tid, tpos_q)
                                aanum = codonnum_to_aanum[codonnum]
                                num_addl_alt_aas += 1
                                if aanum == TER:
                                    stp_found = TRUE
                                    break
                            achange = f"p.{aanum_to_aa[TER]}{apos}{alt_aas[0]}ext"
                            if stp_found:
                                achange += f"{lenaltaas + num_addl_alt_aas - 1}"
                            else:
                                achange += "?"
                    elif alt_aas_first == TER:  # 1st alt_aa is TER.
                        so = (SO_INI, SO_STG)
                        achange = f"p.{aanum_to_aa[ref_aa]}{apos}{aanum_to_aa[TER]}"
                    elif TER in alt_aas:  # STG in the middle with ref change
                        ter_idx = alt_aas.index(TER)
                        alt_aas = alt_aas[: ter_idx + 1]
                        if alt_aas_first != ref_aa:
                            so = (SO_INI, SO_STG)
                            alt_aas = "".join([aanum_to_aa[aanum] for aanum in alt_aas])
                            achange = f"p.{aanum_to_aa[ref_aa]}{apos}delins{alt_aas}"
                        else:
                            diff_apos = None
                            diff_i = None
                            for i in range(1, lenaltaas):
                                apos_q = apos + i
                                alt_aa = alt_aas[i]
                                pseq_aa = pseq[apos_q - 1]
                                if alt_aa != pseq_aa:
                                    diff_apos = apos_q
                                    diff_i = i
                                    break
                                elif apos_q == len(pseq) - 1:
                                    break
                                elif alt_aa == pseq_aa and alt_aa == TER:
                                    break
                            if diff_apos is None:
                                so = (SO_SYN,)
                                achange = f"p.{aanum_to_aa[pseq[apos - 1]]}{apos}="
                            else:
                                so = (SO_STG,)
                                achange = f"p.{aanum_to_aa[pseq[diff_apos - 1]]}{diff_apos}{aanum_to_aa[TER]}"
                    else:  # multi-aa insertion in the middle
                        so = (SO_INI,)
                        alt_aa_first = alt_aas[0]
                        alt_aa_last = alt_aas[-1]
                        dup_found = FALSE
                        lenaltaasrepeat = lenaltaas - 1
                        if (
                            alt_aa_first == ref_aa and alt_aa_last != ref_aa
                        ):  # insertion after ref_aa of alt_aas[1:]
                            scan_frag = alt_aas[1:]
                            apos_prev_ref_start = apos - len(scan_frag)
                            apos_next_ref_end = apos + len(scan_frag)
                            alen = self.tr_info[tid][TR_INFO_ALEN_I]
                            if apos_next_ref_end > alen:
                                apos_next_ref_end = alen
                            next_ref = pseq[apos:apos_next_ref_end]
                            if scan_frag == next_ref:
                                dup_found = TRUE
                                apos_q_start = apos + 1
                                max_apos_q_start = apos_q_start
                                while TRUE:
                                    apos_q_f = apos_q_start + lenaltaasrepeat
                                    aas_q_f = pseq[
                                        apos_q_f : apos_q_f + lenaltaasrepeat
                                    ]
                                    if aas_q_f == scan_frag:
                                        apos_q_start = apos_q_f
                                        if apos_q_start > max_apos_q_start:
                                            max_apos_q_start = apos_q_start
                                    else:
                                        break
                            if dup_found:
                                if lenaltaasrepeat == 1:
                                    achange = f"p.{aanum_to_aa[pseq[max_apos_q_start-1]]}{max_apos_q_start}dup"
                                else:
                                    max_apos_q_end = (
                                        max_apos_q_start + lenaltaasrepeat - 1
                                    )
                                    achange = f"p.{aanum_to_aa[pseq[max_apos_q_start-1]]}{max_apos_q_start}_{aanum_to_aa[pseq[max_apos_q_end-1]]}{max_apos_q_end}dup"
                            else:
                                for i in range(1, lenaltaas):
                                    if alt_aas[i] != pseq[apos + i - 1]:
                                        apos = apos + i
                                        alt_aas = alt_aas[i:] + alt_aas[1:i]
                                        break
                                alt_aas = "".join(
                                    [aanum_to_aa[aanum] for aanum in alt_aas]
                                )
                                achange = f"p.{aanum_to_aa[pseq[apos-2]]}{apos-1}_{aanum_to_aa[pseq[apos-1]]}{apos}ins{alt_aas}"
                        elif (
                            alt_aa_first != ref_aa and alt_aa_last == ref_aa
                        ):  # insertion before ref_aa of alt_aas[:-1]
                            scan_frag = alt_aas[:-1]
                            apos_prev_ref_start = apos - len(scan_frag)
                            apos_next_ref_end = apos + len(scan_frag)
                            if apos_prev_ref_start < 1:
                                apos_prev_ref_start = 1
                            prev_ref = pseq[apos_prev_ref_start - 1 : apos - 1]
                            if scan_frag == prev_ref:
                                dup_found = TRUE
                                max_apos_q_start = apos - lenaltaasrepeat
                            if dup_found:
                                if lenaltaasrepeat == 1:
                                    achange = f"p.{aanum_to_aa[pseq[max_apos_q_start-1]]}{max_apos_q_start}dup"
                                else:
                                    max_apos_q_end = (
                                        max_apos_q_start + lenaltaasrepeat - 1
                                    )
                                    achange = f"p.{aanum_to_aa[pseq[max_apos_q_start-1]]}{max_apos_q_start}_{aanum_to_aa[pseq[max_apos_q_end-1]]}{max_apos_q_end}dup"
                            else:
                                for i in range(lenaltaas - 1):
                                    if alt_aas[i] != pseq[apos + i - 1]:
                                        apos = apos + i
                                        alt_aas = alt_aas[i:-1] + alt_aas[:i]
                                        break
                                alt_aas = "".join(
                                    [aanum_to_aa[aanum] for aanum in alt_aas]
                                )
                                achange = f"p.{aanum_to_aa[pseq[apos-2]]}{apos-1}_{aanum_to_aa[pseq[apos-1]]}{apos}ins{alt_aas}"
                        elif (
                            alt_aa_first == ref_aa and alt_aa_last == ref_aa
                        ):  # window search for the most c-terminal repeat
                            apos_prev_ref_start = apos - lenaltaas + 1
                            if apos_prev_ref_start < 1:
                                apos_adjust = apos_prev_ref_start - 1
                                prev_ref = (
                                    bytearray(-apos_prev_ref_start + 2)
                                    + pseq[: apos - 1]
                                )
                            else:
                                apos_adjust = 0
                                prev_ref = pseq[apos_prev_ref_start - 1 : apos - 1]
                            apos_next_ref_end = apos + lenaltaas
                            alen = self.tr_info[tid][TR_INFO_ALEN_I]
                            if apos_next_ref_end > alen:
                                next_ref = pseq[apos:alen].tobytes() + bytearray(
                                    apos_next_ref_end - alen
                                )
                            else:
                                next_ref = pseq[apos:apos_next_ref_end]
                            lenaltaas = len(alt_aas)
                            lenaltaasrepeat = lenaltaas - 1
                            lenprev_ref = len(prev_ref)
                            lennext_ref = len(next_ref)
                            search_pseq = bytearray(
                                lenprev_ref + lenaltaas + lennext_ref
                            )
                            search_pseq[:lenprev_ref] = prev_ref
                            search_pseq[lenprev_ref : lenprev_ref + lenaltaas] = alt_aas
                            search_pseq[-lennext_ref:] = next_ref
                            apos_q_start = -1
                            max_apos_q_start = None
                            for i in range(
                                len(search_pseq) - lenaltaasrepeat - lenaltaasrepeat + 1
                            ):
                                scan_frag = search_pseq[i : i + lenaltaasrepeat]
                                if (
                                    scan_frag
                                    == search_pseq[
                                        i
                                        + lenaltaasrepeat : i
                                        + lenaltaasrepeat
                                        + lenaltaasrepeat
                                    ]
                                ):
                                    dup_found = TRUE
                                    apos_q_start = (
                                        apos - lenaltaasrepeat + i + apos_adjust
                                    )
                                    if (
                                        max_apos_q_start is None
                                        or apos_q_start > max_apos_q_start
                                    ):
                                        max_apos_q_start = apos_q_start
                                    while TRUE:
                                        apos_q_f = apos_q_start + lenaltaasrepeat
                                        aas_q_f = pseq[
                                            apos_q_f : apos_q_f + lenaltaasrepeat
                                        ]
                                        if aas_q_f == scan_frag:
                                            apos_q_start = apos_q_f
                                            if apos_q_start > max_apos_q_start:
                                                max_apos_q_start = apos_q_start
                                            apos_q_f = apos_q_start + lenaltaasrepeat
                                        else:
                                            break
                            if dup_found:
                                if lenaltaasrepeat == 1:
                                    achange = f"p.{aanum_to_aa[pseq[max_apos_q_start-1]]}{max_apos_q_start}dup"
                                else:
                                    max_apos_q_end = (
                                        max_apos_q_start + lenaltaasrepeat - 1
                                    )
                                    achange = f"p.{aanum_to_aa[pseq[max_apos_q_start-1]]}{max_apos_q_start}_{aanum_to_aa[pseq[max_apos_q_end-1]]}{max_apos_q_end}dup"
                            else:
                                for i in range(lenaltaas):
                                    if alt_aas[i] != pseq[apos + i - 1]:
                                        apos = apos + i
                                        alt_aas = alt_aas[i:] + alt_aas[:i]
                                        break
                                alt_aas = "".join(
                                    [aanum_to_aa[aanum] for aanum in alt_aas]
                                )
                                achange = f"p.{aanum_to_aa[pseq[apos-2]]}{apos-1}_{aanum_to_aa[pseq[apos-1]]}{apos}ins{alt_aas}"
                        else:  # delins
                            alt_aas = "".join([aanum_to_aa[aanum] for aanum in alt_aas])
                            achange = f"p.{aanum_to_aa[ref_aa]}{apos}delins{alt_aas}"
        else:  # frameshift_insertion
            ref_codonpos = cpos % 3
            if ref_codonpos == 0:
                ref_cpos = cpos - 2
            elif ref_codonpos == 1:
                ref_cpos = cpos
            elif ref_codonpos == 2:
                ref_cpos = cpos - 1
            ref_tpos = tstart + ref_cpos - cstart
            ref_gpos = gpos + ref_cpos - cpos
            ref_codonnum = self._get_codonnum(tid, ref_tpos)
            ref_codon = codonnum_to_codon[ref_codonnum]
            if cpos == 2 or cpos == 3:
                if cpos == 2:
                    new_bases = ref_codon[0] + alt_base + ref_codon[1:]
                elif cpos == 3:
                    new_bases = ref_codon[:2] + alt_base + ref_codon[2]
                if new_bases[-3:] == "ATG" and "ATG" not in new_bases[:-3]:
                    so = (SO_MRT,)
                    achange = f"p.{aanum_to_aa[MET]}1="
                    return so, achange
                elif "ATG" in new_bases:
                    if strand == PLUSSTRAND:
                        cpos = 4
                        tpos = cpos + tposcposoffset
                        apos = 2
                        idx = new_bases.index("ATG")
                        alt_base = new_bases[idx + 3 :]
                        if cpos == 2:
                            gpos += 2
                        elif cpos == 3:
                            gpos -= 1
                    else:
                        cpos = 3
                        tpos = cpos + tposcposoffset
                        apos = 1
                        idx = new_bases.index("ATG")
                        alt_base = "".join(
                            [rev_bases[b] for b in (new_bases[idx + 3 :])[::-1]]
                        )
                        if cpos == 2:
                            gpos += 1
                    so, achange = self._get_ins_cds_data(
                        tid,
                        cpos,
                        cstart,
                        tpos,
                        tstart,
                        alt_base,
                        chrom,
                        strand,
                        lenalt,
                        apos,
                        gpos,
                        tposcposoffset,
                    )
                    return so, achange
            # makes insertion result bases (3-bases multiple).
            if ref_codonpos == 1:
                lenalt_3 = lenalt % 3
                if lenalt_3 == 1:
                    new_bases = alt_base + ref_codon[0] + ref_codon[1]
                    tpos_q_start = ref_tpos + 2
                elif lenalt_3 == 2:
                    new_bases = alt_base + ref_codon[0]
                    tpos_q_start = ref_tpos + 1
            elif ref_codonpos == 2:
                lenalt_3 = lenalt % 3
                if lenalt_3 == 1:
                    new_bases = ref_codon[0] + alt_base + ref_codon[1]
                    tpos_q_start = ref_tpos + 2
                elif lenalt_3 == 2:
                    new_bases = ref_codon[0] + alt_base
                    tpos_q_start = ref_tpos + 1
            elif ref_codonpos == 0:
                lenalt_3 = lenalt % 3
                if lenalt_3 == 1:
                    new_bases = ref_codon[0] + ref_codon[1] + alt_base
                    tpos_q_start = ref_tpos + 2
                elif lenalt_3 == 2:
                    codonnum = self._get_codonnum(tid, ref_tpos + 3)
                    new_bases = (
                        ref_codon[0]
                        + ref_codon[1]
                        + alt_base
                        + ref_codon[2]
                        + codonnum_to_codon[codonnum][0]
                    )
                    tpos_q_start = ref_tpos + 4
            len_newbases = len(new_bases)
            aanum = codon_to_aanum[new_bases[:3]]
            if aanum == TER:  # first aa of insertion result
                ref_aa = pseq[apos - 1]
                if ref_aa == TER:
                    so = (SO_FSI, SO_STR)
                    achange = f"p.{aanum_to_aa[TER]}{apos}="
                else:
                    so = (SO_FSI, SO_STG)
                    achange = f"p.{aanum_to_aa[ref_aa]}{apos}{aanum_to_aa[TER]}"
            else:
                alt_aas = (aanum,)
                stp_found = FALSE
                for i in range(3, len(new_bases), 3):  # rest of new_bases
                    aanum = codon_to_aanum[new_bases[i : i + 3]]
                    alt_aas += (aanum,)
                    if aanum == TER:
                        stp_found = TRUE
                        break
                if stp_found == FALSE:  # until the end of transcript
                    tlen = self.tr_info[tid][TR_INFO_TLEN_I]
                    for tpos_q in range(tpos_q_start, tlen - 2, 3):
                        codonnum = self._get_codonnum(tid, tpos_q)
                        aanum = codonnum_to_aanum[codonnum]
                        alt_aas += (aanum,)
                        if aanum == TER:
                            stp_found = TRUE
                            break
                ref_apos_found = None
                ref_aa_found = None
                i_found = None
                for i in range(len(alt_aas)):
                    apos_q = apos + i
                    aanum = pseq[apos_q - 1]
                    if aanum != alt_aas[i]:
                        ref_apos_found = apos_q
                        ref_aa_found = aanum
                        i_found = i
                        break
                if ref_apos_found == 1:
                    so = (SO_FSI, SO_MLO)
                    achange = f"p.{aanum_to_aa[MET]}1?"
                else:
                    if stp_found:
                        if i_found is not None:
                            if ref_aa_found == TER:
                                so = (SO_FSI, SO_STL)
                            else:
                                so = (SO_FSI,)
                            ter_dist = len(alt_aas) - i_found
                            if ter_dist == 1:
                                achange = f"p.{aanum_to_aa[ref_aa_found]}{ref_apos_found}{aanum_to_aa[alt_aas[i_found]]}"
                            else:
                                achange = f"p.{aanum_to_aa[ref_aa_found]}{ref_apos_found}{aanum_to_aa[alt_aas[i_found]]}fs{aanum_to_aa[TER]}{len(alt_aas) - i_found}"
                        else:
                            so = (SO_SYN,)
                            achange = f"p.{aanum_to_aa[pseq[apos]]}{apos}="
                    else:
                        so = (SO_FSI,)
                        achange = f"p.{aanum_to_aa[ref_aa_found]}{ref_apos_found}{aanum_to_aa[alt_aas[i_found]]}fs{aanum_to_aa[TER]}?"
        return so, achange

    def _find_next_stp_apos(self, tid, tpos):
        tlen = self.tr_info[tid][TR_INFO_TLEN_I]
        [seq, ex] = self.mrnas[tid]
        next_stp_apos = 1
        stp_found = FALSE
        while TRUE:
            codonnum = 0
            for i in range(3):
                tpos_q = tpos + i
                if tpos_q > tlen:
                    next_stp_apos = NO_NEXT_TER
                    break
                if tpos_q in ex:
                    break
                seqbyteno = int((tpos_q - 1) / 4)
                seqbitno = ((tpos_q - 1) % 4) * 2
                basebits = (seq[seqbyteno] >> (6 - seqbitno)) & 0b00000011
                num_shift = (2 - i) << 1
                shifted_basebits = basebits << num_shift
                codonnum = codonnum | shifted_basebits
            if next_stp_apos == NO_NEXT_TER:
                break
            aanum = codonnum_to_aanum[codonnum]
            if aanum == TER:
                break
            tpos += 3
            next_stp_apos += 1
        return next_stp_apos

    def _get_svn_cds_so(self, tid, cpos, cstart, tpos, tstart, alt_base, apos):
        [seq, ex] = self.mrnas[tid]
        # cpos_codonstart = int((cpos - 1) / 3) * 3 + 1
        cpos_codonstart = (apos - 1) * 3 + 1
        ref_codonnum = 0
        alt_codonnum = 0
        tpos_codonstart = tstart + (cpos_codonstart - cstart)
        alt_basebits = base_to_basenum(alt_base[0])
        for i in range(3):
            tpos_q = tpos_codonstart + i
            if tpos_q in ex:
                ref_codonnum = NBASENUM
                alt_codonnum = NBASENUM
                break
            seqbyteno = int((tpos_q - 1) / 4)
            seqbitno = ((tpos_q - 1) % 4) * 2
            basebits = (seq[seqbyteno] >> (6 - seqbitno)) & 0b00000011
            num_shift = (2 - i) << 1
            shifted_basebits = basebits << num_shift
            ref_codonnum = ref_codonnum | shifted_basebits
            if tpos_q == tpos:
                alt_codonnum = alt_codonnum | (alt_basebits << num_shift)
            else:
                alt_codonnum = alt_codonnum | shifted_basebits
        ref_aanum = codonnum_to_aanum[ref_codonnum]
        alt_aanum = codonnum_to_aanum[alt_codonnum]
        if ref_aanum != TER:
            if alt_aanum != TER:
                if ref_aanum != alt_aanum:
                    so = (SO_MIS,)
                else:
                    so = (SO_SYN,)
            else:
                so = (SO_STG,)
        else:
            if alt_aanum != TER:
                so = (SO_STL,)
            else:
                so = (SO_STR,)
        return so, ref_aanum, alt_aanum

    def _get_primary_mapping(self, all_mappings):
        primary_mappings = {}
        for hugo, mappings in all_mappings.items():
            mappings = all_mappings[hugo]
            if hugo not in primary_mappings:
                primary_mappings[hugo] = ("", "", (SO_NSO,), "", "", -1, "", "", False)
            for mapping in mappings:
                tr = mapping[MAPPING_TR_I]
                if (
                    hugo in self.primary_transcript
                    and tr.split(".")[0] == self.primary_transcript[hugo]
                ):  # defined in primary transcript file
                    primary_mappings[hugo] = mapping
                    break
                else:
                    if SO_NSO in primary_mappings[hugo][MAPPING_SO_I]:
                        primary_mappings[hugo] = mapping
                    elif _compare_mapping(primary_mappings[hugo], mapping) < 0:
                        primary_mappings[hugo] = mapping
        primary_mapping = ("", "", (SO_NSO,), "", "", -1, "", "", False)
        for hugo, mapping in primary_mappings.items():
            if _compare_mapping(primary_mapping, mapping) < 0:
                primary_mapping = mapping
        return primary_mapping

    def _get_codonnum(self, tid, tpos):
        [seq, ex] = self.mrnas[tid]
        tlen = self.tr_info[tid][TR_INFO_TLEN_I]
        codonnum = 0
        incomplete_codon = FALSE
        for i in range(3):
            tpos_q = tpos + i
            if tpos_q in ex:
                codonnum = codonnum | NBASENUM
                break
            if tpos_q > tlen:
                incomplete_codon = TRUE
                break
            tpos_q0 = tpos_q - 1
            seqbyteno = int(tpos_q0 / 4)
            seqbitno = (tpos_q0 % 4) * 2
            base_bits = ((seq[seqbyteno] >> (6 - seqbitno)) & 0b00000011) << (
                (2 - i) << 1
            )
            codonnum = codonnum | base_bits
        if incomplete_codon:
            codonnum = None
        else:
            if codonnum & NBASENUM > 0:
                aanum = XAA
            else:
                aanum = codonnum_to_aanum[codonnum]
        return codonnum

    def summarize_by_gene(self, hugo, input_data):
        out = {}
        sonums = [so_to_sonum[so] for so in set(input_data["so"])]
        out["so"] = sonum_to_so[max(sonums)]
        out["num_noncoding_variants"] = len(
            [c for c in input_data["coding"] if c != "Y"]
        )
        out["num_coding_variants"] = len([c for c in input_data["coding"] if c == "Y"])
        so_counts = {}
        all_mappings_lines = input_data["all_mappings"]
        for lineno in range(len(all_mappings_lines)):
            line = all_mappings_lines[lineno]
            all_mappings = json.loads(line)
            numsample = input_data["numsample"][lineno]
            if hugo in all_mappings:
                counts = {}
                for mapping in all_mappings[hugo]:
                    sos = mapping[2]
                    for so in sos.split(","):
                        if so == "2KU" or so == "2KD":
                            continue
                        if so not in counts:
                            counts[so] = TRUE
                for so in counts:
                    if so not in so_counts:
                        so_counts[so] = 0
                    so_counts[so] += numsample
        so_count_keys = list(so_counts.keys())
        so_count_keys.sort()
        so_count_l = [f"{so}({so_counts[so]})" for so in so_count_keys]
        out["all_so"] = ",".join(so_count_l)
        return out

    def empty_map(self, crv_data):
        return


if __name__ == "__main__":
    crv_data_snv = {
        "uid": 1,
        "chrom": "chr1",
        "pos": 155208824,
        "ref_base": "C",
        "alt_base": "T",
    }
    crv_data_ini = {
        "uid": 1,
        "chrom": "chr1",
        "pos": 155208824,
        "ref_base": "-",
        "alt_base": "TTT",
    }
    crv_data_ind = {
        "uid": 1,
        "chrom": "chr1",
        "pos": 155208824,
        "ref_base": "CCC",
        "alt_base": "-",
    }
    crv_data_fsi = {
        "uid": 1,
        "chrom": "chr1",
        "pos": 155208824,
        "ref_base": "-",
        "alt_base": "T",
    }
    crv_data_fsd = {
        "uid": 1,
        "chrom": "chr1",
        "pos": 155208824,
        "ref_base": "C",
        "alt_base": "-",
    }
    crv_data_com = {
        "uid": 1,
        "chrom": "chr1",
        "pos": 155208824,
        "ref_base": "CA",
        "alt_base": "TAA",
    }
    m = Mapper("", None, live=True)
    m.setup()
    for ti in range(10000):
        t_crx_data = m.map(crv_data_snv)
        t_crx_data = m.map(crv_data_ini)
        t_crx_data = m.map(crv_data_ind)
        t_crx_data = m.map(crv_data_fsi)
        t_crx_data = m.map(crv_data_fsd)
        t_crx_data = m.map(crv_data_com)
