import xml.etree.ElementTree as ET
import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_sm")

'''
Gets the Defintion for phrases that contain the pattern Let ... be ... and Let ... where ...
'''

# parsing of the sentences
def parseXML():
    root = ET.parse('1/1.tex.xml').getroot()
    count = 0
    # Loops through the XML file and finds the defintions in the sentence
    for i, tag in enumerate(root.iter('sentence')):
        if i >= 0:
            sentence = ''
            mathArr = []
            sentence += tag.text
            # Inside the sentence tags there are Math tags that hold math functions
            # this grabs them and adds it to the sentence
            for num, math in enumerate(tag.iter('Math')):
                sentence += math.text
                # Array of math functions for the sentence used later to compare tokens to the math function
                mathArr.append(math.text)
                sentence += math.tail
            # total number of defintions in the file
            count += find_definition(sentence, mathArr, i+1)
    print("Total Number of Definitions found: " ,count)

"""
Parameters:
sentence_id (Int): The ID that corresponds to the sentence in the XML file; used for debugging
mathArr (Array): pass in the array of math functions
sentence (Str): the sentence we are parsing
"""
# pattern matching on the phrase Let * be *
#                                Let * where *
def find_definition(sentence, mathArr, sentence_id):
    matcher = Matcher(nlp.vocab)
    # two patterns we are searching for in the sentence
    pattern = [{"LOWER": "let"}, {"IS_ASCII": True, "OP": '*'}, {"LOWER": "be"}]
    pattern2 = [{"LOWER": "let"}, {"IS_ASCII": True, "OP": '*'}, {"LOWER": "where"}]
    matcher.add("FUNC", None, pattern)
    matcher.add('FUNC2', None, pattern2)
    # SpaCy tokenizing of the sentence
    doc = nlp(sentence)
    # number of tokens
    count = len(doc)
    # If there is a match to the pattern it goes into this loop
    # else there is no match return back and get the next sentence
    for match_id, start, end in matcher(doc):
        matched_span = doc[start:end]
        print("Sentence id: ",sentence_id)
        print(sentence)
        # subject is from the token after 'Let' til the token before 'be | where'
        print("Subject: ", doc[start+1:end-1])
        # definition is from the end to the end of the sentence
        print("Definition: ", doc[end:count])
        print('**********************************************************************************')
        return 1
    return 0

parseXML()