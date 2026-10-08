<div align="center">

# repurpose-kg

**Drug-repurposing candidates from a biomedical graph, scored only on links that did not exist yet.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Status:** problem brief. The question and the measurement are written here. An implementation is not in this repository yet.

</div>

---

## The problem

A knowledge graph of drugs, genes, and diseases will happily predict a link the graph already used to train itself. Random edge splits leak the future into the past: a 2024 indication helps "predict" a 2019 one, and the leaderboard looks solved.

Repurposing is a claim about time. The only honest test is a cut date. Train on the graph as it stood, then score edges that appeared later. Anything else is a reconstruction of the literature, not a candidate list.

## The measurement I would trust

| Rule | Why |
| --- | --- |
| Time split | Training edges are strictly older than test edges |
| No node feature from the future | A disease embedding fit on the full graph is leakage |
| Rank, plus a baseline | A simple co-occurrence baseline sits next to the model |
| Abstention on weak support | A novel-looking pair with one paper does not get a sharp probability |

Hits without the cut date are not results. A demo that highlights a famous repurposing story already in the training era is not a result.

## What this repository is

The evaluation rule for a repurposing graph, written down before a model is fit. Phenotype-side ranking of genes and diseases, which is a different question, is in [phenorank](https://github.com/TechieGoku2623/phenorank). This repository does not ship a trained link predictor.

## Author

**Choppa Devasai Pranatheswar** · [LinkedIn](https://www.linkedin.com/in/devasai-pranatheswar)
