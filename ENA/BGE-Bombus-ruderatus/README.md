---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB96488 (umbrella), PRJEB91068 (experiment), PRJEB91069 (assembly), PRJEB100690 (mito)
---

# BGE - *Bombus ruderatus*

## Submission task description
Submission of raw reads for *Bombus ruderatus* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Bombus-ruderatus-metadata.xlsx)
* [BGE HiFi metadata](./data/iyBomRudr-HiFi.tsv)
* [BGE HiC metadata](./data/iyBomRudr-HiC.tsv)
* [BGE RNAseq metadata](./data/iyBomRudr-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiFi
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput *.bam` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.
#### XML
* I created [iyBomRudr-HiFi.tsv](./data/iyBomRudr-HiFi.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iyBomRudr-HiFi.tsv -p ERGA-BGE -o iyBomRudr-HiFi
    ```

* Study is private, so submission.xml with hold date is used.

* Submit both projects and experiment in one go, i.e:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@iyBomRudr-HiFi.study.xml" -F "EXPERIMENT=@iyBomRudr-HiFi.exp.xml" -F "RUN=@iyBomRudr-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-26T06:15:39.387+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14565391" alias="exp_iyBomRudr_HiFi_WGS_LV6000905157_pr_254_001" status="PRIVATE"/>
        <RUN accession="ERR15159739" alias="run_iyBomRudr_HiFi_WGS_LV6000905157_pr_254_001_bam_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB91068" alias="erga-bge-iyBomRudr-study-rawdata-2025-06-26" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP174064" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB91069" alias="erga-bge-iyBomRudr4_primary-2025-06-26" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP174065" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA33523182" alias="SUBMISSION-26-06-2025-06:15:38:981"/>
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
* I created [iyBomRudr-HiC.tsv](./data/iyBomRudr-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iyBomRudr-HiC.tsv -p ERGA-BGE -o iyBomRudr-HiC
    ```
* Update iyBomRudr-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB91068"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title, since the other data types have the platform named
* Study is public, so submission-noHold.xml is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission-noHold.xml" -F "EXPERIMENT=@iyBomRudr-HiC.exp.xml" -F "RUN=@iyBomRudr-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-09-25T13:14:45.251+01:00" submissionFile="submission-noHold.xml" success="true">
        <EXPERIMENT accession="ERX15056315" alias="exp_iyBomRudr_Hi-C_LV6000905156_HC051-1A1A-CL" status="PRIVATE"/>
        <RUN accession="ERR15651752" alias="run_iyBomRudr_Hi-C_LV6000905156_HC051-1A1A-CL_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA35018355" alias="SUBMISSION-25-09-2025-13:14:44:876"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    </RECEIPT>
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit RNAseq - **TODO**
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [iyBomRudr-RNAseq.tsv](./data/iyBomRudr-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iyBomRudr-RNAseq.tsv -p ERGA-BGE -o iyBomRudr-RNAseq
    ```
* Update iyBomRudr-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB91068"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@iyBomRudr-RNAseq.exp.xml" -F "RUN=@iyBomRudr-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit assembly

* There is also a mitochondrial assembly, so I created a project for this:
    * I created [iyBomRudr-mito.study.xml](./data/iyBomRudr-mito.study.xml) and submitted using curl:
        ```
        curl -u username:password -F "SUBMISSION=@submission-hold.xml" -F "PROJECT=@iyBomRudr-mito.study.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
        ```
        * Receipt:
        ```
        <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
        <RECEIPT receiptDate="2025-10-14T15:21:47.260+01:00" submissionFile="submission-hold.xml" success="true">
            <PROJECT accession="PRJEB100690" alias="erga-bge-iyBomRudr-study-mito-2025-10-14" status="PRIVATE" holdUntilDate="2026-03-07Z">
                <EXT_ID accession="ERP182146" type="study"/>
            </PROJECT>
            <SUBMISSION accession="ERA35060600" alias="SUBMISSION-14-10-2025-15:21:47:160"/>
            <MESSAGES>
                <INFO>All objects in this submission are set to private status (HOLD).</INFO>
            </MESSAGES>
            <ACTIONS>ADD</ACTIONS>
            <ACTIONS>HOLD</ACTIONS>
        </RECEIPT>
        ```
* I created manifest files [iyBomRudr4-manifest.txt](./data/iyBomRudr4-manifest.txt) and [iyBomRudr4-manifest-mito.txt](./data/iyBomRudr4-manifest-mito.txt) and chromosome_list.txt for both primary and mito assembly, plus an unlocalised_list.txt for the primary assembly
* I created a folder on Uppmax (/proj/snic2022-6-208/nobackup/submission/B-ruderatus/) and copied & gzipped manifest, assembly files, chromosome lists and unlocalised list there
* Then all files where submitted (first validation then submission) from Pelle on Uppmax using Webin-CLI:

    ```
    interactive -t 02:00:00 -A uppmax2025-2-58
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./iyBomRudr4-manifest.txt -validate
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./iyBomRudr4-manifest-mito.txt -validate
    ```
* Receipt primary:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/B-ruderatus/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/B-ruderatus/iyBomRudr4_pri_20251014.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/B-ruderatus/chromosome_list.txt.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/B-ruderatus/unlocalized_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28541572
    ```
* Receipt mito:
    ```
    INFO : Your application version is 9.0.1
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/B-ruderatus/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/B-ruderatus/iyBomRudr4_mito_20251014.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/B-ruderatus/mito-chromosome_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28541573
    ```
* I added the accession number to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `Assembly submitted` to `Yes`, as well as set assembly as status `Submitted` in [Tracking_tool_Seq_centers](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/edit?pli=1&gid=0#gid=0)
* Accessioned:
    ```
    ASSEMBLY_NAME     | ASSEMBLY_ACC  | STUDY_ID    | SAMPLE_ID   | CONTIG_ACC                      | SCAFFOLD_ACC | CHROMOSOME_ACC
    iyBomRudr4.1      | GCA_977009165 | PRJEB91069  | ERS21326968 | CDRMXC010000001-CDRMXC010000015 |              | OZ346462-OZ346480
    iyBomRudr4-mito.1 | GCA_977009185 | PRJEB100690 | ERS21326968 |                                 |              | OZ346435-OZ346435
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
    <RECEIPT receiptDate="2025-10-15T07:44:33.423+01:00" submissionFile="update.xml" success="true">
        <PROJECT accession="PRJEB96488" alias="erga-bge-iyBomRudr-study-umbrella-2025-08-27" status="PUBLIC"/>
        <SUBMISSION accession="" alias="SUBMISSION-15-10-2025-07:44:33:240"/>
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
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Bombus ruderatus" -t iyBomRudr4 -p ERGA-BGE -c SCILIFELAB -a PRJEB91068 -x 207645
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
    <RECEIPT receiptDate="2025-08-27T09:44:15.049+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB96488" alias="erga-bge-iyBomRudr-study-umbrella-2025-08-27" status="PRIVATE" holdUntilDate="2026-03-07Z"/>
        <SUBMISSION accession="ERA34838289" alias="SUBMISSION-27-08-2025-09:44:14:868"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
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
    <RECEIPT receiptDate="2025-08-27T09:46:50.487+01:00" submissionFile="submission-release-project.xml" success="true">
        <MESSAGES>
            <INFO>project accession "PRJEB96488" is set to public status.</INFO>
        </MESSAGES>
        <ACTIONS>RELEASE</ACTIONS>
    </RECEIPT>    
    ```
