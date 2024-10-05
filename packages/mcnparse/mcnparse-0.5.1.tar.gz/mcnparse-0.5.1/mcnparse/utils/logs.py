"""Log tools to stdout"""

import logging

__all__ = ["logger"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcnparse")
