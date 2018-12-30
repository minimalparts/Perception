import sys
import csv
import random

def read_gold():
    gold = []
    with open('aware.annot.csv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            if row['Perc'] in ["","P","?"]:
                annot = 'p'
            else:
                annot = 'n'
            gold.append("<sentence>"+row['sentence']+"</sentence><annot>"+annot+"</annot>")
    return gold

gold = read_gold()
random.shuffle(gold)

for g in gold:
    print(g)

