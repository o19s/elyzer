# Elyzer

See step-by-step how Elasticsearch custom analyzers decompose your text into tokens.

My therapist said this would be a good idea...

<pre>
Doug:  hi
Eliza: How are you today.. What would you like to discuss?
Doug:  well I can't really see how my Elasticsearch analyzers work, on the inside
Eliza: How do you know you can't really see how your Elasticsearch analyzers work, on the inside?
Doug:  cause I call _analyze, and it does the whole analyzer or just one step
Eliza  What other reasons might there be?
Doug:  I guess nobody's gotten around to making a good debugger
Eliza  I'm not sure I understand you fully.
Doug   well just keep reading this README then...
Eliza  Come, come, elucidate your thoughts.
</pre>

# Installation

Install through pip3

(ES 2.x & 5.x)

    pip3 install elyzer

# Usage

Give Elyzer some text and have its analyzed. See the process broken down step-by-step on the command line.

Assuming I'd created an `english_bigrams` custom analyzer for the index tmdb, I would run the analyzer like so

```
$ elyzer --es "http://localhost:9200" --index tmdb --analyzer english_bigrams "Mary had a little lamb"
TOKENIZER: standard
{1:Mary}    {2:had} {3:a}   {4:little}  {5:lamb}    
TOKEN_FILTER: standard
{1:Mary}    {2:had} {3:a}   {4:little}  {5:lamb}    
TOKEN_FILTER: lowercase
{1:mary}    {2:had} {3:a}   {4:little}  {5:lamb}    
TOKEN_FILTER: porter_stem
{1:mari}    {2:had} {3:a}   {4:littl}   {5:lamb}    
TOKEN_FILTER: bigram_filter
{1:mari had}    {2:had a}   {3:a littl} {4:littl lamb}  
```

Output is each token, prefixed by the numerical position attribute in the token stream at each step.

## Args

There are four required command line args:

- es: the elasticsearch host (ie http://localhost:9200)
- index: name of the index where your custom analyzer can be found
- analyzer: name of your custom analyzer
- text: the text to analyze


# Shortcomings

aka "Areas for Improvement"
- Only works for custom analyzers right now (as it accesses the settings for your index)
- Attributes besides the token text and position would be handy 

## Who?

Created by [OpenSource Connections](http://opensourceconnections.com)

## License

Released under [Apache 2](LICENSE.txt)

