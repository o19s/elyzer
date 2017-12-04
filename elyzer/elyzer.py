from __future__ import print_function

# define some standard config-free analyzers
standard_analyzers = {
    'simple':       {'tokenizer': 'lowercase',  'filter': []},
    'whitespace':   {'tokenizer': 'whitespace', 'filter': []},
    'keyword':      {'tokenizer': 'keyword',    'filter': []},
    'stop':         {'tokenizer': 'lowercase',  'filter': ['stop']},
    'standard':     {'tokenizer': 'standard',   'filter': ['standard', 'lowercase', 'stop']},
    'snowball':     {'tokenizer': 'standard',   'filter': ['standard', 'lowercase', 'stop', 'snowball']}
}

class AnalyzerNotFound(Exception):
    pass

class MultipleIndexesForAlias(Exception):
    pass


def listify(strVal):
    if (isinstance(strVal, str)):
        return [strVal]
    try:
        unicode #Python 3 this is not defined
    except NameError:
        return strVal

    if (isinstance(strVal, unicode)):
        return [strVal]
    return strVal


def normalizeAnalyzer(analyzer):
    try:
        analyzer['char_filter'] = listify(analyzer['char_filter'])
    except KeyError:
        analyzer['char_filter'] = []


def getAnalyzer(indexName, analyzerName, es):
    # try standard analyzers first
    if analyzerName in standard_analyzers:
        analyzer = standard_analyzers[analyzerName]
        normalizeAnalyzer(analyzer)
        return analyzer

    # otherwise try custom ones
    settings = es.indices.get_settings(index=indexName)

    indexes = list(settings.values())
    index_count = len(indexes)

    if index_count > 1:
      raise MultipleIndexesForAlias()

    try:
        analyzer = indexes[0]['settings']['index']['analysis']['analyzer'][analyzerName]
        normalizeAnalyzer(analyzer)
        return analyzer
    except KeyError:
      raise AnalyzerNotFound()


def printTokens(analyzeResp):
    tokens = analyzeResp['tokens']
    posnToTokens = {}
    for token in tokens:
        try:
            posnToTokens[token['position']].append(token['token'])
        except KeyError:
            posnToTokens[token['position']] = [token['token']]

    outputStr = ""
    for position, tokens in posnToTokens.items():
        outputStr += ("{%s:" % position) + ",".join(tokens) + "}\t"
    print(outputStr)



def stepWise(text, indexName, analyzer, es):
    charFiltersInUse = []
    tokenizer = analyzer['tokenizer']
    filtersInUse = []
    # Just each char filter
    for charFilter in analyzer['char_filter']:
        print("CHAR_FILTER: %s" % charFilter)
        charFiltersInUse.append(charFilter)
        body = {"text": text, "char_filter": charFiltersInUse}
        analyzeResp = es.indices.analyze(index=indexName, body=body)
        printTokens(analyzeResp)

    # Add tokenizer
    print("TOKENIZER: %s" % tokenizer)
    body = {"text": text, "char_filter": charFiltersInUse, "tokenizer": tokenizer}
    analyzeResp = es.indices.analyze(index=indexName, body=body)
    printTokens(analyzeResp)

    # Token Filters
    filters = []
    if 'filter' in analyzer:
        filters = analyzer['filter']
    elif 'filters' in analyzer:
        filters = analyzer['filters']
    else:
        raise ValueError("Weird... No Filters for analyzer %s" % analyzer)
    for currFilter in filters:
        print("TOKEN_FILTER: %s" % currFilter)
        filtersInUse.append(currFilter)
        body = {"text": text, "char_filter": charFiltersInUse, "tokenizer": tokenizer, "filter": filtersInUse}
        analyzeResp = es.indices.analyze(index=indexName, body=body)
        printTokens(analyzeResp)
