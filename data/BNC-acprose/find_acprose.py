#Grab academic texts in the BNC (XML version)

from nltk.tokenize import word_tokenize
import re, os
import sys

word = sys.argv[1] #either 'see' or 'aware'

see_words = ["see","seeing","sees","saw","seen"]
aware_words = ["aware"]

def cleanxml(raw_xml,word):
    if word == "see":
        words = see_words
    else:
        words = aware_words
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_xml)
    tokens = word_tokenize(cleantext)
    #cleantext = ' '.join(word_tokenize(cleantext))
    keep = False
    for t in tokens:
        if t in words:
            keep = True
            break
    if keep:
        return cleantext
    else:
        return ""

def find_academic(filename):
    trigger = False
    f = open(filename,'r')
    for l in f:
        if '<wtext type="ACPROSE">' in l:
            trigger = True
        if trigger:
            l = l.rstrip('\n')
            l = cleanxml(l,word)
            if l != "":
                print(l)
        if '</wtext>' in l:
            trigger = False

listOfFiles = list()
for (dirpath, dirnames, filenames) in os.walk('/home/aurelie/Corpora/BNC/BNC-XML/download/'):
    listOfFiles += [os.path.join(dirpath, file) for file in filenames if '.xml' in file]

for f in listOfFiles:
    find_academic(f)
