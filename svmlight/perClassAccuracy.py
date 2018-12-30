import sys
import pandas as pd
from sklearn.metrics import confusion_matrix

gold = sys.argv[1]
predicted = sys.argv[2]

with open(gold) as f:
    goldlines = f.read().splitlines()

with open(predicted) as f:
    predlines = f.read().splitlines()

goldannots = []
predannots = []

for g in goldlines:
    goldannots.append(g.split()[0])

for p in predlines:
    if float(p) > 0:
        predannots.append("1")
    else:
        predannots.append("-1")

#pgold = pd.Series(goldannots)
#ppred = pd.Series(predannots)
#print(pd.crosstab(pgold, ppred, rownames=['True'], colnames=['Predicted'], margins=True))

cm = confusion_matrix(goldannots,predannots, labels=["1", "-1"])
print(cm)

accuracy = (cm[0][0]+cm[1][1]) / sum(cm.flatten())
majority = max(sum(cm[0]),sum(cm[1])) / sum(cm.flatten())

print("Accuracy:", accuracy)
print("Majority class baseline:", majority)
print("Increase over baseline:", accuracy - majority)

print("Precision class 1:",cm[0][0] / sum(cm[0]))
print("Precision class -1:",cm[1][1] / sum(cm[1]))
print("\n\n")

