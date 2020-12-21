import xml.etree.ElementTree as ET
import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_sm")

'''
Gets the Defintion for phrases that contain the pattern Let ... 
This is the simple version that gets replaced by the file let_be_defintion.py
'''

# parsing of the sentences
def parseXML():
    root = ET.parse('1/1.tex.xml').getroot()
    val = 0
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
            # total number of defintions in the file
            val += find_definition(sentence, mathArr, i+1)

    print("Total Number of Definitions found: " ,val)

"""
Parameters:
sentence_id (Int): The ID that corresponds to the sentence in the XML file; used for debugging
mathArr (Array): pass in the array of math functions
sentence (Str): the sentence we are parsing
"""
# pattern matching on the phrase Let * 
def find_definition(sentence, mathArr, sentence_id):
    matcher = Matcher(nlp.vocab)
    # two patterns we are searching for in the sentence
    pattern = [{"LEMMA": "let"}, {"IS_ASCII": True, "OP": '*'}]
    matcher.add("FUNC", None, pattern)
    # SpaCy tokenizing of the sentence
    doc = nlp(sentence)
    # number of tokens
    count=len(doc)
    # If there is a match to the pattern it goes into this loop
    # else there is no match return back and get the next sentence
    for match_id, start, end in matcher(doc):
        matched_span = doc[start:end]
        print("Sentence id: ",sentence_id)
        print(sentence)
        arr = findMath(mathArr, doc, start, end, count)
        print("Subject: ", arr[0])
        print("Definition: ", doc[arr[1]:count])
        print('**********************************************************************************')

        return 1
    return 0

""" 
Parameters: 
mathArr (Array): pass in the array of math functions
end (Int): int value of the end of the pattern
start (Int): int value of the start of the pattern
doc (Array): tokenized sentence
count (Int): number of Tokens
"""
# gets the full string from the math tag after the phrase
# we need this function because math functions can be longer than one token
# we want to grab the entire function
# returns the next token or tokens as the subject and the rest of the sentence as the defintion
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

# adds the next token to the substring
def concat_math(sub_string, doc, start, index):
    sub_string = str(doc[start+1:index+1])
    return sub_string

parseXML()