---
Redmine_issue: https://projects.nbis.se/issues/5872
Repository: ENA
Submission_type: HiFi, Isoseq, RNA, mito, assembly, umbrella # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB111466 (umbrella), PRJEB72358 (reads + assembly), PRJEB111463 (mito assembly)
---

# VR EBP - *Gomphus clavatus*

## Submission task description
Within the VR-EBP (Earth Biogenome Project) a fungi, *Gomphus clavatus*, is to be submitted. There are raw reads in form of HiFi, Isoseq and Illumina RNA sequences, an annotated genome assembly and a mito assembly. An umbrella project will be created to collect the two assemblies.

## Procedure overview and links to examples
* [Metadata template](./data/VR-EBP-Gomphus-clavatus-metadata.xlsx)
* Notes on how to [Create EMBL file](https://github.com/NBISweden/annotation-cluster/wiki/ENA-submission#create-embl-file)
* Umbrella project at ENA [how to](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#umbrella-studies)
* [SOP Umbrella projects](../SOP/register_umbrella_projects.md)

### Steps
* [Collect metadata](#collect-metadata)
* [Submit 3 studies](#register-study) (umbrella, raw reads + genome assembly, mito assembly)
* [Submit sample](#register-sample)
* Prepare and submit [raw reads](#register-experiment)
* Prepare and submit [genome assembly](#genome-assembly)
* Prepare and submit [mito assembly](#mito-assembly)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->
* I asked the PI to fill the sample metadata a bit late, in spite of knowing that these things take time.
* If your timeline doesn't align with the researcher's, everything will be dealyed. 
## Detailed step by step description

### Collect metadata

* PI was asked to fill the sample metadata in the template
* I also asked if I should register a ToLID (tree of life ID)
* The NBIS bioinformatician filled the assembly metadata
* The experiments was divided into three tabs, one each of HiFi, Iso and Illumina RNA, and 2 (1 for PacBio and 1 for Illumina) NGI responsible persons were asked to fill in the metadata for these.

* **Update 2026-01-23:** Sample metadata remaining: longitude and latitude needs to be verified/updated, and specimen voucher ID is missing.

### Register study
* All metadata regarding studies is in the ENA_study tab of the metadata template.
* For the *raw reads and the genome* assembly a project was registered in the Webin Portal, receiving `PRJEB72358` as accession number. 
    * Study alias: `GomCla1` 
    * Locus tag: `GOMCLA` 
    * Release date: `2026-02-05`
* **Update 2026-01-23**: The release date was changed to `2026-06-03`

* A study for the *mitochondrial* assembly was registered in the Webin Portal with a release date of `2026-06-03`, study alias `GomClav1-mito`. The accession number obtained was `PRJEB111463`.

* An *umbrella* study was submitted programmatically, with a release date of `2026-06-03`, using [submission.xml](./data/submission.xml) and [umbrella.xml](./data/umbrella.xml):

    ```
    curl -u Username:Password -F "SUBMISSION=@submission.xml" -F "PROJECT=@umbrella.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```

    * Receipt of the sumbission:
    ```
    <RECEIPT receiptDate="2026-04-13T15:13:46.401+01:00" submissionFile="submission.xml" success="true">
        <PROJECT accession="PRJEB111466" alias="GomClav-umbrella" status="PRIVATE" holdUntilDate="2026-06-03+01:00"/>
        <SUBMISSION accession="ERA36069970" alias="SUBMISSION-13-04-2026-15:13:46:186"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
* Accession number received: `PRJEB111466`


### Register sample
* A ToLID was not provided, so I asked for one according to [SOP](../SOP/register_ToLID.md)
    * Taxonomy id: `80588`
    * Specimen ID: `` (this took too long to obtain, so I decided to do submission anyway, then we can **update the sample record later**)
    * Scientific name: `Gomphus clavatus`
    * Received id: `gfGomClav1`
* The sample was registered using the Webin Portal uploading [sample.tsv](./data/sample.tsv) (2026-04-13)
* Received accession number: `ERS29654094`

### Register experiment
* Manifests were created and copied to Uppmax, for each of the three types of sequences:
    * [PacBio HiFi manifest](./data/PRJEB72358-hifi-manifest.txt)
    * [PacBio Isoseq manifest](./data/PRJEB72358-isoseq-manifest.txt)
    * [Illumina RNA manifest](./data/PRJEB72358-Illumina-RNA-manifest.txt)
* They were each submitted using Webin-CLI:
    ```
    interactive -t 08:00:00 -A uppmax2025-2-58
    module load ascp
    java -jar ../webin-cli-9.0.1.jar -context reads -userName $1 -password $2 -manifest $3 -outputDir Webin_output/ -submit
    ```
* HiFi: `ERX16384961`, `ERR17001312`
* Isoseq: `ERX16384963`, `ERR17001314`
* RNA: `ERX16384962`, `ERR17001313`

### Genome assembly
* The bioinformatician produced the embl flat file, which I copied to my laptop
* However, it turned out that it was created without exposing variables of EMBLmyGFF3, so I redid the embl file using `sbatch run_emblmygff3_GOMCLA.sh` on nac-login cluster (script [run_emblmygff3_GOMCLA.sh](./scripts/run_emblmygff3_GOMCLA.sh))
* Validation and submission of [PRJEB72358-genome-manifest.txt](./data/PRJEB72358-genome-manifest.txt) was done locally using webin-cli
    ```
    java -jar ../../../Downloads/webin-cli-9.0.1.jar -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./PRJEB72358-genome-manifest.txt -validate
    ```
* Validation of this file also failed, many duplicated features and they seem to be related to introns. Hence, I need to remove/ignore introns by updating the features .json file:
    ```
    EMBLmyGFF3 --expose_translations
    /* update translation_gff_feature_to_embl_feature.json so that both exons and introns are ignored */
    "exon": {
   "remove": true
    },
    "intron": {
    "remove": true
    },
    ```
* However, when running EMBLmyGFF3 again I get the following:
    ```
    11:06:51 WARNING feature: Unknown qualifier 'makerName' - skipped              ]
    11:06:51 ERROR feature: >>three_prime_utr<< is not a valid EMBL feature type. You can ignore this message if you don't need the feature.
    Otherwise tell me which EMBL feature it corresponds to by adding the information within the json mapping file.
    11:06:51 ERROR feature: >>stop_codon<< is not a valid EMBL feature type. You can ignore this message if you don't need the feature.
    Otherwise tell me which EMBL feature it corresponds to by adding the information within the json mapping file.
    11:06:51 ERROR feature: >>five_prime_utr<< is not a valid EMBL feature type. You can ignore this message if you don't need the feature.
    Otherwise tell me which EMBL feature it corresponds to by adding the information within the json mapping file.
    11:06:51 ERROR feature: >>start_codon<< is not a valid EMBL feature type. You can ignore this message if you don't need the feature.
    Otherwise tell me which EMBL feature it corresponds to by adding the information within the json mapping file.
    11:06:51 WARNING feature: Unknown qualifier 'uniprot_id' - skipped
    ```
    * While I *think* that makerName, start_codon, and stop_codon also can be ignored, I decided to fix the utr errors by changing `three_prime_UTR` to `three_prime_utr` (and dito for five prime) in translation_gff_feature_to_embl_feature.json
* I redid the EMBLmyGFF3 and only the errors I expected remained, so I did a validation with webin-cli (version v2 was copied to PRJEB72358-GOMCLA.embl and gzipped). This resulted in three remaining errors:
    ```
    ERROR: "gene" Features with locations "complement(2589763..2593363)" are duplicated - consider merging qualifiers. [ line: 184423 of PRJEB72358-GOMCLA.embl.gz,  line: 184371 of PRJEB72358-GOMCLA.embl.gz]
    ERROR: "gene" Features with locations "4332788..4336134" are duplicated - consider merging qualifiers. [ line: 212005 of PRJEB72358-GOMCLA.embl.gz, line: 211978 of PRJEB72358-GOMCLA.embl.gz]
    ERROR: "gene" Features with locations "6178906..6182409" are duplicated - consider merging qualifiers. [ line: 1073970 of PRJEB72358-GOMCLA.embl.gz, line: 1073935 of PRJEB72358-GOMCLA.embl.gz]
    ```
    * Duplications (extracted gff3 is in [duplicate_genes.gff3](./data/duplicate_genes.gff3)):
    ```
    NBISG00000001526 and NBISG00000001527
    NBISG00000001971 and NBISG00000001972
    NBISG00000006661 and NBISG00000006662
    ```
    * I asked bioinformaticians for help and received an updated .gff3 file where the script [filter_gomphus.sh](./scripts/filter_gomphus.sh) was used.
* **Version 3:**
    * I copied the new (filtered) .gff3 to my laptop and created a new .embl file:
        ```
        EMBLmyGFF3 gomcla_filtered.gff3 gomcla.fasta  --topology linear --molecule_type 'genomic DNA' --transl_table 1 --species 'Gomphus Clavatus' --locus_tag GOMCLA --project_id PRJEB72358 -o PRJEB72358-GOMCLA-v3.embl
        cp PRJEB72358-GOMCLA-v3.embl PRJEB72358-GOMCLA.embl
        gzip PRJEB72358-GOMCLA.embl
        conda deactivate
        java -jar ../webin-cli-9.0.1.jar -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./PRJEB72358-genome-manifest.txt -validate
        ```
    * It finally validated without errors:
        ```
        INFO : Connecting to FTP server : webin2.ebi.ac.uk
        INFO : Creating report file: /home/yvonne/Gomphus-clavatus/././webin-cli.report
        INFO : Uploading file: /home/yvonne/Gomphus-clavatus/PRJEB72358-GOMCLA.embl.gz
        INFO : Files have been uploaded to webin2.ebi.ac.uk.
        INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ29300436
        ```
* Accession number: `ERZ29300436`

* Note: When running webin-cli locally on my laptop, I need to do `conda deactivate` before since I otherwise have an environment loaded by default that has wrong java version, but EMBLmyGFF3 needs the python version (3.10) which I have in my automatically activated conda environment.

* Accessioned:
    ```
    ASSEMBLY_NAME | ASSEMBLY_ACC  | STUDY_ID   | SAMPLE_ID   | CONTIG_ACC                      | SCAFFOLD_ACC | CHROMOSOME_ACC
    gfGomCla1.1   | GCA_982584905 | PRJEB72358 | ERS29654094 | CEWXVF010000001-CEWXVF010000028 |              |
    ```

### Mito assembly
* Since mito assemblies consists of only one sequence in the sequence file, a [chromosome assembly](https://ena-docs.readthedocs.io/en/latest/submit/assembly/genome.html#chromosome-assembly) submission is the way to go:
    * The manifest needs one additional file, therein referenced as `CHROMOSOME_LIST: chromosome_list.txt.gz`
    * In this [chromosome_list.txt](./data/chromosome_list.txt), a single row is added `1	MIT	Linear-Chromosome	Mitochondrion`
    * The [naming convention](https://ena-docs.readthedocs.io/en/latest/submit/fileprep/assembly.html#chromosome-list-file)
* Validation and submission of [PRJEB111463-mito-manifest.txt](./data/PRJEB111463-mito-manifest.txt) was done using webin-cli
    ```
    java -jar ../../../Downloads/webin-cli-9.0.1.jar -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./PRJEB111463-mito-manifest.txt -validate
    ```
* Receipt:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /home/yvonne/Gomphus-clavatus/././webin-cli.report
    INFO : Uploading file: /home/yvonne/Gomphus-clavatus/gomcla_mtdna.fasta.gz
    INFO : Uploading file: /home/yvonne/Gomphus-clavatus/chromosome_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ29285835
    ```
* Accession number: `ERZ29285835`
* Accessioned:
    ```
    ASSEMBLY_NAME    | ASSEMBLY_ACC  | STUDY_ID    | SAMPLE_ID   | CONTIG_ACC | SCAFFOLD_ACC | CHROMOSOME_ACC
    gfGomCla1-mito.1 | GCA_982449375 | PRJEB111463 | ERS29654094 |            |              | OZ457914-OZ457914
    ´´´
