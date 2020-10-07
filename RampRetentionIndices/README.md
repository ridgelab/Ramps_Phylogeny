# Ramps_Phylogeny
# Ramp retention index


######################

Step 1: Create table of gene, state (ramp present or absent), and species with that state.
    python makeRampStateTable.py ..IdentifyRamps/data/vertebrate_mammalian_table ../PresenceAbsencePhylogenies/data/vertebrate_mammalian_ramps.fasta vertebrate_mammalian_chars

Step 2: Score characters according to the Open Tree of Life. The script scoreCharactersOnTree.py is from 
https://github.com/ridgelab/codon_congruence. A copy is included here for convenience.
    python scoreCharactersOnTree.py -c vertebrate_mammalian_chars -r data/vertebrate_mammalian_reference.nwk -o vertebrate_mammalian_state_change

Step 3: Calculate retention index
    python calcRetentionIndex.py vertebrate_mammalian_state_change_0 RI_vertebrate_mammalian

###################
Comparison of retention index with random permutations

Step 1: Create 1000 randomly-shuffled trees of the Open Tree of Life
The input for this script is a reference phylogeny with each character and species on a separate line, which can be 
created using regular expressions. An example for Mammalia is included as data/vertebrate_mammalian_ref_unformatted.nwk.
    python Permutations/makeRandom.py vertebrate_mammalian_reference_unformatted.nwk vertebrate_mammalian_shuffled.nwk

Step 2: Score characters according to the permutations of the Open Tree of Life.
    mkdir vertebrate_mammalian_perms
    python scoreCharactersOnTree.py -c vertebrate_mammalian_chars -r vertebrate_mammalian_shuffled.nwk -o vertebrate_mammalian_perms/state_change_perm

Step 3: Calculate retention indices - This will create a directory of retention indices for each permutation as well
as a summary file of the mean retention index for each permutation.
   python Permutations/calcPermRetentionIndex.py vertebrate_mammalian_perms vertebrate_mammalian_RI_files retention_summary_vertebrate_mammalian 



