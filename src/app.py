from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from src.search import get_search_results

app = FastAPI()

# allow frontend comms
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

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
async def search_database(request: SearchRequest):
    try:
        results = get_search_results(request.query, request.top_k)
        return {'results': results}
    except Exception as e:
        return {'error': str(e)}
