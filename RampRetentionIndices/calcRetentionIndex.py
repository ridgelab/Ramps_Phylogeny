#!/usr/bin/env python
import sys
import numpy as np

infile = open(sys.argv[1],"r")
outfile = open(sys.argv[2], "w")

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
print("The mean retention index is ",mean)
print("The standard deviation of the retention indices is ",sd)

infile.close()
outfile.close()
