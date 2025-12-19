---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: 
---

# BGE - *Dysdera unguimmanis*

## Submission task description
Submission of raw reads for *Dysdera unguimmanis* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Dysdera-unguimmanis-metadata.xlsx)
* [BGE HiFi metadata](./data/qqDysUngu-HiFi.tsv)
* [BGE HiC metadata](./data/qqDysUngu-HiC.tsv)
* [BGE RNAseq metadata](./data/qqDysUngu-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiC
#### Preparations
* Sample ID did **not** give BioSample ID via ERGA tracker portal, only a specimen ID was given as label. Instead I looked it up in BioSample and found an original (i.e. not derived from any other BioSample) sample that I used.
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [qqDysUngu-HiC.tsv](./data/qqDysUngu-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qqDysUngu-HiC.tsv -p ERGA-BGE -o qqDysUngu-HiC
    ```
* Update qqDysUngu-HiC.exp.xml to reference accession number of previously registered study (by another node):
    ```
    <STUDY_REF accession="PRJEB96373"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title, since the other data types have the platform named
* Study will be private, so submission.xml with hold date is used.
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@qqDysUngu-HiC.exp.xml" -F "RUN=@qqDysUngu-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-12-17T13:45:20.062Z" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX15429507" alias="exp_qqDysUngu_Hi-C_ERGA_DU_3619_00003_HC056-1A1A" status="PRIVATE"/>
        <RUN accession="ERR16038814" alias="run_qqDysUngu_Hi-C_ERGA_DU_3619_00003_HC056-1A1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA35407829" alias="SUBMISSION-17-12-2025-13:45:19:816"/>
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
* I created [qqDysUngu-RNAseq.tsv](./data/qqDysUngu-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qqDysUngu-RNAseq.tsv -p ERGA-BGE -o qqDysUngu-RNAseq
    ```
* Update qqDysUngu-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession=""/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@qqDysUngu-RNAseq.exp.xml" -F "RUN=@qqDysUngu-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)
