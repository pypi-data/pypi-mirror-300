"""This file represents dataclasses.

This file contains the following classes:
    * Data
    * DatabaseData
    * FileData
    * PandasData
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable

import pandas as pd
import pandera as pa
import pandera.io


class Data(ABC):
    """This is an base class that represents data used by models at Accrete."""

    @abstractmethod
    def initialize_database(self) -> None:
        """An abstract function that initialize database."""
        pass

    @abstractmethod
    def get_data(self) -> None:
        """An abstract function that returns the data."""
        pass

    @abstractmethod
    def initialize_schema(self) -> None:
        """An abstract function that initialize data schema."""
        pass


class DatabaseData(Data):
    """This is an base class that represents data read from a database.

    Application engineer TODO: implement this class.
    """

    pass


class FileData(Data):
    """This is an base class that represents data read from file."""

    pass


class PandasData(FileData):
    """This is a class that represents data read using pandas."""

    def __init__(self, df_path: str, schema_path: str) -> None:
        """Initialize the class with data and schema.

        Args:
            df_path: Path to the data file.
            schema_path: Path to where the schema is stored.
        """
        self.initialize_database(df_path)
        self.initialize_schema(schema_path)

    def initialize_database(self, path: str | Path) -> None:
        """Iinitialize database from file path.

        Args:
            path: Path to the data file.
        """
        # self.df = pd.read_parquet(path)e
        if isinstance(path, str):
            path = Path(path)

        if path.suffix == ".parquet":
            self.df = pd.read_parquet(path)
        elif path.suffix == ".csv" or path.suffix == ".txt":
            self.df = pd.read_csv(path)
        elif path.suffix == ".json":
            self.df = pd.read_json(path)
        else:
            raise ValueError(f"Unsupported file extension: {path.suffix}")

    def get_data(self, remapping: dict | Callable = None) -> pd.DataFrame:
        """Return the data in its DataFrame representation.

        Args:
            remapping: A map of column names in the data to names
                used by the code.

        Returns:
            pd.DataFrame: DataFrame representation of the data.
        """
        df = self.df.copy()
        self.schema.validate(df)
        if remapping:
            df.rename(columns=remapping, inplace=True)
        return df

    def initialize_schema(self, path: str) -> None:
        """Initialize dataframe schema.

        Args:
            path: Path to where the schema is stored.
        """
        self.schema = pa.io.from_yaml(path)


def do_inference(data: Data, remapper: dict | Callable = None) -> pd.DataFrame:
    """Initialize dataframe schema.

    Args:
    data: data to do inference on.
    remapper: A map of column names in the data to names
        used by the code.

    Returns:
        pd.DataFrame: DataFrame representation of inference data.
    """
    return data.get_data(remapper)
