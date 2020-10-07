# Ramps_Phylogeny
# IdentifyRamps

######################

Data files were downloaded from the NCBI and then parsed for coding seequence regions using the program
gff3_parser.py from https://github.com/ridgelab/analyze_CDS_regions. The dataset is included for
convenience in data/vertebrate_mammalian_table and data/vertebrate_other_table.
The data should be uncompressed using gunzip prior to running analyses.

The examples in this README are including for analyzing Mammalian vertebrates. The same scripts can be
used to analyze non-mammalian vertebrates by switching the name of the input file to vertebrate_other for 
all commands.

######################

Step 1: Make individual species Fasta files
    python makeSpeciesFastas.py data/vertebrate_mammalian_table species_fastas/vertebrate_mammalian

Step 2: Identify ramp sequences from each species Fasta file.
    This command will take approximately 2 days, 16 CPUs, and 16G of memory per processor core.
    bash runRamps.bash species_fastas/vertebrate_mammalian ramp_fastas/vertebrate_mammalian

Step 3: Combine ramp sequences and sequences after the ramp into one Fasta file each
    cat ramp_fastas/vertebrate_mammalian/ramps_* >> vertebrate_mammalian_ramps.fasta
    cat ramp_fastas/vertebrate_mammalian/after_* >> vertebrate_mammalian_after.fasta

Step 4: Make combined sequence Fasta file
    python makeCombinedSeqFasta.py vertebrate_mammalian_ramps.fasta vertebrate_mammalian_after.fasta vertebrate_mammalian_combined.fasta

