"""Run as a module.

uv run python -m accountable_record [COMMAND] [OPTIONS]
"""

from accountable_record.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
