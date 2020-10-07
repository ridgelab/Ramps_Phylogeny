#! /usr/bin/env python
# This script makes the input state change file for the codon_congruence scripts
# input is ref table of genes, and fasta of ramp sequences
# output is state change file
import sys

refFile = open(sys.argv[1],"r")
inFile = open(sys.argv[2],"r")
outFile = open(sys.argv[3],"w")

#make dictionary of each species to the orthologs it has
geneToSpecies = {}
for line in refFile:
    fields = line.split("\t")
    gene = fields[0]
    species = fields[1]
    if gene not in geneToSpecies:
        geneToSpecies[gene] = set()
    geneToSpecies[gene].add(species)

refFile.close()

#Now make a dictionary of ramp genes to species
rampsToSpecies = {}
for line in inFile:
    if line[0] == ">":
        fields = line.split("__")
        species = fields[0][1:]
        gene = fields[1]
        if gene.startswith("LOC") or "CDS" in gene:
            continue
        if gene not in rampsToSpecies:
            rampsToSpecies[gene] = []
        rampsToSpecies[gene].append(species)
    else:
        continue

inFile.close()

outFile.write("Character\tState\tSpecies\n")
zeros = []
for gene in rampsToSpecies:
    if len(rampsToSpecies[gene]) < 2:
        continue
    for sp in geneToSpecies[gene]:
        if sp not in rampsToSpecies[gene]:
            zeros.append(sp)
    if len(zeros) < 2:
        continue
    outFile.write(gene + "\t0\t")
    outFile.write(",".join(zeros) + "\n")
    outFile.write(gene + "\t1\t")
    outFile.write(",".join(rampsToSpecies[gene])+ "\n")

outFile.close()
