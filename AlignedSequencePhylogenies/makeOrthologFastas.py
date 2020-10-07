#! /usr/bin/env python
# Input is a refseq table from here:
# /fslhome/lmckinno/fsl_groups/fslg_RidgeLab/compute/refseq_Dec_17_2019
# Output is a directory of ortholog files

import sys
import os

infile = open(sys.argv[1],"r")
outDir = sys.argv[2]

genes = {}
for line in infile:
    fields = line.split('\t')
    species = fields[1]
    header = ">" + fields[1] + "_" + fields[2]
    seq = fields[3].upper().replace("*","")
    gene = fields[0]
    gene = gene.replace("/","-").replace("\\","-")
    if gene.startswith("LOC") or gene.startswith("CDS"):
        pass
    elif gene not in genes:
        genes[gene] = {species:[header,seq]}
    else:
        if species in genes[gene]:
            print("Comparing: ",len(genes[gene][species][1]), " to ", len(seq))
            if len(genes[gene][species][1]) < len(seq): #Use < for longest, > for shortest
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

    print(gene)
    outfile = open(currentDir + "/" + gene + ".fasta","w")
    for species in genes[gene]:
        header = genes[gene][species][0]
        seq = genes[gene][species][1]
        outfile.write(header + "\n")
        outfile.write(seq + "\n")

    outfile.close()
    num += 1
