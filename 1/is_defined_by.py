import xml.etree.ElementTree as ET
import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_sm")

# parsing of the file sentences
def parseXML():
    root = ET.parse('1.tex.xml').getroot()
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
    pattern = [{"LOWER": "is"}, {"LOWER": "defined"} ,{"LEMMA": "by"}]
    pattern2 = [{"LOWER": "is"}, {"LOWER": "defined"} ,{"LEMMA": "on"}]
    pattern3 = [{"LOWER": "is"}, {"LOWER": "defined"} ,{"LEMMA": "via"}]
    matcher.add("FUNC", None, pattern)
    matcher.add("FUNC2", None, pattern2)
    matcher.add("FUNC3", None, pattern3)
    doc = nlp(sentence)

    count = len(doc)
    x = 0
    for match_id, start, end in matcher(doc):
        matched_span = doc[start:end]
        x += 1
        if x == 1:
            print("Sentence id: ",sentence_id)
            print(sentence)
            first_sub_string = find_Math_before(mathArr, doc, start, end)
            print("Subject: ", first_sub_string)
            second_sub_string = find_Math_after(mathArr, doc, end, count)
            print("Definition: ", second_sub_string)
            print('**********************************************************************************')
        return 1
    return 0

def find_Math_before(mathArr, doc, start, end):
    for math in mathArr:
        sub_string = str(doc[start-1])
        for n in range(start-1, -1, -1):
            if sub_string in math:
                if sub_string == math:
                    return sub_string
                else:
                    sub_string = concat_math(sub_string, doc, start, n)
                    
    return doc[start-1]

def find_Math_after(mathArr, doc, start, end):
    for math in mathArr:
        sub_string = str(doc[start])
        for n in range(end):
            if sub_string in math:
                if sub_string == math:
                    return sub_string
                else:
                    sub_string = concat_math(sub_string, doc, start, start+(n+1))
                    
    return doc[start:end]

def concat_math(sub_string, doc, start, index):
    if start > index:
        sub_string = str(doc[index:start])
    else:
        sub_string = str(doc[start:index])
    return sub_string

parseXML()