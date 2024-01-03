from typing import List, Set, Tuple
from serpapi import GoogleSearch
from urllib.parse import urlparse


def get_organic_results(location: str, query: str, key: str) -> List[str]:
    """
    Retrieves the organic search results for a given query and location.

    :param location: The location to consider for the search.
    :param query: The search query.
    :param key: The API key for SerpApi.
    :return: A list of links from the organic search results.
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

    :param links: A list of URLs (strings).
    :param search_domain: The domain (string) to search for in the list of URLs.
    :return: A tuple containing the index of the found domain and a list of URLs preceding it.
             Returns (-1, []) if the domain is not found.
    """
    # Find the index of the link that matches the search domain
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

    :param links: A list of URLs (strings).
    :param filter_keywords: A set of keywords (strings) to filter out from the URLs.
    :return: A list of URLs that do not contain the specified keywords.
    """
    filteringLink = [
        link
        for link in links
        if not any(keyword in link for keyword in filter_keywords)
    ]
    return filteringLink
