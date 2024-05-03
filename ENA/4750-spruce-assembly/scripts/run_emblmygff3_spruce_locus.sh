#!/bin/bash
#SBATCH -n 2
#SBATCH -t 5-00:00:00
#SBATCH -J EMBLmygff3

source /projects/martin/prog/bin/conda_init.sh
conda activate /home/asoares/.conda/envs/EMBLmyGFF3

EMBLmyGFF3 Picab02_230926_at01_longest_no_TE_sorted_CDSonly-nogeneID-pseudoFix.gff3.gz Picab02_chromosomes_and_unplaced.fa.gz  --topology linear --molecule_type 'genomic DNA' --transl_table 1 --species 'Picea abies' --locus_tag PABIES --locus_numbering_start 1000001 --project_id ERP154169 -o ERP154169-PABIES-locus-nosort-v4.embl
sed 's/LOCUS1//' ERP154169-PABIES-locus-nosort-v4.embl > ERP154169-PABIES-fixlocustag-nosort-v4.embl
gzip ERP154169-PABIES-fixlocustag-nosort-v4.embl
