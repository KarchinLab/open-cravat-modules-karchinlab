import importlib.util
import sys
import types
from pathlib import Path


cravat = types.ModuleType("cravat")
cravat.BaseMapper = object
sys.modules.setdefault("cravat", cravat)

module_path = Path(__file__).parents[1] / "mappers" / "hg38" / "hg38.py"
spec = importlib.util.spec_from_file_location("hg38_incomplete_codon_test", module_path)
hg38 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hg38)


def _packed_sequence(bases):
    packed = bytearray()
    for offset in range(0, len(bases), 4):
        value = 0
        for index, base in enumerate(bases[offset : offset + 4]):
            value |= hg38.base_to_basenum(base) << (6 - index * 2)
        packed.append(value)
    return bytes(packed)


def _mapper(transcripts):
    mapper = object.__new__(hg38.Mapper)
    mapper.mrnas = {}
    mapper.tr_info = {}
    for tid, (sequence, declared_length) in transcripts.items():
        mapper.mrnas[tid] = [_packed_sequence(sequence), set()]
        info = [None] * (hg38.TR_INFO_TLEN_I + 1)
        info[hg38.TR_INFO_TLEN_I] = declared_length
        mapper.tr_info[tid] = info
    return mapper


def test_incomplete_terminal_codon_returns_unknown_consequence():
    mapper = _mapper({1: ("A" * 570 + "AT", 572)})

    result = mapper._get_svn_cds_so(1, 418, 1, 571, 154, "G", 140)

    assert result == ((hg38.SO_UNK,), hg38.XAA, hg38.XAA)


def test_inconsistent_declared_length_cannot_read_past_stored_sequence():
    mapper = _mapper({1: ("ATGC", 6)})

    result = mapper._get_svn_cds_so(1, 1, 1, 5, 5, "G", 1)

    # The declared transcript length is inconsistent with its packed sequence.
    assert result == ((hg38.SO_UNK,), hg38.XAA, hg38.XAA)


def test_invalid_transcript_does_not_prevent_valid_transcript_consequence():
    mapper = _mapper({1: ("A" * 570 + "AT", 572), 2: ("ATG", 3)})

    incomplete = mapper._get_svn_cds_so(1, 418, 1, 571, 154, "G", 140)
    valid = mapper._get_svn_cds_so(2, 2, 1, 2, 1, "C", 1)

    assert incomplete == ((hg38.SO_UNK,), hg38.XAA, hg38.XAA)
    assert valid[0] == (hg38.SO_MIS,)


def test_incomplete_terminal_codon_has_safe_protein_notation():
    mapper = _mapper({1: ("A" * 570 + "AT", 572)})

    so, achange, cchange, coding = mapper._get_snv_map_data(
        1, 418, 1, 571, 154, "T", "G", hg38.PLUSSTRAND, hg38.FRAG_CDS,
        140, 13072370, 13072370, 13072370, "chr20", 0, 1, 1, None, None, 0,
    )

    assert so == (hg38.SO_UNK,)
    assert achange == "p.?"
    assert cchange == "c.418T>G"
    assert coding == hg38.CODING

