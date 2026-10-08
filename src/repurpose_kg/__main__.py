"""Score two future indications. One depends on a gene link that did not exist yet."""

from __future__ import annotations

from .engine import format_report, score

EDGES = [
    {"kind": "drug_gene", "node": "metformin", "gene": "AMPK", "year": 2016},
    {"kind": "drug_gene", "node": "metformin", "gene": "GDF15", "year": 2023},
    {"kind": "disease_gene", "node": "aging", "gene": "AMPK", "year": 2017},
    {"kind": "disease_gene", "node": "aging", "gene": "GDF15", "year": 2018},
    {"kind": "indication", "drug": "metformin", "disease": "aging", "year": 2021, "support": 4},
    {"kind": "drug_gene", "node": "compound-x", "gene": "NEW", "year": 2022},
    {"kind": "disease_gene", "node": "fibrosis", "gene": "NEW", "year": 2022},
    {"kind": "indication", "drug": "compound-x", "disease": "fibrosis", "year": 2024, "support": 1},
]


def main() -> int:
    print(format_report(score(EDGES, 2020)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
