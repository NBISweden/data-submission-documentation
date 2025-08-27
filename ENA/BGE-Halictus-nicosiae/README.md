---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB96354 (umbrella), PRJEB90995 (experiment), PRJEB90996 (assembly)
---

# BGE - *Halictus nicosiae*

## Submission task description
Submission of raw reads for *Halictus nicosiae* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Halictus-nicosiae-metadata.xlsx)
* [BGE HiFi metadata](./data/iyHalNico-HiFi.tsv)
* [BGE HiC metadata](./data/iyHalNico-HiC.tsv)
* [BGE RNAseq metadata](./data/iyHalNico-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiFi
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput *.bam` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.
#### XML
* I created [iyHalNico-HiFi.tsv](./data/iyHalNico-HiFi.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iyHalNico-HiFi.tsv -p ERGA-BGE -o iyHalNico-HiFi
    ```

* Study is private, so submission.xml with hold date is used.

* Submit both projects and experiment in one go, i.e:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@iyHalNico-HiFi.study.xml" -F "EXPERIMENT=@iyHalNico-HiFi.exp.xml" -F "RUN=@iyHalNico-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-25T10:22:27.503+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14562399" alias="exp_iyHalNico_HiFi_WGS_LV6000911885_pr_230_001" status="PRIVATE"/>
        <RUN accession="ERR15157107" alias="run_iyHalNico_HiFi_WGS_LV6000911885_pr_230_001_bam_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB90995" alias="erga-bge-iyHalNico-study-rawdata-2025-06-25" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP173990" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB90996" alias="erga-bge-iyHalNico6_primary-2025-06-25" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP173991" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA33518804" alias="SUBMISSION-25-06-2025-10:22:27:224"/>
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
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [iyHalNico-HiC.tsv](./data/iyHalNico-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iyHalNico-HiC.tsv -p ERGA-BGE -o iyHalNico-HiC
    ```
* Update iyHalNico-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90995"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title, since the other data types have the platform named
* Study will be private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@iyHalNico-HiC.exp.xml" -F "RUN=@iyHalNico-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-08-24T11:50:39.469+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14868749" alias="exp_iyHalNico_Hi-C_LV6000911877_HC045-1A1A" status="PRIVATE"/>
        <RUN accession="ERR15464854" alias="run_iyHalNico_Hi-C_LV6000911877_HC045-1A1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA34531124" alias="SUBMISSION-24-08-2025-11:50:39:317"/>
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
* I created [iyHalNico-RNAseq.tsv](./data/iyHalNico-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iyHalNico-RNAseq.tsv -p ERGA-BGE -o iyHalNico-RNAseq
    ```
* Update -RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90995"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@iyHalNico-RNAseq.exp.xml" -F "RUN=@iyHalNico-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
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
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Halictus nicosiae" -t iyHalNico6 -p ERGA-BGE -c SCILIFELAB -a PRJEB90995 -x 3229267
    ```
    Explanation of arguments:
    * -s: scientific name e.g. "Lithobius stygius"
    * -t: tolId e.g. qcLitStyg1
    * -a: the accession number of the raw reads project e.g. PRJEB76283
    * -x: NCBI taxonomy id e.g. 2750798

* Copy `submission-umbrella.xml` from any of the previous BGE species
* Submit using curl:
    ```
    curl -u Username:Password -F "SUBMISSION=@submission-umbrella.xml" -F "PROJECT=@umbrella.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-08-25T13:06:21.833+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB96354" alias="erga-bge-iyHalNico-study-umbrella-2025-08-25" status="PRIVATE" holdUntilDate="2027-08-25+01:00"/>
        <SUBMISSION accession="ERA34667764" alias="SUBMISSION-25-08-2025-13:06:21:679"/>
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
    <RECEIPT receiptDate="2025-08-25T13:09:02.543+01:00" submissionFile="submission-release-project.xml" success="true">
        <MESSAGES>
            <INFO>project accession "PRJEB96354" is set to public status.</INFO>
        </MESSAGES>
        <ACTIONS>RELEASE</ACTIONS>
    </RECEIPT>    
    ```

* **Note:** Add the assembly project `` when it has been submitted and made public, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.
