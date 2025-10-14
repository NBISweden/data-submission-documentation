---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB91488 (umbrella), PRJEB90632 (experiment), PRJEB90633 (assembly)
---

# BGE - *Decticus albifrons*

## Submission task description
Submission of raw reads for *Decticus albifrons* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Decticus-albifrons-metadata.xlsx)
* [BGE HiFi metadata](./data/iqDecAlbi-HiFi.tsv)
* [BGE HiC metadata](./data/iqDecAlbi-HiC.tsv)
* [BGE RNAseq metadata](./data/iqDecAlbi-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiFi

#### Preparations
* There are 4 bam files
* Sample ID led to BioSample ID in ERGA tracker portal

#### XML

* I created [iqDecAlbi-HiFi.tsv](./data/iqDecAlbi-HiFi.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iqDecAlbi-HiFi.tsv -p ERGA-BGE -o iqDecAlbi-HiFi
    ```
    * Removed 3 extra experiments
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@iqDecAlbi-HiFi.study.xml" -F "EXPERIMENT=@iqDecAlbi-HiFi.exp.xml" -F "RUN=@iqDecAlbi-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-19T07:08:32.911+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14538615" alias="exp_iqDecAlbi_HiFi_WGS_LV6000905101_pr_192" status="PRIVATE"/>
        <RUN accession="ERR15133374" alias="run_iqDecAlbi_HiFi_WGS_LV6000905101_pr_192_bam_1" status="PRIVATE"/>
        <RUN accession="ERR15133375" alias="run_iqDecAlbi_HiFi_WGS_LV6000905101_pr_192_bam_2" status="PRIVATE"/>
        <RUN accession="ERR15133376" alias="run_iqDecAlbi_HiFi_WGS_LV6000905101_pr_192_bam_3" status="PRIVATE"/>
        <RUN accession="ERR15133377" alias="run_iqDecAlbi_HiFi_WGS_LV6000905101_pr_192_bam_4" status="PRIVATE"/>
        <PROJECT accession="PRJEB90632" alias="erga-bge-iqDecAlbi-study-rawdata-2025-06-19" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP173637" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB90633" alias="erga-bge-iqDecAlbi3_primary-2025-06-19" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP173638" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA33373288" alias="SUBMISSION-19-06-2025-07:08:32:344"/>
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
* I received sample ID from [NGI](https://docs.google.com/spreadsheets/d/10ZPAhkp1fCmpqR9GAZMRJ9wdXa8m-1G_/), which I checked in the [ERGA tracking portal](https://genomes.cnag.cat/erga-stream/samples/) which returned biosample [SAMEA116283198](https://www.ebi.ac.uk/biosamples/samples/SAMEA116283198).

* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [iqDecAlbi-HiC.tsv](./data/iqDecAlbi-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iqDecAlbi-HiC.tsv -p ERGA-BGE -o iqDecAlbi-HiC
    ```
* The study XML will not be submitted
* **Note:** There are 2 HiC datasets -> 2 experiments
* Update iqDecAlbi-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90632"/>
    ```

* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library names and titles, since the other data types have the platform named
* Study will be private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@iqDecAlbi-HiC.exp.xml" -F "RUN=@iqDecAlbi-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-27T09:48:05.385+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14570452" alias="exp_iqDecAlbi_Hi-C_LV6000905100_HC035-1A1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX14570453" alias="exp_iqDecAlbi_Hi-C_LV6000905100_HC035-1A2A" status="PRIVATE"/>
        <RUN accession="ERR15164724" alias="run_iqDecAlbi_Hi-C_LV6000905100_HC035-1A1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR15164725" alias="run_iqDecAlbi_Hi-C_LV6000905100_HC035-1A2A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA33527309" alias="SUBMISSION-27-06-2025-09:48:05:050"/>
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
* I created [iqDecAlbi-RNAseq.tsv](./data/iqDecAlbi-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iqDecAlbi-RNAseq.tsv -p ERGA-BGE -o iqDecAlbi-RNAseq
    ```
* Update iqDecAlbi-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90632"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@iqDecAlbi-RNAseq.exp.xml" -F "RUN=@iqDecAlbi-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit assembly

* I created a manifest file [iqDecAlbi3-manifest.txt](./data/iqDecAlbi3-manifest.txt), copied the files (fasta, chromosome & unlocalized list) to local laptop, gzipped all files, validated (successfully) and then submitted using Webin-CLI:
    ```
    java -jar ~/webin-cli-8.2.0.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./iqDecAlbi3-manifest.txt -validate
    ```
* Receipt:
    ```
    INFO : Your application version is 8.2.0
    INFO : A new application version is available. Please download the latest version 9.0.0 from https://github.com/enasequence/webin-cli/releases
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /home/yvonne/BGE/D-albifrons/././webin-cli.report
    INFO : Uploading file: /home/yvonne/BGE/D-albifrons/iqDecAlbi-asm.fa.gz
    INFO : Uploading file: /home/yvonne/BGE/D-albifrons/chromosome_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28268319
    ```
* I added the accession number to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `Assembly submitted` to `Yes`, as well as set assembly as status `Submitted` in [Tracking_tool_Seq_centers](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/edit?pli=1&gid=0#gid=0)
* Accessioned:
    ```
    ASSEMBLY_NAME | ASSEMBLY_ACC  | STUDY_ID   | SAMPLE_ID   | CONTIG_ACC                      | SCAFFOLD_ACC | CHROMOSOME_ACC
    iqDecAlbi3.1  | GCA_971833225 | PRJEB90633 | ERS21327138 | CCWOFZ010000001-CCWOFZ010000021 |              | OZ312699-OZ312714
    ```

#### Add assembly to umbrella
* **Note:** Add the assembly project `PRJEB90633` when it has been submitted and made public, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.
* Create [update.xml](./data/update.xml) and [umbrella_modified.xml](./data/umbrella_modified.xml)
* Submit:
    ```
    curl -u Username:Password -F "SUBMISSION=@update.xml" -F "PROJECT=@umbrella_modified.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-08-25T16:48:38.674+01:00" submissionFile="update.xml" success="true">
        <PROJECT accession="PRJEB91488" alias="erga-bge-iqDecAlbi-study-umbrella-2025-07-02" status="PUBLIC"/>
        <SUBMISSION accession="" alias="SUBMISSION-25-08-2025-16:48:38:576"/>
        <MESSAGES/>
        <ACTIONS>MODIFY</ACTIONS>
    </RECEIPT>
    ```

### Umbrella project
For each of the BGE species, an **umbrella** project has to be created and linked to the main BGE project, [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

1. Release the child project via browser
1. Collect scientific name and tolId from the metadata template sheet
1. Go to [ENA browser](https://www.ebi.ac.uk/ena/browser/home) and enter the scientific name as search term
    1. To the left side, there should be a **Taxon** subheading, that gives the identifier
1. Copy experiment accession number from metadata in top of this README
* There is a CNAG script, that should do the deed of creating the xml file:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Decticus albifrons" -t iqDecAlbi -p ERGA-BGE -c SCILIFELAB -a PRJEB90632 -x 470614
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
    <RECEIPT receiptDate="2025-07-02T07:45:26.357+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB91488" alias="erga-bge-iqDecAlbi-study-umbrella-2025-07-02" status="PRIVATE" holdUntilDate="2025-07-04+01:00"/>
        <SUBMISSION accession="ERA33548614" alias="SUBMISSION-02-07-2025-07:45:26:002"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>    
    ```
