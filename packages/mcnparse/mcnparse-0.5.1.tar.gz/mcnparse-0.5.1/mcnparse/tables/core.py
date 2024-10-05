"""Functions and utilities for parsing MCNP tables"""

import warnings
from pandas import DataFrame  # type: ignore
from ..utils.types import (
    List,
    Union,
    Int64Dtype,
    Float64Dtype,
    Table126,
)
from ..utils.functions import split_and_clean, parse_scientific

__all__ = ["parse_table126"]


def parse_table_126_row(line: str) -> List[Union[int, float]]:
    items = split_and_clean(line)
    return [
        int(items[1]),  # cell
        int(items[2]),  # tracks_entering
        int(items[3]),  # population
        int(items[4]),  # collisions
        parse_scientific(items[5]),  # collisions_weighted
        parse_scientific(items[6]),  # number_weighted_energy
        parse_scientific(items[7]),  # flux_weighted_energy
        parse_scientific(items[8]),  # average_track_weight
        parse_scientific(items[9]),  # average_track_length_mfp
    ]


def parse_table126(lines: List[str]) -> Table126:
    try:
        blank_lines = [i for i, line in enumerate(lines) if line.strip() == ""]
        data_start = blank_lines[1] + 1
        data_end = blank_lines[2]
        table126 = Table126(
            DataFrame(
                data=[parse_table_126_row(line) for line in lines[data_start:data_end]],
                columns=[
                    "cell",
                    "tracks_entering",
                    "population",
                    "collisions",
                    "collisions_weighted",
                    "number_weighted_energy",
                    "flux_weighted_energy",
                    "average_track_weight",
                    "average_track_length_mfp",
                ],
            ).astype(
                {
                    "cell": Int64Dtype(),
                    "tracks_entering": Int64Dtype(),
                    "population": Int64Dtype(),
                    "collisions": Int64Dtype(),
                    "collisions_weighted": Float64Dtype(),
                    "number_weighted_energy": Float64Dtype(),
                    "flux_weighted_energy": Float64Dtype(),
                    "average_track_weight": Float64Dtype(),
                    "average_track_length_mfp": Float64Dtype(),
                }
            )
        )
    except IndexError as e:
        warnings.warn(f"Could not parse Table 126\n{str(e)}")
        table126 = Table126()

    return table126
