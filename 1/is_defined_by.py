import xml.etree.ElementTree as ET
import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_sm")

'''
Gets the Defintion for phrases that contain the pattern (The ... of) ... is defined by ...
'''

# parsing of the file sentences
def parseXML():
    root = ET.parse('1.tex.xml').getroot()
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
            # total number of defintions found in the file
            count += find_complex_definition(sentence, mathArr, i+1)

    print("Total Number of Definitions found: " ,count)

# basic version of the defintion finding, can be tested by calling this function over find_complex_defintion
def find_definition(sentence, mathArr, sentence_id):
    matcher = Matcher(nlp.vocab)
    pattern = [{"LOWER": "is"}, {"LOWER": "defined"} ,{"LEMMA": "by"}]
    pattern2 = [{"LOWER": "is"}, {"LOWER": "defined"} ,{"LEMMA": "on"}]
    pattern3 = [{"LOWER": "is"}, {"LOWER": "defined"} ,{"LEMMA": "via"}]
    matcher.add("FUNC", None, pattern)
    matcher.add("FUNC2", None, pattern2)
    matcher.add("FUNC3", None, pattern3)
    doc = nlp(sentence)
    # length of tokens
    count = len(doc)

    for match_id, start, end in matcher(doc):
        matched_span = doc[start:end]
        print("Sentence id: ",sentence_id)
        print(sentence)
        first_sub_string = find_Math_before(mathArr, doc, start, end)
        print("Subject: ", first_sub_string)
        second_sub_string = find_Math_after(mathArr, doc, end, count)
        print("Definition: ", second_sub_string)
        print('**********************************************************************************')
        return 1
    return 0

# pattern matching on the phrase is defined by
def find_complex_definition(sentence, mathArr, sentence_id):
    matcher = Matcher(nlp.vocab)
    pattern = [{"LOWER": "is"}, {"LOWER": "defined"} ,{"LEMMA": "by"}]
    pattern2 = [{"LOWER": "is"}, {"LOWER": "defined"} ,{"LEMMA": "on"}]
    pattern3 = [{"LOWER": "is"}, {"LOWER": "defined"} ,{"LEMMA": "via"}]
    matcher.add("FUNC", None, pattern)
    matcher.add("FUNC2", None, pattern2)
    matcher.add("FUNC3", None, pattern3)
    doc = nlp(sentence)

    count = len(doc)
    for match_id, start, end in matcher(doc):
        matched_span = doc[start:end]
        print("Sentence id: ",sentence_id)
        print(sentence)
        # check for substring 'the * of' this signifies a subject that is longer than one token
        if the_of(str(doc[0:start]), start, end, mathArr):
            second_sub_string = find_Math_after(mathArr, doc, end, count)
            print("Definition: ", second_sub_string)
            print('**********************************************************************************')
        # simple sentence version
        else:
            first_sub_string = find_Math_before(mathArr, doc, start, end)
            print("Subject: ", first_sub_string)
            second_sub_string = find_Math_after(mathArr, doc, end, count)
            print("Definition: ", second_sub_string)
            print('**********************************************************************************')
        return 1
    return 0

# sub defintion inside the if then statement
# finds the correct subject of the sentence
def the_of(sentence, start_id, end_id, mathArr):
    matcher = Matcher(nlp.vocab)
    pattern = [{"LOWER": "the"}, {"IS_ASCII": True, "OP": "*"}, {"LOWER": "of"}]
    matcher.add("FUNC_complex", None, pattern)
    doc = nlp(sentence)
    count = len(doc)
    for match_id, start, end in matcher(doc):
        second_sub_string = find_Math_after(mathArr, doc, end, start_id)
        print("Subject: " + str(doc[start:end]) + ' ' + str(second_sub_string))
        return 1
    return 0

# gets the full string from the math tag before the phrase
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

# gets the full string from the math tag after the phrase
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