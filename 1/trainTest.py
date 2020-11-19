import xml.etree.ElementTree as ET
import spacy
from spacy.matcher import Matcher
import random
nlp = spacy.load("en_core_web_sm")


def train(sentence):
    matcher = Matcher(nlp.vocab)
    pattern = [{'LOWER': 'is'}]
    matcher.add("FUNC", None, pattern)
   
    doc = nlp(sentence)
    for match_id, start, end in matcher(doc):
        matched_span = doc[start:end]
        print(start, end)
        entities = [(matched_span.start_char, matched_span.end_char, "FUNC")]
        training_example = (doc.text, {"entities": entities})
        print(training_example)

def trainModel():
    TRAIN_DATA = [
            ("Uber blew through $1 million a week", {"entities": [(0, 4, "ORG")]}),
            ("Google rebrands its business apps", {"entities": [(0, 6, "ORG")]})]

    nlp = spacy.blank("en")
    optimizer = nlp.begin_training()
    for i in range(20):
        random.shuffle(TRAIN_DATA)
        for text, annotations in TRAIN_DATA:
            nlp.update([text], [annotations], sgd=optimizer)
    nlp.to_disk("model")

trainModel()