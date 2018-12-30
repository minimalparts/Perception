################################################################
#concreteness.py
################################################################

from utils import cosine_similarity,normalise
import numpy as np
from math import isnan
import sys
import re

target_forms=["see","sees","saw","seen","seeing"]
perceptual=["woman","man","child","family","film","movie","painting","car","apple","cat","mountain","hat"]
stopwords=["","(",")","a","about","an","and","are","around","as","at","away","be","become","became","been","being","by","did","do","does","during","each","for","from","get","have","has","had","he","her","his","how","i","if","in","is","it","its","made","make","many","most","not","of","on","or","s","she","some","that","the","their","there","this","these","those","to","under","was","were","what","when","where","which","who","will","with","you","your"]

#################################################
# Read gold standard file
#################################################

def readGold():
	print "Loading gold standard..."
	gold={}
	gold_lines=open("../annotation/see.annot.txt",'r')
	
	#Make dictionary with key=row, value=vector
	for l in gold_lines:
		items=l.rstrip('\n').split('\t')
		sentence=items[0].lower()
		gold[sentence]=[items[1],items[2]]
		#print sentence,items[2]
	print "Gold standard loaded..."
	print len(gold),"entries..."
	gold_lines.close()
	return gold


#############################################
#Main function
##############################################

gold=readGold()

corpus=open("../data/ALL.see.data",'r')
sentence=""
for l in corpus:
	if "<sentence>" in l:
		m=re.search("<sentence>(.*)<.sentence>",l)
		if m:
			sentence=m.group(1).lower()
			#print sentence
	if "<gr" in l:	
		m=re.search(";(.*)</gr>",l)
		if m:
			if sentence in gold:
				print "<sentence>"+sentence+"</sentence>"
				print l.rstrip('\n')
				print "<annot>"+gold[sentence][1]+"</annot>"
				print "<sense>"+gold[sentence][0]+"</sense>"
corpus.close()
