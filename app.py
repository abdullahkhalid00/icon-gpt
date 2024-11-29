from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

from search import get_search_results

app = FastAPI()

class SearchResult(BaseModel):
    emoji: str
    # TODO: add unicode: str
    tags: List[str]
    short_description: str
    long_description: str
    score: float

class SearchResponse(BaseModel):
    results: List[SearchResult]


@app.get('/')
async def read_root():
    return 'FastAPI endpoint running at /search', 200

@app.post(
    '/search', response_model=SearchResponse,
    description='Runs a vector search on the deployed MongoDB collection.')
async def search_database(query: str, top_k: int = 5):
    try:
        results = get_search_results(query, top_k)
        return {'results': results}
    except Exception as e:
        return {'error': str(e)}
