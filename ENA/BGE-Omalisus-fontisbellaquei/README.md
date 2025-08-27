---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB96498 (umbrella), PRJEB91106 (experiment), PRJEB91107 (assembly)
---

# BGE - *Omalisus fontisbellaquei*

## Submission task description
Submission of raw reads for *Omalisus fontisbellaquei* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Omalisus-fontisbellaquei-metadata.xlsx)
* [BGE HiFi metadata](./data/icOmaFont-HiFi.tsv)
* [BGE HiC metadata](./data/icOmaFont-HiC.tsv)
* [BGE RNAseq metadata](./data/icOmaFont-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiFi

#### Preparations
* The data files (trimmed reads) were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput *.bam` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.
* **Note:** ULI Ampli Fi protocol has been used 

#### XML
* I created [icOmaFont-HiFi.tsv](./data/icOmaFont-HiFi.tsv), and added `.bam` to file name
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icOmaFont-HiFi.tsv -p ERGA-BGE -o icOmaFont-HiFi
    ```
    * Edit run .xml and change to `fastq` (2 rows)
* The study XML also needs to be submitted
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@icOmaFont-HiFi.study.xml" -F "EXPERIMENT=@icOmaFont-HiFi.exp.xml" -F "RUN=@icOmaFont-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-26T11:50:40.809+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14566158" alias="exp_icOmaFont_HiFi_WGS_FS55571907_pr_239_001" status="PRIVATE"/>
        <RUN accession="ERR15160505" alias="run_icOmaFont_HiFi_WGS_FS55571907_pr_239_001_fastq_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB91106" alias="erga-bge-icOmaFont-study-rawdata-2025-06-26" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP174097" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB91107" alias="erga-bge-icOmaFont1_primary-2025-06-26" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP174098" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA33523712" alias="SUBMISSION-26-06-2025-11:50:40:600"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit HiC **TODO**

#### Preparations
* There is an issue with the sample for this dataset, the sample ID given from NGI (tube or well id) is not registered in COPO/BioSamples. 2025-03-20: I've sent an email to the sample coordinator for advice on what to do.

* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [icOmaFont-HiC.tsv](./data/icOmaFont-HiC.tsv) (**TODO**)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icOmaFont-HiC.tsv -p ERGA-BGE -o icOmaFont-HiC
    ```
* The study XML also needs to be submitted
* Update icOmaFont-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB91106"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@icOmaFont-HiC.exp.xml" -F "RUN=@icOmaFont-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)


### Submit RNAseq - **TODO**

#### Preparations

#### XML
* I created [icOmaFont-RNAseq.tsv](./data/icOmaFont-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icOmaFont-RNAseq.tsv -p ERGA-BGE -o icOmaFont-RNAseq
    ```
* Update icOmaFont-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB91106"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@icOmaFont-RNAseq.exp.xml" -F "RUN=@icOmaFont-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
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
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Omalisus fontisbellaquei" -t icOmaFont1 -p ERGA-BGE -c SCILIFELAB -a PRJEB91106 -x 350094
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
    <RECEIPT receiptDate="2025-08-27T11:21:37.841+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB96498" alias="erga-bge-icOmaFont-study-umbrella-2025-08-27" status="PRIVATE" holdUntilDate="2027-08-27+01:00"/>
        <SUBMISSION accession="ERA34838334" alias="SUBMISSION-27-08-2025-11:21:37:358"/>
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
    <RECEIPT receiptDate="2025-08-27T11:22:13.759+01:00" submissionFile="submission-release-project.xml" success="true">
        <MESSAGES>
            <INFO>project accession "PRJEB96498" is set to public status.</INFO>
        </MESSAGES>
        <ACTIONS>RELEASE</ACTIONS>
    </RECEIPT>    
    ```

* **Note:** Add the assembly project `` when it has been submitted and made public, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.
