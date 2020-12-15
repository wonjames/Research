from spacy.lang.en import English
from spacy.pipeline import EntityRuler
import re
text = 'If f(t) and g(t) are continuous and \mathscr{L}\mskip-3.0mu f\mskip 3.0mu \left(s\right)=\mathscr{L}\mskip-3.0mu g \mskip 3.0mu \left(s\right) , then f(t)=g(t)'
x = re.search(r'(?i)^if.then\w*', text)
print(x)