import urllib3
urllib3.disable_warnings()

import argparse
from elasticsearch import Elasticsearch
from elyzer import stepWise, getAnalyzer

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--es', type=str,
                        help='Root URL to Elasticsearch, ie http://localhost:9200',
                        default='http://localhost:9200')
    parser.add_argument('--index', type=str, required=True,
                        help='Name of the index to find the analyzer, ie tweets')
    parser.add_argument('--analyzer', type=str, required=True,
                        help='Name of the custom analyzer, ie my_text_analyzer')
    parser.add_argument('--text', type=str, required=True,
                        help='Text to analyze, ie "mary had a little lamb"')
    return vars(parser.parse_args())

def main():
    try:
        args = parse_args()
        es = Elasticsearch(args['es'])
        stepWise(es=es,
                 text=args['text'],
                 indexName=args['index'],
                 analyzer=getAnalyzer(indexName=args['index'],
                                      analyzerName=args['analyzer'],
                                      es=es))

    except KeyboardInterrupt:
        print('Interrupted')

if __name__ == "__main__":
    main()
