"""Preception - classification

Usage:
  classify.py --file=<s> --lr=<n> --batch=<n> --epochs=<n> --hidden=<n> --wdecay=<n> 
  classify.py (-h | --help)
  classify.py --version
"""

import sys
import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as td
import numpy as np
from docopt import docopt
from random import shuffle
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score


class MLP(nn.Module):
    def __init__(self,inputsize,hiddensize):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(inputsize,hiddensize)
        self.fc2 = nn.Linear(hiddensize,hiddensize)
        self.fc3 = nn.Linear(hiddensize,2)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.softmax(self.fc3(x),dim=1)
        return x



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
            if annot == "p":
                annots.append([0,1])
            else:
                annots.append([1,0])
        except:
            continue
    return np.array(features),np.array(annots)

def predict(p):
    if p[0] > [1]:
        return 0
    else:
        return 1

def baseline(targets):
    nitem = len(targets)
    n0 = sum([1 for i in targets if list(i) == [1,0]])
    n1 = sum([1 for i in targets if list(i) == [0,1]])
    c0 = n0 / nitem
    c1 = n1 / nitem
    if c0 > c1:
        return c0
    else:
        return c1

def return_classes(targets):
    classes = []
    for i in targets:
        if i[0] > i[1]:
            classes.append(0)
        else:
            classes.append(1)
    return classes


args = docopt(__doc__, version='Ideal Words 0.1')
lrate = float(args["--lr"])
batchsize = int(args["--batch"])
epochs = int(args["--epochs"])
hiddensize = int(args["--hidden"])
wdecay = float(args["--wdecay"])
filename = args["--file"]

features,annots = read_features(filename)
ids = [i for i in range(len(annots))]
shuffle(ids)
kf = KFold(n_splits=5)

for train, test in kf.split(ids):
    train_ids = np.array(ids)[train]
    test_ids = np.array(ids)[test]
    
    net = MLP(features.shape[1],hiddensize)
    optimizer = torch.optim.Adam(net.parameters(), lr=lrate, weight_decay=wdecay)   
    #criterion = nn.CrossEntropyLoss()
    criterion = nn.MSELoss()

    for epoch in range(epochs):
        print("Epoch {}".format(epoch))
        losses = []
        shuffle(train_ids)
        c = 0
        for i in range(0,len(train_ids),batchsize):
            X, Y = features[train_ids[i:i+batchsize]], annots[train_ids[i:i+batchsize]]
            X, Y = Variable(torch.FloatTensor(X), requires_grad=True), Variable(torch.FloatTensor(Y), requires_grad=False)
            net.zero_grad()
            output = net(X)
            loss = criterion(output, Y)
            losses.append(float(loss.data.numpy()))
            loss.backward()
            optimizer.step()
            prediction = output.data.numpy()[0]
            #print(i,prediction,annots[i])
            c+=1
            if c %20 == 0:
                print("LOSS",sum(losses) / len(losses))
                losses.clear()


    predictions = []
    golds = []

    for i in range(len(test_ids)):
        output = net(Variable(torch.FloatTensor([features[test_ids[i]]])))
        output = output.data.numpy()[0]
        gold = annots[test_ids[i]]
        predictions.append(output)
        golds.append(gold)
        #print(test_ids[i],gold,output)

    print("BASELINE:",baseline(golds))
    #print(return_classes(golds))
    #print(return_classes(predictions))
    print("TEST:",accuracy_score(return_classes(golds),return_classes(predictions)))
    

