import xml.etree.ElementTree as ET
import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_sm")

def parseXML():
    root = ET.parse('1.14.xml').getroot()
    count = 0
    for i, tag in enumerate(root.iter('sentence')):
        if i == 16 or i == 13:
            num = 0
            sentence = ''
            mathArr = []
            #print(tag.text, end='')
            sentence += tag.text
            for num, math in enumerate(tag.iter('Math')):
                #print("Math: ", math.text)
                #print("Math Tail: ", math.tail)
                sentence += math.text
                mathArr.append(math.text)
                sentence += math.tail
            if num >= 1:
                print(sentence)
                val = finddef2(sentence, mathArr)
                if val:
                    print(i+1)
                    print()
                    count +=1
    print(count)

def finddef2(sentence, mathArr):
    
    matcher = Matcher(nlp.vocab)
    pattern = [{"LEMMA": "if"}, {"IS_ASCII": True, "OP": '*'}, {"LEMMA": "then"}]
    
    matcher.add("FUNC", None, pattern)
    doc = nlp(sentence)
    count=0
    for tok in doc:
        print(tok)
        count+=1
    x = 0
    for match_id, start, end in matcher(doc):
        matched_span = doc[start:end]
        print('here')
        x += 1
        if x == 1:
            #print(matched_span.text)
            print(sentence)
            print("Subject: ", doc[start+1:end-1])
            print("Definition: ", doc[end:count])

        return True
    return False

parseXML()