"""
Architecture Validator
"""

from __future__ import annotations

from .index import RepositoryIndex


class ArchitectureValidator:

    def validate(
        self,
        index: RepositoryIndex,
    ) -> bool:

        return bool(index.graph.nodes())
