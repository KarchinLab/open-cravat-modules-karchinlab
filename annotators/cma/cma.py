"""OpenCRAVAT adapter for the Cancer Mutation Atlas aggregate database."""

# pyright: reportMissingImports=false
import json
import os
import re
import sqlite3
import sys
from collections import defaultdict

from cravat import BaseAnnotator

SCHEMA_VERSION = 8
AA3 = {
    "Ala": "A",
    "Arg": "R",
    "Asn": "N",
    "Asp": "D",
    "Cys": "C",
    "Gln": "Q",
    "Glu": "E",
    "Gly": "G",
    "His": "H",
    "Ile": "I",
    "Leu": "L",
    "Lys": "K",
    "Met": "M",
    "Phe": "F",
    "Pro": "P",
    "Ser": "S",
    "Thr": "T",
    "Trp": "W",
    "Tyr": "Y",
    "Val": "V",
    "Ter": "*",
    "Sec": "U",
    "Pyl": "O",
}


def _protein(value):
    if not value or not (value := str(value).strip()):
        return None
    value = re.sub(r"^p\.", "", value, flags=re.IGNORECASE)
    return re.sub(
        "|".join(AA3), lambda m: AA3[m.group().title()], value, flags=re.IGNORECASE
    ).upper()


def _codes(value):
    if value is None:
        return set()
    if isinstance(value, str):
        return {x.strip() for x in value.split(",") if x.strip()}
    return set(value)


def _span(position, ref):
    return (position - 1, position) if ref == "-" else (position, position + len(ref) - 1)


def _repeat_shift_match(db_pos, db_ref, db_alt, max_right_shift, pos, ref, alt):
    shift = pos - db_pos
    if shift < 0 or shift > max_right_shift:
        return False
    if db_ref == ref == "-":
        allele, query = db_alt, alt
    elif db_alt == alt == "-":
        allele, query = db_ref, ref
    else:
        return shift == 0 and db_ref == ref and db_alt == alt
    offset = shift % len(allele)
    return query == allele[offset:] + allele[:offset]


class CravatAnnotator(BaseAnnotator):
    def setup(self):
        version = self.cursor.execute("PRAGMA user_version").fetchone()[0]
        if version != SCHEMA_VERSION:
            raise ValueError(
                f"CMA database schema {version} is unsupported; rebuild cma.sqlite (expected {SCHEMA_VERSION})"
            )
        with open(os.path.join(self.data_dir, "oncotree.json")) as handle:
            records = json.load(handle)
        self.nodes = {r["code"]: (r.get("parent"), int(r["level"])) for r in records}
        self.nodes.setdefault("TISSUE", (None, 0))
        raw = self.conf.get("depth", 1)
        self.depth = None if raw is None or str(raw).lower() == "none" else int(raw)
        if self.depth is not None and self.depth < -1:
            raise ValueError("cma.depth must be -1, non-negative, or none")
        self.requested_nodes = _codes(self.conf.get("nodes"))
        self.direct_nodes = _codes(self.conf.get("direct"))
        self.max_search_distance = int(
            self.cursor.execute(
                "SELECT value FROM metadata WHERE key='max_search_distance'"
            ).fetchone()[0]
        )

    def _ancestor(self, code, depth):
        while self.nodes[code][1] > depth:
            code = self.nodes[code][0]
        return code

    def _descendant(self, code, parent):
        while code is not None:
            if code == parent:
                return True
            code = self.nodes[code][0]
        return False

    def _match(self, data, secondary):
        pos = data["pos"]
        ref = data["ref_base"]
        alt = data["alt_base"]
        query_start, query_end = _span(pos, ref)
        rows = list(
            self.cursor.execute(
                "SELECT allele_id,position,ref,alt,max_right_shift,hugo,protein_change "
                "FROM allele WHERE chromosome=? AND position BETWEEN ? AND ?",
                (
                    data["chrom"],
                    pos - self.max_search_distance,
                    query_end + self.max_search_distance,
                ),
            )
        )
        ids = [r[0] for r in rows if _repeat_shift_match(r[1], r[2], r[3], r[4], pos, ref, alt)]
        if ids:
            return "Exact Match", ids
        gene = data.get("hugo") or data.get("gene")
        gene = str(gene).strip().upper() if gene else None
        change = _protein(data.get("achange") or data.get("hgvsp"))
        if gene and change:
            ids = [r[0] for r in rows if r[5] == gene and r[6] == change]
            if ids:
                return "Protein Change", ids
        ids = []
        for allele_id, allele_pos, allele_ref, *_rest in rows:
            allele_start, allele_end = _span(allele_pos, allele_ref)
            if allele_start <= query_end and allele_end >= query_start:
                ids.append(allele_id)
        return ("Genomic Location", ids) if ids else None

    def _coverage(self, data):
        bed = data["pos"] - 1
        row = self.cursor.execute(
            "SELECT c.end,d.direct_counts FROM coverage c JOIN coverage_counts d USING(counts_id) WHERE c.chromosome=? AND c.start<=? ORDER BY c.start DESC LIMIT 1",
            (data["chrom"], bed),
        ).fetchone()
        return (
            {}
            if row is None or row[0] <= bed
            else {str(k): int(v) for k, v in json.loads(row[1]).items()}
        )

    def annotate(self, input_data, secondary_data=None):
        matched = self._match(input_data, secondary_data)
        if matched is None:
            return None
        match, ids = matched
        marks = ",".join("?" for _ in ids)
        variants = dict(
            self.cursor.execute(
                f"SELECT oncotree_code,sum(count) FROM variant_count WHERE allele_id IN ({marks}) GROUP BY oncotree_code",
                ids,
            )
        )
        coverage = self._coverage(input_data)
        rows = []
        if self.depth is not None:
            if self.depth == -1:
                rv, rc, targets = variants, coverage, sorted(set(variants) | set(coverage))
            else:
                rv, rc = defaultdict(int), defaultdict(int)
                for code, n in variants.items():
                    rv[self._ancestor(code, self.depth)] += n
                for code, n in coverage.items():
                    rc[self._ancestor(code, self.depth)] += n
                targets = sorted(
                    {c for c, (_p, d) in self.nodes.items() if d == self.depth} | set(rv) | set(rc)
                )
            rows.extend((c, rv.get(c, 0), rc.get(c, 0)) for c in targets)
        for node in sorted(self.requested_nodes):
            rows.append(
                (
                    node,
                    sum(n for c, n in variants.items() if self._descendant(c, node)),
                    sum(n for c, n in coverage.items() if self._descendant(c, node)),
                )
            )
        existing = {r[0] for r in rows}
        rows.extend(
            (c, variants.get(c, 0), coverage.get(c, 0))
            for c in sorted(self.direct_nodes - existing)
        )
        direct_map = {
            code: [variants.get(code, 0), coverage.get(code, 0)]
            for code in sorted(set(variants) | set(coverage))
        }
        rows = [r for r in rows if r[1] > 0]
        rows.sort(key=lambda r: (-r[1], r[0]))
        return {
            "variant_count": sum(variants.values()),
            "variant_count_tissue": [list(r) for r in rows],
            "match": match,
            "direct_counts": json.dumps(direct_map, separators=(",", ":")) if direct_map else None,
        }

    def summarize_by_gene(self, hugo, input_data):
        # OpenCRAVAT calls this at report time on an instance that never ran setup().
        if self.cursor is None:
            database = os.path.join(self.data_dir, "cma.sqlite")
            self.dbconn = sqlite3.connect(f"file:{database}?mode=ro", uri=True)
            self.cursor = self.dbconn.cursor()
        rows = self.cursor.execute(
            "SELECT oncotree_code,positive_cases,cases_tested FROM gene "
            "WHERE gene=? ORDER BY positive_cases DESC,oncotree_code",
            (hugo,),
        ).fetchall()
        if not rows:
            return None
        return {
            "positive_cases": sum(int(count) for _code, count, _tested in rows),
            "gene_count": json.dumps(
                [[code, int(count), int(tested)] for code, count, tested in rows],
                separators=(",", ":"),
            ),
            "cases_tested": sum(int(tested) for _code, _count, tested in rows),
        }


if __name__ == "__main__":
    CravatAnnotator(sys.argv).run()
