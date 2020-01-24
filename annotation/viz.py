import numpy as np
from math import sqrt
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import sys

def read_features(filename):
    features = []
    annots = []
    f= open(filename,'r')
    for l in f:
        try:
            items=l.rstrip().split()
            annot=items[-1]
            vec=[float(i) for i in items[1].split(',')]
            vec=np.array(vec)
            features.append(vec)
            annots.append(annot)
        except:
            continue
    return features,annots

def cosine_similarity(v1, v2):
    if len(v1) != len(v2):
        return 0.0
    num = np.dot(v1, v2)
    den_a = np.dot(v1, v1)
    den_b = np.dot(v2, v2)
    return num / (sqrt(den_a) * sqrt(den_b))


def compute_PCA(m,dim):
    m -= np.mean(m, axis = 0)
    pca = PCA(n_components=dim)
    pca.fit(m)
    return pca.transform(m)


def draw_plot(features,annots):
    txt = "Class distribution for "+sys.argv[1]+"\n(red = perceptual, blue = non-perceptual)"
    fig = plt.figure()#num=0,figsize=(8.27, 11.69), dpi=300)
    ax  = fig.add_subplot(1, 1, 1)
    ax.set_title(txt)
    for i in range(len(annots)):
        if annots[i] == 'p':
            plt.plot(features[i][0],features[i][1],'o',color='red')
        else:
            plt.plot(features[i][0],features[i][1],'o',color='blue')
    filename = sys.argv[2]
    plt.savefig(filename)
    #plt.show()    


features, annots = read_features(sys.argv[1])
m_2d = compute_PCA(features,2)
#print(m_2d)
draw_plot(m_2d,annots)
