---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB90653 (experiment), PRJEB90654 (assembly)
---

# BGE - *Sphingonotus rubescens*

## Submission task description
Submission of raw reads for *Sphingonotus rubescens* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Sphingonotus-rubescens-metadata.xlsx)
* [BGE HiFi metadata](./data/iqSphRube-HiFi.tsv)
* [BGE HiC metadata](./data/iqSphRube-HiC.tsv)
* [BGE RNAseq metadata](./data/iqSphRube-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiFi

#### Preparations
* There are 5 bam files
* Sample ID gave BioSample ID via ERGA tracker portal

#### XML
* I created [iqSphRube-HiFi.tsv](./data/iqSphRube-HiFi.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iqSphRube-HiFi.tsv -p ERGA-BGE -o iqSphRube-HiFi
    ```
    * 5 bam files so needed to remove 4 experiments
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@iqSphRube-HiFi.study.xml" -F "EXPERIMENT=@iqSphRube-HiFi.exp.xml" -F "RUN=@iqSphRube-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-19T10:14:46.291+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14538783" alias="exp_iqSphRube_HiFi_WGS_LV6000908962_pr_194" status="PRIVATE"/>
        <RUN accession="ERR15133547" alias="run_iqSphRube_HiFi_WGS_LV6000908962_pr_194_bam_1" status="PRIVATE"/>
        <RUN accession="ERR15133548" alias="run_iqSphRube_HiFi_WGS_LV6000908962_pr_194_bam_2" status="PRIVATE"/>
        <RUN accession="ERR15133549" alias="run_iqSphRube_HiFi_WGS_LV6000908962_pr_194_bam_3" status="PRIVATE"/>
        <RUN accession="ERR15133550" alias="run_iqSphRube_HiFi_WGS_LV6000908962_pr_194_bam_4" status="PRIVATE"/>
        <RUN accession="ERR15133551" alias="run_iqSphRube_HiFi_WGS_LV6000908962_pr_194_bam_5" status="PRIVATE"/>
        <PROJECT accession="PRJEB90653" alias="erga-bge-iqSphRube-study-rawdata-2025-06-19" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP173658" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB90654" alias="erga-bge-iqSphRube1_primary-2025-06-19" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP173659" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA33380838" alias="SUBMISSION-19-06-2025-10:14:45:669"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    ```
    * Note: I didnt get a `</RECEIPT>`but assume that it was my terminal window acting up

* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit HiC

#### Preparations
* I received sample ID from [NGI](https://docs.google.com/spreadsheets/d/10ZPAhkp1fCmpqR9GAZMRJ9wdXa8m-1G_/), which I checked in the [ERGA tracking portal](https://genomes.cnag.cat/erga-stream/samples/) which returned biosample [SAMEA116287545](https://www.ebi.ac.uk/biosamples/samples/SAMEA116287545).

* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [iqSphRube-HiC.tsv](./data/iqSphRube-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iqSphRube-HiC.tsv -p ERGA-BGE -o iqSphRube-HiC
    ```
* Update iqSphRube-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90653"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study will be private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@iqSphRube-HiC.exp.xml" -F "RUN=@iqSphRube-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-27T14:24:41.830+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14571488" alias="exp_iqSphRube_Hi-C_LV6000908964_HC037-1A1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX14571489" alias="exp_iqSphRube_Hi-C_LV6000908964_HC037-1A2A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX14571490" alias="exp_iqSphRube_Hi-C_LV6000908964_HC037-1A2B" status="PRIVATE"/>
        <RUN accession="ERR15165757" alias="run_iqSphRube_Hi-C_LV6000908964_HC037-1A1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR15165758" alias="run_iqSphRube_Hi-C_LV6000908964_HC037-1A2A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR15165759" alias="run_iqSphRube_Hi-C_LV6000908964_HC037-1A2B_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA33529482" alias="SUBMISSION-27-06-2025-14:24:41:537"/>
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
* I created [iqSphRube-RNAseq.tsv](./data/iqSphRube-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iqSphRube-RNAseq.tsv -p ERGA-BGE -o iqSphRube-RNAseq
    ```
* Update iqSphRube-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90653"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@iqSphRube-RNAseq.exp.xml" -F "RUN=@iqSphRube-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
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
