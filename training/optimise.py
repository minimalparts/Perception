from bayes_opt import BayesianOptimization
from bayes_opt.observer import JSONLogger
from bayes_opt.event import Events
from bayes_opt.util import load_logs
from classify import read_features, validate
from math import isnan
from random import shuffle
import numpy as np
import os
import sys

basedir = sys.argv[1]
word = sys.argv[2]
jsonname = basedir+"/optim.json"
external_vector_file = basedir+"/"+basedir+"_"+word+"_optim_features.txt"
checkpointsdir = basedir+'/optim'

if not os.path.exists(checkpointsdir):
    os.makedirs(checkpointsdir)

logger = JSONLogger(path=jsonname)
pbounds = {'hiddensize': (100, 400), 'lrate': (0.001, 0.01), 'wdecay': (0.001,0.01), 'batchsize': (4,200), 'epochs': (1,50)}

features, annots = read_features(external_vector_file)
ids = [i for i in range(len(annots))]
shuffle(ids)
train_ids = np.array(ids[:150])
test_ids = np.array(ids[151:])

def train(lrate, batchsize, epochs, hiddensize, wdecay):
    score = validate(features, train_ids, test_ids, annots, lrate, int(batchsize), int(epochs), int(hiddensize), wdecay)
    if isnan(score):
        score = 0
    return score

optimizer = BayesianOptimization(
    f=train,
    pbounds=pbounds,
    random_state=1,
)

optimizer.subscribe(Events.OPTMIZATION_STEP, logger)
#load_logs(optimizer, logs=["eva.optimisation_logs.r1.json"])

optimizer.maximize(
    init_points=2,
    n_iter=200,
)

print(optimizer.max)
