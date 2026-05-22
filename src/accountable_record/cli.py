"""Public command-line entry points."""

from accountable_record.commands.root import main

__all__ = [
    "main",
]


if __name__ == "__main__":
    raise SystemExit(main())
