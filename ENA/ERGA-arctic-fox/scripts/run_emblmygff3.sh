#!/bin/bash
#SBATCH -n 2
#SBATCH -t 5-00:00:00
#SBATCH -J EMBLmygff3

source /projects/martin/prog/bin/conda_init.sh
conda activate /home/asoares/.conda/envs/EMBLmyGFF3

EMBLmyGFF3 /projects/annotation/arctic_fox/Delivery/gff/ENA_compatible_final_annotation.gff /projects/annotation/arctic_fox/Delivery/fasta/genome.fa  --topology linear --molecule_type 'genomic DNA' --transl_table 1 --species 'Vulpes lagopus' --locus_tag VULLAG --project_id PRJEB71153 -o PRJEB71153-VulLag.embl
