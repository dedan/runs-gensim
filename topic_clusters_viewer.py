#!/usr/bin/env python
# encoding: utf-8

'''
clusters viewer

The points in the plots are colored (grayscaled) by the value
a human gave as rating of how good this term fits the sparqle query termn.
'''
import numpy as np
import pylab as plt
import tools
from sumatra.parameters import build_parameters
import sys
from os import path
import pickle
import os
from hcluster import pdist, linkage, dendrogram



# define what should happen when a point is picked
def onpick(event):
    plt.subplot(2, 1, 1)
    event.artist.figure.axes[0].texts = []
    plt.annotate(event.artist.name, (event.artist._x, event.artist._y))


# setup
p = build_parameters(sys.argv[1])
result_path = path.join(p['base_path'], p['result_path'])
output_dir = path.join(result_path, p['sumatra_label'])
if not path.exists(output_dir):
    os.mkdir(output_dir)
logger = tools.get_logger('gensim', path.join(output_dir, "run.log"))
logger.info("running %s" % ' '.join(sys.argv))

data = pickle.load(open(path.join(result_path,
                                  p['data_label'], 'data.pickle')))

for key, val in data.iteritems():
# for bla in [1]:
#     key, val = 'eagle', data['eagle']
    

    fig = plt.figure()
    fig.canvas.mpl_connect('pick_event', onpick)
    plt.subplot(3, 1, 1)
    plt.title(key)

    proj = np.dot(val['U'][:, 0:2].T, val['vecs'])

    print np.shape(proj)
    Y = pdist(proj.T)
    Z = linkage(Y)
    dendrogram(Z)
    
    ax = plt.subplot(3, 1, 2)
    

    for i in range(proj.shape[1]):
        col = (1 - (val['ratings'][i] / 100.0)) * 0.7
        pt, = ax.plot(proj[0, i], proj[1, i],
                       '.',
                       color=('%f' % col),
                       picker=3)
        ax.text(proj[0, i], proj[1, i], i)
        pt.name = val['keys'][i]

    plt.subplot(3, 1, 3)
    plt.plot(val['d'])
    plt.savefig(key + ".png")
#    plt.show()
