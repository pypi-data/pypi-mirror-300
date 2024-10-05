"""Deserialize MCNParse files"""

from pandas import read_json
from .types import DataFrame, Union, Literal, Optional

__all__ = ["deserialize"]
Languages = Literal["python", "r"]


def deserialize(
    file_path: str, lang: Optional[Languages] = "python"
) -> Union[DataFrame, str]:
    """Open mcnparse tables

    Parameters
    ----------
    file_path : str
        Path to .json.gz file of interest

    Returns
    -------
    DataFrame
        Deserialized dataframe
    """
    if lang == "r":
        return """\
install.packages(c("jsonlite", "R.utils"))
library(jsonlite)
library(R.utils)

open_r <- function(file_path) {
  # Decompress the .gz file and read its content
  json_data <- gzcon(file(file_path, "rb")) %>%
               readLines() %>%
               paste(collapse = "")

  # Parse the JSON data
  parsed_data <- fromJSON(json_data, simplifyVector = FALSE)

  return(as.data.frame(parsed_data))
}
"""
    elif lang == "python":
        return read_json(file_path, orient="records", lines=True, compression="gzip")

    raise ValueError(f"Unknown language: {lang} provided")
