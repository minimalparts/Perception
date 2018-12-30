#Grab academic texts in the BNC (XML version)

from nltk.tokenize import word_tokenize
import re, os

def cleanxml(raw_xml):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_xml)
    cleantext = ' '.join(word_tokenize(cleantext))
    return cleantext.lower()

def find_academic(filename):
    trigger = False
    f = open(filename,'r')
    for l in f:
        if '<wtext type="ACPROSE">' in l:
            trigger = True
        if trigger:
            l = l.rstrip('\n')
            print(cleanxml(l))
        if '</wtext>' in l:
            trigger = False

listOfFiles = list()
for (dirpath, dirnames, filenames) in os.walk('/home/aurelie/Corpora/BNC/BNC-XML/download/'):
    listOfFiles += [os.path.join(dirpath, file) for file in filenames if '.xml' in file]

for f in listOfFiles:
    find_academic(f)
