

import json
import tools
import gvgen
import os

senna_path = '/Users/dedan/Downloads/senna-v2.0/'
sentence = 'My brother has a dog that has a cat'
tagged = '[{"term": "My", "chk": "B-NP", "pos": "PRP$", "srl": ["B-A0", "O"]}, {"term": "brother", "chk": "E-NP", "pos": "NN", "srl": ["E-A0", "O"]}, {"srl": ["S-V", "O"], "term": "has", "chk": "S-VP", "pos": "VBZ", "base": "has"}, {"term": "a", "chk": "B-NP", "pos": "DT", "srl": ["B-A1", "B-A0"]}, {"term": "dog", "chk": "E-NP", "pos": "NN", "srl": ["I-A1", "E-A0"]}, {"term": "that", "chk": "S-NP", "pos": "WDT", "srl": ["I-A1", "S-R-A0"]}, {"srl": ["I-A1", "S-V"], "term": "has", "chk": "S-VP", "pos": "VBZ", "base": "has"}, {"term": "a", "chk": "B-NP", "pos": "DT", "srl": ["I-A1", "B-A1"]}, {"term": "cat", "chk": "E-NP", "pos": "NN", "srl": ["E-A1", "E-A1"]}]'
dot_filename = 'test.dot'
jpg_filename = 'test.jpg'

# print json.dumps(tools.tag(sentence, senna_path))


graph = gvgen.GvGen()

bla = json.loads(tagged)
old = None
boxes = []
for i in range(len(bla[0]['srl'])-1, len(bla[0]['srl'])-2, -1):
    for word in bla:
        current_ending = word['srl'][i].split('-')[-1]
        if current_ending != old or current_ending == 'O':
            box = graph.newItem(current_ending)
            if current_ending == 'V':
                top_box = box
            if current_ending != 'O' and current_ending != 'V':
                boxes.append(box)
            old = current_ending
        graph.newItem(word['term'], box)
    for sub_box in boxes:
        graph.newLink(top_box, sub_box)


f = open(dot_filename,'w')
graph.dot(f)
f.close()
os.system('dot -Tjpg %(dot)s -o %(jpg)s' %{"dot": dot_filename, "jpg": jpg_filename})
os.system('open test.jpg')
print boxes
