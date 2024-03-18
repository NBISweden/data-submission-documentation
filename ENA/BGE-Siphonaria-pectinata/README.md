---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB74038
---

# BGE - *Siphonaria pectinata*

## Submission task description
Submission of raw reads for *Siphonaria pectinata* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Siphonaria-pectinata-metadata.xlsx)

## Lessons learned
* When it comes to preregistered samples, done via COPO, there is a struggle to identify which sample has been used for sequencing. Ideally the data producer would use the BioSample accession number instead of an identifier that is found in several of the registered samples.

## Detailed step by step description

### Collect metadata
* There were 2 BioSamples that matched the label provided by NGI (ERGA_KE_1616_002) in their README file, [SAMEA113595500](https://www.ebi.ac.uk/biosamples/samples/SAMEA113595500) and [SAMEA113595495](https://www.ebi.ac.uk/biosamples/samples/SAMEA113595495). NGI confirmed that it was the latter that should be used (the former is derived from the latter). 

### Register study
* Title and abstract for the study was decided together with a colleague.
* Release date was set 2 years in the future, 2026-03-07, but it is likely that the study will be released as soon as the rest of the sequencing datasets have been produced and submitted. At the latest, we expect the datasets to be public when the assembly has been submitted as well.
* The study was registered via the browser, using NBIS DM broker account, received accession number: `PRJEB74038`

### Submit HiFi
* NGI filled and checked the experiment metadata
* Both fastq and bam files were available. Together with a colleague, it was decided to submit the bam file.
* A [HiFi manifest](./data/reads-PacBio-HiFi-manifest.txt) was created by downloading a manifest template from [NBIS DM>Data publication>ENA>ERGA_VR-EBP](https://drive.google.com/drive/folders/1VOXZot7ji1Ea5KZFvmb2Pbm9YGtHwy99) google drive
* The submission was validated and submitted at Uppmax using Webin-CLI:
```
  interactive -t 03:00:00 -A naiss2023-5-307
  module load ascp
  java -jar ../webin-cli-7.0.1.jar -ascp -context reads -userName $1 -password $2 -manifest reads-PacBio-HiFi-manifest.txt -outputDir Webin_output/ -submit
```
* Note on validation: I first tried using the study alias (SipPec1) in the manifest file but received an error that it was unknown. Hence, always use the study accession number.
* Received accession number: `ERX12137308`, `ERR12764099`

### Submit Hi-C

### Submit RNAseq

### Submit assembly

