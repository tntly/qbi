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

