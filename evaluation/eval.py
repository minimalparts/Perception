################################################################
#concreteness.py
################################################################

from utils import cosine_similarity,normalise
import numpy as np
from math import isnan
import sys
import re

target_forms=["see","sees","saw","seen","seeing"]
#perceptual=["woman","man","child","family","film","movie","painting","car","apple","cat","mountain","hat","house","eye"]
perceptual=["bedroom", "valley", "aircraft", "employer", "dad", "pistol", "stockholder", "chump", "applicant", "murderer", "steeple", "seashore", "daughter", "lawn", "barroom", "furniture", "spouse", "cargo", "radar", "psychologist", "vase", "battlefield", "vicinity", "perceiver", "citizen", "apartment", "lab", "dictionary", "colonel", "battlefront", "anaconda", "artist", "cattle", "aerator", "customer", "businessman", "suburb", "desk", "melilotus", "trader", "hallway", "campaigner", "adversary", "micrometeorite", "professor", "lawyer", "highway", "employee", "bumblebee", "composer", "southerner", "micelle", "kitchen", "cafeteria", "transducer", "electron", "airplane", "redcoat", "tray", "clergyman", "factory", "sword", "weaponry", "historian", "reporter", "movie", "prisoner", "hotel", "serviceman", "anteroom", "subsection", "porch", "equipment", "wife", "doorway", "cadaver", "poet", "grandma", "curate", "salesman", "roadway", "sidewalk", "policeman"]
stopwords=["","(",")","a","about","an","and","are","around","as","at","away","be","become","became","been","being","by","did","do","does","during","each","for","from","get","have","has","had","he","her","his","how","i","if","in","is","it","its","made","make","many","most","not","of","on","or","s","she","some","that","the","their","there","this","these","those","to","under","was","were","what","when","where","which","who","will","with","you","your"]

#################################################
# Read dm file
#################################################

def readDM():
	print "Loading dm space..."
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
	print "Space loaded..."
	dmlines.close()
	return dm_dict


#############################################
# Check for referential use
#############################################

def referential(sentence, obj):
	refs=["page","table","p.","pp.","chapter","below","appendix"]
	m=re.search("^[0-9]*$",obj)
	if m or obj in refs or "( see" in sentence or "see pp." in sentence or "see p." in sentence or len(obj)==1:
		print "REFERENTIAL"
		return True
	else:
		return False

#############################################
# Check consider sense (see as)
#############################################

def seeAs(sentence):
	m=re.search("see[^,]*\sas\s",sentence)
	if m:
		print "SEE AS"
		return True
	else:
		return False

##############################################
# Check for proper name
#############################################

def properName(obj):
	if obj[0].isupper():
		return True
	else:
		return False

##############################################
# Understand
##############################################

def understand(sentence,obj):
	if obj=="point" or "you see" in sentence or "i see" in sentence:
		return True
	else:
		return False

#############################################
#Main function, called by mkQueryPage.py
##############################################

dm_dict=readDM()
senses_precisions={}
senses_counts={}


corpus=open(sys.argv[1],'r')
best_cos=0.0
prediction="p"
ref=False
consider=False
proper=False
getit=False
correct=0
for l in corpus:
	if "<sentence>" in l:
		sentence=l.rstrip('\n')
		best_cos=0.0
		prediction="p"
		consider=seeAs(sentence)
		print sentence
	if "<gr" in l:	
		m=re.search(";(.*)</gr>",l)
		if m:
			print l.rstrip('\n')
			obj=m.group(1)
			proper=properName(obj)
			obj=obj.lower()
			ref=referential(sentence,obj)				#referential use
			getit=understand(sentence,obj)
			if obj in dm_dict:
				for w in perceptual:
					cos=cosine_similarity(dm_dict[w],dm_dict[obj])
					#print w,cos
					if cos > best_cos:	
						best_cos=cos
		print "ref",ref,"consider",consider,"proper",proper
		if ref or proper:
			print "PERCEPTUAL"
			prediction="p"
		else:
			if consider or getit:
				print "NON-PERCEPTUAL"
				prediction="n"
			else:
				if best_cos > 0.20:
					print "PERCEPTUAL"
					prediction="p"
				else:
					print "NON-PERCEPTUAL"
					prediction="n"
	if "<annot" in l:
		m=re.search("<annot>(.*)</annot>",l)
		if m:
			annot=m.group(1)
			if annot=="n" or annot=="p":
				if prediction == annot:
					print "+1"
					correct=1
				else:
					print "+0"
					correct=0
	if "<sense" in l:
		m=re.search("<sense>(.*)</sense>",l)
		sense=m.group(1)
		if sense in senses_precisions:
			senses_precisions[sense]+=correct
			senses_counts[sense]+=1
		else:
			senses_precisions[sense]=correct
			senses_counts[sense]=1
		print l
		print "---"
corpus.close()

score=0.0
num_items=0
for k,v in senses_precisions.items():
	print k,v, senses_counts[k], float(v)/float(senses_counts[k])
	if k.isdigit():
		score+=v
		num_items+=senses_counts[k]

print "OVERALL SCORE",score,num_items,float(score)/float(num_items)
