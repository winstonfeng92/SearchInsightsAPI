from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Set
from utils import (
    get_organic_results,
    find_link_and_preceding_links,
    filter_out_specific_links,
    get_unique_domains,
    create_word_set,
    filter_websites,
)
from constants import FILTER_KEYWORDS


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


class SearchRequest(BaseModel):
    location: str
    query: str
    api_key: str
    search_domain: str


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.post("/search")
def search_and_filter(request: SearchRequest) -> dict:
    filter_keywords = FILTER_KEYWORDS.union({request.search_domain})
    query_filter_keywords = create_word_set(request.query)

    try:
        organic_results = get_organic_results(
            request.location, request.query, request.api_key
        )

        # Find Link and Preceding Links
        index, preceding_links = find_link_and_preceding_links(
            organic_results, request.search_domain
        )

        # DEPRECATED Filter Out Specific Links and Get Unique Domains - deprecated this info, just show preceding links unfiltered
        filtered_preceding_links = filter_out_specific_links(
            preceding_links, filter_keywords
        )

        # get unique domains, filter out uber
        filtered_links = get_unique_domains(
            filter_out_specific_links(organic_results, filter_keywords)
        )

        # perform additional filtering based on query keywords
        query_filtered_links = filter_websites(
            query_filter_keywords, list(filtered_links)
        )

        response = {
            "domain_position": index + 1
            if index != -1
            else "Domain not found within the first page (first 8 links)",
            "links_before_searched_domain": preceding_links if index != -1 else [],
            "potential_fractured_presence": query_filtered_links,
            "links_preceding_owner_site": preceding_links,
            "all_links_first_page": organic_results,
        }

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
