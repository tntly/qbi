import requests
from bs4 import BeautifulSoup

def fetch_and_parse_html(url):
    # Set up the headers like in the JavaScript fetch request
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

    # Send the GET request with the headers
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the content of the page with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Return the parsed HTML (You can perform further operations on the soup here)
        return soup
    else:
        # If the request fails, return the status code for debugging
        return f"Failed to retrieve content. Status code: {response.status_code}"

# URL to fetch
url = "https://www.ncbi.nlm.nih.gov/clinvar/?term=chr1%3A123456-789000"

# Call the function
soup = fetch_and_parse_html(url)

# Print the parsed HTML or the status message
print(soup.prettify() if isinstance(soup, BeautifulSoup) else soup)
