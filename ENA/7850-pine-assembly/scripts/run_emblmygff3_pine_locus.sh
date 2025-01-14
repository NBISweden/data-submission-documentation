#!/bin/bash
#SBATCH -n 2
#SBATCH -t 5-00:00:00
#SBATCH -J EMBLmygff3-pine

source /projects/martin/prog/bin/conda_init.sh
conda activate /home/asoares/.conda/envs/EMBLmyGFF3
gzip Pinsy01_240308_at01_longest_no_TE_killed_embl_ids-2025-01-10.gff3
EMBLmyGFF3 Pinsy01_240308_at01_longest_no_TE_killed_embl_ids-2025-01-10.gff3.gz Pinsy01_chromosomes_and_unplaced.fasta.gz  --topology linear --molecule_type 'genomic DNA' --transl_table 1 --species 'Pinus sylvestris' --locus_tag PSYLV --locus_numbering_start 1000001 --project_id ERP161594 -o ERP161594-PSYLV-fixlocustag.embl
sed 's/LOCUS1//' ERP161594-PSYLV-fixlocustag.embl > ERP161594-PSYLV.embl
gzip ERP161594-PSYLV.embl