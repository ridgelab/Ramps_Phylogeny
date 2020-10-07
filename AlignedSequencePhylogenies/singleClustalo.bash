#!/bin/bash

mkdir -p ../../${3}/Aligned/${2}
mkdir -p ../../${3}/Matrix/${2}
prefix='aligned_'
newfile=$prefix$1
prefix2='matrix_'
distfile=$prefix2$1
echo "Clustalo... inputs are " $1 "and " $2
clustalo -i $1 -o ../Aligned/${2}/${newfile} --distmat-out ../Matrix/${2}/${distfile} --full --force --percent-id
