import xml.etree.ElementTree as ET
import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_sm")
'''
Gets the Defintion for phrases that contain the pattern Let 
This is no longer used but was used in the beginning using REGEX
Use files let_definition.py and let_be_definition.py
'''

def parseXML():
    root = ET.parse('1/1.tex.xml').getroot()
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
    pattern = [{'TEXT': {'REGEX': '(?i)^let\w*$'}}, {'IS_SENT_START': False, 'OP': '*'}]
    
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
            arr = findMath(mathArr, doc, start, end, count)
            print("Subject: ", arr[0])
            print("Definition: ", doc[arr[1]:count])

        return True
    return False

def findMath(mathArr, doc, start, end, count):
    for math in mathArr:
        sub_string = str(doc[start+1])
        for n in range(count):
            if sub_string in math:
                if sub_string == math:
                    return [sub_string,start+n+2]
                else:
                    sub_string = concat_math(sub_string, doc, start, (start+(n+2)))
                    
    return [sub_string, end+1]

def concat_math(sub_string, doc, start, index):
    sub_string = str(doc[start+1:index+1])
    return sub_string

parseXML()