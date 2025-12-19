---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: 
---

# BGE - *Spelaeobates novaki*

## Submission task description
Submission of raw reads for *Spelaeobates novaki* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Spelaeobates-novaki-metadata.xlsx)
* [BGE HiFi metadata](./data/icSpeNova-HiFi.tsv)
* [BGE HiC metadata](./data/icSpeNova-HiC.tsv)
* [BGE RNAseq metadata](./data/icSpeNova-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiC - **TODO**
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [icSpeNova-HiC.tsv](./data/icSpeNova-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icSpeNova-HiC.tsv -p ERGA-BGE -o icSpeNova-HiC
    ```
* Update icSpeNova-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB96375"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title, since the other data types have the platform named
* Study is public, so submission.xml without hold date is used.
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@icSpeNova-HiC.exp.xml" -F "RUN=@icSpeNova-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-12-17T13:55:11.680Z" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX15429515" alias="exp_icSpeNova_Hi-C_FS42595395_HC058-2A1B" status="PRIVATE"/>
        <RUN accession="ERR16038822" alias="run_icSpeNova_Hi-C_FS42595395_HC058-2A1B_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA35407900" alias="SUBMISSION-17-12-2025-13:55:11:482"/>
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
* I created [icSpeNova-RNAseq.tsv](./data/icSpeNova-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icSpeNova-RNAseq.tsv -p ERGA-BGE -o icSpeNova-RNAseq
    ```
* Update icSpeNova-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession=""/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@icSpeNova-RNAseq.exp.xml" -F "RUN=@icSpeNova-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)
