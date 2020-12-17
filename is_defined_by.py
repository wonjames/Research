import xml.etree.ElementTree as ET
import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_sm")

'''
Gets the Defintion for phrases that contain the pattern (The ... of) ... is defined by ...
'''

# parsing of the file sentences
def parseXML():
    root = ET.parse('1/1.tex.xml').getroot()
    count = 0
    # Loops through the XML file and finds the defintions in the sentence
    for i, tag in enumerate(root.iter('sentence')):
        if i >= 0:
            sentence = ''
            mathArr = []
            sentence += tag.text
            # Inside the sentence tags there are Math tags that hold math functions
            # this grabs them and adds it to the sentence
            for num, math in enumerate(tag.iter('Math')):
                sentence += math.text
                # Array of math functions for the sentence used later to compare tokens to the math function
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
"""
Parameters:
sentence_id (Int): The ID that corresponds to the sentence in the XML file; used for debugging
mathArr (Array): pass in the array of math functions
sentence (Str): the sentence we are parsing
"""
# pattern matching on the phrase is defined by
def find_complex_definition(sentence, mathArr, sentence_id):
    matcher = Matcher(nlp.vocab)
    # three patterns we are searching for in the sentence
    pattern = [{"LOWER": "is"}, {"LOWER": "defined"} ,{"LEMMA": "by"}]
    pattern2 = [{"LOWER": "is"}, {"LOWER": "defined"} ,{"LEMMA": "on"}]
    pattern3 = [{"LOWER": "is"}, {"LOWER": "defined"} ,{"LEMMA": "via"}]
    matcher.add("FUNC", None, pattern)
    matcher.add("FUNC2", None, pattern2)
    matcher.add("FUNC3", None, pattern3)
    # tokenizes the sentence
    doc = nlp(sentence)

    count = len(doc)
    # If there is a match to the pattern it goes into this loop
    # else there is no match return back and get the next sentence
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
""" 
Parameters: 
mathArr (Array): pass in the array of math functions
end_id (Int): int value of the end of the pattern 
start_id (Int): int value of the start of the pattern
sentence (Str): the sentence we are parsing
"""
# statement before the is defined by phrase
# finds the correct subject of the sentence
# Ex Sentence: The ... of ... is defined by ...
# the subject will be found inbetween 'the' and 'of'
# definition is not found in this function but back in the find_complex_defintion function
def the_of(sentence, start_id, end_id, mathArr):
    matcher = Matcher(nlp.vocab)
    pattern = [{"LOWER": "the"}, {"IS_ASCII": True, "OP": "*"}, {"LOWER": "of"}]
    matcher.add("FUNC_complex", None, pattern)
    doc = nlp(sentence)
    count = len(doc)
    for match_id, start, end in matcher(doc):
        # gets the subject of the sentence
        second_sub_string = find_Math_after(mathArr, doc, end, start_id)
        print("Subject: " + str(doc[start:end]) + ' ' + str(second_sub_string))
        return 1
    # if the sentence does not contain the phrase the * of * then return 0 (false)
    return 0

""" 
Parameters: 
mathArr (Array): pass in the array of math functions
end (Int): int value of the end of the pattern
start (Int): int value of the start of the pattern
doc (Array): tokenized sentence
"""
# gets the full string from the math tag before the phrase
# we need this function because math functions can be longer than one token
# we want to grab the entire function
def find_Math_before(mathArr, doc, start, end):
    # loops through the math array, looks at each math function separately
    for math in mathArr:
        # gets the substring before the phrase 'is defined by'
        sub_string = str(doc[start-1])
        # iters backwards through the sentence
        for n in range(start-1, -1, -1):
            # the sub_string is contained in the math function
            if sub_string in math:
                # sub_string matches the full math tag
                # we found the entire math function, return the substring
                if sub_string == math:
                    return sub_string
                # add the next token to the substring and loop again
                else:
                    sub_string = concat_math(sub_string, doc, start, n)
    # sub string was not found in the math array so the token before 
    # the phrase is not part of a math function
    # return just the token before the start            
    return doc[start-1]

""" 
Parameters: 
mathArr (Array): pass in the array of math functions
end (Int): int value of the end of the pattern
start (Int): int value of the start of the pattern
doc (Array): tokenized sentence
"""
# gets the full string from the math tag after the phrase
# we need this function because math functions can be longer than one token
# we want to grab the entire function
# same idea as above
def find_Math_after(mathArr, doc, start, end):
    for math in mathArr:
        sub_string = str(doc[start])
        # loops forward this time through the sentence
        for n in range(end):
            if sub_string in math:
                if sub_string == math:
                    return sub_string
                else:
                    sub_string = concat_math(sub_string, doc, start, start+(n+1))
    # sub string was not found in the math array so the token after 
    # the phrase is not part of a math function
    # return the substring from the end of the pattern to the end of the sentence
    return doc[start:end]

# returns the new substring
def concat_math(sub_string, doc, start, index):
    # if start > index then the index is being added to front of the substring
    if start > index:
        sub_string = str(doc[index:start])
    # else add it to the end of the substring
    else:
        sub_string = str(doc[start:index])
    return sub_string

parseXML()