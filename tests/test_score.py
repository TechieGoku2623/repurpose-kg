"""A gene link from after the cut raises the leaky score and not the time score."""

from __future__ import annotations

import unittest

from repurpose_kg import GraphError, score
from repurpose_kg.__main__ import EDGES


class ScoreTests(unittest.TestCase):
    def test_future_gene_link_is_excluded_from_the_time_score(self) -> None:
        report = score(EDGES, 2020)
        candidates = report["candidates"]
        assert isinstance(candidates, list)
        metformin = next(row for row in candidates if row["drug"] == "metformin")
        assert isinstance(metformin, dict)
        self.assertEqual(metformin["time_score"], 1)
        self.assertEqual(metformin["leaky_score"], 2)
        self.assertEqual(metformin["decision"], "rank")

    def test_one_paper_abstains(self) -> None:
        report = score(EDGES, 2020)
        candidates = report["candidates"]
        assert isinstance(candidates, list)
        weak = next(row for row in candidates if row["drug"] == "compound-x")
        assert isinstance(weak, dict)
        self.assertEqual(weak["decision"], "abstain")
        self.assertEqual(weak["time_score"], 0)
        self.assertEqual(weak["leaky_score"], 1)

    def test_no_future_indication_raises(self) -> None:
        early = [edge for edge in EDGES if edge["kind"] != "indication"]
        early.append({"kind": "indication", "drug": "metformin", "disease": "aging", "year": 2018, "support": 4})
        with self.assertRaises(GraphError):
            score(early, 2020)


if __name__ == "__main__":
    unittest.main()
