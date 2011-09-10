'''
Created on 21.07.2011

@author: dedan
'''

from nltk.corpus import wordnet as wn
import json
import subprocess as sp

p = sp.Popen(['blabla', '-path',  '/Users/dedan/Downloads/senna-v2.0/'],
             executable='/Users/dedan/Downloads/senna-v2.0/senna',
             stdin=sp.PIPE,
             stdout=sp.PIPE)
# TODO: also has to work with

tagged = p.communicate('To drink alcohol is very good for you in Berlin')[0]

words = []
for line in tagged.split('\n'):
    if not line == '':
        tmp = line.split()
        words.append({'term': tmp[0],
                      'pos': tmp[1],
                      'chk': tmp[2]})
        if not tmp[3] == "O":
            words[-1]['ner'] = tmp[3]
        if len(tmp) > 5:
            if not tmp[4] == "-":
                words[-1]['base'] = tmp[4]
            words[-1]['srl'] = tmp[5]

print json.dumps(words, indent=2)





#        m = regx.search(line)
#        print m.groups()
#        if m.group(3).endswith('ADJP'):
#            words.append(m.group(1))
#
#print words
#
#for word in words:
#    lemmas = [s.lemmas for s in wn.synsets(word, pos=wn.ADJ)]
#    lemmas = sum(lemmas, [])
#    print lemmas
#    print [l.antonyms() for l in lemmas]


