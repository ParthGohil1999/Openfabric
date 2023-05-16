import os
import warnings
from ontology_dc8f06af066e4a7880a5938933236037.simple_text import SimpleText

from openfabric_pysdk.context import OpenfabricExecutionRay
from openfabric_pysdk.loader import ConfigClass
from time import time

import nltk
from nltk.corpus import wordnet


############################################################
# Callback function called on update config
############################################################
def config(configuration: ConfigClass):
    # TODO Add code here
    pass


############################################################
# Callback function called on each execution pass
############################################################
def execute(request: SimpleText, ray: OpenfabricExecutionRay) -> SimpleText:
    output = []
    for text in request.text:
        # TODO Add code here
        response = get_response(text)
        output.append(response)

    return SimpleText(dict(text=output))

def get_response(text):
    # Tokenize the input text
    tokens = nltk.word_tokenize(text)

    # Check if the question is about a scientific term
    if 'what' in tokens and 'is' in tokens and 'science' in tokens:
        response = "Science is the systematic study of the natural world through observation and experimentation."
    # Check if the question is about a specific scientific topic
    elif 'what' in tokens and 'is' in tokens:
        term = get_term(tokens)
        if term:
            response = get_definition(term)
        else:
            response = "I'm sorry, I don't know the answer to that question."
    else:
        response = "I'm sorry, I'm not able to answer that question about science."

    return response

def get_term(tokens):
    # Remove question words and auxiliary verbs
    stopwords = ['what', 'is', 'are', 'the', 'of', 'in', 'on', 'for', 'to']
    filtered_tokens = [token for token in tokens if token.lower() not in stopwords]

    # Get the first noun from the filtered tokens
    for token in filtered_tokens:
        synsets = wordnet.synsets(token)
        if synsets and synsets[0].pos() == 'n':
            return token

    return None

def get_definition(term):
    synsets = wordnet.synsets(term)
    if synsets:
        definition = synsets[0].definition()
        return f"The definition of {term} is: {definition}"
    else:
        return f"I'm sorry, I don't know the definition of {term}."
