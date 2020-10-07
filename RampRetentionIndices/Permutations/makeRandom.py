#! /usr/bin/env python
import sys
from random import shuffle
inputF = open(sys.argv[1])
output = open(sys.argv[2],'w')


lines = inputF.readlines()

species = []
badChar = ['(',')',',',';']
for line in lines:
	if not line.strip() in badChar:
		species.append(line.strip())

for i in range(1000):
    shuffle(species)
    curSpecies = 0
    tree = ""
    for line in lines:
    	if not line.strip() in badChar:
    		tree += species[curSpecies]
    		curSpecies +=1
    	else:
    		tree += line.strip()
    output.write(tree + "\n")

output.close()
inputF.close()

