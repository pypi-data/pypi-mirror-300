"""Utility functions for MCNParse"""

from typing import List
from re import Pattern
from functools import lru_cache

__all__ = [
    "split_and_clean",
    "parse_scientific",
    "get_regex_index",
]


@lru_cache(maxsize=None)
def parse_scientific(value: str) -> float:
    """Convert scientific notation to float"""
    return float(value.replace("E", "e"))


def split_and_clean(line: str) -> List[str]:
    """Split string into each word and remove whitespace"""
    return [item for item in line.split() if item]


def get_regex_index(lines: List[str], pattern: Pattern) -> List[int]:
    """Get indices for matches in list of strings"""
    return [i for i, line in enumerate(lines) if pattern.match(line)]
