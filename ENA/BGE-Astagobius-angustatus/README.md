---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: 
---

# BGE - *Astagobius angustatus*

## Submission task description
Submission of raw reads for *Astagobius angustatus* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Astagobius-angustatus-metadata.xlsx)
* [BGE HiFi metadata](./data/icAstAngu-hifi.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Collecting metadata
* I then looked at the delivery README for the HiFi dataset (on Uppmax) and extracted the Name (`ERGA_TD_5269_06`). I then went to [BioSamples](https://www.ebi.ac.uk/biosamples/samples?text=Astagobius+angustatus&page=2) and extracted the 2 samples that had this name as `specimen_id`. Since `SAMEA113399603` was the same as `SAMEA113399597`, I decided to use the latter. 
* I checked the [ERGA tracking portal](https://genomes.cnag.cat/erga-stream/samples/), using both the biosample accession number as well as the species name, but there was no hit. I guess in this case we will not have a tube or well id, so will use UGC user id (`pr_056_001`) instead.

### Creating xml
* I copied [submission.xml](./data/submission.xml) from BGE-Crayfish, using the same embargo date
* Running the script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icAstAngu-hifi.tsv -p ERGA-BGE -o icAstAngu-HiFi
    ```

### Data transfer
* Create folder `bge-astagobius` at ENA upload area using Filezilla
* Using aspera from Uppmax to ENA upload area:
    ```
    interactive -t 03:00:00 -A naiss2023-5-307
    module load ascp
    export ASPERA_SCP_PASS='password'
    ascp -k 3 -d -q --mode=send -QT -l300M --host=webin.ebi.ac.uk --user=Webin-XXXX /proj/snic2021-6-194/INBOX/BGE_Astagobius_angustatus/pr_056/rawdata/pr_056_001/m84045_240223_153821_s3.hifi_reads.bc2053.bam /bge-astagobius/ &
    ```
* Keep track of progress using FileZilla
