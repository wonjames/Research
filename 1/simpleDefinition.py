import xml.etree.ElementTree as ET
import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_sm")

def parseXML():
    root = ET.parse('1.14.xml').getroot()
    count = 0
    for i, tag in enumerate(root.iter('sentence')):
        if i >= 0:
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
                val = finddef2(sentence, mathArr)
                if val:
                    #print(i+1)
                    #print()
                    count +=1
    print(count)

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
            #print(matched_span.text)
            print(sentence)
            print("Subject: ", doc[start+1:end-1])
            print("Definition: ", doc[end:count])
            
        #print(doc[(end+2)].text)
        '''print(doc[(start-2)].text)
        for i, defintion in enumerate(mathArr):
            if sentence.find(mathArr[i]) > matched_span.end_char:
                count += 1
        
        if count >= 1:
            print("Definition found")'''

        return True
    return False

parseXML()