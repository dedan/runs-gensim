
import os
import csv
import glob

path = '/Users/dedan/projects/mpi/data/corpora/sparql/gsquared_new_csvs/'

word_id = {}
with open('/Users/dedan/projects/mpi/data/corpora/sparql/id_word.txt') as f:
    for line in f.readlines():
        idx, word = line.strip().split('\t')
        word_id[word] = idx


ref = open(path + 'reference.queries', 'w')
for fname in glob.glob(path + '*.csv'):
    wordid = word_id[os.path.basename(fname)[:-4]]
    print fname
    table = csv.reader(open(fname), delimiter=',')
    out = open(fname[:-3]+'txt', 'w')
    print fname[:-3]+'txt'
    for row in table:
        print row[0]
        out.write(row[0].replace(' ', '_') +'\n')
        ref.write(wordid + ' 0 0 ' + row[0].replace(' ', '_') + " " + row[1] + '\n')
    out.close()

