#!/bin/bash
#SBATCH -n 2
#SBATCH -t 5-00:00:00
#SBATCH -J EMBLmygff3

source /projects/martin/prog/bin/conda_init.sh
conda activate /home/asoares/.conda/envs/EMBLmyGFF3

EMBLmyGFF3 gomcla.gff3 gomcla.fasta  --topology linear --molecule_type 'genomic DNA' --transl_table 1 --species 'Gomphus Clavatus' --locus_tag GOMCLA --project_id PRJEB72358 -o PRJEB72358-GOMCLA.embl
