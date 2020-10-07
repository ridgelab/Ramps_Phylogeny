#! /usr/bin/env python
#This program combines the ramp fasta and after fasta to create the full sequence
#Input is the ramps fasta and the after ramps fasta and the combined fasta output
import sys

ramps = open(sys.argv[1],"r")
after = open(sys.argv[2],"r")

combined = open(sys.argv[3],"w")



header_r = ramps.readline()
header_a = after.readline()
while header_r != "":
	seq_r = ramps.readline()
	seq_a = after.readline()
	if header_r != header_a:
		print("Different headers: ", header_r, "\t", header_a)
	else:
		combined.write(header_r + seq_r.strip() + seq_a)
	header_r = ramps.readline()
	header_a = after.readline()


ramps.close()
after.close()
combined.close()
