"""This module contains the manager class to interact with the portal"""

import requests
from .opendataset import OpenDataSet

class Manager:
    """Class manager to interact with the portal.
    """
    def __init__(self) -> None:
        self.url = "http://datos.gob.es/apidata"
        self._search_result = None

    def _list_datasets(self, start_page=0, pages_limit=1):
        """Aux function to get the collection of datasets from the portal. The collection is huge,
        so be sure to limit the number of pages to download.

        Args:
            start_page (int, optional): Page to start the download from. Defaults to 0.
            pages_limit (int, optional): Limit of pages to download. Defaults to 1.

        Returns:
            list of the metadata of the datasets.
        """
        start_url = f'{self.url}/catalog/dataset.json?_page={start_page}'
        all_datasets = []
        i = start_page
        while start_url and i<pages_limit+start_page:
            # Download the page
            response = requests.get(start_url, timeout=10)
            data = response.json()

            # Extract and normalize the datasets
            page_datasets = data["result"]["items"]

            # Add the datasets to the collection
            all_datasets += page_datasets

            # Obtain the URL for the next page
            next_page_url = data["result"]["next"]
            start_url = next_page_url if next_page_url else None
            if pages_limit is not None:
                i+=1
        return all_datasets

    def _query_datasets(self, query: str, start_page=0, pages_limit=1):
        """Aux function to get the collection of datasets from the portal based on a string query.
        The collection is huge, so be sure to limit the number of pages to download.

        Args:
            query (str): String to search in the datasets.
            start_page (int, optional): Page to start the download from. Defaults to 0.
            pages_limit (int, optional): Limit of pages to download. Defaults to 1.

        Returns:
            list of the metadata of the datasets.
        """
        start_url = f'{self.url}/catalog/dataset/title/{query}.json?_page={start_page}'
        all_datasets = []
        i = start_page
        while start_url and i<pages_limit+start_page:
            # Download the page
            response = requests.get(start_url, timeout=10)
            data = response.json()

            # Extract and normalize the datasets
            page_datasets = data["result"]["items"]

            # Add the datasets to the collection
            all_datasets += page_datasets

            # Obtain the URL for the next page
            next_page_url = data["result"]["next"]
            start_url = next_page_url if next_page_url else None
            if pages_limit is not None:
                i+=1
        return all_datasets

    def get_datasets(self, start_page=0, pages_limit=1) -> list:
        """Function to list the collection of datasets from the portal. 
        The collection is huge, so be sure to limit the number of pages to download.

        Args:
            start_page (int, optional): Page to start the download from. Defaults to 0.
            pages_limit (int, optional): Limit of pages, each contains 10 results. Defaults to 1.

        Returns:
            list: list of OpenDataSet objects.
        """
        if not self._search_result:
            self._search_result = self._list_datasets(start_page, pages_limit)

        datasets = []
        for dataset in self._search_result:
            opendataset = self._create_dataset(dataset)
            datasets.append(opendataset)
        return datasets

    def search_datasets(self, query: str, start_page=0, pages_limit=1) -> list:
        """Search datasets in the portal by a string query.

        Args:
            query (str): String query to search.
            start_page (int, optional): Page to start the download from. Defaults to 0.
            pages_limit (int, optional): Limit of pages, each contains 10 results. 
            Defaults to 1.

        Returns:
            list: list of OpenDataSet objects.
        """
        self._search_result = self._query_datasets(query, start_page, pages_limit)
        datasets = []
        for dataset in self._search_result:
            opendataset = self._create_dataset(dataset)
            datasets.append(opendataset)
        return datasets

    def _create_dataset(self, dataset_meta: dict) -> OpenDataSet:
        """Aux function to create a OpenDataSet object from a dataset metadata.

        Args:
            dataset_meta (dict): Metada of a dataset retrieved by the 
            search_datasets or get_datasets methods

        Returns:
            OpenDataSet: OpenDataSet object.
        """
        dataset = OpenDataSet(url=dataset_meta["_about"])
        return dataset

    def get_dataset(self, id: str) -> OpenDataSet:
        """Function to create an OpenDataSet object from a dataset id.

        Args:
            id (str): Dataset id from the portal.

        Returns:
            OpenDataSet: OpenDataSet object.
        """
        dataset = OpenDataSet(url=f'{self.url}/catalog/dataset/{id}')
        return dataset
