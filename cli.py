import argparse
import pprint
from search import get_search_results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Enter your query.')
    parser.add_argument('-q', '--query', type=str, required=True, help='The query based on which you want to generate the emoji.')
    args = parser.parse_args()
    query = args.query
    results = get_search_results(query_embedding=query)
    pprint.pprint(results, sort_dicts=False)
