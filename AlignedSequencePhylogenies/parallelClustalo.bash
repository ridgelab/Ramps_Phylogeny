#!/bin/bash
#This script uses clustalo to create alignments of all the files.
#Input is the directory to align and the number


WORKDIR=$1/$2
cd $WORKDIR
pwd
declare -a my_array
while read FN
do
	if [[ $FN == *" "* ]]; then
		echo "$FN has spaces"
		mv "$FN" "${FN// /_}"
		FN=${FN// /_}
	fi
	if [[ $FN != *"aligned"* ]] && [[ $FN != *"matrix"* ]]; then
		if [[ $(wc -l < ${FN}) -eq 4 ]]
		then
			echo $FN
			echo ">Dummy" >> ${FN}
			echo "A" >> ${FN}
		fi
		if [[ $(wc -l <${FN}) -ge 4 ]]
		then
		
			prefix='aligned_'
			newfile=$prefix$FN
			prefix2='matrix_'
			distfile=$prefix2$FN
			if [[ ! -f "${3}/${2}/${newfile}" ]] || [[ ! -f "${3}/${2}/${distfile}" ]]; then
				echo "$newfile - aligning!"
				my_array+=($FN)
			fi
		fi
	fi

done < <(find . -maxdepth 1 -type f -name '*.fasta' -printf "%f\n")

num=${#my_array[@]}
echo "the array contains $num elements"
echo ${my_array[@]}
if [[ $num -ge 1 ]]; then
echo "Running clustalo!!!"
parallel singleClustalo.bash ::: ${my_array[@]} ::: $2 ::: $1
fi
