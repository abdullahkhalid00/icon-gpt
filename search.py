import os
import torch
import logging
import warnings

from dotenv import load_dotenv
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
from sentence_transformers import SentenceTransformer

# load .env
load_dotenv()

# ignore warnings
warnings.filterwarnings('ignore')

# configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# pre-load mongodb config
try:
    logger.info('Loading MongoDB config...')
    client = MongoClient(os.getenv('uri'), server_api=ServerApi('1'))
    db = client[os.getenv('db_name')]
    coll = db[os.getenv('coll_name')]
    vector_index = os.getenv('vector_index')
    logger.info('Config loaded successfully.')
except Exception as e:
    logger.error(f'Failed to configure MongoDB (check .env): {e}')
    raise

# configure inference device
device = 'cuda' if torch.cuda.is_available() else 'cpu'
if device == 'cpu':
    logger.warning(
        f'CUDA is recommended. Please consult README.md for installation instructions.')

# pre-load embedding model
try:
    logger.info('Loading SentenceTransformer model...')
    model = SentenceTransformer(
        os.getenv('embedding_model'), trust_remote_code=True, device=device)
    logger.info(f'Model loaded successfully on: {device}.')
except Exception as e:
    logger.error(f'Failed to load SentenceTransformer model: {e}')
    raise


def get_search_results(query, top_k, model=model):
    try:
        query_embedding = model.encode(
            query, show_progress_bar=False, normalize_embeddings=False).tolist()
        pipeline = [
            {
                '$vectorSearch': {
                    'index': vector_index,
                    'queryVector': query_embedding,
                    'path': 'embeddings',
                    'exact': True,
                    'limit': top_k
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'emoji': 1,
                    'tags': 1,
                    'short_description': 1,
                    'long_description': 1,
                    'score': {
                        '$meta': 'vectorSearchScore'
                    }
                }
            }
        ]
        results = coll.aggregate(pipeline)
        logger.info('Generated search results successfully.')
        return list(results)
    except Exception as e:
        logger.error(f'Failed to run vector search with error: {e}')
        raise
