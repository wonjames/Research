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

def find_definition(sentence, mathArr, sentence_id):
    matcher = Matcher(nlp.vocab)
    pattern = [{"LEMMA": "if"}, {"OP": '*'}, {"LEMMA": "then"}]
    matcher.add("FUNC", None, pattern)
    doc = nlp(sentence)
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