import xml.etree.ElementTree as ET
import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_sm")
'''
Gets the Defintion for phrases that contain the pattern then ... where ...
'''

def parseXML():
    root = ET.parse('1.tex.xml').getroot()
    count = 0
    for i, tag in enumerate(root.iter('sentence')):
        if i >= 0:
            sentence = ''
            mathArr = []
            sentence += tag.text
            for num, math in enumerate(tag.iter('Math')):
                sentence += math.text
                mathArr.append(math.text)
                sentence += math.tail
            
            count += find_definition(sentence, mathArr, i+1)
    print("Total Number of Definitions found: " ,count)

def find_definition(sentence, mathArr, sentence_id):
    matcher = Matcher(nlp.vocab)
    pattern = [{"LEMMA": "then"}, {"OP": '*'}, {"LOWER": "where"}]
    matcher.add("FUNC", None, pattern)
    # SpaCy tokenizer
    doc = nlp(sentence)
    # length of tokens in sentence
    count = len(doc)
    for match_id, start, end in matcher(doc):
        matched_span = doc[start:end]
        print("Sentence id: ",sentence_id)
        print(sentence)
        print("Subject: ", doc[start+1:end-1])
        print("Definition: ", doc[end:count])
        print('**********************************************************************************')
        return 1
    return 0

parseXML()