import requests
import urllib.parse

def get_clinvar_data(ucsc_coords: str, assembly="GRCh38"):
    """
    Fetches ClinVar data for a given UCSC-style chromosome location.

    Args:
        ucsc_coords (str): Chromosome coordinates in UCSC format (e.g., 'chr2:12345-12345').
        assembly (str): Genome assembly ('GRCh38' or 'GRCh37').

    Returns:
        dict: JSON response from ClinVar if successful, otherwise None.
    """
    base_url = "https://www.ncbi.nlm.nih.gov/clinvar/variation/search/"

    # Parse the UCSC coordinate format (e.g., 'chr2:12345-67890')
    try:
        chrom, pos_range = ucsc_coords.replace("chr", "").split(":")
        start, end = pos_range.split("-")
    except ValueError:
        print("Invalid UCSC coordinate format. Expected format: 'chr2:12345-67890'")
        return None

    # Construct the query for ClinVar
    query = f"({chrom}[CHR] AND {start}:{end}[CPOS])"

    # URL encode the query
    encoded_query = urllib.parse.quote(query, safe="()[]:")

    # Construct the full URL with the appropriate genome assembly
    assembly_id = "GCF_000001405.38" if assembly == "GRCh38" else "GCF_000001405.25"
    full_url = f"{base_url}?term={encoded_query}&assembly={assembly_id}"

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9",
        "Referer": "https://www.ncbi.nlm.nih.gov/clinvar/",
    }

    try:
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP issues
        return response.json()  # Return JSON response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching ClinVar data: {e}")
        return None
""" 
# Example usage
ucsc_input = "chr2:12345-67890"
result = get_clinvar_data(ucsc_input)
print(result)


count_variant = variant_df['ci'].value_counts()
print(count_variant) """

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

def extract_all_syndrome_names(html):
    # Parse the HTML content
    soup = html
    
    # Find all 'td' elements with the class 'pad-right'
    syndrome_td = soup.find_all('td', class_='pad-right')
    
    # Extract the text inside these 'td' elements
    syndrome_names = [td.get_text(strip=True) for td in syndrome_td]
    
    # Filter and return all occurrences of the syndrome name
    syndrome_list = [name for name in syndrome_names]
    
    return syndrome_list


def fetch_conditions(ucsc_coords: str, assembly="GRCh38"):
    # Set up the headers like in the JavaScript fetch request
    encoded_coords = quote(ucsc_coords)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1"
    }

    url = f"https://www.ncbi.nlm.nih.gov/clinvar/?term={encoded_coords}"
    print(url)


    # Send the GET request with the headers
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the content of the page with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        data = extract_all_syndrome_names(soup)

        # Return the parsed HTML (You can perform further operations on the soup here)
        return data
    else:
        # If the request fails, return the status code for debugging
        return f"Failed to retrieve content. Status code: {response.status_code}"
