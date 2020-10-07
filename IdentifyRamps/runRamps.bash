#!/bin/bash
#First argument is the directory with the input files
#Second argument is the directory to put the output files.

echo "Running ramps!!!"
while read FN
do
	prefix='ramps_'
	newfile=$prefix$FN
	prefix2='after_'
	newfile2=$prefix2$FN
	echo $newfile
	python3 ExtRamp/ExtRamp_v2.py -t 16 -i $1$FN -o $2$newfile -x $2$newfile2
done < <(find $1 -maxdepth 1 -type f -name '*.fasta' -printf "%f\n")
