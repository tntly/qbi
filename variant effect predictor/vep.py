# Import required libraries
import requests
import sys

# Define a function to query the Ensembl Variant Effect Predictor (VEP) API
def query_ensembl_vep(chromosome, start, end, allele):
    # Base URL for Ensembl REST API
    server = "https://rest.ensembl.org"
    # Construct endpoint URL with parameters: chromosome location, positions, strand (1), and variant allele
    ext = f"/vep/human/region/{chromosome}:{start}-{end}:1/{allele}?"
    
    # Make GET request to the API with appropriate headers
    r = requests.get(server+ext, headers={"Content-Type": "application/json"})
    # Check if the request was successful
    if not r.ok:
        r.raise_for_status()  # Raise an exception for HTTP errors
        sys.exit()            # Exit the program if request fails
    
    # Return the JSON response
    return r.json()

# Use the function to query a variant in BRCA1 gene
brca1 = query_ensembl_vep(17, 41276133, 41276133, "T")

# Print the first (and typically only) item in the response list
print(brca1[0])

# Iterate through all key-value pairs in the first response item
# This displays the top-level structure of the data
for key, value in brca1[0].items():
    print(key, value)
    print("\n")

# Iterate through all transcript consequences for this variant
# This shows how the variant affects different transcripts of the gene
for i in brca1[0]['transcript_consequences']:
    print(i)
    print("\n")
