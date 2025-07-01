---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB90636 (experiment), PRJEB90637 (assembly)
---

# BGE - *Niphargus gammariformis*

## Submission task description
Submission of raw reads for *Niphargus gammariformis* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Niphargus-gammariformis-metadata.xlsx)
* [BGE HiFi metadata](./data/qmNipGamm-HiFi.tsv)
* [BGE HiC metadata](./data/qmNipGamm-HiC.tsv)
* [BGE RNAseq metadata](./data/qmNipGamm-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiFi

#### Preparations
* There are 2 bam files
* Sample ID led to BioSample ID in ERGA tracker portal

#### XML
* I created [qmNipGamm-HiFi.tsv](./data/qmNipGamm-HiFi.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qmNipGamm-HiFi.tsv -p ERGA-BGE -o qmNipGamm-HiFi
    ```
    * Removed 1 extra experiment

* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@qmNipGamm-HiFi.study.xml" -F "EXPERIMENT=@qmNipGamm-HiFi.exp.xml" -F "RUN=@qmNipGamm-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-19T07:59:19.812+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14538624" alias="exp_qmNipGamm_HiFi_WGS_DE105_006_pr_148" status="PRIVATE"/>
        <RUN accession="ERR15133387" alias="run_qmNipGamm_HiFi_WGS_DE105_006_pr_148_bam_1" status="PRIVATE"/>
        <RUN accession="ERR15133388" alias="run_qmNipGamm_HiFi_WGS_DE105_006_pr_148_bam_2" status="PRIVATE"/>
        <PROJECT accession="PRJEB90636" alias="erga-bge-qmNipGamm-study-rawdata-2025-06-19" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP173641" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB90637" alias="erga-bge-qmNipGamm6_primary-2025-06-19" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP173642" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA33375318" alias="SUBMISSION-19-06-2025-07:59:19:532"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) 

* Note: More data is needed (status 'Top-up' in tracker)
* **TODO** Update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit HiC

#### Preparations
* I received sample IDs from [NGI](https://docs.google.com/spreadsheets/d/15BObG5Z8CExbTa2bu4h8qvsr6xn8M0MT/), which I checked in the [ERGA tracking portal](https://genomes.cnag.cat/erga-stream/samples/) which returned biosample [SAMEA115536145](https://www.ebi.ac.uk/biosamples/samples/SAMEA115536145).

* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

* 2 more data sets has been produced, based on biosample SAMEA115536142
* Note to self, need to make sure that the xmls are correct since separate samples and library names

#### XML
* I created [qmNipGamm-HiC.tsv](./data/qmNipGamm-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qmNipGamm-HiC.tsv -p ERGA-BGE -o qmNipGamm-HiC
    ```
* Update qmNipGamm-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90636"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study will be private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@qmNipGamm-HiC.exp.xml" -F "RUN=@qmNipGamm-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-30T06:53:55.720+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14574809" alias="exp_qmNipGamm_Hi-C_DE105_010_HC016-1A1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX14574810" alias="exp_qmNipGamm_Hi-C_DE105_013_HC016-2A1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX14574811" alias="exp_qmNipGamm_Hi-C_DE105_013_HC016-2A1B" status="PRIVATE"/>
        <RUN accession="ERR15169078" alias="run_qmNipGamm_Hi-C_DE105_010_HC016-1A1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR15169079" alias="run_qmNipGamm_Hi-C_DE105_013_HC016-2A1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR15169080" alias="run_qmNipGamm_Hi-C_DE105_013_HC016-2A1B_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA33538379" alias="SUBMISSION-30-06-2025-06:53:55:382"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)


### Submit RNAseq - **TODO**

#### Preparations

#### XML
* I created [qmNipGamm-RNAseq.tsv](./data/qmNipGamm-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qmNipGamm-RNAseq.tsv -p ERGA-BGE -o qmNipGamm-RNAseq
    ```
* Update qmNipGamm-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90636"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@qmNipGamm-RNAseq.exp.xml" -F "RUN=@qmNipGamm-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Umbrella project - **TODO**
For each of the BGE species, an **umbrella** project has to be created and linked to the main BGE project, [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

1. Release the child project via browser
1. Collect scientific name and tolId from the metadata template sheet
1. Go to [ENA browser](https://www.ebi.ac.uk/ena/browser/home) and enter the scientific name as search term
    1. To the left side, there should be a **Taxon** subheading, that gives the identifier
1. Copy experiment accession number from metadata in top of this README
* There is a CNAG script, that should do the deed of creating the xml file:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "" -t  -p ERGA-BGE -c SCILIFELAB -a  -x 
    ```
    Explanation of arguments:
    * -s: scientific name e.g. "Lithobius stygius"
    * -t: tolId e.g. qcLitStyg1
    * -a: the accession number of the raw reads project e.g. PRJEB76283
    * -x: NCBI taxonomy id e.g. 2750798

* Copy `submission-umbrella.xml` from any of the previous BGE species, check that the hold date is as wanted.
* Submit using curl:
    ```
    curl -u Username:Password -F "SUBMISSION=@submission-umbrella.xml" -F "PROJECT=@umbrella.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    
    ```
* **Note:** Add the assembly project `` when it has been submitted and made public, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.
