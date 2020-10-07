#!/usr/bin/env python
#Input is
#1) input directory of state change files
#2) output directory for RI files
#3) output file for summary file

import sys
import os
import numpy as np

if not os.path.exists(sys.argv[2]):
        os.makedirs(sys.argv[2])

allFile = open(sys.argv[3],"w")
allFile.write("Permutation number,meanRI,sdRI\n")

for filename in os.listdir(sys.argv[1]):
    infile = open(sys.argv[1] + "/" + filename,"r")
    n = filename.split("_")[-1]
    outfile = open(sys.argv[2] + "_" + n, "w")
    
    header = infile.readline()
    RIs = []
    for line in infile:
        gene,origin,loss,root_loss,n_small,n_total,percent_total,p = line.split("\t")
        if float(n_small) == 1:
            continue
        g = float(n_small)
        s = float(origin) + float(loss) + float(root_loss)
        m = 1
        retention_index = float(g - s) / (g - m)
        RIs.append(retention_index)
        outfile.write(gene + "\t" + str(retention_index) + "\n")
    
    RIs = np.array(RIs)
    mean = np.mean(RIs)
    sd = np.std(RIs)
    allFile.write(n + "," + str(mean) + "," + str(sd) + "\n")
    infile.close()
    outfile.close()
