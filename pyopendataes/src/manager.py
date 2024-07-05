import requests
import pandas as pd
from .opendataset import OpenDataSet

class Manager:
    def __init__(self) -> None:
        self.url = "http://datos.gob.es/apidata"    

    def list_datasets(self, start_page=0, pages_limit=1):
        """Get the collection of datasets from the portal. The collection is huge, so be sure to limit the number of pages to download.

        Args:
            start_page (int, optional): Page to start the download from. Defaults to 0.
            pages_limit (int, optional): Limit of pages to download. Defaults to 1.

        Returns:
            pd.DataFrame: Pandas dataframe with the metadata of the datasets.
        """        
        start_url = f'{self.url}/catalog/dataset.json?_page={start_page}'	
        all_datasets = []
        i = start_page
        while start_url and i<pages_limit+start_page:
            # Download the page
            response = requests.get(start_url)
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

    def _create_dataset(self, dataset_meta: dict) -> OpenDataSet:
        dataset = OpenDataSet(url=dataset_meta["_about"])
        dataset._extract_from_meta(dataset_meta)

        return dataset
    
