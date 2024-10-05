"""Core functions for mcnparse"""

import re
import numpy as np  # type: ignore
from pandas import concat  # type: ignore
from .utils.types import (
    List,
    Tuple,
    Dict,
    Optional,
    Union,
    Regions,
    Table126,
    AllTable126,
    TallyTests,
    AllTallyTests,
    TallyData,
    AllTallyData,
    ParsedOutput,
)
from .utils.logs import logger
from .utils.serialization import serialize
from .tables import parse_table126
from .tallies import parse_tally

__all__ = ["mcnparse", "find_regions"]


REGEX: Dict[str, re.Pattern] = {
    "table126": re.compile(r".*?print table 126$"),
    "tally": re.compile(r"(?=.*1tally\s+\d+\s+nps\s*=)(?!.*\s{19}print table 30).*"),
}


def find_regions(output_lines: List[str]) -> Regions:
    """Find regions of interest in the MCNP output

    _extended_summary_

    Parameters
    ----------
    output_lines : List[str]
        MCNP output file

    Returns
    -------
    Regions
        Dictionary containing tuples with the range of regions of interest
    """
    regions: Dict[str, List[int]] = {
        key: [i for i, line in enumerate(output_lines) if pattern.match(line)]
        for key, pattern in REGEX.items()
    }
    tallies: List[int] = regions["tally"]
    tally_range: Dict[str, Tuple[int, int]] = {
        output_lines[val[0]].split()[1]: val
        for val in list(zip(tallies, tallies[1:] + [len(output_lines)]))
    }
    all_regions: Regions = {
        "table126": (regions["table126"][0], int(np.min(tallies))),
        "tallies": tally_range,
    }

    return all_regions


def parse_single(file_path: str, run_name: Union[str, None] = None) -> ParsedOutput:
    """Parse a single MCNP output file"""
    logger.info(f"Begin parsing {file_path}")
    with open(file_path, mode="rt") as conn:
        output_lines: List[str] = conn.read().split(sep="\n")

    if run_name is None:
        run_name = file_path

    regions: Regions = find_regions(output_lines)
    table126: Table126 = parse_table126(
        output_lines[regions["table126"][0] : regions["table126"][1]]
    )
    tally_locs = regions["tallies"]
    tally_info: List[Tuple[TallyData, TallyTests]] = [
        parse_tally(output_lines[tally_locs[tally][0] : tally_locs[tally][1]], tally)
        for tally in tally_locs
    ]
    tally_data: TallyData = concat([tally[0] for tally in tally_info])  # type: ignore
    tally_tests: TallyTests = concat([tally[1] for tally in tally_info])  # type: ignore
    logger.info(f"Finished parsing {file_path}")
    return {
        "table126": table126.assign(run=run_name),  # type: ignore
        "data": tally_data.assign(run=run_name),  # type: ignore
        "tests": tally_tests.assign(run=run_name),  # type: ignore
    }


def mcnparse(
    file_paths: Union[str, List[str]],
    run_names: Union[None, Union[str, List[str]]] = None,
    return_dict: Optional[bool] = False,
    save_data: Optional[bool] = True,
) -> Union[Optional[ParsedOutput], None]:
    """Parse set of MCNP output files

    Batch processing for many MCNP output files. The output JSON (either
    compressed or not) contains keys:

        - "table126"
        - "data"
        - "tests"

    For the cell population chart, the results of binned tallies, and the
    results of the 10 statistical checks for the tfc bin for each tally. All
    of these are formatted to function as DataFrames in either Python (pandas)
    or in R.

    To load in Python:

    ```py
    import json
    import pandas as pd
    with open(FILENAME, mode='rt') as conn:
        all_outputs = json.load(conn)

    table126 = pd.DataFrame(all_outputs['table126'])
    tally_data = pd.DataFrame(all_outputs['data'])
    statistical_checks = pd.DataFrame(all_outputs['tests'])
    ```

    To load in R:

    ```r
    library(jsonlite)
    all_outputs <- fromJSON(FILENAME)
    table126 = as.data.frame(all_outputs[["table126"]])
    tally_data = as.data.frame(all_outputs[["data"]])
    statistical_checks = as.data.frame(all_outputs[["tests"]])
    ```

    Parameters
    ----------
    file_paths : Union[str, List[str]]
        Paths to mcnp output files
    run_names : Union[None, Union[str, List[str]]], optional
        Names for corresponding runs, by default None. If None, the filename
        will be used
    compress : bool, optional
        If true, save to a .tar.gz file that uncompresses to json. If false,
        save to a json file, by default True.
    """
    if isinstance(file_paths, str):
        file_paths = [file_paths]
    if run_names is None:
        run_names = [file.replace(".o", "") for file in file_paths]
    if len(file_paths) != len(run_names):
        logger.warning(
            "None equal number of run names. Will use file_paths as run names"
        )
        run_names = [file.replace(".o", "") for file in file_paths]

    parsed_data: List[ParsedOutput] = [
        parse_single(file, run) for run, file in list(zip(run_names, file_paths))
    ]
    logger.info("Organizing all the data")
    data: AllTallyData = concat(
        [parsed["data"] for parsed in parsed_data]  # type: ignore
    )
    tests: AllTallyTests = concat(
        [parsed["tests"] for parsed in parsed_data]  # type: ignore
    )
    table126: AllTable126 = concat(
        [parsed["table126"] for parsed in parsed_data]  # type: ignore
    )
    output: ParsedOutput = {"data": data, "tests": tests, "table126": table126}
    if save_data:
        serialize(output)  # type: ignore
    if return_dict:
        return output
    return None
