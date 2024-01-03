from typing import List, Set, Tuple
from serpapi import GoogleSearch
from urllib.parse import urlparse
import re


def get_organic_results(location: str, query: str, key: str) -> List[str]:
    """
    Retrieves the organic search results for a given query and location.
    """
    params = {
        "q": query,
        "location": location,
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "api_key": key,
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    organic_results = results.get("organic_results", [])
    links = [result["link"] for result in organic_results if "link" in result]
    return links


def find_link_and_preceding_links(
    links: List[str], search_domain: str
) -> Tuple[int, List[str]]:
    """
    Searches the array for a specific domain and returns its position in the array,
    along with a list of links that come before it.
    """
    for index, link in enumerate(links):
        parsed_url = urlparse(link)
        if search_domain == parsed_url.netloc:
            # Return the index and the list of links before the found link
            return index, links[:index]
    return -1, []


def get_unique_domains(urls: List[str]) -> Set[str]:
    domains = set()
    for url in urls:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        # remove 'www.' if present
        domain = domain.replace("www.", "")
        domains.add(domain)
    return domains


def filter_out_specific_links(links: List[str], filter_keywords: Set[str]) -> List[str]:
    """
    Filters out links that contain any of the specified keywords.
    """
    filteringLink = [
        link
        for link in links
        if not any(keyword in link for keyword in filter_keywords)
    ]
    return filteringLink


def create_word_set(input_string):
    # Remove special characters
    cleaned_string = re.sub(r"[^\w\s]", "", input_string)

    # split
    words = cleaned_string.lower().split()
    word_set = {word for word in words if len(word) >= 3}

    return word_set


def filter_websites(words_set, websites):
    # Filter websites containing at least one word from the words_set
    filtered_websites = [
        site for site in websites if any(word in site for word in words_set)
    ]
    return filtered_websites
