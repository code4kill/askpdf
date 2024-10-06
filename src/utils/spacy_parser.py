"""
This file uses the spacy (transformer models [en_core_web_trf]) library to extract named entities from the text.
"""


import spacy

nlp = spacy.load('en_core_web_trf')

def extract_named_entity(text):
    """
    Extracts the person entities from the text.

    Args:
        text: The text to be parsed.

    Returns:
        The person entities.
    """
    doc = nlp(text)
    named_entities = {'person': [], 'ORG': []}
    for ent in doc.ents:
      if ent.label_ == 'PERSON':
        named_entities['person'].append(ent.text)
      elif ent.label_ == 'ORG':
        named_entities['ORG'].append(ent.text)
    return named_entities
  