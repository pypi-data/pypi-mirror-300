"""Types hints"""

from typing import List, Tuple, Dict, TypedDict, Literal, Union, Optional, Generator
from pandas import (  # type: ignore
    DataFrame,
    StringDtype,
    Int64Dtype,
    Float64Dtype,
    BooleanDtype,
)

__all__ = [
    # Types
    "List",
    "Tuple",
    "Dict",
    "TypedDict",
    "Literal",
    "Union",
    "Optional",
    "Generator",
    "StringDtype",
    "Int64Dtype",
    "Float64Dtype",
    "BooleanDtype",
    "TallyTypes",
    "Regions",
    "Table126",
    "AllTable126",
    "TallyData",
    "AllTallyData",
    "TallyTests",
    "AllTallyTests",
    "ParsedOutput",
]

TallyTypes = Literal["2", "4", "5", "8"]


class Regions(TypedDict):
    table126: Tuple[int, int]
    tallies: Dict[str, Tuple[int, int]]


class Table126(DataFrame):
    cell: Int64Dtype
    tracks_entering: Int64Dtype
    population: Int64Dtype
    collisions: Int64Dtype
    collisions_weighted: Float64Dtype
    number_weighted_energy: Float64Dtype
    flux_weighted_energy: Float64Dtype
    average_track_weight: Float64Dtype
    average_track_length_mfp: Float64Dtype


class AllTable126(Table126):
    run: StringDtype


class TallyData(DataFrame):
    tally: Int64Dtype
    energy: Float64Dtype
    value: Float64Dtype
    re: Float64Dtype


class AllTallyData(TallyData):
    run: StringDtype


class TallyTests(DataFrame):
    tally: Int64Dtype
    mean_behavior: StringDtype
    re_value: Float64Dtype
    re_decrease: BooleanDtype
    re_rate: BooleanDtype
    vov_value: Float64Dtype
    vov_decrease: BooleanDtype
    vov_rate: BooleanDtype
    fom_value: StringDtype
    fom_behavior: StringDtype
    pdf_slope: Float64Dtype


class AllTallyTests(TallyTests):
    run: StringDtype


class ParsedOutput(TypedDict):
    table126: AllTable126
    data: AllTallyData
    tests: AllTallyTests
