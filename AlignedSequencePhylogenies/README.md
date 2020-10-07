# Ramps_Phylogeny
# Aligned Sequence Phylogenies

######################

The files in this directory are used to infer phylogenies using concatenated sequence data from ramp sequences,
the portion after the ramp, and the whole gene sequence. The input files are created in the IdentifyRamps directory as
vertebrate_mammalian_ramps.fasta, vertebrate_mammalian_after.fasta, and vertebrate_mammalian_combined.fasta.

######################

Step 1: Make a Fasta file of ramp sequences for each orthologous gene.
The orthologous Fasta files will be organized in sub-directories of 1000 genes each.
    python makeOrthologFastas.py ../IdentifyRamps/vertebrate_mammalian_ramps.fasta vertebrate_mammalian_ramp_orthos

Step 2: Align ortholog Fasta files using Clustalo. For convenience, we have included our bash script used to run Clustalo
on all of the files in parallel. The following command should be ran for each sub-directory
created in Step 1, by replacing the number 1 with each sub-directory number.
This can be done using a bash for loop or by running multiple jobs at once.
    ./parallelClustalo.bash vertebrate_mammalian_ramp_orthos 1

Step 3: Make matrix of concatenated sequence data for the ramps in TNT and IQTree format
    python makeSupermatrix.py -id vertebrate_mammalian_ramp_orthos/Aligned/ -it ../IdentifyRamps/data/vertebrate_mammalian_table -tnt vertebrate_mammalian.tnt -iqtree vertebrate_mammalian.phy

Step 4: Reconstruct the phylogeny using parsimony.
    This command requires the TNT program, which can be downloaded here: http://www.lillo.org.ar/phylogeny/tnt/
    ./tnt proc mammal_runfile

Step 5: Reconstruct phylogeny using maximum likelihood
    This command requires IQTree, which can be downloaded here: iqtree.org
    ./iqtree-1.6.8-Linux/bin/iqtree -s vertebrate_mammalian.phy

Step 6: Compare phylogenies with reference phylogenies
    The phylogenies were compared to the reference Open Tree of Life using ete3 branch percent comparison.
    The OTL tree was downloaded from the OTL API using getOTLTree.py, which can be found at https://github.com/ridgelab/codon_pairing/tree/master/other_scripts. 
    The scripts used for the ete comparisons can be found at https://github.com/ridgelab/codon_pairing/tree/master/parsimony/comparisons.

Step 6: Repeat steps 1-5 for the portion after the ramp and the whole gene sequence.
