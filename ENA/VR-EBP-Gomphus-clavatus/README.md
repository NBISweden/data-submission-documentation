---
Redmine_issue: https://projects.nbis.se/issues/5872
Repository: ENA
Submission_type: HiFi, Isoseq, RNA, mito, assembly, umbrella # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB72358
---

# VR EBP - *Gomphus clavatus*

## Submission task description
Within the VR-EBP (Earth Biogenome Project) a fungi, *Gomphus clavatus*, is to be submitted. There are raw reads in form of HiFi, Isoseq and Illumina RNA sequences, an annotated genome assembly and a mito assembly. An umbrella project will be created to collect the two assemblies.

## Procedure overview and links to examples
* [Metadata template](https://docs.google.com/spreadsheets/d/1uYqRAjXW04U5RW3K_R2k89tnC6-qMtfi/edit#gid=268563316)
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

* **TODO** A study for the *mitochondrial* assembly was registered in the Webin Portal with a release date of `2026-06-03`, study alias `mito-GomCla1`. The accession number obtained was ``.

* **TODO**An *umbrella* study was submitted programmatically, with a release date of `2026-06-03`, using [submission.xml](./data/submission.xml) and [umbrella.xml](./data/umbrella.xml):

    ```
    curl -u Username:Password -F "SUBMISSION=@submission.xml" -F "PROJECT=@umbrella.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"    
    ```

    * Accession number received: ``
    * Receipt of the sumbission:

    ```

    ```

### Register sample **TODO**
* A ToLID was not provided, so I asked for one according to [SOP](../SOP/register_ToLID.md)
    * Taxonomy id: `80588`
    * Specimen ID: ``
    * Scientific name: `Gomphus clavatus`
    * Received id: `gfGomClav1` (not done, but expected id to be received)
* The sample was registered using the Webin Portal uploading [sample-metadata.tsv]()
* Received accession number: ``

### Register experiment **TODO**
* Manifests were created and copied to Uppmax, for each of the three types of sequences:
    * [PacBio HiFi manifest](./data/PRJEB72358-hifi-manifest.txt)
    * [PacBio Isoseq manifest](./data/PRJEB72358-isoseq-manifest.txt)
    * [Illumina RNA manifest](./data/PRJEB72358-Illumina-RNA-manifest.txt)
* They were each submitted using Webin-CLI:
    ```
    interactive -t 08:00:00 -A naiss2023-5-307
    module load ascp
    java -jar ../webin-cli-6.5.0.jar -ascp -context reads -userName $1 -password $2 -manifest $3 -outputDir Webin_output/ -submit
    ```
* HiFi: ``, ``
* Isoseq: ``, ``
* RNA: ``, ``, ``

### Genome assembly **TODO**
* The bioinformatician produced the embl flat file, which I copied to my laptop
* However, it turned out that it was created without exposing variables of EMBLmyGFF3, so I redid the embl file using `sbatch run_emblmygff3_GOMCLA.sh` on nac-login cluster (script [run_emblmygff3_GOMCLA.sh](./scripts/run_emblmygff3_GOMCLA.sh))
* Validation and submission of [PRJEB72358-genome-manifest.txt](./data/PRJEB72358-genome-manifest.txt) was done using webin-cli
    ```
    java -jar ../../../Downloads/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./PRJEB72358-genome-manifest.txt -validate
    ```
* Accession number: ``

### Mito assembly **TODO**
* Since mito assemblies consists of only one sequence in the sequence file, a [chromosome assembly](https://ena-docs.readthedocs.io/en/latest/submit/assembly/genome.html#chromosome-assembly) submission is the way to go:
    * The manifest needs one additional file, therein referenced as `CHROMOSOME_LIST: chromosome_list.txt.gz`
    * In this [chromosome_list.txt](), a single row is added `identifier	MIT	Linear-Chromosome	Mitochondrion` (note, update this when I have the identifier)
    * The [naming convention](https://ena-docs.readthedocs.io/en/latest/submit/fileprep/assembly.html#chromosome-list-file)
* Validation and submission of [PRJEBXXXX-mito-manifest.txt](./data/PRJEBXXXXX-mito-manifest.txt) was done using webin-cli
    ```
    java -jar ../../../Downloads/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./PRJEBXXXX-mito-manifest.txt -validate
    ```
* Accession number: ``

