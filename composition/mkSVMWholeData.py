################################################################
#concreteness.py
################################################################

from utils import cosine_similarity,normalise,mkQueryDist
import numpy as np
from math import isnan
import sys
import re

window_size=5
target_forms=["see","sees","saw","seen","seeing"]

#################################################
# Read dm file
#################################################

def readDM():
	#print "Loading dm space..."
	dm_dict={}
	#dmlines=open("EN-wform.w.5.cbow.neg10.400.subsmpl.txt",'r')
	dmlines=open("ukwac.predict.dm",'r')
	
	#Make dictionary with key=row, value=vector
	for l in dmlines:
		items=l.rstrip('\n').split('\t')
		row=items[0]
		#if row not in stopwords: 
		vec=[float(i) for i in items[1:]]
		dm_dict[row]=normalise(vec)
	#print "Space loaded..."
	dmlines.close()
	return dm_dict


#################################
# Print function
#################################

def printInstance(v,annot):
	l=str(annot)+" "
	for i in range(len(v)):
		l=l+str(i+1)+":"+str(v[i])+" "
	l=l[:-1]
	print l


#############################################
#Main function, called by mkQueryPage.py
##############################################

dm_dict=readDM()
senses_precisions={}
senses_counts={}


corpus=open(sys.argv[1],'r')
annot=""
v=[]
for l in corpus:
	sentence=l.rstrip('\n').split()
	best_cos=0.0
	#print sentence
	
	window=""
	for i in range(len(sentence)):
		w=sentence[i].lower()
		if w in target_forms:
			for j in range((max(0,i-window_size)),min(len(sentence),i+window_size+1)):
				if j !=i:
					window+=sentence[j]+" "
			break
	window=window[:-1]
	#print window
	v=mkQueryDist(window,dm_dict)

        if len(v) > 0:				
            printInstance(v,1)			#Print default annotation of 1, just to have something there...
			
corpus.close()

