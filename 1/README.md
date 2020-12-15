## Research Defintion Pattern Recognition
By: James Won

## About
This research project was conducted under Professor Youssef at The George Washington University. We looked into math definitions through XML files and searched for patterns in the sentences that contain definitions. We used the dataset from DLMF NIST. Pattern Recognition was done through SpaCy and Python. In this one semester research project we were able to find 4 patterns that clearly show definitions in the sentences. These patterns were: "is defined by", "Let * be | then *", "Suppose * then | is *", "If * then *".

## Running the Project
- Python must be installed
- Clone Repository
- Run command `python is_defined_by.py` for "is defined by" definitions
- Run command `python if_then_definition.py` for "if then" definitions
- Run command `python suppose_definition.py` for "suppose be | is" definitions
- Run command `python let_be_definition.py` for "let be | where" definitions
- Each commonad will print out the sentences that have defintions that match the pattern and include the predicted subject and defintion