import urllib3
urllib3.disable_warnings()

import argparse
from elasticsearch import Elasticsearch, TransportError

try:
    from elyzer import stepWise, getAnalyzer
    from envDefault import EnvDefault
except ImportError:
    from .elyzer import stepWise, getAnalyzer
    from .envDefault import EnvDefault


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--es', type=str,
                        help='Root URL to Elasticsearch, ie http://localhost:9200 (defaults to envvar ELYZER_ES_URL or localhost:9200)',
                        action=EnvDefault,
                        required=True,
                        envvar='ELYZER_ES_URL',
                        default='http://localhost:9200')
    parser.add_argument('--index', type=str, action=EnvDefault,
                        required=True, envvar='ELYZER_INDEX',
                        help='Name of the index to find the analyzer, ie tweets (defaults to envvar ELYZER_INDEX)')
    parser.add_argument('--analyzer', type=str, action=EnvDefault, required=True,
                        envvar='ELYZER_ANALYZER',
                        help='Name of the custom analyzer, ie my_text_analyzer (defaults to envvar ELYZER_ANALYZER)')
    parser.add_argument('text', type=str,
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
    except TransportError as e:
        print("Unexpected Elasticsearch Transport Exception:")
        print(e.error)
        print(e.info)


if __name__ == "__main__":
    main()
