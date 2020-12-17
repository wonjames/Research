import xml.etree.ElementTree as ET
import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_sm")
'''
Gets the Defintion for phrases that contain the pattern if ... then ...
'''
# parsing of the xml file
def parseXML():
    root = ET.parse('1/1.14.xml').getroot()
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
            # total defintions found
            count += find_definition(sentence, mathArr, i+1)
    print("Total Number of Definitions found: " ,count)

"""
Parameters:
sentence_id (Int): The ID that corresponds to the sentence in the XML file; used for debugging
mathArr (Array): pass in the array of math functions
sentence (Str): the sentence we are parsing
"""
# pattern matching on the phrase if * then *
def find_definition(sentence, mathArr, sentence_id):
    matcher = Matcher(nlp.vocab)
    # patterns we are searching for in the sentence
    pattern = [{"LEMMA": "if"}, {"OP": '*'}, {"LEMMA": "then"}]
    matcher.add("FUNC", None, pattern)
    # SpaCy tokenizer
    doc = nlp(sentence)
    # length of tokens in sentence
    count = len(doc)
    # If there is a match to the pattern it goes into this loop
    # else there is no match return back and get the next sentence
    for match_id, start, end in matcher(doc):
        matched_span = doc[start:end]
        print("Sentence id: ",sentence_id)
        print(sentence)
        # subject is from the token after 'then' til the token before 'where'
        print("Subject: ", doc[start+1:end-1])
        # definition is from the end to the end of the sentence
        print("Definition: ", doc[end:count])
        print('**********************************************************************************')
        return 1
    return 0

parseXML()