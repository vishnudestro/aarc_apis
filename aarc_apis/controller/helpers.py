import urllib, json
import requests

from pycorenlp import StanfordCoreNLP
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk
from neo4j.v1 import GraphDatabase

from dynaconf import settings

driver = GraphDatabase.driver(settings.NEO4J_IP, auth=(settings.USER_NAME, settings.PASSWORD))

stanford_nlp = StanfordCoreNLP(settings.STANFORD_IP)

lemmatizer = WordNetLemmatizer()
stop=nltk.corpus.stopwords.words('english')

def nlp_wrapper(input_data):
    """The NLP Wrapper is used to annotate the given sentence to generate tokenize, depparse, ssplit, pos, lemma, ner, openie in json fromat.
    
    Parameters
    ----------
    input_data : dict(json)
        The json the contains the input sentence.
    
    Returns
    -------
    dict(json)
        The json contain's the elements like error, received sentence, and the output for the sentence.
    """
    sentence = input_data['sentence']
    output = stanford_nlp.annotate(sentence, 
                properties={"annotators":"tokenize, depparse, ssplit, pos, lemma, ner, openie" , "outputFormat": "json"})	
    output['received_sentence'] = sentence
    output['error'] = False
    return output

def tokeniser(word):
    """NLTK word tokeniser is used to get token from the input sentence
    
    Parameters
    ----------
    input_data : dict(json)
        The json the contains the input sentence.
    
    Returns
    -------
    dict(json)
        The json contain's the elements like error, received sentence, and the output for the sentence.
    """
    tag_nodes=[]
    token=nltk.word_tokenize(word)
    pos_tag=nltk.pos_tag(token)

    for tag in pos_tag:
        tag_nodes.append(tag)
    
    return pos_tag

def process_url(url):
    try:
        output = requests.get(url)        
        output = output.json()
        return output
    except requests.ConnectionError as e:
        logger.error("Invalid connection during wikidata handling")
        return None


def microsoft_conceptnet(word):
    print("word --", word)
    query = """MATCH (i:Instance)-[r:IS_A]->(c:Concept) where i.name = '{word}' RETURN
            i.name AS Instance, tofloat(r.probability)/10000 AS score, 
            c.name AS Concept ORDER BY r.probability DESC LIMIT 5;""".format(word=word)
    conList=[]
    with driver.session() as session:
        with session.begin_transaction() as tx:
            records = tx.run(query)
            for record in records:
                name=str(record["Concept"])
                sc=str(record["score"])
                conList.append([name,sc]) 
    return conList

def sentence_parser(sentence):
    data = sentence.encode()
    response = requests.post(
        settings.STANFORD_IP, params={
            'properties': str({"annotators":"tokenize,ssplit,pos,parse","outputFormat": "conll"})
        }, data=data, headers={'Connection': 'close'})
    outputs=str(response.text)
    outputs = outputs.strip().split(u"\n")
    sentences = []
    split_sentences = []

    for output in outputs:
        split_sentences = output.strip().split("\t")
        sentence = getString(split_sentences)
        sentences.append(sentence)
    
    sentence_rephrase ='\n'.join("\t"+line.encode('utf8').decode('utf8') + u"\t_\t_" for line in sentences)
    join_sentence = [sentence_rephrase]        
    join_sentence = '\n\n'.join(join_sentence)

    return join_sentence

def getString(split_sentences):
    data = split_sentences
    split_sentences.insert(4,data[3])
    output = '\t'.join(str(sentence) for sentence in split_sentences)
    return output

