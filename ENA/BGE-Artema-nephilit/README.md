---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB90607 (experiment), PRJEB90608 (assembly)
---

# BGE - *Artema nephilit*

## Submission task description
Submission of raw reads for *Artema nephilit* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.

## Procedure overview and links to examples

* [ERGA-BGE_ReadData_Submission_Guide](https://github.com/ERGA-consortium/ERGA-submission/blob/main/BGE/ERGA-BGE_ReadData_Submission_Guide.md)
* [BGE mRupRup umbrella project](https://www.ncbi.nlm.nih.gov/bioproject/1084634)

## Lessons learned

## Detailed step by step description

### Submit HiFi

#### Preparations
* The sample ID from UGC was used to obtain the BioSample ID in ERGA tracker portal

#### XML
* I created [qqArtNeph-HiFi.tsv](./data/qqArtNeph-HiFi.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qqArtNeph-HiFi.tsv -p ERGA-BGE -o qqArtNeph-HiFi
    ```
* The study XML also needs to be submitted
* Submission.xml with hold date is used.
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission-hold.xml" -F "PROJECT=@qqArtNeph-HiFi.study.xml" -F "EXPERIMENT=@qqArtNeph-HiFi.exp.xml" -F "RUN=@qqArtNeph-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-18T15:44:29.572+01:00" submissionFile="submission-hold.xml" success="true">
        <EXPERIMENT accession="ERX14538034" alias="exp_qqArtNeph_HiFi_WGS_LV6000659149_pr_189" status="PRIVATE"/>
        <RUN accession="ERR15132795" alias="run_qqArtNeph_HiFi_WGS_LV6000659149_pr_189_bam_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB90607" alias="erga-bge-qqArtNeph-study-rawdata-2025-06-18" status="PRIVATE" holdUntilDate="2026-09-09+01:00">
            <EXT_ID accession="ERP173609" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB90608" alias="erga-bge-qqArtNeph1_primary-2025-06-18" status="PRIVATE" holdUntilDate="2026-09-09+01:00">
            <EXT_ID accession="ERP173610" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA33332717" alias="SUBMISSION-18-06-2025-15:44:29:370"/>
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
* I received sample ID from NGI, which I checked in the [ERGA tracking portal](https://genomes.cnag.cat/erga-stream/samples/) which returned biosample.

* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [qqArtNeph-HiC.tsv](./data/qqArtNeph-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qqArtNeph-HiC.tsv -p ERGA-BGE -o qqArtNeph-HiC
    ```
* Update qqArtNeph-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90607"/>
    ```

* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission-hold.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission-hold.xml"  -F "EXPERIMENT=@qqArtNeph-HiC.exp.xml" -F "RUN=@qqArtNeph-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-30T09:14:43.255+01:00" submissionFile="submission-hold.xml" success="true">
        <EXPERIMENT accession="ERX14574861" alias="exp_qqArtNeph_Hi-C_LV6000659157_HC031-1A1A-CL" status="PRIVATE"/>
        <RUN accession="ERR15169130" alias="run_qqArtNeph_Hi-C_LV6000659157_HC031-1A1A-CL_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA33538684" alias="SUBMISSION-30-06-2025-09:14:42:980"/>
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
* I created [qqArtNeph-RNAseq.tsv](./data/qqArtNeph-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qqArtNeph-RNAseq.tsv -p ERGA-BGE -o qqArtNeph-RNAseq
    ```
* Update qqArtNeph-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90607"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission-hold.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission-hold.xml" -F "EXPERIMENT=@qqArtNeph-RNAseq.exp.xml" -F "RUN=@qqArtNeph-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
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
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Artema nephilit" -t qqArtNeph -p ERGA-BGE -c SCILIFELAB -a PRJEB90607 -x 2068848
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
    <RECEIPT receiptDate="2025-07-01T12:24:53.571+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB91431" alias="erga-bge-qqArtNeph-study-umbrella-2025-07-01" status="PRIVATE" holdUntilDate="2025-07-03+01:00"/>
        <SUBMISSION accession="ERA33545287" alias="SUBMISSION-01-07-2025-12:24:53:174"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>    
    ```
* **Note:** Add the assembly project `` when it has been submitted and made public, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.
