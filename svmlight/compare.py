#Compare system and human predictions
import sys
import numpy as np

sys_file = sys.argv[1]
hum_file = sys.argv[2]

def read_system():
    preds = []
    f = open(sys_file)
    for l in f:
        l = float(l.rstrip('\n'))
        if l < 0:
            preds.append(-1)
        else:
            preds.append(1)
    f.close()
    return np.array(preds)

def read_human():
    annots = []
    f = open(hum_file)
    for l in f:
        annots.append(int(l.split()[0]))
    f.close()
    return np.array(annots)


preds = read_system()
annots = read_human()

diffs = preds - annots
print(1 - sum(1 for i in diffs if i != 0) / len(diffs))
