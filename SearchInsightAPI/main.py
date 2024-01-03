from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Set
from utils import (
    get_organic_results,
    find_link_and_preceding_links,
    filter_out_specific_links,
    get_unique_domains,
)
from .constants import (
    FILTER_KEYWORDS,
)  # Adjust the import path as per your project structure

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

    try:
        # Get Organic Results
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
        filtered_links = get_unique_domains(
            filter_out_specific_links(organic_results, filter_keywords)
        )

        # Structuring the response
        response = {
            "domain_position": index
            if index != -1
            else "Domain not found within the first page (8 links)",
            "links_before_searched_domain": preceding_links if index != -1 else [],
            "potential_fractured_presence": list(filtered_links),
            "links_preceding_owner_site": preceding_links,
            "all_links_first_page": organic_results,
        }

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
