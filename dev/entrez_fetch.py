import os
import requests
import pandas as pd
from urllib.parse import quote

def fetch_and_process_data(ucsc_coords: str):
    # URL encoding the search term
    encoded_coords = quote(ucsc_coords)

    # Define the URL and headers
    url = "https://www.ncbi.nlm.nih.gov/clinvar"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/x-www-form-urlencoded",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1",
        "Priority": "u=0, i"
    }

    # Define the body data for the POST request
    body = {
        "term": encoded_coords,
        "EntrezSystem2.PEntrez.clinVar.Entrez_PageController.PreviousPageName": "results",
        "EntrezSystem2.PEntrez.clinVar.clinVar_Facets.FacetsUrlFrag": "filters%3D",
        # Add other form data here as needed
        "EntrezSystem2.PEntrez.clinVar.clinVar_Entrez_ResultsPanel.Entrez_DisplayBar.SendTo": "File",
        "EntrezSystem2.PEntrez.DbConnector.Cmd": "file"
        # Add the full body parameters as required
    }

    # Make the POST request to fetch the data
    response = requests.post(url, headers=headers, data=body)

    # Check if the request was successful
    if response.status_code == 200:
        # Assuming the response is a file (like a .txt or .csv), save it to disk
        file_name = 'downloaded_data.txt'  # Adjust this to the actual file format
        with open(file_name, 'wb') as file:
            file.write(response.content)

        # Process the downloaded file into a pandas DataFrame (assuming it's CSV or a format that pandas can read)
        try:
            # Replace with appropriate read function based on the file format (e.g., read_csv, read_table)
            df = pd.read_csv(file_name, delimiter='\t')  # Adjust delimiter as needed for your file format
            print(df.head())  # Output the first few rows of the DataFrame for verification

            # Delete the file after processing
            os.remove(file_name)
            print(f"File {file_name} deleted successfully.")
            return df
        except Exception as e:
            # Handle any issues with reading the file
            print(f"Error processing file: {e}")
            return None
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

# Example usage
ucsc_coords = "chr2:12345-67890"  # Example search term
df = fetch_and_process_data(ucsc_coords)
