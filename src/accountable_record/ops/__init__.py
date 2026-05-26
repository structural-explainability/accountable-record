"""Operational implementation layers for Accountable Record.

WHY: The public mental model of the repository is the staged pipeline. This
package contains the behind-the-scenes operations that pipeline stages delegate
to: checks, exporters, generators, resolvers, and validators.

Keep this package initializer intentionally quiet. Import concrete operations
from their specific subpackages so dependencies remain explicit and searchable.
"""

__all__: list[str] = []
