import os
import gzip
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import pyarrow as pa
import pyarrow.parquet as pq
from .logs import logger
from .types import Dict, Optional, Generator, DataFrame


def chunk_generator(
    df: DataFrame, chunk_size: int
) -> Generator[str, None, None]:
    """Generate chunks for dataframe serialization"""
    total_rows = len(df)
    for i in range(0, total_rows, chunk_size):
        yield df.iloc[i : i + chunk_size].to_json(orient="records", lines=True)


def serialize_dataframe(
    df: DataFrame,
    filename: str,
    directory: str,
    chunk_threshold: Optional[int] = 100000,
) -> None:
    """Serialize dataframes from MCNP output"""
    filepath = os.path.join(directory, filename)
    total_elements = df.size

    if chunk_threshold and total_elements > chunk_threshold:
        logger.warning(
            f"Dataset {filename} exceeds {chunk_threshold} elements. Chunking will be applied."
        )
        with gzip.open(filepath + ".json.gz", "wt", encoding="utf-8") as f:
            for chunk in chunk_generator(df, chunk_threshold):
                f.write(chunk)
    else:
        df.to_json(filepath + ".json.gz", orient="records", lines=True, compression="gzip")

    # with open(filepath + ".parquet", mode='wb') as conn:
    #     df.to_parquet(conn, compression='gzip')

    # with pa.OSFile(filepath + ".parquet", "wb") as conn:
    #     pq.write_table(pq.Table.from_pandas(df), conn, compression="gzip")

    logger.info(f"Serialized {filename} (Total elements: {total_elements})")


def serialize(
    data: Dict[str, DataFrame],
    chunk_threshold: Optional[int] = 100000,
) -> None:
    """Serialize MCNP output Data

    Parameters
    ----------
    data : Dict[str, DataFrame]
        Data from MCNP output files to be saved
    chunk_threshold : Optional[int], optional
        Threshold to chunk dataframe at, by default 100000
    """
    directory = f"mcnp_out_{ datetime.now().strftime("%Y-%m-%d_%H%M")}"
    os.makedirs(directory, exist_ok=True)
    logger.info(f"Starting serialization process to directory: {directory}")

    def process_dataframe(key: str, df: DataFrame) -> None:
        filename = f"{key}"
        serialize_dataframe(df, filename, directory, chunk_threshold)

    with ThreadPoolExecutor() as executor:
        executor.map(
            lambda item: process_dataframe(item[0], item[1]), data.items()
        )

    logger.info(
        f"Serialization complete. Total DataFrames processed: {len(data)}"
    )
