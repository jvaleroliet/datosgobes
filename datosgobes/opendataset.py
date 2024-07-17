"""This module contains the OpenDataSet and Distribution classes."""

import requests
from .data_download import download_data


class OpenDataSet:
    """OpenDataSet class is the core class of the datosgobes package.
    It represents a dataset from the datos.gob.es catalog, 
    and provides methods to access its metadata and download its distributions.
    """
    def __init__(self, url:str):
        self.url = url
        self.id = url.split('/')[-1]
        # self.metadata = {}

    def __repr__(self):
        return f"OpenDataSet('{self.id}')"

    @property
    def metadata(self):
        """Fetch metadata from the API and store it in the metadata attribute."""
        response = requests.get(
            f"http://datos.gob.es/apidata/catalog/dataset/{self.id}",
            timeout=10
        )
        return response.json()["result"]["items"][0]

    @property
    def publisher_data_url(self):
        """Returns the URL of the publisher's data."""
        return self.metadata.get('identifier')

    @property
    def title(self):
        """Extract the title of the dataset, in all languages available."""
        titles = {d['_lang']: d['_value'] for d in self.metadata.get('title', [])}
        return titles

    @property
    def description(self):
        """Extract the description of the dataset, in all languages available."""
        descriptions = {d['_lang']: d['_value'] for d in self.metadata.get('description', [])}
        return descriptions

    @property
    def keywords(self):
        """Group keywords by language and remove duplicates."""
        keywords = {}
        for entry in self.metadata.get('keyword', []):
            lang_code = entry['_lang']
            keyword = entry['_value']
            keywords.setdefault(lang_code, set()).add(keyword)
        return {lang: list(values) for lang, values in keywords.items()}

    @property
    def distributions(self):
        """
        Returns a list of Distribution objects, each containing information
        for a single distribution.
        """
        distributions = self.metadata.get('distribution', [])
        distribution_objects = []
        for distribution_data in distributions:
            distribution_objects.append(Distribution(distribution_data))
        return distribution_objects

    def get_distribution_by_format(self, format):
        """
        Returns the distribution information for a specific format (e.g., text/csv).
        """
        matched_distributions = []
        for distribution in self.distributions:
            if distribution.format == format:
                matched_distributions.append(distribution)
        return matched_distributions

class Distribution:
    """ Represents a distribution of a dataset. 
    A dataset can have multiple distributions, each with its own access URL and format.
    Each distribution can be downloaded and if possible its data 
    can be accessed as a pandas DataFrame.
    """
    def __init__(self, metadata):
        self.metadata = metadata

    def __repr__(self):
        return f"Distribution(accessURL={self.access_url}, " \
        f"format={self.format}, titles={self.titles})"

    @property
    def access_url(self):
        """Urls to access the distribution."""
        return self.metadata.get('accessURL')

    @property
    def byte_size(self):
        """ Size of the distribution in bytes."""
        return self.metadata.get('byteSize')

    @property
    def format(self):
        """ Format of the distribution."""
        return self.metadata.get('format')['value']

    @property
    def titles(self):
        """ Extract title information for all languages available."""
        return {d['_lang']: d['_value'] for d in self.metadata.get('title', [])}

    def download_data(self, output_file=None):
        """
        Downloads the data from the distribution URL and optionally saves it
        to a file or attempts to load it as a pandas DataFrame.

        This method utilizes the download_data function from the data_download module.

        Args:
            output_file (str, optional): Path to the file where 
                downloaded data should be saved. Defaults to None.

        Returns:
            pandas.DataFrame | bytes | None: The loaded DataFrame on success, 
                raw bytes on unknown format, or None on errors.
        """
        return download_data(self.access_url, output_file)

    @property
    def data(self):
        """
        Returns the downloaded data as a pandas DataFrame, raw bytes, 
        or None if the access url is not available.
        """
        if self.access_url:
            return self.download_data()  # Download data if not already downloaded
        return None
