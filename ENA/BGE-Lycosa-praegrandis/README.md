---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB90409 (experiment), PRJEB90410 (assembly)
---

# BGE - *Lycosa praegrandis*

## Submission task description
Submission of raw reads for *Lycosa praegrandis* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Lycosa-praegrandis-metadata.xlsx)
* [BGE HiFi metadata](./data/qqLycPrae-HiFi.tsv)
* [BGE HiC metadata](./data/qqLycPrae-HiC.tsv)
* [BGE RNAseq metadata](./data/qqLycPrae-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiFi

#### Preparations
* There are 2 bam files for this library, need to make sure it works in the xml files
* The sample ID leed to the BioSample ID via the ERGA tracker portal

#### XML
* I created [qqLycPrae-HiFi.tsv](./data/qqLycPrae-HiFi.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qqLycPrae-HiFi.tsv -p ERGA-BGE -o qqLycPrae-HiFi
    ```
    * 2 experiments were created, but since it is from the same libary (i.e. identical rows), I removed the second.
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@qqLycPrae-HiFi.study.xml" -F "EXPERIMENT=@qqLycPrae-HiFi.exp.xml" -F "RUN=@qqLycPrae-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-12T13:37:57.987+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14519092" alias="exp_qqLycPrae_HiFi_WGS_LV6000912294_pr_190" status="PRIVATE"/>
        <RUN accession="ERR15114402" alias="run_qqLycPrae_HiFi_WGS_LV6000912294_pr_190_bam_1" status="PRIVATE"/>
        <RUN accession="ERR15114403" alias="run_qqLycPrae_HiFi_WGS_LV6000912294_pr_190_bam_2" status="PRIVATE"/>
        <PROJECT accession="PRJEB90409" alias="erga-bge-qqLycPrae-study-rawdata-2025-06-12" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP173413" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB90410" alias="erga-bge-qqLycPrae1_primary-2025-06-12" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP173414" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA33176679" alias="SUBMISSION-12-06-2025-13:37:57:553"/>
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
* I received sample ID from [NGI](https://docs.google.com/spreadsheets/d/10ZPAhkp1fCmpqR9GAZMRJ9wdXa8m-1G_/), which I checked in the [ERGA tracking portal](https://genomes.cnag.cat/erga-stream/samples/) which returned biosample [SAMEA116289568](https://www.ebi.ac.uk/biosamples/samples/SAMEA116289568).

* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [qqLycPrae-HiC.tsv](./data/qqLycPrae-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qqLycPrae-HiC.tsv -p ERGA-BGE -o qqLycPrae-HiC
    ```
* Update qqLycPrae-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90409"/>
    ```
* I added 'Illumina' to the title and library name, since the other data types have the platform named
* Remove additional/duplicate `<PAIRED/>` row (error in script)
* Study is be private, so submission.xml with hold date is used.
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@qqLycPrae-HiC.exp.xml" -F "RUN=@qqLycPrae-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
    * Error, 1 pair of run files are missing from upload area, `qqLycPrae_YB-4221-HC033-1A1A_S159_L008`, must have missed them. Did an upload and renamed using FileZilla.
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-12T15:38:29.087+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14519214" alias="exp_qqLycPrae_Hi-C_LV6000912286_HC033-1A1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX14519215" alias="exp_qqLycPrae_Hi-C_LV6000912286_HC033-1A2A" status="PRIVATE"/>
        <RUN accession="ERR15114525" alias="run_qqLycPrae_Hi-C_LV6000912286_HC033-1A1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR15114526" alias="run_qqLycPrae_Hi-C_LV6000912286_HC033-1A2A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA33180017" alias="SUBMISSION-12-06-2025-15:38:28:602"/>
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
* I created [qqLycPrae-RNAseq.tsv](./data/qqLycPrae-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qqLycPrae-RNAseq.tsv -p ERGA-BGE -o qqLycPrae-RNAseq
    ```
* Update qqLycPrae-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession=""/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@qqLycPrae-RNAseq.exp.xml" -F "RUN=@qqLycPrae-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Umbrella project - **TODO**
For each of the BGE species, an **umbrella** project has to be created and linked to the main BGE project, [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

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
