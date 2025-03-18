---
Redmine_issue: https://projects.nbis.se/issues/6717
Repository: ENA
Submission_type: VR-EBP, HiFi, Iso-Seq, RNA-seq, Nanopore, assembly, annotation # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB72355  PRJEB72356  PRJEB72357
---

# VR-EBP *Anthophora* spp. x3 

## Submission task description
Submit genomic and assembly data for the three *Anthophora* bee species (*plagiata*, *quadrimaculata*, and *retusa*) as part of the VR-EBP initiative. The sample metadata was collected from the respective PI's.

## Procedure overview and links to examples

Studies for each species were created separately by another Data Steward. 

The submissions did, with two procedural exceptions, follow the standardized pipelines for raw PacBio HiFi, PacBio Iso-Seq, and Illumina RNA-seq data. For *Anthophora plagiata* the PacBio HiFi data was replaced by Oxford Nanopore data, which only required new metadata options in the template, but otherwise behaved just like the other data (except for fastq header issue described below).

1. Paths to relevant raw data were provided by bioinformatician
1. Sample metadata was provided by PI by sending links to spreadsheet templates to be filled in
1. Samples were registered in each study based on the provided sample metadata (sample.tsv)
1. Technical metadata was provided by NGI by sending links to spreadsheet templates to be filled in.
1. Assembly metadata was provided by bioinformaticians by sending links to spreadsheet templates to be filled in. 
1. Manifest files for raw data were created for each data type for each species.
1. Webin-CLI client and manifest files were uploaded to respective data folders at Uppmax.
1. Data was validated before submitted from Uppmax to ENA by webin-CLI client.

After verificaton of submitted raw data, an assembly manifest file was created for each species referencing the respective submitted raw data. Manifests were, again, uploaded along webin-CLI client to Uppmax, and assemblies were validated and then submitted to ENA.

All manifests and sample metadata files are available in the subfolders for each species.

The following assembly accession numbers were received:

| ASSEMBLY_NAME | ASSEMBLY_ACC | STUDY_ID | SAMPLE_ID | CONTIG_ACC | SCAFFOLD_ACC | CHROMOSOME_ACC |
| ------------- | ------------ | -------- | --------- | ---------- | ------------ | -------------- |
| iyAntPlag1 | GCA_963995485 | PRJEB72356 | ERS18361400 | CAXEFL010000001-CAXEFL010000295 |  | 
| iyAntQuad1 | GCA_963995475 | PRJEB72355 | ERS18418632 | CAXEFK010000001-CAXEFK010000039 |  | 
| iyAntRet1  | GCA_963995495 | PRJEB72357 | ERS18426632 | CAXEFM010000001-CAXEFM010001422 |  | 

All three projects were released to public 2025-02-05, upon request from PI.

## Lessons learned
For *Anthophora plagiata*, the Nanopore raw data (single fastq-file, 39 Gb) initially failed ENA validation with an error due to the fastq header being longer than 256 letters (351):

```
@9692b9dd-f1d4-45d3-bfb0-be9e74d349e1
runid=5895ba0bb236428daa3045b763444a1cb30acd79 read=15 ch=1336 start_time=2022-09-27T15:31:45.046680+02:00 flow_cell_id=PAM03458 protocol_group_id=op_058_001_220927_NIW sample_id=op_058_001 parent_read_id=9692b9dd-f1d4-45d3-bfb0-be9e74d349e1 basecall_model_version_id=2021-05-05_dna_r9.4.1_promethion_768_922a514b
```
It was detemined that retaining the *runid* would be sufficient for future findability purposes, allowing the reminder of the header to be removed. 
The solution was to:

1. Unzip the fastq on UPPMAX to create a renamed woking copy of the file.
1. Export the initial 100 rows of that file to another separate file.
1. Use `grep` and `sed` to identify a sufficiently long string to retain relevant information in the header while decresing the header length to <256 letters:</br>
```
sed 's/ read.*//g' [original].fastq > [truncated].fastq
```
1. Run `sed` on the smaller test file and verify it performs as expected.
1. Run the `sed` string again on the working copy of the original file.
1. Gzip the modified file.
1. Submit the modified, zipped, file. 

The solution should work as described on any fastq file containing a `read=[number]` after a `runid`. Otherwise the above command line can be modified to fit the particulars of the header in question. 

-------

Also, all three species of *Anthophora* EMBL flatfiles returned the same webin-CLI validation errors of containing multiple duplicate introns. After contact, the bioinformatician provided a fix, and new files could be submitted without issues.

_______

Half way through the raw data submissions the Aspera ftp client stopped working with the error message:

```
Session Stop (Error: Failure processing peer license: Deprecated peer license)

ERROR: Failed to upload files using Aspera. Failed to upload files to FTP server because of a system error.
```

The error seems connected to the Aspera Uppmax client version license running out, and required contact with Uppmax staff through the SUPR support form to update the client. It was also recommended that we always load Aspera using the generic command line:

`module load ascp`

