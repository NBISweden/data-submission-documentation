#!/bin/bash
#SBATCH -n 2
#SBATCH -t 5-00:00:00
#SBATCH -J EMBLmygff3

source /projects/martin/prog/bin/conda_init.sh
conda activate /home/asoares/.conda/envs/EMBLmyGFF3

EMBLmyGFF3 Linum_perenne_hap1_final_cleaned_TSS_transcript_updated.gff Linum_perenne_hap1_noMit_noPlast_rm_nomoth.fasta  --topology linear --molecule_type 'genomic DNA' --transl_table 1 --species 'Linum perenne' --locus_tag LINPERHAP1 --project_id PRJEB87194 -o Linum_perenne_hap1_final_cleaned_TSS_transcript_updated.embl
gzip -k Linum_perenne_hap1_final_cleaned_TSS_transcript_updated.embl

