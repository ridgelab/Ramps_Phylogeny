#! /usr/bin/env python

import sys
import os

infile = open(sys.argv[1],"r")
outDir = sys.argv[2]

if not os.path.exists(outDir):
        os.makedirs(outDir)

genes = {}
for line in infile:
    line = line.strip()
    if line[0] == ">":
        header = line
    else:
        seq = line
        fields = header.split("__")
        species = fields[0]
        gene = fields[1]
        gene = gene.replace("/","-").replace("\\","-")
        if gene.startswith("LOC") or gene.startswith("CDS"):
            pass
        elif gene not in genes:
            genes[gene] = {species:[header,seq]}
        else:
            if species in genes[gene]:
                if len(genes[gene][species][1]) < len(seq): #Use < for longest isoform, > for shortest
                    genes[gene][species] = [header,seq]
            else:
                genes[gene][species] = [header,seq]

infile.close()

num = 1
directoryNum = 1
for gene in genes:
    if num % 1000 == 1:
        if not os.path.exists(outDir + "/" + str(directoryNum)):
            os.mkdir(outDir + "/" + str(directoryNum))
        currentDir = outDir + "/" + str(directoryNum)
        directoryNum += 1

    outfile = open(currentDir + "/" + gene + ".fasta","w")
    for species in genes[gene]:
        header = genes[gene][species][0]
        seq = genes[gene][species][1]
        outfile.write(header + "\n")
        outfile.write(seq + "\n")

    outfile.close()
    num += 1
