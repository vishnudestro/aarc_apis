import urllib
import json
import requests
import socket
import pickle

from rake_nltk import Rake
from dynaconf import settings

from aarc_apis.controller import helpers

def logical_handler(input_data):
    """The function used to define the logical connection between the words in a sentence.
    
    Parameters
    ----------
    input_data : dict(json)
        The json the contains the input sentence.
    
    Returns
    -------
    dict(json)
        The json contain's the elements like error, received sentence, and the output for the sentence.
    """
    response = {}
    sentence = str(input_data['sentence']).strip()

    url = settings.LOGICAL_FORM + '/deplambda-demo/UniversalDependencyParserEnglish?query={"sentence":"'+ sentence +'"}'
    output = helpers.process_url(url)
    
    response['error'] = False
    response['received_sentence'] = input_data['sentence']
    response['logical_form'] = output
    
    return response

def wikidata_handler(input_data):
    """The function used to define the relationship between the words in a sentence.
    
    Parameters
    ----------
    input_data : dict(json)
        The json the contains the input sentence.
    
    Returns
    -------
    dict(json)
        The json contain's the elements like error, received sentence, and the output for the sentence.
    """
    response = {}
    sentence = input_data['sentence']
    
    url = settings.WIKI_DATA + '/v.1/wiki?query=' + sentence
    output = helpers.process_url(url)
    
    response['error'] = False
    response['received_sentence'] = input_data['sentence']
    response['wiki_response'] = output
    
    return response

def tag_ner(input_data):
    """NER(Named Entity Recognization)labels sequences of words such as PERSON, ORGANIZATION, LOCATION.
    
    Parameters
    ----------
    input_data : dict(json)
        The json the contains the input sentence.
    
    Returns
    -------
    dict(json)
        The json contain's the elements like error, received sentence, and the output for the sentence.
    """
    response = {}
    
    output = helpers.nlp_wrapper(input_data)
    ner_tags = output["sentences"][0]["entitymentions"]
    
    response['error'] = False
    response['received_sentence'] = input_data['sentence']
    response['entity_mentions'] = ner_tags
    
    return response

def tag_pos(input_data):
    """POS(Part-Of-Speech)assigns pos tag to each word, such as noun, verb, adjective, etc.,
    
    Parameters
    ----------
    input_data : dict(json)
        The json the contains the input sentence.
    
    Returns
    -------
    dict(json)
        The json contain's the elements like error, received sentence, and the output for the sentence.
    """
    response = {}
    
    output = helpers.nlp_wrapper(input_data)
    pos_tag = output["sentences"][0]["tokens"]
    
    response['error'] = False
    response['received_sentence'] = input_data['sentence']
    response['tokenize'] = pos_tag
    
    return response

def enhanced_dependencies(input_data):
    """Enhanced Dependencies show the basic dependencies and additional features such as obl, nmod.
    
    Parameters
    ----------
    input_data : dict(json)
        The json the contains the input sentence.
    
    Returns
    -------
    dict(json)
        The json contain's the elements like error, received sentence, and the output for the sentence.
    """
    response = {}
    
    output = helpers.nlp_wrapper(input_data)   
    enhanced_dependencies = output["sentences"][0]["enhancedPlusPlusDependencies"]
    
    response['error'] = False
    response['received_sentence'] = input_data['sentence']
    response['enhanced_dependencies'] = enhanced_dependencies
    
    return response
    
def triples(input_data):
    """Triples used to extraction of relation tuples, such as (Mark Zuckerberg; founded; Facebook).
 
    Parameters
    ----------
    input_data : dict(json)
        The json the contains the input sentence.
    
    Returns
    -------
    dict(json)
        The json contain's the elements like error, received sentence, and the output for the sentence.
    """
    response = {}
    
    output = helpers.nlp_wrapper(input_data)
    triples = output["sentences"][0]["openie"]
    
    response['error'] = False
    response['received_sentence'] = input_data['sentence']
    response['triples'] = triples
    
    return response

def keyword_tokenizer(input_data):
    """The keyword tokenizer is used to get the keywords from the given sentence
    
    Parameters
    ----------
    input_data : dict(json)
        The json the contains the input sentence.
    
    Returns
    -------
    dict(json)
        The json contain's the elements like error, received sentence, and the output for the sentence.
    """
    response = {}
    rake = Rake()
    topics_list=[]
    
    get_sentence = input_data['sentence']
    rake.extract_keywords_from_text(get_sentence)
    
    ranked_topics = rake.get_ranked_phrases_with_scores()

    # Step 1: Get each topic from the ranked topics
    for topic in ranked_topics:
        pos = helpers.tokeniser(topic[1])
        # Step 2: Get each tag from pos tag and check the tag starts with(NN, JJ, CD)
        for tag in pos:
            if(tag[1].startswith('NN')) or (tag[1].startswith('JJ')) or (tag[1].startswith('CD')):

                tag_data=tag[0].lower().lstrip().rstrip()
                topics_list.append(tag_data)
    
    response['error'] = False
    response['received_sentence'] = input_data['sentence']
    response['keyword_extraction'] = topics_list    

    return response

def framenet(input_sentence):
    """Managing semantic parsing using frames of the context for the input sentence
    
    Parameters
    ----------
    input_data : dict(json)
        The json the contains the input sentence.
    
    Returns
    -------
    dict(json)
        The json contain's the elements like error, received sentence, and the output for the sentence.
    """
    output = []
    response = {}

    parse_sentence = helpers.sentence_parser(input_sentence)         
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(20.0)
    client.connect((settings.FRAMENET_JAVA_CLIENT_IP, settings.FRAMENET_JAVA_CLIENT_PORT))
    client.sendall(parse_sentence.encode('utf8'))
    client.shutdown(socket.SHUT_WR)
    
    while True:
        chunk = client.recv(102400)
        if not chunk:
            break
        output.append(chunk)
    
    response['error'] = False
    response['received_sentence'] = input_sentence
    response['framenet_output'] = json.loads(output[0])     
     
    return response
