# Update annotation of *L. perenne*
*L. perenne* hap1 annotation for TSS1 gene (mentioned in their paper) was incorrect, and research group asked us to update the annotation. There were originally 2 transcripts predicted, `t1STRG.34.1.p1` and `t1STRG.34.1.p2`, and somewhere when merging, the incorrect one (p1) was kept.

Bioinformatician has corrected the annotation, and it is time for submission of the updated version.

The current version is: [GCA_965240515.2]()https://www.ebi.ac.uk/ena/browser/view/GCA_965240515.2

I will work on nac-login:
* I've located the manifest used last time, and made an updated version [Linum_per_hap1-v2_manifest.txt](./data/Linum_per_hap1-v2_manifest.txt) where name of embl file and assembly name is the only update.
* I've located the fasta file, and copied to my working directory, and also put a copy of the .gff file the bioinformatician has fixed there.
* Create an embl flat-file using the following settings (see also [run_emblmygff3_PER_HAP1.sh](./scripts/run_emblmygff3_PER_HAP1.sh)):
    ```
    source /projects/martin/prog/bin/conda_init.sh
    conda activate /home/asoares/.conda/envs/EMBLmyGFF3

    EMBLmyGFF3 Linum_perenne_hap1_final_cleaned_TSS_transcript_updated.gff Linum_perenne_hap1_noMit_noPlast_rm_nomoth.fasta  --topology linear --molecule_type 'genomic DNA' --transl_table 1 --species 'Linum perenne' --locus_tag LINPERHAP1 --project_id PRJEB87194 -o Linum_perenne_hap1_final_cleaned_TSS_transcript_updated.embl
    gzip -k Linum_perenne_hap1_final_cleaned_TSS_transcript_updated.embl

    ```
* Execute the script on nac-login (Submitted batch job 424533):
    ```
    sbatch ./run_emblmygff3_PER_HAP1.sh
    ```

