import logging
import os
import warnings
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from sentence_transformers import SentenceTransformer

load_dotenv()

warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

try:
    logger.info('Loading SentenceTransformer model...')
    model = SentenceTransformer('nomic-ai/nomic-embed-text-v1', trust_remote_code=True)
    logger.info('Model loaded successfully.')
except Exception as e:
    logger.error(f'Failed to load SentenceTransformer model: {e}')
    raise e


def ping_mongodb_connection(uri):
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        logger.info('Pinged MongoDB deployment. Connection successful.')
        return client
    except Exception as e:
        logger.error(f'Failed to connect to MongoDB with error: {e}')
        raise e

def get_search_results(query, top_k=3, model=model):
    uri = os.getenv('uri')
    db_name = os.getenv('db_name')
    coll_name = os.getenv('coll_name')
    vector_index = os.getenv('vector_index')

    if not all([uri, db_name, coll_name, vector_index]):
        error = 'One or more env variables are missing.'
        logger.error(error)
        raise EnvironmentError(error)
    
    client = ping_mongodb_connection(uri)
    db = client[db_name]
    coll = db[coll_name]

    try:
        query_embedding = model.encode(query).tolist()
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
        raise e
