---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB90649 (experiment), PRJEB90650 (assembly)
---

# BGE - *Propomacrus cypriacus*

## Submission task description
Submission of raw reads for *Propomacrus cypriacus* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Propomacrus-cypriacus-metadata.xlsx)
* [BGE HiFi metadata](./data/icProCypr-HiFi.tsv)
* [BGE HiC metadata](./data/icProCypr-HiC.tsv)
* [BGE RNAseq metadata](./data/icProCypr-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiFi

#### Preparations
* Sample ID gave me the BioSample ID via ERGA tracker portal

#### XML
* I created [icProCypr-HiFi.tsv](./data/icProCypr-HiFi.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icProCypr-HiFi.tsv -p ERGA-BGE -o icProCypr-HiFi
    ```

* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@icProCypr-HiFi.study.xml" -F "EXPERIMENT=@icProCypr-HiFi.exp.xml" -F "RUN=@icProCypr-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-19T08:55:28.454+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14538746" alias="exp_icProCypr_HiFi_WGS_LV6000912300_pr_191" status="PRIVATE"/>
        <RUN accession="ERR15133510" alias="run_icProCypr_HiFi_WGS_LV6000912300_pr_191_bam_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB90649" alias="erga-bge-icProCypr-study-rawdata-2025-06-19" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP173654" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB90650" alias="erga-bge-icProCypr1_primary-2025-06-19" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP173655" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA33377578" alias="SUBMISSION-19-06-2025-08:55:28:082"/>
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
* I received sample ID from [NGI](https://docs.google.com/spreadsheets/d/10ZPAhkp1fCmpqR9GAZMRJ9wdXa8m-1G_/), which I checked in the [ERGA tracking portal](https://genomes.cnag.cat/erga-stream/samples/) which returned biosample [SAMEA116289685](https://www.ebi.ac.uk/biosamples/samples/SAMEA116289685).

* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [icProCypr-HiC.tsv](./data/icProCypr-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icProCypr-HiC.tsv -p ERGA-BGE -o icProCypr-HiC
    ```
* Update icProCypr-HiFi.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90649"/>
    ```
* The study XML will not be submitted

* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study will be private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@icProCypr-HiC.exp.xml" -F "RUN=@icProCypr-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-07-01T06:28:29.733+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14577979" alias="exp_icProCypr_Hi-C_LV6000912289_HC028-1A1A" status="PRIVATE"/>
        <RUN accession="ERR15172555" alias="run_icProCypr_Hi-C_LV6000912289_HC028-1A1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA33544639" alias="SUBMISSION-01-07-2025-06:28:29:468"/>
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
* I created [icProCypr-RNAseq.tsv](./data/icProCypr-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icProCypr-RNAseq.tsv -p ERGA-BGE -o icProCypr-RNAseq
    ```
* Update icProCypr-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90649"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@icProCypr-RNAseq.exp.xml" -F "RUN=@icProCypr-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
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
