---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: Hi-C # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: 
---

# BGE - *Troglohyphantes liburnicus*

## Submission task description
Submission of raw reads HiC for *Troglohyphantes liburnicus* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). 


## Procedure overview and links to examples

* [Metadata template](./data/BGE-Troglohyphantes-liburnicus-metadata.xlsx)
* [BGE HiC metadata](./data/qqTroLibu-HiC.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->
* Trying to add experiment to an existing study.

## Detailed step by step description

### Submit HiC

#### Preparations
* I received sample ID from [NGI](https://docs.google.com/spreadsheets/d/15BObG5Z8CExbTa2bu4h8qvsr6xn8M0MT/), which I checked in the [ERGA tracking portal](https://genomes.cnag.cat/erga-stream/samples/) which returned biosample [SAMEA115118123](https://www.ebi.ac.uk/biosamples/samples/SAMEA115118123).

* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [qqTroLibu-HiC.tsv](./data/qqTroLibu-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qqTroLibu-HiC.tsv -p ERGA-BGE -o qqTroLibu-HiC
    ```
* Change `STUDY_REF` in qqStaHerc-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB96410"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title, since the other data types have the platform named
* Study will be private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@qqTroLibu-HiC.exp.xml" -F "RUN=@qqTroLibu-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-11-28T13:53:53.955Z" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX15368721" alias="exp_qqTroLibu_Hi-C_FF03939998_HC022-1A1A" status="PRIVATE"/>
        <RUN accession="ERR15973992" alias="run_qqTroLibu_Hi-C_FF03939998_HC022-1A1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA35282735" alias="SUBMISSION-28-11-2025-13:53:53:759"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    </RECEIPT>
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)
