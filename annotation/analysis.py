import sys

############################################
# Load sense definitions
###########################################

def loadDefinitions():
	definitions={}
	f=open("senses-summary.txt",'r')
	for l in f:
		l=l.rstrip('\n')
		fields=l.split("::")
		sense=fields[0]	
		definition=fields[1]
		definitions[sense]=definition
	f.close()	
	return definitions

def getSensesSummary():
	senses={}
	perceptuals={}
	f=open("see.annot.txt")
	for l in f:
		l=l.rstrip('\n')
		fields=l.split('\t')
		sense=fields[1]
		perceptual=fields[2]
		if sense in senses:
			senses[sense]+=1
		else:
			senses[sense]=1
		if perceptual in perceptuals:
			perceptuals[perceptual]+=1
		else:
			perceptuals[perceptual]=1
	f.close()
	return senses,perceptuals

defs=loadDefinitions()
senses,perceptuals=getSensesSummary()

for k,v in senses.items():
	if k in defs:
		print defs[k],v

for k,v in perceptuals.items():
	print k,v
