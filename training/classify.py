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

# torch.cuda.is_available() checks and returns a Boolean True if a GPU is available, else it'll return False
is_cuda = torch.cuda.is_available()

# If we have a GPU available, we'll set our device to GPU. We'll use this device variable later in our code.
if is_cuda:
    device = torch.device("cuda")
    print("GPU is available")
else:
    device = torch.device("cpu")
    print("GPU not available, CPU used")

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

def train_model(features, annots, train_ids, lrate, batchsize, epochs, hiddensize, wdecay):
    net = MLP(features.shape[1],hiddensize).to(device)
    optimizer = torch.optim.Adam(net.parameters(), lr=lrate, weight_decay=wdecay)   
    #criterion = nn.CrossEntropyLoss()
    criterion = nn.MSELoss()

    for epoch in range(epochs):
        #print("Epoch {}".format(epoch))
        losses = []
        shuffle(train_ids)
        c = 0
        for i in range(0,len(train_ids),batchsize):
            X, Y = features[train_ids[i:i+batchsize]], annots[train_ids[i:i+batchsize]]
            X, Y = Variable(torch.FloatTensor(X).to(device), requires_grad=True), Variable(torch.FloatTensor(Y).to(device), requires_grad=False)
            net.zero_grad()
            output = net(X)
            loss = criterion(output, Y)
            losses.append(float(loss.data.cpu().numpy()))
            loss.backward()
            optimizer.step()
            prediction = output.data.cpu().numpy()[0]
            #print(i,prediction,annots[i])
            c+=1
            #if c %20 == 0:
            #    print("LOSS",sum(losses) / len(losses))
            #    losses.clear()
    return net

def test_model(net, features, annots, test_ids):
    predictions = []
    golds = []
    for i in range(len(test_ids)):
        output = net(Variable(torch.FloatTensor([features[test_ids[i]]]).to(device)))
        output = output.data.cpu().numpy()[0]
        gold = annots[test_ids[i]]
        predictions.append(output)
        golds.append(gold)
        #print(test_ids[i],gold,output)

    accuracy = accuracy_score(return_classes(golds),return_classes(predictions))
    return accuracy
    
def validate(features, train_ids, test_ids, annots, lrate, batchsize, epochs, hiddensize, wdecay):
    net = train_model(features, annots, train_ids, lrate, batchsize, epochs, hiddensize, wdecay)
    accuracy = test_model(net, features, annots, test_ids)
    return accuracy

if __name__ == '__main__':

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
    
        net = train_model(train_ids, annots, lrate, batchsize, epochs, hiddensize, wdecay)
        accuracy = test_model(net,test_ids)
        print("BASELINE:",baseline(golds))
        print("TEST:",accuracy)

