import xml.etree.ElementTree as ET
import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_sm")
'''
Gets the Defintion for phrases that contain the pattern if * then * using REGEX
This is an old verison, use the file if_then_definition.py instead
'''
def parseXML():
    root = ET.parse('1/1.14.xml').getroot()
    count = 0
    for i, tag in enumerate(root.iter('sentence')):
        if i >= 0:
            num = 0
            sentence = ''
            mathArr = []
            sentence += tag.text
            for num, math in enumerate(tag.iter('Math')):
                sentence += math.text
                mathArr.append(math.text)
                sentence += math.tail
            if num >= 1:
                val = finddef2(sentence, mathArr)
                if val:
                    count +=1
    print('Found: ', count)

def finddef2(sentence, mathArr):
    
    matcher = Matcher(nlp.vocab)
    pattern = [{'TEXT': {'REGEX': '(?i)^if\w*$'}}, {'IS_SENT_START': False, 'OP': '*'}, {'TEXT': {'REGEX': '(?i)^then\w*$'}}]
    
    matcher.add("FUNC", None, pattern)
    doc = nlp(sentence)
    count=0
    for tok in doc:
        count+=1
    x = 0
    for match_id, start, end in matcher(doc):
        matched_span = doc[start:end]
        x += 1
        if x == 1:
            print(sentence)
            print("Subject: ", doc[start+1:end-1])
            print("Definition: ", doc[end:count])

        return True
    return False

parseXML()