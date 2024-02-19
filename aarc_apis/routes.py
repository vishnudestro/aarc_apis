import urllib
import json
import requests

from flask import Flask, render_template, request, jsonify,logging,json
from flask.blueprints import Blueprint

from aarc_apis.controller import sentence_handler, helpers
from dynaconf import settings

api = Blueprint('AARC_APIS', __name__)

@api.route("/sentence/<string:type_>", methods=['POST'])
def sentence_api_handler(type_ = None):
    """The function handle sentence based api, Only applicable for a sentence
    
    Parameters
    ----------
    type_ : str, optional
        The type of the sentence service that is requested, by default None
    Returns
    -------
    dict(json)
        The return value must be in json to showcase
    """
    get_input_json = request.get_json()

    if type_ == "logic":
        output = sentence_handler.logical_handler(get_input_json)
    
    elif type_ == "wiki":
        output = sentence_handler.wikidata_handler(get_input_json)
    
    elif type_ == "ner_tag":
        output = sentence_handler.tag_ner(get_input_json)
    
    elif type_ == "pos_tag":
        output = sentence_handler.tag_pos(get_input_json)
    
    elif type_ == "enhance_dep":
        output = sentence_handler.enhanced_dependencies(get_input_json)
    
    elif type_ == "triples":
        output = sentence_handler.triples(get_input_json)
    
    elif type_ == "all":
        output = helpers.nlp_wrapper(get_input_json)
    
    elif type_ == "keyword":
        output = sentence_handler.keyword_tokenizer(get_input_json)
    
    elif type_ == "framenet":
        sentence = get_input_json["sentence"]
        output = sentence_handler.framenet(sentence)
    else:
        return None

    return jsonify(output), 200

@api.route("/word/<string:type_>", methods=['GET'])
def wordnet_handler(type_ = None):
    """Handles all the wordnet based api functions that is applicable only for the words. 
    
    Parameters
    ----------
    type_ : str, optional
        The type of the wordnet service that is requested, by default None
    """
    wordnet_url = None
    word = str(request.args.get('query'))
    
    #TODO: Check the usage of Substance meronyms and Sybstance holonyms and Check which gateways aren't used
    if type_ == 'synonyms':
        wordnet_url = settings.WORDNET_IP +'/synonyms/1/' + str(word)
    
    elif type_ == 'antonyms':
        wordnet_url = settings.WORDNET_IP +'/antonyms/1/' + str(word)
    
    elif type_ == 'holonyms':
        wordnet_url = settings.WORDNET_IP +'/holonyms/1/' + str(word)
    
    elif type_ == 'sub_holonyms':
        wordnet_url = settings.WORDNET_IP +'/substance_holonyms/1/' + str(word)
    
    elif type_ == 'meronyms':
        wordnet_url = settings.WORDNET_IP +'/meronyms/1/' + str(word)
    
    elif type_ == 'sub_meronyms':
        wordnet_url = settings.WORDNET_IP +'/substance_meronyms/1/' + str(word)
    
    elif type_ == 'hyponyms':
        wordnet_url = settings.WORDNET_IP +'/hyponyms/1/' + str(word)
    
    elif type_ == 'hypernyms':
        wordnet_url = settings.WORDNET_IP +'/hypernyms/1/' + str(word)
    
    elif type_ == 'causes':
        wordnet_url = settings.WORDNET_IP +'/causes/1/' + str(word)
    
    elif type_ == 'definition':
        wordnet_url = settings.WORDNET_IP +'/definition/1/' + str(word)
    
    else:
        pass
    
    output = helpers.process_url(url = wordnet_url)
    return jsonify(output), 200

@api.route("/word/micro_concept", methods=['GET'])
def micro_concept():
    """The fuction is used to call microsoft conceptnet to get concept(get related words) for a WORD
    
    Returns
    -------
    dict(json)
        The return json data contain the related words according to the user input
    """
    word =str(request.args.get('word'))
    
    output = helpers.microsoft_conceptnet(word)
    return jsonify(output)

@api.route("/word/concept")
def conceptnet():
    """The fuction used get concept according to the user input WORD
    
    Returns
    -------
    dict(json)
        Contains related concept to the input word
    """
    word = str(request.args.get('word'))
    conceptnet_url =  settings.CONCEPTNET_IP + '/c/en/' +word 
    
    # WARNING: DO NOT use triple quotes to specify the user agent. Triple quotes 
    # treats new line as \n which is not parsed by requests properly. 
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)\
         AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
    output = requests.get(conceptnet_url, headers=headers)
    return jsonify(output.json())