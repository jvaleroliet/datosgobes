import pandas as pd
import requests
from io import BytesIO

def download_data(url, output_file=None):
    
    """
    Downloads the data from the provided URL and optionally saves it to a file or attempts to load it as a pandas DataFrame.

    Args:
        url (str): The URL of the data to download.
        output_file (str, optional): Path to the file where downloaded data should be saved.
            Defaults to None.

    Returns:
        pandas.DataFrame | bytes | None: The loaded DataFrame on success, raw bytes on unknown format, or None on errors.
    """
    try:
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            # Check for content-type header
            content_type = response.headers.get('Content-Type')

            if output_file:
                with open(output_file, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                return None  # Indicate successful download to file

            else:
                # Try loading data as pandas DataFrame based on content type and potential extensions
                try:
                    if content_type:
                        if content_type.startswith('text/csv'):
                            return pd.read_csv(url, engine='python')

                        elif content_type.startswith('application/json'):
                            # Likely JSON format
                            return pd.read_json(response.content)
                        elif content_type.startswith('application/vnd.ms-excel'):
                            # Likely Excel format, attempt loading with xlrd
                            return pd.read_excel(url, engine='xlrd')
                        elif content_type.startswith('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'):
                            # Likely Excel format, attempt loading with openpyxl
                            return pd.read_excel(url, engine='openpyxl')
                        else:
                            # Unknown format, return raw bytes
                            return response.content

                except:
                    print("Failed to parse data as pandas DataFrame.")
    except:
        print("Failed to download data from URL.")            
