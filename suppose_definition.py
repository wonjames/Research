import xml.etree.ElementTree as ET
import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_sm")

'''
Gets the Defintion for phrases that contain the pattern suppose ... is ...
                                                        suppose ... are ... 
                                                        suppose ... then ...
'''
#parsing of the sentences
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
# pattern matching on the phrase Suppose * is *
#                                Suppose * are *
#                                Suppose * then *
def find_definition(sentence, mathArr, sentence_id):
    matcher = Matcher(nlp.vocab)
    # adds the patterns to the matcher
    pattern = [{"LEMMA": "suppose"}, {"IS_ASCII": True, "OP": '*'}, {"LOWER": "is"}]
    pattern2 = [{"LEMMA": "suppose"}, {"IS_ASCII": True, "OP": '*'}, {"LOWER": "are"}]
    pattern3 = [{"LEMMA": "suppose"}, {"IS_ASCII": True, "OP": '*'}, {"LOWER": "then"}]
    matcher.add("FUNC", None, pattern)
    matcher.add('FUNC2', None, pattern2)
    matcher.add('FUNC3', None, pattern3)
    # SpaCy tokenizer
    doc = nlp(sentence)
    # length of the tokens in the sentence
    count = len(doc)
    # If there is a match to the pattern it goes into this loop
    # else there is no match return back and get the next sentence
    for match_id, start, end in matcher(doc):
        matched_span = doc[start:end]
        print("Sentence id: ",sentence_id)
        print(sentence)
        # subject is from the token after 'Suppose' til the token before 'is | are | then'
        print("Subject: ", doc[start+1:end-1])
        # definition is from the end to the end of the sentence
        print("Definition: ", doc[end:count])
        print('**********************************************************************************')
        return 1
    return 0

parseXML()