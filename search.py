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


def ping_mongodb_connection(uri):
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        logger.info('Pinged MongoDB deployment. Connection successful.')
        return client
    except Exception as e:
        logger.error(f'Failed to connect to MongoDB with error: {e}')


def get_search_results(query_embedding, model=SentenceTransformer('nomic-ai/nomic-embed-text-v1', trust_remote_code=True)):
    client = ping_mongodb_connection(os.getenv('uri'))
    db = client[os.getenv('db_name')]
    coll = db[os.getenv('coll_name')]
    vector_index = os.getenv('vector_index')
    try:
        pipeline = [
            {
                '$vectorSearch': {
                    'index': vector_index,
                    'queryVector': model.encode(query_embedding).tolist(),
                    'path': 'embeddings',
                    'exact': True,
                    'limit': 3
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
        logger.info(f'Generated search results successfully.')
        return list(results)
    except Exception as e:
        logger.error(f'Failed to run vector search with error: {e}')
