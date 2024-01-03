# SearchInsightsAPI

## Description

SearchInsightsAPI is a FastAPI application designed to analyze and provide insights into online search results, specifically for restaurants. It systematically identifies online presences, tracks domain rankings, and helps in understanding online visibility for various restaurant businesses.

This API exists to help systematically identify fractured online presence using automation.

## Features

- **Search Query Processing**: Takes specific restaurant-related queries and location data to analyze search results.
- **Domain Ranking Analysis**: Identifies the ranking position of specified restaurant domains in search results.
- **Aggregation Site Filtering**: Filters out common review and aggregation sites to focus on primary business websites.
- **Insightful Reporting**: Generates reports on potential fractured online presences and the sequence of domain appearances in search results.

## Installation and Usage

To set up the SearchInsightsAPI on your local machine, follow these steps:

```bash
git clone https://github.com/winstonfeng92/SearchInsightsAPI.git
cd SearchInsightsAPI
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
pip install -r requirements.txt
```

Run the FastAPI server using the following command:

```bash
uvicorn main:app --reload
```

## API Endpoints

POST /search: Takes in parameters such as location, query, API key, and search domain, and returns search insights including domain position, potential fractured presences, and preceding links.
