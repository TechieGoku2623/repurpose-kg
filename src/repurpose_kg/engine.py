"""Gene links dated on or after the cut do not enter the time-split score.

A pair with fewer than two supporting papers abstains. It does not receive
a sharp probability.
"""

from __future__ import annotations

from typing import Mapping


class GraphError(ValueError):
    """The cut or the edge list cannot be scored."""


def score(edges: list[Mapping[str, object]], cut_year: int) -> dict[str, object]:
    if not edges:
        raise GraphError("no edges")
    parsed = [_edge(edge) for edge in edges]
    candidates = [edge for edge in parsed if edge["kind"] == "indication" and edge["year"] >= cut_year]
    if not candidates:
        raise GraphError("no indication appears on or after the cut")
    ranked = []
    for edge in candidates:
        timed = _overlap(parsed, edge["drug"], edge["disease"], cut_year, leaky=False)
        leaked = _overlap(parsed, edge["drug"], edge["disease"], cut_year, leaky=True)
        support = int(edge["support"])
        ranked.append(
            {
                "drug": edge["drug"],
                "disease": edge["disease"],
                "year": edge["year"],
                "support": support,
                "time_score": timed,
                "leaky_score": leaked,
                "decision": "abstain" if support < 2 else "rank",
            }
        )
    ranked.sort(key=lambda row: (-int(row["time_score"]), row["drug"]))
    return {"cut_year": cut_year, "candidates": ranked}


def format_report(report: dict[str, object]) -> str:
    lines = [
        "repurpose-kg",
        "",
        f"cut year: {report['cut_year']}",
        "future indications:",
    ]
    candidates = report["candidates"]
    assert isinstance(candidates, list)
    for row in candidates:
        assert isinstance(row, dict)
        lines.append(
            f"  {row['drug']} + {row['disease']}  {row['year']}  "
            f"time {row['time_score']}  leaky {row['leaky_score']}  {row['decision']}"
        )
    lines.append("")
    lines.append("time score ignores gene links from the cut year onward")
    return "\n".join(lines)


def _edge(edge: Mapping[str, object]) -> dict[str, object]:
    kind = str(edge.get("kind", ""))
    year = edge.get("year")
    if kind not in {"drug_gene", "disease_gene", "indication"}:
        raise GraphError("unknown edge kind")
    if isinstance(year, bool) or not isinstance(year, int):
        raise GraphError("year must be an integer")
    if kind == "indication":
        drug = str(edge.get("drug", "")).strip()
        disease = str(edge.get("disease", "")).strip()
        support = edge.get("support", 1)
        if not drug or not disease:
            raise GraphError("an indication needs a drug and a disease")
        if isinstance(support, bool) or not isinstance(support, int) or support < 1:
            raise GraphError("support must be a positive integer")
        return {"kind": kind, "year": year, "drug": drug, "disease": disease, "support": support}
    node = str(edge.get("node", "")).strip()
    gene = str(edge.get("gene", "")).strip()
    if not node or not gene:
        raise GraphError("a gene link needs a node and a gene")
    return {"kind": kind, "year": year, "node": node, "gene": gene}


def _overlap(
    edges: list[dict[str, object]],
    drug: object,
    disease: object,
    cut_year: int,
    leaky: bool,
) -> int:
    drug_genes = set()
    disease_genes = set()
    for edge in edges:
        year = int(edge["year"])
        if not leaky and year >= cut_year:
            continue
        if edge["kind"] == "drug_gene" and edge["node"] == drug:
            drug_genes.add(edge["gene"])
        if edge["kind"] == "disease_gene" and edge["node"] == disease:
            disease_genes.add(edge["gene"])
    return len(drug_genes & disease_genes)
