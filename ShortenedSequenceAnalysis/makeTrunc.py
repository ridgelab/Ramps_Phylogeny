#! /usr/bin/env python
#This script removes the first 50 codons from each gene in a fasta file
import sys

infile = open(sys.argv[1],"r")
outfile = open(sys.argv[2],"w")

for line in infile:
    fields = line.split("\t")
    fields[3] = fields[3].replace("*","")
    fields[3] = fields[3][150:] #This line removes 50 codons or 150 nucleotides
    newline = "\t".join(fields)
    outfile.write(newline)

infile.close()
outfile.close()
