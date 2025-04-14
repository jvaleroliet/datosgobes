import requests
import pandas as pd
from .opendataset import OpenDataSet

class Manager:
    def __init__(self) -> None:
        self.url = "http://datos.gob.es/apidata" 
        self._search_result = None   
        ## based on https://stackoverflow.com/questions/41946166/requests-get-returns-403-while-the-same-url-works-in-browser
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

    def _list_datasets(self, start_page=0, pages_limit=1):
        """Get the collection of datasets from the portal. The collection is huge, so be sure to limit the number of pages to download.

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
            response = requests.get(start_url, headers=self.headers)
            data = response.json()

            # Extract and normalize the datasets
            page_datasets = data["result"]["items"]

            # Add the datasets to the collection
            all_datasets += page_datasets

            # Obtain the URL for the next page
            if "next" in data["result"].keys():
                next_page_url = data["result"]["next"]
            else:
                next_page_url = None
            start_url = next_page_url if next_page_url else None
            if pages_limit != None:
                i+=1
        return all_datasets

    def _query_datasets(self, query: str, start_page=0, pages_limit=1):
        """Get the collection of datasets from the portal based on a string query. The collection is huge, so be sure to limit the number of pages to download.

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
            response = requests.get(start_url, headers=self.headers)
            data = response.json()

            # Extract and normalize the datasets
            page_datasets = data["result"]["items"]

            # Add the datasets to the collection
            all_datasets += page_datasets

            # Obtain the URL for the next page
            next_page_url = data["result"]["next"]
            start_url = next_page_url if next_page_url else None
            if pages_limit != None:
                i+=1
        return all_datasets

    
    def get_datasets(self, start_page=0, pages_limit=1) -> list:
        if not self._search_result:
            self._search_result = self._list_datasets(start_page, pages_limit)

        datasets = []
        for dataset in self._search_result:
            opendataset = self._create_dataset(dataset)
            datasets.append(opendataset)
        return datasets
    
    def search_datasets(self, query: str, start_page=0, pages_limit=1) -> list:
        self._search_result = self._query_datasets(query, start_page, pages_limit)
        datasets = []
        for dataset in self._search_result:
            opendataset = self._create_dataset(dataset)
            datasets.append(opendataset)
        return datasets
    
    def _create_dataset(self, dataset_meta: dict) -> OpenDataSet:
        dataset = OpenDataSet(url=dataset_meta["_about"])
        return dataset
    
    def get_dataset(self, id: str) -> OpenDataSet:
        dataset = OpenDataSet(url=f'{self.url}/catalog/dataset/{id}')
        return dataset
