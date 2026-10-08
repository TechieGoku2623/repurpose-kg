"""Score drug-disease links using only edges that already existed."""

from .engine import GraphError, score

__all__ = ["GraphError", "score"]
