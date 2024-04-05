#!/bin/bash
#SBATCH -n 2
#SBATCH -t 5-00:00:00
#SBATCH -J EMBLmygff3

source /projects/martin/prog/bin/conda_init.sh
conda activate /home/asoares/.conda/envs/EMBLmyGFF3

EMBLmyGFF3 Lsc.v1.2.gff LSc.v1.2.fa  --topology linear --molecule_type 'genomic DNA' --transl_table 1 --species 'Larinioides sclopetarius' --locus_tag LARSCL --project_id PRJEB74312 -o PRJEB74312-LARSCL.embl
gzip PRJEB74312-LARSCL.embl
