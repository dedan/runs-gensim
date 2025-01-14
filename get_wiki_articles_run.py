#!/usr/bin/env python
# encoding: utf-8
"""

get the wikipedia articles for lists of words provided in textfiles

these textfiles have to be together in one folder. Necessary is also a
reference.queries file in the same folder which contains the human ratings.

Output is an articles.pickle file that can later be investigated with e.g.
    * topic_clusters_task
    * topic_noise_task

further output is the file info.pickle which contains information on
missing words, etc..

"""

from gensim.corpora import wikicorpus
from gensim.parsing.preprocessing import preprocess_string
import codecs
import glob
import mwclient
import os
import pickle
import re
import sys
import tools
import unicodedata as ud
import urllib


def main(param_file=None):

    # setup
    p, base_path, output_dir = tools.setup(param_file)
    logger = tools.get_logger('gensim', os.path.join(output_dir, "run.log"))
    logger.info("running %s" % ' '.join(sys.argv))

    # initializations
    articles = {}
    all_missing = []
    redir_on = {}
    collisions = {}
    non_ascii = []
    site = mwclient.Site('en.wikipedia.org', '/w/api.php/')

    # get all txt files in a folder and iterate over them
    filelist = glob.glob(os.path.join(base_path,
                                      p['folder_path'],
                                      "*.txt"))
    for f in filelist:

        # get the word we are working on
        f_name = os.path.basename(f)
        k_word = os.path.splitext(f_name)[0]
        logger.info("working on file: %s" % f_name)

        # try to convert the word into ascii for the http query
        file_obj = codecs.open(f, "r", "utf-8")
        counter = 0
        words = []
        for w in file_obj.readlines():
            try:
                s = w.strip().decode('ascii')
                words.append(s)
            except Exception:
                counter += 1
                non_ascii.append(w.strip())
        logger.info("\t%d words containing non ascii are ommited" % counter)

        articles[k_word] = {}
        logger.info("\tfound %d words in file" % len(words))

        for word in words:
            data = {}
            page = site.Pages[word]

            # follow the redirect and check for collisions
            if page.redirect:
                res = re.search('\[\[(.+)\]\]', page.edit())
                redir_word = urllib.unquote(res.groups()[0])
                if redir_word in redir_on:
                    logger.warning("[%s AND %s] both redirect on --> %s" %
                                    (word, redir_on[redir_word], redir_word))
                    collisions[redir_word] = redir_on[redir_word]
                else:
                    logger.info("[%s] redir from [%s]" % (redir_word, word))
                    redir_on[redir_word] = word
                text = site.Pages[redir_word].edit()
                data['redirected'] = redir_word

            else:
                text = page.edit()

            # check for missing wikipedia articles
            if  text == "":
                all_missing.append(word)
                continue

            # preprocess the received article
            data['text'] = wikicorpus.filter_wiki(text)
            in_ascii = ud.normalize('NFKD',
                                    data['text']).encode('ascii', 'ignore')
            data['text'] = preprocess_string(in_ascii)
            articles[k_word][word] = data

    logger.info('add human rating to the articles')
    id_word = {}
    sparql_path = os.path.join(base_path, p['sparql_path'])
    with open(os.path.join(sparql_path, 'id_word.txt')) as f:
        for line in f.readlines():
            idx, word = line.strip().split('\t')
            id_word[idx] = word

    #add human rating to the wikipedia data
    not_found = []
    with open(os.path.join(base_path,
                           p['folder_path'],
                           p['human_file'])) as f:
        for line in f.readlines():
            arr = line.split()
            word = id_word[arr[0]]
            term = arr[3]
            try:
                articles[word][term]['rating'] = float(arr[4])

            except KeyError:
                not_found.append(term)
    logger.info("%d words from the ref queries not found" % len(not_found))

    f = open(os.path.join(output_dir, "articles.pickle"), 'wb')
    pickle.dump(articles, f)
    f.close

    info = {}
    info['missing'] = all_missing
    info['redirs'] = redir_on
    info['collisions'] = collisions
    info['not_found'] = not_found
    info['non_ascii'] = non_ascii
    f = open(os.path.join(output_dir, "info.pickle"), 'wb')
    pickle.dump(info, f)
    f.close

    logger.info("%d redirecting collisions (see info.pkl)" % len(collisions))

if __name__ == '__main__':
    main()
