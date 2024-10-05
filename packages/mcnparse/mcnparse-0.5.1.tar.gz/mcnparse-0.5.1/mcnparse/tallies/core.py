"""Functions and utilities for parsing binned mcnp tallies"""

import re

# import logging
# import warnings
from pandas import DataFrame  # type: ignore
from ..utils.types import (
    List,
    Tuple,
    BooleanDtype,
    Int64Dtype,
    Float64Dtype,
    StringDtype,
    TallyTests,
    TallyData,
)
from ..utils.functions import parse_scientific, get_regex_index


__all__ = ["parse_tally"]

STAT_CHECK = re.compile(r"\s+results of 10 statistical checks")
SURFACE = re.compile(r"\s+surface\s+\d+")
CELL = re.compile(r"\s+cell\s+\d+")
POINT_DETECTOR = re.compile(r" detector located at x,y,z = ")
RING_DETECTOR = re.compile(r" detector symmetric about ")
END_BINS = re.compile(r"\s+total\s+\d+\.\d+E[+-]\d+\s+\d+\.\d+\s*$")


def parse_bin_line(line: str) -> List[float]:
    """Convert line of binned values to list of values

    Parameters
    ----------
    line : str
        Single line in set of binned values

    Returns
    -------
    List[float]
        List containing the bin, value, and uncertainty
    """
    line_split: List[str] = line.split()
    return [
        parse_scientific(line_split[0]),
        parse_scientific(line_split[1]),
        float(line_split[2]),
    ]


def parse_bin_lines(lines: List[str], name: int) -> TallyData:
    """Parse whole set of energy bins to dataframe

    _extended_summary_

    Parameters
    ----------
    lines : List[str]
        Lines that compose the energy bin values
    name : int
        Name of the tally (the number)

    Returns
    -------
    TallyData
        DataFrame with the binned values
    """
    out = DataFrame(
        data=[parse_bin_line(line) for line in lines],
        columns=["energy", "value", "re"],
    )
    out = out.assign(tally=name)[["tally", "energy", "value", "re"]]

    out = out.astype(
        {
            "tally": Int64Dtype(),
            "energy": Float64Dtype(),
            "value": Float64Dtype(),
            "re": Float64Dtype(),
        }
    )
    return out  # type: ignore


def parse_surface_tally(lines: List[str], name: str) -> TallyData:
    """Parser for F1 and F2 tallies"""
    data = lines[
        (2 + get_regex_index(lines, SURFACE)[0]) : get_regex_index(lines, END_BINS)[0]
    ]
    return parse_bin_lines(data, int(name))


def parse_cell_tally(lines: List[str], name: str) -> TallyData:
    """Parser for F4, F6, F7, and F8 tallies"""
    data = lines[
        (2 + get_regex_index(lines, CELL)[0]) : get_regex_index(lines, END_BINS)[0]
    ]
    return parse_bin_lines(data, int(name))


def parse_f5(lines: List[str], name: str) -> TallyData:
    """Parser for F5 tallies"""
    start_points = get_regex_index(lines, POINT_DETECTOR) + get_regex_index(
        lines, RING_DETECTOR
    )
    end_points = get_regex_index(lines, END_BINS)
    # uncollided = len(start_points) == 2

    data = parse_bin_lines(lines[start_points[0] + 2 : end_points[0]], int(name))

    # if uncollided:
    #     data = concat(
    #         [
    #             data,
    #             parse_bin_lines(
    #                 lines[start_points[1] + 3 : end_points[1]], int(name) * 1000
    #             ),
    #         ]
    #     )

    return data


def parse_statistical_checks(lines: List[str], name: str) -> TallyTests:
    """Parser for 10 statistical checks"""

    stat_results = lines[get_regex_index(lines, STAT_CHECK)[0] + 6].split()[1:]
    out = DataFrame(
        data=[
            [stat_results[0]],
            [float(stat_results[1])],
            [stat_results[2] == "yes"],
            [stat_results[3] == "yes"],
            [float(stat_results[4])],
            [stat_results[5] == "yes"],
            [stat_results[6] == "yes"],
            [stat_results[7]],
            [stat_results[8]],
            [float(stat_results[9])],
        ],
        index=[
            "mean_behavior",
            "re_value",
            "re_decrease",
            "re_rate",
            "vov_value",
            "vov_decrease",
            "vov_rate",
            "fom_value",
            "fom_behavior",
            "pdf_slope",
        ],
    ).T
    out = out.assign(tally=int(name))[
        [
            "tally",
            "mean_behavior",
            "re_value",
            "re_decrease",
            "re_rate",
            "vov_value",
            "vov_decrease",
            "vov_rate",
            "fom_value",
            "fom_behavior",
            "pdf_slope",
        ]
    ]
    out = out.astype(
        {
            "tally": Int64Dtype(),
            "mean_behavior": StringDtype(),
            "re_value": Float64Dtype(),
            "re_decrease": BooleanDtype(),
            "re_rate": BooleanDtype(),
            "vov_value": Float64Dtype(),
            "vov_decrease": BooleanDtype(),
            "vov_rate": BooleanDtype(),
            "fom_value": StringDtype(),
            "fom_behavior": StringDtype(),
            "pdf_slope": Float64Dtype(),
        }
    )
    return out  # type: ignore


def parse_tally(lines: List[str], name: str) -> Tuple[TallyData, TallyTests]:
    """Parse Tally Data and Statistical Checks

    _extended_summary_

    Parameters
    ----------
    lines : List[str]
        Lines of MCNP output corresponding to the specific tally
    name : str
        String representation of the tally

    Returns
    -------
    Tuple[TallyData, TallyTests]
        Tally data as a dataframe and the statistical checks
    """
    tally_tests: TallyTests = parse_statistical_checks(lines, name)
    tally_kind: str = list(name)[-1]
    tally_data: TallyData = {
        "1": parse_surface_tally,
        "2": parse_surface_tally,
        "4": parse_cell_tally,
        "5": parse_f5,
        "6": parse_cell_tally,
        "7": parse_cell_tally,
        "8": parse_cell_tally,
    }[tally_kind](lines, name)
    return tally_data, tally_tests
