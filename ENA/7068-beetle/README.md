---
Redmine_issue: https://projects.nbis.se/issues/7068
Repository: ENA
Submission_type: HiC, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: https://www.ebi.ac.uk/ena/browser/view/PRJEB69220
---

# 7068 - Beetle assembly

## Submission task description
"We need help with depositing / submitting an annotated genome assembly of our model species (a beetle; Acanthoscelides obtectus) to ENA (i.e., preparation of files for submission and submission). The assembly is a PacBio assembly that have been superscaffolded (chromosome level) using Hi-C data. The annotation was originally made by BILS. We have a fasta file and a gff file."

This was the initial request, though it turns out that it is a gtf file, not gff.

## Procedure overview and links to examples
### Links

* [NBIS Create EMBL file](https://github.com/NBISweden/annotation-cluster/wiki/ENA-submission#create-embl-file)
* Issues with [CDS phase loss](https://github.com/agshumate/Liftoff/issues/67) when using LiftOff
* <https://github.com/NBISweden/AGAT/blob/master/README.md#using-docker>
* <https://agat.readthedocs.io/en/latest/tools/agat_convert_sp_gxf2gxf.html>

### Steps
* Create metadata template file
* Identify where the files are  
  * PacBio
  * HiC
  * Assembly files, .fasta and .gtf
* Fill the metadata sheet  
  * Locus tag?
* Create the EMBL flat file  
  * Transform from .gtf to .gff
* Get ENA account credentials
* Submit study and sample
* Transfer reads and submit experiment
* Create manifest file for assembly, and submit

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->
* There were a lot of issues with the assembly file, in the end a bioinformatician had to be consulted, since it wasn't produced in a standard way.
* There is a conversion script, for converting from gtf to gff format, see description at <https://agat.readthedocs.io/en/latest/tools/agat_convert_sp_gxf2gxf.html> (I never managed to get it to work though)
* Definition of the values 'isolate' and 'clone' for the 'ASSEMBLY_TYPE' metadata field: * "If the sample came from something collected in the field or an animal in the lab, then it's an isolate. If it's a cell culture that is clonally reproduced asexually, then it's a clone."*
* For annotation assemblies, there are ways of setting arguments (in json file) for the EMBLmyGFF3 script
* Always check that the annotation is on CDS level, not only on mRNA level

## Detailed step by step description

### Metadata template

* I asked the PI if it was ok to collect metadata in a Google sheet and share with them, and since this was approved I made a copy of the default (ERC000011) metadata template and asked the research group to fill all they could.

### Study

* The release date was as soon as possible, this ENA study will not be connected to a paper.
* I asked about preferred locus tag but didn't get an answer, so I decided it would be AOBTE (for the previous assembly it was ACAOB)
* Study accession number: PRJEB69220

### Sample

* I copy-pasted the sample metadata from the metadata template and saved as tsv ([PRJEB69220-sample.tsv](./data/PRJEB69220-sample.tsv)), using Visual Studio.
* The uploaded tsv accession number: ERS16799299, AobtHiC (alias)

### Experiment

* During initial meeting, they said that both PacBio and HiC sequences had been used in order to do the assembly, and therefore there would be 2 samples. Later, it turns out that the PacBio experiment had already been published. Hence, only the HiC sequences was submitted.

* Files were transfered as follows:

```
ssh -X user@rackham.uppmax.uu.se

interactive -A naiss2023-22-289 module load ascp

ascp -QT -l300M -L- /uppmax-path/a.obtectus/raw_data/genome/HiC/P17301/P17301_102/02-FASTQ/201218_A00621_0323_AHGVMKDSXY/P17301_102_S3_L004_R1_001.fastq.gz Webin-XXXXX@webin.ebi.ac.uk:/P17301_102_S3_L004_R1_001.fastq.gz

ascp -QT -l300M -L- /uppmax-path/a.obtectus/raw_data/genome/HiC/P17301/P17301_102/02-FASTQ/201218_A00621_0323_AHGVMKDSXY/P17301_102_S3_L004_R2_001.fastq.gz Webin-XXXXX@webin.ebi.ac.uk:/P17301_102_S3_L004_R2_001.fastq.gz
```

* The experiment metadata was copy-pasted from the metadata template and saved as tsv ([PRJEB69220-experiment.tsv](./data/PRJEB69220-experiment.tsv)) using Visual Studio
* The uploaded tsv accession numbers: ERX11670345 (experiment) and ERR12260057 (run)

### Assembly

* There was an iterative process of creating embl-file, doing test submission of a project, validating the embl-file, collecting errors, etc, documented separately in [assembly-fix.md](./assembly-fix.md)

* The main take-aways are to check if annotation is on CDS, and that EMBLmyGFF3 settings might need to be adjusted:
    * If ENA validation complains about
    ```
    ERROR: "exon" Features locations are duplicated
    ERROR: Abutting features cannot be adjacent between neighbouring exons
    ```
    * Solution is to update the file translation_gff_feature_to_embl_feature.json:
    ```
    conda activate py38
    EMBLmyGFF3 --expose_translations

    "exon": {
        "remove": true
    }
    ```
* Finally, the assembly was ready for submission, using [PRJEB69220-assembly-manifest.txt](./data/PRJEB69220-assembly-manifest.txt):
  ```
    EMBLmyGFF3 A.obtectus_v2.0_gt_tidy_v1.3.gff.gz A.obtectus_v2.0.fasta --topology linear --molecule_type 'genomic DNA' --transl_table 1 --species "Acanthoscelides obtectus" --locus_tag AOBTE --project_id PRJEB69220 -o AOBTE_PRJEB69220.embl
    gzip AOBTE_PRJEB69220.embl
    java -jar ../../Downloads/webin-cli-6.5.0.jar -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./PRJEB69220-assembly-manifest.txt -validate
    java -jar ../../Downloads/webin-cli-6.5.0.jar -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./PRJEB69220-assembly-manifest.txt -submit
  ```
* Assembly accession number ERZ21868640
