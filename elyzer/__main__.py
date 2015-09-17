import argparse
from elasticsearch import Elasticsearch
from elyzer import stepWise, getAnalyzer

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--es', type=str)
    parser.add_argument('--index', type=str)
    parser.add_argument('--analyzer', type=str)
    parser.add_argument('--text', type=str)
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
