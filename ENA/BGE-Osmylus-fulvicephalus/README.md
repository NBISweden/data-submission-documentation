---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB91535 (umbrella), PRJEB90646 (experiment), PRJEB90647 (assembly), PRJEB104486 (mito)
---

# BGE - *Osmylus fulvicephalus*

## Submission task description
Submission of raw reads for *Osmylus fulvicephalus* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Osmylus-fulvicephalus-metadata.xlsx)
* [BGE HiFi metadata](./data/inOsmFulv-HiFi.tsv)
* [BGE HiC metadata](./data/inOsmFulv-HiC.tsv)
* [BGE RNAseq metadata](./data/inOsmFulv-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiFi
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput *.bam` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.
#### XML
* I created [inOsmFulv-HiFi.tsv](./data/inOsmFulv-HiFi.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f inOsmFulv-HiFi.tsv -p ERGA-BGE -o inOsmFulv-HiFi
    ```

* Study is private, so submission.xml with hold date is used.

* Submit both projects and experiment in one go, i.e:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@inOsmFulv-HiFi.study.xml" -F "EXPERIMENT=@inOsmFulv-HiFi.exp.xml" -F "RUN=@inOsmFulv-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-19T08:14:27.196+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14538627" alias="exp_inOsmFulv_HiFi_WGS_FS55571909_pr_220" status="PRIVATE"/>
        <RUN accession="ERR15133391" alias="run_inOsmFulv_HiFi_WGS_FS55571909_pr_220_bam_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB90646" alias="erga-bge-inOsmFulv-study-rawdata-2025-06-19" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP173651" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB90647" alias="erga-bge-inOsmFulv5_primary-2025-06-19" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP173652" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA33375940" alias="SUBMISSION-19-06-2025-08:14:26:874"/>
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
* I created [inOsmFulv-HiC.tsv](./data/inOsmFulv-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f inOsmFulv-HiC.tsv -p ERGA-BGE -o inOsmFulv-HiC
    ```
* Update inOsmFulv-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90646"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study will be private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@inOsmFulv-HiC.exp.xml" -F "RUN=@inOsmFulv-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-30T07:09:30.987+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14574817" alias="exp_inOsmFulv_Hi-C_FS55571895        _HC026-1A1A-CL" status="PRIVATE"/>
        <RUN accession="ERR15169086" alias="run_inOsmFulv_Hi-C_FS55571895        _HC026-1A1A-CL_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA33538413" alias="SUBMISSION-30-06-2025-07:09:30:789"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
    * **Note:** A lot of spaces in experiment & run aliases due to additional spaces in `tube or sample ID`, might not have any effect but should be updated via browser. Doesn't seems to be able to according to ENA docs: "*Note that under no circumstances can an object’s own accession or alias attribute be edited.*"
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit RNAseq - **TODO**
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [inOsmFulv-RNAseq.tsv](./data/inOsmFulv-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f inOsmFulv-RNAseq.tsv -p ERGA-BGE -o inOsmFulv-RNAseq
    ```
* Update -RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90646"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@inOsmFulv-RNAseq.exp.xml" -F "RUN=@inOsmFulv-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit assembly
* There is a mito assembly so first I need a new project:
    * Create [inOsmFulv-mito.study.xml](./data/inOsmFulv-mito.study.xml)
    * Submit using curl:
        ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@inOsmFulv-mito.study.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
        ```
    * Receipt:
        ```
        <?xml version="1.0" encoding="UTF-8"?>
        <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
        <RECEIPT receiptDate="2025-11-28T09:39:37.301Z" submissionFile="submission.xml" success="true">
            <PROJECT accession="PRJEB104486" alias="erga-bge-inOsmFulv5_mito-2025-11-28" status="PRIVATE" holdUntilDate="2026-03-07Z">
                <EXT_ID accession="ERP185779" type="study"/>
            </PROJECT>
            <SUBMISSION accession="ERA35282239" alias="SUBMISSION-28-11-2025-09:39:37:272"/>
            <MESSAGES>
                <INFO>All objects in this submission are set to private status (HOLD).</INFO>
            </MESSAGES>
            <ACTIONS>ADD</ACTIONS>
            <ACTIONS>HOLD</ACTIONS>
        </RECEIPT>    
        ```
* I created manifest files [inOsmFulv5-manifest.txt](./data/inOsmFulv5-manifest.txt) and [inOsmFulv5-mito-manifest.txt](./data/inOsmFulv5-mito-manifest.txt)
* I created a folder on Uppmax (/proj/snic2022-6-208/nobackup/submission/O-fulvicephalus) and copied & gzipped manifest, assembly files, unlocalised list and chromosome lists there
* Then all files where submitted (first validation then submission) from Pelle on Uppmax using Webin-CLI:

    ```
    interactive -t 08:00:00 -A uppmax2025-2-58
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./inOsmFulv5-manifest.txt -validate
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./inOsmFulv5-mito-manifest.txt -validate    
    ```
* Receipt primary:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/O-fulvicephalus/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/O-fulvicephalus/inOsmFulv5_pri_20251126.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/O-fulvicephalus/chromosome_list.txt.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/O-fulvicephalus/unlocalised_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28674206
    ```
* Receipt mito:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/O-fulvicephalus/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/O-fulvicephalus/inOsmFulv5_mito_20251126.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/O-fulvicephalus/mito-chromosome_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28674205
    ```
* I added the accession number to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `Assembly submitted` to `Yes`, as well as set assembly as status `Submitted` in [Tracking_tool_Seq_centers](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/edit?pli=1&gid=0#gid=0)
* Accessioned:
    ```
    ASSEMBLY_NAME | ASSEMBLY_ACC  | STUDY_ID   | SAMPLE_ID   | CONTIG_ACC                      | SCAFFOLD_ACC | CHROMOSOME_ACC

    ```
* Release study and check that it is shown under umbrella

#### Add assembly to umbrella
* Add the assembly project when it has been submitted, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.
* Create [update.xml](./data/update.xml) and [umbrella_modified.xml](./data/umbrella_modified.xml)
* Submit:
    ```
    curl -u Username:Password -F "SUBMISSION=@update.xml" -F "PROJECT=@umbrella_modified.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-11-28T10:48:35.017Z" submissionFile="update.xml" success="true">
        <PROJECT accession="PRJEB91535" alias="erga-bge-inOsmFulv-study-umbrella-2025-07-02" status="PUBLIC"/>
        <SUBMISSION accession="" alias="SUBMISSION-28-11-2025-10:48:34:788"/>
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
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Osmylus fulvicephalus" -t inOsmFulv -p ERGA-BGE -c SCILIFELAB -a PRJEB90646 -x 446453
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
    <RECEIPT receiptDate="2025-07-02T08:27:19.916+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB91535" alias="erga-bge-inOsmFulv-study-umbrella-2025-07-02" status="PRIVATE" holdUntilDate="2025-07-04+01:00"/>
        <SUBMISSION accession="ERA33548753" alias="SUBMISSION-02-07-2025-08:27:19:615"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>    
    ```
