---
Redmine_issue: https://projects.nbis.se/issues/8794
Repository: ENA
Submission_type: WGS # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
  NGI
Top_level_acccession: PRJEB115107
---

# 8794 - Submission of common chiffchaff (Phylloscopus collybita) WGS data

## Submission task description
Research group contacted NBIS Data Management with request for help with publishing sequence data in the ENA, due to the reason it not being a standard deposition, as with the former issue from the same research group [#8061](ENA/8061-songbird-Phylloscopus/README.md).

Medium dataset (~120 files, ~400Mb data). Normally an experiment only references a single or paired files, but not in this case. As a consequence, standard submission templates cannot be used. The solution is to manually modify xml files in a programmatical submission to accomodate multiple runs per experiment.

## Procedure overview and links to examples

* Consult with research group and decide on scope and timeline. Initial request was postponed by DS due to the then ongoing issue (#8061) not advancing
* Suitable checklist was a modified version of ToL (ERC000053)
* Research group provided [metadata in template](./data/Chiffchaff_metadata_template_Tree-of-life_ERC000053.xlsx). Unfilled columns were manually removed.
* DS registered Study in the ENA portal using information from the metadata template (PRJEB115107)
* DS registered samples based on the information in the template by converting the information in the template to [.tsv format](./data/Chiffchaff_samples.tsv) and submitting it in the portal
* Researcher group provided paths to fastq files relevant for submission in the template
*  File transfer from Dardel to ENA was made by the Data Steward using lftp (see Lessons learned below)
*  md5sums were calculated for the files on Dardel and copied to the template
*  A [submission.xml](./data/submission.xml) file was made with release date set to 2026-07-01
*  A [Chiffchaff_experiments.xml](./data/Chiffchaff_experiments.xml) was assembled manually, based on the procedure in support issue #8061 to reflect a unique experiment per sample
*  A [Chiffchaff_runs_files.xml](./data/Chiffchaff_runs_files.xml) was assembled to reflect multiple runs per unique experiment
*  All xml files were validated online at [https://www.xmlvalidation.com](https://www.xmlvalidation.com) before being submitted
*  Ingestion of the uploaded fastq files at the ENA was done in one go using the curl command:
  
```
curl -u [Username]:[password] -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@Chiffchaff_experiments.xml.xml" -F "RUN=@Chiffchaff_runs_files.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
```
* Successful submission was confirmed by the [xml receipt](./data/receipt.xml)

## Lessons learned
When transferring fastq files from Dardel to ENA the Aspera protocol could not be used due to current restrictions imposed on the ENA side. Any attempt resulted in connection errors.

Since the ENA does not support file transfer via `scp` or `rsync`, the solution was to make a local install
of `lftp` on Dardel via Conda.

In the home directory, on Dardel I ran:

`ml PDC/24.11`

`ml miniconda3`

`conda create --name lftp-env -c conda-forge lftp`

`source activate lftp-env`

This installs and activates the lftp environment. Then files can be transfered by `cd` into directory with files on Dardel, and from there run:

`lftp webin2.ebi.ac.uk -u Webin-[XXXXX]`

`(enter password at prompt)`

`mput *.gz`

When all files in the current directory are transfered, exit lftp with `bye`, and `cd` into next directory. Repeat process until all relevant files are transfered.

