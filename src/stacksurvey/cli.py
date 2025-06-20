"""Command-line interface for stacksurvey package."""

import sys
from typing import List, Optional

from .__main__ import main


def run(args: Optional[List[str]] = None) -> int:
    """Run the CLI with the given arguments."""
    return main(args)


if __name__ == "__main__":
    sys.exit(run())
