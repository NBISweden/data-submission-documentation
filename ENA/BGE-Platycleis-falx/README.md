---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB91538 (umbrella), PRJEB90655 (experiment), PRJEB90656 (assembly)
---

# BGE - *Platycleis falx*

## Submission task description
Submission of raw reads for *Platycleis falx* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.

## Procedure overview and links to examples

* [ERGA-BGE_ReadData_Submission_Guide](https://github.com/ERGA-consortium/ERGA-submission/blob/main/BGE/ERGA-BGE_ReadData_Submission_Guide.md)
* [BGE mRupRup umbrella project](https://www.ncbi.nlm.nih.gov/bioproject/1084634)

## Lessons learned

## Detailed step by step description

### Submit HiFi

#### Preparations
* The sample ID from UGC was used to obtain the BioSample ID in ERGA tracker portal
* There are 4 bam files

#### XML
* I created [iqPlaFalx-HiFi.tsv](./data/iqPlaFalx-HiFi.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iqPlaFalx-HiFi.tsv -p ERGA-BGE -o iqPlaFalx-HiFi
    ```
    * Remove 3 experiments
* The study XML also needs to be submitted
* Submission.xml with hold date is used.
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission-hold.xml" -F "PROJECT=@iqPlaFalx-HiFi.study.xml" -F "EXPERIMENT=@iqPlaFalx-HiFi.exp.xml" -F "RUN=@iqPlaFalx-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-19T10:25:50.670+01:00" submissionFile="submission-hold.xml" success="true">
        <EXPERIMENT accession="ERX14538784" alias="exp_iqPlaFalx_HiFi_WGS_LV6000903690_pr_193" status="PRIVATE"/>
        <RUN accession="ERR15133552" alias="run_iqPlaFalx_HiFi_WGS_LV6000903690_pr_193_bam_1" status="PRIVATE"/>
        <RUN accession="ERR15133553" alias="run_iqPlaFalx_HiFi_WGS_LV6000903690_pr_193_bam_2" status="PRIVATE"/>
        <RUN accession="ERR15133554" alias="run_iqPlaFalx_HiFi_WGS_LV6000903690_pr_193_bam_3" status="PRIVATE"/>
        <RUN accession="ERR15133555" alias="run_iqPlaFalx_HiFi_WGS_LV6000903690_pr_193_bam_4" status="PRIVATE"/>
        <PROJECT accession="PRJEB90655" alias="erga-bge-iqPlaFalx-study-rawdata-2025-06-19" status="PRIVATE" holdUntilDate="2026-09-09+01:00">
            <EXT_ID accession="ERP173660" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB90656" alias="erga-bge-iqPlaFalx1_primary-2025-06-19" status="PRIVATE" holdUntilDate="2026-09-09+01:00">
            <EXT_ID accession="ERP173661" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA33381450" alias="SUBMISSION-19-06-2025-10:25:50:285"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit HiC

#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal

#### XML
* I created [iqPlaFalx-HiC.tsv](./data/iqPlaFalx-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iqPlaFalx-HiC.tsv -p ERGA-BGE -o iqPlaFalx-HiC
    ```
* Update iqPlaFalx-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90655"/>
    ```

* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission-hold.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission-hold.xml"  -F "EXPERIMENT=@iqPlaFalx-HiC.exp.xml" -F "RUN=@iqPlaFalx-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-30T12:00:17.817+01:00" submissionFile="submission-hold.xml" success="true">
        <EXPERIMENT accession="ERX14576326" alias="exp_iqPlaFalx_Hi-C_LV6000903690_HC036-1A2A-CL" status="PRIVATE"/>
        <EXPERIMENT accession="ERX14576327" alias="exp_iqPlaFalx_Hi-C_LV6000903690_HC036-1A2B-CL" status="PRIVATE"/>
        <RUN accession="ERR15170752" alias="run_iqPlaFalx_Hi-C_LV6000903690_HC036-1A2A-CL_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR15170753" alias="run_iqPlaFalx_Hi-C_LV6000903690_HC036-1A2B-CL_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA33539129" alias="SUBMISSION-30-06-2025-12:00:17:349"/>
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
* I created [iqPlaFalx-RNAseq.tsv](./data/iqPlaFalx-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iqPlaFalx-RNAseq.tsv -p ERGA-BGE -o iqPlaFalx-RNAseq
    ```
* Update iqPlaFalx-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90655"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission-hold.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission-hold.xml" -F "EXPERIMENT=@iqPlaFalx-RNAseq.exp.xml" -F "RUN=@iqPlaFalx-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Umbrella project
For each of the BGE species, an **umbrella** project has to be created and linked to the main BGE project, [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

1. Release the child project via browser
1. Collect scientific name and tolId from the metadata template sheet
1. Go to [ENA browser](https://www.ebi.ac.uk/ena/browser/home) and enter the scientific name as search term
    1. To the left side, there should be a **Taxon** subheading, that gives the identifier
1. Copy experiment accession number from metadata in top of this README
* There is a CNAG script, that should do the deed of creating the xml file:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Platycleis falx" -t iqPlaFalx -p ERGA-BGE -c SCILIFELAB -a PRJEB90655 -x 470658
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
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-07-02T09:08:45.566+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB91538" alias="erga-bge-iqPlaFalx-study-umbrella-2025-07-02" status="PRIVATE" holdUntilDate="2025-07-04+01:00"/>
        <SUBMISSION accession="ERA33548801" alias="SUBMISSION-02-07-2025-09:08:45:274"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>    
    ```
* **Note:** Add the assembly project `` when it has been submitted and made public, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.
