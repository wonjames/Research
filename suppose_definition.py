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
            
            count += find_definition(sentence, mathArr, i+1)
    print("Total Number of Definitions found: " ,count)
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