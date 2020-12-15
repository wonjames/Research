import xml.etree.ElementTree as ET
import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_sm")

def parseXML():
    root = ET.parse('1/1.14.xml').getroot()
    count = 0
    '''for tag in root.iter():
        print(tag.text)
    '''
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
                val = findDef(sentence, mathArr)
                if val:
                    count +=1
    print(count)

def findDef(sentence, mathArr):
    tokens = sentence.split()
    first = False
    second = False
    ret_val = []
    ret_val2 = []
    for i, tok in enumerate(tokens):
        if tok == 'is' and tokens[i+1] == 'defined' and tokens[i+2] == 'by':
            for idx, math in enumerate(mathArr):
                if not first:
                    ret_val = compare_first_def(tokens[i-1], math, tokens, i-1)
                    first = ret_val[0]
                if not second:
                    ret_val2 = compare_second_def(tokens[i+3], math, tokens, i+3)
                    second = ret_val2[0]
                if first and second:
                    print(sentence)
                    print('Subject: ', ret_val[1])
                    print('Definition: ', ret_val2[1])
                    print()
                    return True

    return False

def compare_first_def(substring, full_string, tokens, index):
    if substring in full_string:
        new_tok = tokens[index]
        for n in range(index+1):
            if new_tok == full_string:
                #print(full_string)
                return [True, new_tok]
            else:
                new_tok = tokens[index-(n+1)] + ' ' + new_tok
    return [False, '']
                

def compare_second_def(substring, full_string, tokens, index):
    if substring in full_string:
        total_length = len(tokens)
        remaining_length = total_length - index
        new_tok = tokens[index]
        for n in range(remaining_length-1):
            if new_tok == full_string:
                #print(full_string)
                return [True, new_tok]
            else:
                new_tok += ' ' + tokens[index+n+1]
                if index+n+1 == total_length-1:
                    if new_tok[:-1] == full_string:
                        #print(full_string)
                        return [True, new_tok[:-1]]
    return [False, '']

def finddef2(sentence, mathArr):
    #print(sentence)
    matcher = Matcher(nlp.vocab)
    pattern = [{'LOWER': 'if'}]
    pattern2 = [{"LEMMA": "then"}]
    matcher.add("FUNC", None, pattern)
    matcher.add("FUNC2", None, pattern2)
    doc = nlp(sentence)
    for match_id, start, end in matcher(doc):
        matched_span = doc[start:end]
        print(doc[(end+2)].text)
        '''print(doc[(start-2)].text)
        for i, defintion in enumerate(mathArr):
            if sentence.find(mathArr[i]) > matched_span.end_char:
                count += 1
        
        if count >= 1:
            print("Definition found")'''
        entities = [(matched_span.start_char, matched_span.end_char, "FUNC")]
        training_example = (doc.text, {"entities": entities})
        print(training_example)
        print()
    return True

def train(sentence, mathArr):
    matcher = Matcher(nlp.vocab)
    pattern = [{'LOWER': 'is'}, {"LOWER": "defined"}, {"LOWER": "by"}]
    matcher.add("FUNC", None, pattern)
    doc = nlp(sentence)
    count = 0
    start_check = True
    end_check = True
    for match_id, start, end in matcher(doc):
        matched_span = doc[start:end]
        print(doc[(start-2)].text)
        for i, defintion in enumerate(mathArr):
            if sentence.find(mathArr[i]) < matched_span.start_char and start_check:
                count += 1
                start_check = False
            elif sentence.find(mathArr[i]) > matched_span.end_char and end_check:
                count += 1
                end_check = False
        entities = [(matched_span.start_char, matched_span.end_char, "FUNC")]
        training_example = (doc.text, {"entities": entities})
        if count == 2:
            print("Definition found")
        print(training_example)
        print()

parseXML()