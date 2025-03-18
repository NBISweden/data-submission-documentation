---
Redmine_issue: https://projects.nbis.se/issues/7850
Repository: ENA
Submission_type: assembly
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB77112/ERP161594
---

# 7850 - Submission of pine (*Pinus sylvestris*) genome assembly

## Submission task description
Raw data is already submitted, to project ERP161594, needed now is help with creating an .embl file and submissin to ENA using Webin-CLI. A manifest is already prepared, and deducing by this the assembly should be submitted to the same project as the raw reads.

Similar to Spruce, were we also helped out.

* Annotation with 49387 coding genes.
* No unplaced scaffolds
* AGP file exists but when submitting spruce we never got it to work.
* Should be submitted using researchers ENA credentials

## Procedure overview and links to examples

* [UPSC-0230.Manifest.txt](./data/UPSC-0230.Manifest.txt)
* [UPSC-0230.ChromosomeList.txt](./data/UPSC-0230.ChromosomeList.txt)

* Make .embl file from Pinsy01_chromosomes_and_unplaced.fasta.gz and Pinsy01_240308_at01_longest_no_TE.gff3.gz

## Lessons learned
* Had issues with Webin-CLI requiring newer java runtime version (version 17) 
    * I managed to update to java 17 on my laptop, but Webin-CLI on pine requires too much memory (`ERROR: Java heap space` - out of memory error...) so I had to do it on nac
    * nac java version is out of date as well, and I don't know how to update (or how to use another java version) so I used version 7.3.1 of Webin-CLI
    * Webin-CLI version 7.3.1 only works until February 2025 -> this needs to be solved on nac since I will have large genomes also in the future to deal with

## Detailed step by step description
1. Clear out questions
1. Data transfer - Transfer fasta and gff files to where the embl file will be created
1. Create the embl file
1. Download latest Webin-CLI
1. Do a validation
1. Fix any errors
1. Submit flat file and chromosome list
1. Copy the embl file to Klemming (PDC, KTH) storage

### Questions
* Where to compute .embl file? Need to ensure sorting order, as for spruce, I'm guessing, and that was an issue
    * Check spruce documentation (private repo), on how to solve it
    * I'm guessing my computer won't be able to, as usual, too little memory for too much conda environment
    * Worst case, I need to ask colleague to do it
* LOCUS tag? I need to login to ENA and check the status of study, is 'functional annotation will be submitted' clicked and have they asked for a locus tag already
    * It is not done
    * Need to ask about what tag they want, PINSY? Answer PSYLV
* What more than the .embl file is definitely needed for a chromosome level assembly?
    * [ENA docs](https://ena-docs.readthedocs.io/en/latest/submit/assembly/genome.html#chromosome-assembly):
        *    1 manifest file
        *    1 FASTA file OR 1 flat file
        *    1 chromosome list file
        *    0-1 unlocalised list files
        *    0-1 AGP files

### Create EMBL file
* All necessary files (.fasta and .gff) were copied to NBIS annotation cluster (nac-login)
* Copied the exposed translation*.json files from previous submissions
* A script was created: [run_emblmygff3_pine_locus.sh](./scripts/run_emblmygff3_pine_locus.sh)
* The script was copied to nac and executed:
    ```
    sbatch run_emblmygff3_pine_locus.sh
    ```
    * Job 285007
* Need to check order and numbering, if they seems ok.

### Validation and submission
* Add the locus tag (via browser)
* Validate on nac:
    ```
    java -jar ../webin-cli-7.3.1.jar -ascp -context genome -userName Webin-XXX -password 'password' -manifest UPSC-0230.Manifest.txt -validate
    ```
    * 186 errors with `Features locations are duplicated - consider merging qualifiers.`
    * I've handed it back to bioinformatician for merging the offending entries
* New gff (Pinsy01_240308_at01_longest_no_TE_NODUPv01.gff3.gz) was added to the sbatch script, which then was executed (job 285054).
* New validation, also failed:
    ```
    ERROR: "5'UTR" Features locations are duplicated - consider merging qualifiers. [ line: 108571150 of ERP161594-PSYLV.embl.gz,  line: 108571128 of ERP161594-PSYLV.embl.gz]
    ```
    * Put it back in the hands of bioinformatician

* Received a new gff, rerun the the script and validate again
    * sbatch run_emblmygff3_pine_locus.sh -> job 285112
    * java -jar ../webin-cli-7.3.1.jar -ascp -context genome -userName Webin-XXX -password 'password' -manifest UPSC-0230.Manifest.txt -validate
    * INFO : Submission(s) validated successfully.
    * java -jar ../webin-cli-7.3.1.jar -ascp -context genome -userName Webin-XXX -password 'password' -manifest UPSC-0230.Manifest.txt -submit
    * Receipt:
        ```
        INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ25037051
        ```
    * Copy all files used for submission (and creating the embl file) to /cfs/klemming/projects/supr/uppstore2017145/V2/users/yvonnek/ENA/
