# Ramps_Phylogeny
# Truncated analysis

######################

This directory contains the script used to remove the first 50 codons from each gene. This serves as a control, since 
the ramp sequence is estimated to occur within the first 50 codons. After removing 50 codons, ramps can be identified
and the analyses can be repeated using the scripts in the other directories.

######################

Step 1: Remove the first 50 codons from each gene
    python makeTrunc.py ../IdentifyRamps/data/vertebrate_mammalian_table vertebrate_mammalian_shortened

