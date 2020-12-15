import xml.etree.ElementTree as ET
import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_sm")

'''
Gets the Defintion for phrases that contain the pattern Let ... 
This is the simple version that get sreplaced by the file let_be_defintion.py
'''

def parseXML():
    root = ET.parse('1/1.tex.xml').getroot()
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
    pattern = [{"LEMMA": "let"}, {"IS_ASCII": True, "OP": '*'}]
    
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
            print("Sentence id: ",sentence_id)
            print(sentence)
            arr = findMath(mathArr, doc, start, end, count)
            print("Subject: ", arr[0])
            print("Definition: ", doc[arr[1]:count])
            print('**********************************************************************************')

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