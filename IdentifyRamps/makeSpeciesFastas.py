#! /usr/bin/env python
#This program takes one of the tables from the refseq directory and makes a fasta file for each species to hold its genes.
import sys
infile = open(sys.argv[1],"r")

SpeciesFastas = {} #key is species, value is file
linenum = 1
for line in infile:
	line = line.strip()
	fields = line.split("\t")
	if len(fields) < 5:
		fields.append("none") #This line is because some of the genes don't have "Standard" at the end
		print("Line: ",linenum)
		print(fields)
	species = fields[1]
	if species not in SpeciesFastas:
		newFile = open(species + ".fasta","w")
		SpeciesFastas[species] = newFile
#	else:
#		newFile = open(species + ".fasta","a")
	header = ">" + fields[1] + "__" + fields[0] + "__" + fields[2] + "__" + fields[4] + "__" + str(linenum)
	seq = fields[3].replace("*","")
	SpeciesFastas[species].write(header + "\n")
	SpeciesFastas[species].write(seq + "\n")
#	SpeciesFastas[species].close()
	linenum += 1

#Close all the files
infile.close()
for species in SpeciesFastas:
	SpeciesFastas[species].close()


