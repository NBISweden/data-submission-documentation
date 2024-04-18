---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB75035
---

# BGE - *Pinna rudis*

## Submission task description
Submission of raw reads for *Pinna rudis* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Pinna-rudis-metadata.xlsx)
* [ERGA-BGE_ReadData_Submission_Guide](https://github.com/ERGA-consortium/ERGA-submission/blob/main/BGE/ERGA-BGE_ReadData_Submission_Guide.md)
* [BGE mRupRup umbrella project](https://www.ncbi.nlm.nih.gov/bioproject/1084634)

## Lessons learned
* There was some struggle to identify which COPO registered biosample number to use, there had been a mistake when uploading to NGI so the sample was labelled with a specimen id for another species.

## Detailed step by step description

### Collect metadata
* After some struggle biosample [SAMEA112748815](https://www.ebi.ac.uk/biosamples/samples/SAMEA112748815) was identified as origin

### Register sequencing study
* BGE projects should follow a certain standard when it comes to naming, which was followed in this study.
* Release date was set 2 years in the future, 2026-03-07 (same as for all our BGE projects). This should be updated when all datasets have been submitted, so that the annotation group can access them.
* The study was registered via the browser, using NBIS DM broker account, received accession number: `PRJEB75035`

### Submit HiFi
