---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB96358 (umbrella), PRJEB91066 (experiment), PRJEB91067 (assembly)
---

# BGE - *Stenosis austini*

## Submission task description
Submission of raw reads for *Stenosis austini* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Stenosis-austini-metadata.xlsx)
* [BGE HiFi metadata](./data/icSteAust-HiFi.tsv)
* [BGE HiC metadata](./data/icSteAust-HiC.tsv)
* [BGE RNAseq metadata](./data/icSteAust-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiFi
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput *.bam` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.
#### XML
* I created [icSteAust-HiFi.tsv](./data/icSteAust-HiFi.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icSteAust-HiFi.tsv -p ERGA-BGE -o icSteAust-HiFi
    ```

* Study is private, so submission.xml with hold date is used.

* Submit both projects and experiment in one go, i.e:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@icSteAust-HiFi.study.xml" -F "EXPERIMENT=@icSteAust-HiFi.exp.xml" -F "RUN=@icSteAust-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-26T05:42:35.751+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14565370" alias="exp_icSteAust_HiFi_WGS_LV6000912695_pr_231_001" status="PRIVATE"/>
        <RUN accession="ERR15159718" alias="run_icSteAust_HiFi_WGS_LV6000912695_pr_231_001_bam_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB91066" alias="erga-bge-icSteAust-study-rawdata-2025-06-26" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP174062" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB91067" alias="erga-bge-icSteAust9_primary-2025-06-26" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP174063" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA33523128" alias="SUBMISSION-26-06-2025-05:42:35:298"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>    
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/), including a comment that Project is private

### Submit HiC
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [icSteAust-HiC.tsv](./data/icSteAust-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icSteAust-HiC.tsv -p ERGA-BGE -o icSteAust-HiC
    ```
* Update icSteAust-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB91066"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title, since the other data types have the platform named
* Study will be private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@icSteAust-HiC.exp.xml" -F "RUN=@icSteAust-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-08-24T11:58:18.537+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14868750" alias="exp_icSteAust_Hi-C_LV6000912703_HC049-1A1A" status="PRIVATE"/>
        <RUN accession="ERR15464855" alias="run_icSteAust_Hi-C_LV6000912703_HC049-1A1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA34531826" alias="SUBMISSION-24-08-2025-11:58:18:352"/>
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
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [icSteAust-RNAseq.tsv](./data/icSteAust-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icSteAust-RNAseq.tsv -p ERGA-BGE -o icSteAust-RNAseq
    ```
* Update -RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB91066"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@icSteAust-RNAseq.exp.xml" -F "RUN=@icSteAust-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
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
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Stenosis austini" -t icSteAust9 -p ERGA-BGE -c SCILIFELAB -a PRJEB91066 -x 3229215
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
    <RECEIPT receiptDate="2025-08-25T13:30:07.576+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB96358" alias="erga-bge-icSteAust-study-umbrella-2025-08-25" status="PRIVATE" holdUntilDate="2027-08-25+01:00"/>
        <SUBMISSION accession="ERA34670140" alias="SUBMISSION-25-08-2025-13:30:07:429"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    </RECEIPT>    
    ```
* Release the umbrella by adding the umbrella project accession number from the receipt above in file [submission-release-project.xml](./data/submission-release-project.xml)
* Submit using curl:
    ```
    curl -u Username:Password -F "SUBMISSION=@submission-release-project.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-08-25T13:31:01.273+01:00" submissionFile="submission-release-project.xml" success="true">
        <MESSAGES>
            <INFO>project accession "PRJEB96358" is set to public status.</INFO>
        </MESSAGES>
        <ACTIONS>RELEASE</ACTIONS>
    </RECEIPT>    
    ```

* **Note:** Add the assembly project `` when it has been submitted and made public, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.
