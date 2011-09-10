

import csv
import glob

path = '/Users/dedan/projects/mpi/data/corpora/sparql/gsquared_new/*.csv'

for fname in glob.glob(path):
    print fname
    table = csv.reader(open(fname), delimiter=',')
    out = open(fname[:-3]+'txt', 'w')
    print fname[:-3]+'txt'
    for row in table:
        print row[0]
        out.write(row[0] +'\n')
    out.close()

