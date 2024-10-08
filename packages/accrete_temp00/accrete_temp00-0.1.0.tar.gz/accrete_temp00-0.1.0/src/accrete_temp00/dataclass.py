"""This file represents Dataset objects.

This file contains the following classes:
    * Dataset (abstract base class)
    * ExampleDataset which is a subclass of Dataset
"""

from abc import ABC, abstractmethod

import pandas as pd
import pandera as pa
import pandera.io


class Dataset(ABC):
    """This is an base class that represents data used by models at Accrete."""

    @abstractmethod
    def load_and_validate(self):
        """Loads schema class for data field."""
        pass


class ExampleDataset(Dataset):
    """This is an example class that contains a single pandas.DataFrame.

    Attributes:
    dataFrame (pandas.DataFrame): contains the DataFrame that stores data.
    """

    dataFrame: pd.DataFrame

    def __init__(self, dataFrame_path: str, schema_path: str) -> None:
        """Initialize the Dataset class."""
        self.dataFrame = self.load_and_validate(dataFrame_path, schema_path)

    def load_and_validate(
        self, dataFrame_path: str, schema_path: str
    ) -> pd.DataFrame:
        """Load the Dataframe and validate with pandera.DataFrameSchema."""
        dataFrame = pd.read_csv(dataFrame_path)
        schema = pa.io.from_yaml(schema_path)
        schema.validate(dataFrame)
        return dataFrame

    def infer_and_save_schema(self, schema_path: str = None) -> None:
        """Infer schema from data and save to path.

        Create pandera.DataFrameSchema from self.dataFrame and write
        pandera.DataFrameSchema to yaml file at input path.
        """
        schema = pa.infer_schema(self.dataFrame)
        schema.to_yaml(schema_path)
