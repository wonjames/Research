import xml.etree.ElementTree as ET
import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_sm")

def parseXML():
    root = ET.parse('1.14.xml').getroot()
    val = 0
    for i, tag in enumerate(root.iter('sentence')):
        if i >= 0:
            sentence = ''
            mathArr = []
            sentence += tag.text
            for num, math in enumerate(tag.iter('Math')):
                sentence += math.text
                mathArr.append(math.text)
                sentence += math.tail
            
            val += find_definition(sentence, mathArr, i+1)
    print("Total Number of Definitions found: " ,val)
def find_definition(sentence, mathArr, sentence_id):
    
    matcher = Matcher(nlp.vocab)
    pattern = [{"LEMMA": "suppose"}, {"IS_ASCII": True, "OP": '*'}, {"LOWER": "is"}]
    pattern2 = [{"LEMMA": "suppose"}, {"IS_ASCII": True, "OP": '*'}, {"LOWER": "then"}]
    matcher.add("FUNC", None, pattern)
    matcher.add('FUNC2', None, pattern2)
    doc = nlp(sentence)
    count=0
    for tok in doc:
        count+=1
    x = 0
    for match_id, start, end in matcher(doc):
        matched_span = doc[start:end]
        x += 1
        if x == 1:
            print("Sentence id: ",sentence_id)
            print(sentence)
            print("Subject: ", doc[start+1:end-1])
            print("Definition: ", doc[end:count])
            print('**********************************************************************************')

        return True
    return False

parseXML()