---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB96352 (umbrella), PRJEB96318 (experiment), PRJEB96319 (assembly), PRJEB100694 (mito)
---

# BGE - *Cataglyphis aphrodite*

## Submission task description
Submission of raw reads for *Cataglyphis aphrodite* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Cataglyphis-aphrodite-metadata.xlsx)
* [BGE HiFi metadata](./data/iyCatAphr-HiFi.tsv)
* [BGE HiC metadata](./data/iyCatAphr-HiC.tsv)
* [BGE RNAseq metadata](./data/iyCatAphr-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiFi
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput *.bam` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.
#### XML
* I created [iyCatAphr-HiFi.tsv](./data/iyCatAphr-HiFi.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iyCatAphr-HiFi.tsv -p ERGA-BGE -o iyCatAphr-HiFi
    ```

* Study is private, so submission.xml with hold date is used.

* Submit both projects and experiment in one go, i.e:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@iyCatAphr-HiFi.study.xml" -F "EXPERIMENT=@iyCatAphr-HiFi.exp.xml" -F "RUN=@iyCatAphr-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-08-24T11:27:25.544+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14868746" alias="exp_iyCatAphr_HiFi_WGS_LV6000912098_pr_251_001" status="PRIVATE"/>
        <RUN accession="ERR15464851" alias="run_iyCatAphr_HiFi_WGS_LV6000912098_pr_251_001_bam_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB96318" alias="erga-bge-iyCatAphr-study-rawdata-2025-08-22" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP179061" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB96319" alias="erga-bge-iyCatAphr12_primary-2025-08-22" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP179062" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA34528960" alias="SUBMISSION-24-08-2025-11:27:25:397"/>
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
* I created [iyCatAphr-HiC.tsv](./data/iyCatAphr-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iyCatAphr-HiC.tsv -p ERGA-BGE -o iyCatAphr-HiC
    ```
* Update iyCatAphr-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB96318"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title, since the other data types have the platform named
* Study will be private, so submission.xml with hold date is used.
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@iyCatAphr-HiC.exp.xml" -F "RUN=@iyCatAphr-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-08-24T11:34:26.709+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14868747" alias="exp_iyCatAphr_Hi-C_LV6000912131_HC039-1A1A" status="PRIVATE"/>
        <RUN accession="ERR15464852" alias="run_iyCatAphr_Hi-C_LV6000912131_HC039-1A1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA34529601" alias="SUBMISSION-24-08-2025-11:34:26:581"/>
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
* I created [iyCatAphr-RNAseq.tsv](./data/iyCatAphr-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iyCatAphr-RNAseq.tsv -p ERGA-BGE -o iyCatAphr-RNAseq
    ```
* Update iyCatAphr-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB96318"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@iyCatAphr-RNAseq.exp.xml" -F "RUN=@iyCatAphr-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit assembly
* There is also a mitochondrial assembly, so I created a project for this:
    * I created [iyCatAphr-mito.study.xml](./data/iyCatAphr-mito.study.xml) and submitted using curl:
        ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@iyCatAphr-mito.study.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
        ```
        * Receipt:
        ```
        <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
        <RECEIPT receiptDate="2025-10-14T15:40:56.458+01:00" submissionFile="submission.xml" success="true">
            <PROJECT accession="PRJEB100694" alias="erga-bge-iyCatAphr-study-mito-2025-10-14" status="PRIVATE" holdUntilDate="2026-03-07Z">
                <EXT_ID accession="ERP182150" type="study"/>
            </PROJECT>
            <SUBMISSION accession="ERA35060658" alias="SUBMISSION-14-10-2025-15:40:56:394"/>
            <MESSAGES>
                <INFO>All objects in this submission are set to private status (HOLD).</INFO>
            </MESSAGES>
            <ACTIONS>ADD</ACTIONS>
            <ACTIONS>HOLD</ACTIONS>
        </RECEIPT>
        ```

* I created manifest files [iyCatAphr12-manifest.txt](./data/iyCatAphr12-manifest.txt) and [iyCatAphr12-manifest-mito.txt](./data/iyCatAphr12-manifest-mito.txt) and chromosome_list.txt for both primary and mito assembly
* I created a folder on Uppmax (/proj/snic2022-6-208/nobackup/submission/C-aphrodite/) and copied & gzipped manifests, assembly files and chromosome lists there
* Then all files where submitted (first validation then submission) from Pelle on Uppmax using Webin-CLI:

    ```
    interactive -t 08:00:00 -A uppmax2025-2-58
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./iyCatAphr12-manifest.txt -validate
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./iyCatAphr12-manifest-mito.txt -validate    
    ```
* Receipt primary:
    ```
    INFO : Your application version is 9.0.1
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/C-aphrodite/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/C-aphrodite/iyCatAphr12_pri_20251013.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/C-aphrodite/chromosome_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28541574
    ```
* Receipt mito:
    ```
    INFO : Your application version is 9.0.1
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/C-aphrodite/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/C-aphrodite/iyCatAphr12_mito_20251013.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/C-aphrodite/mito-chromosome_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28541575
    ```
* I added the accession numbers to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `Assembly submitted` to `Yes`, as well as set assembly as status `Submitted` in [Tracking_tool_Seq_centers](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/edit?pli=1&gid=0#gid=0)
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
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Cataglyphis aphrodite" -t iyCatAphr12 -p ERGA-BGE -c SCILIFELAB -a PRJEB96318 -x 3229133
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
    <RECEIPT receiptDate="2025-08-25T12:32:17.411+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB96352" alias="erga-bge-iyCatAphr-study-umbrella-2025-08-25" status="PRIVATE" holdUntilDate="2027-08-25+01:00"/>
        <SUBMISSION accession="ERA34664529" alias="SUBMISSION-25-08-2025-12:32:17:254"/>
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
    <RECEIPT receiptDate="2025-08-25T12:35:23.705+01:00" submissionFile="submission-release-project.xml" success="true">
        <MESSAGES>
            <INFO>project accession "PRJEB96352" is set to public status.</INFO>
        </MESSAGES>
        <ACTIONS>RELEASE</ACTIONS>
    </RECEIPT>    
    ```
