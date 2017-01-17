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


def normalizeAnalyzer(analyzer):
    try:
        if (isinstance(analyzer['char_filter'], str) or isinstance(analyzer['char_filter'], unicode)):
            analyzer['char_filter'] = [analyzer['char_filter']]
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
    try:
        analyzer = settings[indexName]['settings']['index']['analysis']['analyzer'][analyzerName]
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
    for position, tokens in posnToTokens.iteritems():
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
        analyzeResp = es.indices.analyze(index=indexName, body=text,
                                             char_filters=",".join(charFiltersInUse))
        printTokens(analyzeResp)

    # Add tokenizer
    print("TOKENIZER: %s" % tokenizer)
    analyzeResp = es.indices.analyze(index=indexName, body=text,
                                     char_filters=",".join(charFiltersInUse),
                                     tokenizer=tokenizer)
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
        analyzeResp = es.indices.analyze(index=indexName, body=text,
                                         char_filters=",".join(charFiltersInUse),
                                         filters=",".join(filtersInUse),
                                         tokenizer=tokenizer)
        printTokens(analyzeResp)
