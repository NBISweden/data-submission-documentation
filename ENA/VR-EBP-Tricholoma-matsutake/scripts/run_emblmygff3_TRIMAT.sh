#!/bin/bash
#SBATCH -n 2
#SBATCH -t 5-00:00:00
#SBATCH -J EMBLmygff3

source /projects/martin/prog/bin/conda_init.sh
conda activate /home/asoares/.conda/envs/EMBLmyGFF3

EMBLmyGFF3 pmne_functional_v2.removeReactomeMetaCyc_ENA.fixed.gff gfTriMats.pri.20231213.fa.gz  --topology linear --molecule_type 'genomic DNA' --transl_table 1 --species 'Tricholoma matsutake' --locus_tag TRIMAT --project_id PRJEB72359 -o PRJEB72359-TRIMAT.embl
gzip PRJEB72359-TRIMAT.embl
