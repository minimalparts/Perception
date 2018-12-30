import sys
import random

f = sys.argv[1]
o = sys.argv[2]
num_folds = int(sys.argv[3])

def write_list(l,filename):
    f = open(filename,'w')
    for e in l:
        f.write(e+'\n')
    f.close()

with open(f) as data:
    lines = data.read().splitlines()

#random.shuffle(lines)
fold_size = int(len(lines) / num_folds)
print("Fold size is",fold_size)

folds = [lines[x:x+fold_size] for x in range(0, len(lines), fold_size)]
print(len(folds),"folds")

for i in range(len(folds)):
    folds_tmp = folds[:]
    write_list(folds[i],o+str(i)+".tst")
    folds_tmp.pop(i)
    write_list(sum(folds_tmp,[]),o+str(i)+".tr")
