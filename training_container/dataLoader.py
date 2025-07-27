import pandas as pd
import json
import xml.etree.ElementTree as ET
from typing import Union, List, Dict, Any


class DataLoader:
    """
    A service to load data from various sources and formats into a pandas DataFrame.
    """

    def load_data(self, data_source: Union[str, List[Dict[str, Any]], Dict[str, List[Any]]]) -> pd.DataFrame:
        """
        Loads data from the given source.

        The source can be a file path (for .json, .xml, .csv) or an in-memory
        object (list of dicts or dict of lists).

        Args:
            data_source: The data source to load from.

        Returns:
            A pandas DataFrame containing the loaded data.

        Raises:
            ValueError: If the file format is not supported.
            TypeError: If the data_source type is not supported.
        """
        if isinstance(data_source, str):
            if data_source.endswith('.json'):
                return self._from_json_file(data_source)
            elif data_source.endswith('.xml'):
                return self._from_xml_file(data_source)
            elif data_source.endswith('.csv'):
                return pd.read_csv(data_source)
            else:
                raise ValueError(f"Unsupported file format for {data_source}. Supported formats are .json, .xml, .csv.")
        elif isinstance(data_source, list):
            return self._from_list_of_dicts(data_source)
        elif isinstance(data_source, dict):
            return self._from_dict_of_lists(data_source)
        else:
            raise TypeError(
                "Unsupported data source type. Please provide a file path, a list of dictionaries, or a dictionary of lists.")

    def _from_json_file(self, file_path: str) -> pd.DataFrame:
        print(f"Loading data from JSON file: {file_path}", flush=True)
        with open(file_path, 'r') as f:
            data = json.load(f)
        return pd.DataFrame(data)

    def _from_xml_file(self, file_path: str) -> pd.DataFrame:
        print(f"Loading data from XML file: {file_path}", flush=True)
        try:
            # pandas.read_xml is powerful and requires 'lxml'
            return pd.read_xml(file_path)
        except Exception as e:
            print(f"pandas.read_xml failed: {e}. Falling back to a basic XML parser.", flush=True)
            tree = ET.parse(file_path)
            root = tree.getroot()
            data = []
            for item in root:
                record = {child.tag: child.text for child in item}
                data.append(record)
            return pd.DataFrame(data)

    def _from_list_of_dicts(self, data: List[Dict[str, Any]]) -> pd.DataFrame:
        print("Loading data from a list of dictionaries.", flush=True)
        return pd.DataFrame(data)

    def _from_dict_of_lists(self, data: Dict[str, List[Any]]) -> pd.DataFrame:
        print("Loading data from a dictionary of lists.", flush=True)
        return pd.DataFrame(data)