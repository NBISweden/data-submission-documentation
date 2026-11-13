# Update annotation of *L. perenne*
*L. perenne* hap1 annotation for TSS1 gene (mentioned in their paper) was incorrect, and research group asked us to update the annotation. There were originally 2 transcripts predicted, `t1STRG.34.1.p1` and `t1STRG.34.1.p2`, and somewhere when merging, the incorrect one (p1) was kept.

Bioinformatician has corrected the annotation, and it is time for submission of the updated version.

The current version is: [GCA_965240515.2]()https://www.ebi.ac.uk/ena/browser/view/GCA_965240515.2

I will work on nac-login:
* I've located the manifest used last time, and made an updated version [Linum_per_hap1-v2_manifest.txt](./data/Linum_per_hap1-v2_manifest.txt) where name of embl file and assembly name is the only update.
* I've located the fasta file, and copied to my working directory, and also put a copy of the .gff file the bioinformatician has fixed there.
* Looking at the .gff file I see that it is not sorted, this might become an issue for EMBLmyGFF3
    * I will make an attempt at running AGAT, see if I can get the .gff sorted according to strand order:
        ```
        source ~/conda_init.sh
        conda activate /home/lucso605/.conda/envs/agat
        agat_convert_sp_gxf2gxf.pl -g Linum_perenne_hap1_final_cleaned_TSS_transcript_updated.gff -o Linum_perenne_hap1_final_cleaned_TSS_transcript_updated_agat.gff
        ```
    * Made no difference (in fact very little at all, so likely this was already done), will skip
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
* There are issues (warnings) running EMBLmyGFF3:
    ```
    14:36:45 WARNING feature: Unknown qualifier 'cov' - skipped                    ]
    14:36:45 WARNING feature: Unknown qualifier 'fPKM' - skipped
    14:36:45 WARNING feature: Unknown qualifier 'gene_id' - skipped
    14:36:45 WARNING feature: Unknown qualifier 'makerName' - skipped
    14:36:45 WARNING feature: Unknown qualifier 'tPM' - skipped
    14:36:45 WARNING feature: Unknown qualifier 'transcript_id' - skipped
    14:36:45 WARNING feature: Unknown qualifier '_AED' - skipped
    14:36:45 WARNING feature: Unknown qualifier '_QI' - skipped
    14:36:45 WARNING feature: Unknown qualifier '_eAED' - skipped
    14:36:45 WARNING feature: Unknown qualifier 'uniprot_id' - skipped
    ```
* I likely can fix at least some of them by exposing translations. I asked Gemini, who suggested that I update the exposed `translation_gff_attribute_to_embl_qualifier.json` with the following:
    ```
    {
    "cov": {
        "source": "cov",
        "target": "note",
        "prefix": "coverage:"
    },
    "fPKM": {
        "source": "fPKM",
        "target": "note",
        "prefix": "FPKM:"
    },
    "tPM": {
        "source": "tPM",
        "target": "note",
        "prefix": "TPM:"
    },
    "_AED": {
        "source": "_AED",
        "target": "note",
        "prefix": "MAKER_AED:"
    },
    "_eAED": {
        "source": "_eAED",
        "target": "note",
        "prefix": "MAKER_eAED:"
    },
    "_QI": {
        "source": "_QI",
        "target": "note",
        "prefix": "MAKER_QI:"
    },
    "makerName": {
        "source": "makerName",
        "target": "note",
        "prefix": "makerName:"
    },
    "gene_id": {
        "source": "gene_id",
        "target": "note",
        "prefix": "original_gene_id:"
    },
    "transcript_id": {
        "source": "transcript_id",
        "target": "note",
        "prefix": "original_transcript_id:"
    },
    "uniprot_id": {
        "source": "uniprot_id",
        "target": "db_xref",
        "prefix": "UniProtKB/TrEMBL:"
    }
    }
    ```
* Rerun of the EBMLmyGFF3 script
* Validate & submit:
    ```
    java -jar ~/webin-cli-10.0.0.jar -username Webin-[XXXXX] -password [PASSWORD] -context genome -manifest Linum_per_hap1-v2_manifest.txt -validate
    ```
    * Validation failed, there are duplicated features, and also something about `Abutting features cannot be adjacent between neighbouring exons`
    * I will try update translations to ignore the exons, but this will likely not fix everything. Bioinformatician is informed
* Receipt:
    ´´´
    ```
