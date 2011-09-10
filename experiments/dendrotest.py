from hcluster import pdist, linkage, dendrogram, centroid
import numpy
from numpy.random import rand
import pylab as plt

X = rand(10,100)
X[0:5,:] *= 2
X = X.T
print numpy.shape(X)
Y = pdist(X)
print numpy.shape(Y)
Z = linkage(Y)
dendrogram(Z)
plt.show()