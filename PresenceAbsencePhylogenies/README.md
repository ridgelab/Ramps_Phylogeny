# Ramps_Phylogeny
# PresenceAbsencePhylogeny

######################

The scripts in this directory are used to recover phylogenies based on the presence or absence
of ramp sequences in orthologous genes. The input files needed are created in the IdentifyRamps directory,
which are vertebrate_mammalian_ramps.fasta and vertebrate_other_ramps.fasta.

######################

Step 1: Make a Fasta file for each orthologous gene
    python makeOrthologFastas.py data/vertebrate_mammalian_ramps.fasta data/vertebrate_mammalian_ramp_orthos

Step 2: Make a matrix of characters in TNT and IQTree formats
    python makePresenceAbsenceMatrix.py -id vertebrate_mammalian_ramp_orthos/Aligned/ -it ../IdentifyRamps/data/vertebrate_mammalian_table -tnt vertebrate_mammalian.tnt -iqtree vertebrate_mammalian.phy

Step 3: Reconstruct phylogeny using parsimony
    This command requires the TNT program, which can be downloaded here: http://www.lillo.org.ar/phylogeny/tnt/
    ./tnt proc mammal_runfile

Step 4: Reconstruct phylogeny using maximum likelihood
    This command requires IQTree, which can be downloaded here: iqtree.org
    ./iqtree-1.6.8-Linux/bin/iqtree -s vertebrate_mammalian.phy

Step 5: Compare phylogenies with reference phylogenies
    The phylogenies were compared to the reference Open Tree of Life using ete3 branch percent comparison.
    The OTL tree was downloaded from the OTL API using getOTLTree.py, which can be found at https://github.com/ridgelab/codon_pairing/tree/master/other_scripts. 
    The scripts used for the ete comparisons can be found at https://github.com/ridgelab/codon_pairing/tree/master/parsimony/comparisons.
