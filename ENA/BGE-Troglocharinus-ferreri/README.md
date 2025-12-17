---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: 
---

# BGE - *Troglocharinus ferreri*

## Submission task description
Submission of raw reads for *Troglocharinus ferreri* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). Hi-C and RNAseq datasets will be produced and submitted. HiFi and assembly is/will be submitted by another node.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Troglocharinus-ferreri-metadata.xlsx)
* [BGE HiC metadata](./data/icTroFerr-HiC.tsv)
* [BGE RNAseq metadata](./data/icTroFerr-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiC
#### Preparations
* Sample ID gave 2 BioSample ID:s and 2 ToLID:s via ERGA tracker portal. Hence, a virtual sample is needed, but lucklily someone else has requested a new ToLID 
    * Create [icTroFerr-HiC-virtual-sample.tsv](./data/icTroFerr-HiC-virtual-sample.tsv) and submit via browser to ENA.
    * Sample accession received: `ERS28354596`
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [icTroFerr-HiC.tsv](./data/icTroFerr-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icTroFerr-HiC.tsv -p ERGA-BGE -o icTroFerr-HiC
    ```
* Update icTroFerr-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB96376"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title, since the other data types have the platform named
* Study is public, so submission.xml without hold date is used.
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@icTroFerr-HiC.exp.xml" -F "RUN=@icTroFerr-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-12-17T14:19:32.560Z" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX15429796" alias="exp_icTroFerr_Hi-C_FS38819720_FS38819721_HC057-1A1A" status="PRIVATE"/>
        <RUN accession="ERR16039103" alias="run_icTroFerr_Hi-C_FS38819720_FS38819721_HC057-1A1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA35407927" alias="SUBMISSION-17-12-2025-14:19:32:163"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    </RECEIPT>
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit RNAseq - **TODO**
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [icTroFerr-RNAseq.tsv](./data/icTroFerr-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icTroFerr-RNAseq.tsv -p ERGA-BGE -o icTroFerr-RNAseq
    ```
* Update icTroFerr-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB96376"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@icTroFerr-RNAseq.exp.xml" -F "RUN=@icTroFerr-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)
