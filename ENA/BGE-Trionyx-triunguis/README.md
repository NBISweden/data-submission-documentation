---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB100764 (umbrella), PRJEB96316 (experiment), PRJEB96317 (assembly), PRJEB100729 (mito)
---

# BGE - *Trionyx triunguis*

## Submission task description
Submission of raw reads for *Trionyx triunguis* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Trionyx-triunguis-metadata.xlsx)
* [BGE HiFi metadata](./data/rTriTgu-HiFi.tsv)
* [BGE HiC metadata](./data/rTriTgu-HiC.tsv)
* [BGE RNAseq metadata](./data/rTriTgu-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiFi
#### Preparations
* The `tube or well id` given has been used to create 2 BioSamples -> a virtual sample is needed
    * I created [rTriTgu-HiFi-virtual-sample.tsv](./data/rTriTgu-HiFi-virtual-sample.tsv) and registered the sample
    * Accession number received: `ERS26118506`  
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput *.bam` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.
#### XML
* I created [rTriTgu-HiFi.tsv](./data/rTriTgu-HiFi.tsv)

* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f rTriTgu-HiFi.tsv -p ERGA-BGE -o rTriTgu-HiFi
    ```
* There are 2 .bam files and script created 2 experiments (duplicates). Hence, one of them was manually removed.
* Study is private, so submission.xml with hold date is used.

* Submit both projects and experiment in one go, i.e:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@rTriTgu-HiFi.study.xml" -F "EXPERIMENT=@rTriTgu-HiFi.exp.xml" -F "RUN=@rTriTgu-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-08-24T11:16:23.825+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14868745" alias="exp_rTriTgu_HiFi_WGS_TT9_pr_259_001" status="PRIVATE"/>
        <RUN accession="ERR15464849" alias="run_rTriTgu_HiFi_WGS_TT9_pr_259_001_bam_1" status="PRIVATE"/>
        <RUN accession="ERR15464850" alias="run_rTriTgu_HiFi_WGS_TT9_pr_259_001_bam_2" status="PRIVATE"/>
        <PROJECT accession="PRJEB96316" alias="erga-bge-rTriTgu-study-rawdata-2025-08-22" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP179059" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB96317" alias="erga-bge-rTriTgu1_primary-2025-08-22" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP179060" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA34528105" alias="SUBMISSION-24-08-2025-11:16:23:592"/>
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
* Sample ID gave 4 BioSample ID:s via ERGA tracker portal --> virtual sample is needed
    * I created [rTriTgu-HiC-virtual-sample.tsv](./data/rTriTgu-HiC-virtual-sample.tsv) and registered the sample
    * Accession number received: `ERS26118849`     
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [rTriTgu-HiC.tsv](./data/rTriTgu-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f rTriTgu-HiC.tsv -p ERGA-BGE -o rTriTgu-HiC
    ```
* Update rTriTgu-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB96316"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title , since the other data types have the platform named
* Study will be private, so submission.xml with hold date is used.
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@rTriTgu-HiC.exp.xml" -F "RUN=@rTriTgu-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-09-25T09:29:25.301+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX15053399" alias="exp_rTriTgu_Hi-C_TT2_TT6_HC027-4A1A" status="PRIVATE"/>
        <RUN accession="ERR15648906" alias="run_rTriTgu_Hi-C_TT2_TT6_HC027-4A1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA35017333" alias="SUBMISSION-25-09-2025-09:29:24:976"/>
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
* I created [rTriTgu-RNAseq.tsv](./data/rTriTgu-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f rTriTgu-RNAseq.tsv -p ERGA-BGE -o rTriTgu-RNAseq
    ```
* Update rTriTgu-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB96316"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@rTriTgu-RNAseq.exp.xml" -F "RUN=@rTriTgu-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit assembly
* There is also a mitochondrial assembly, so I created a project for this:
    * I created [rTriTgu-mito.study.xml](./data/rTriTgu-mito.study.xml) and submitted using curl:
        ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@rTriTgu-mito.study.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
        ```
        * Receipt:
        ```
        <?xml version="1.0" encoding="UTF-8"?>
        <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
        <RECEIPT receiptDate="2025-10-15T09:08:19.605+01:00" submissionFile="submission.xml" success="true">
            <PROJECT accession="PRJEB100729" alias="erga-bge-rTriTgu-study-mito-2025-10-15" status="PRIVATE" holdUntilDate="2026-03-07Z">
                <EXT_ID accession="ERP182185" type="study"/>
            </PROJECT>
            <SUBMISSION accession="ERA35060794" alias="SUBMISSION-15-10-2025-09:08:19:546"/>
            <MESSAGES>
                <INFO>All objects in this submission are set to private status (HOLD).</INFO>
            </MESSAGES>
            <ACTIONS>ADD</ACTIONS>
            <ACTIONS>HOLD</ACTIONS>
        </RECEIPT>
        ```
* I created manifest files [rTriTgu1-manifest.txt](./data/rTriTgu1-manifest.txt) and [rTriTgu1-manifest-mito.txt](./data/rTriTgu1-manifest-mito.txt) and chromosome_list.txt for both primary and mito assembly, plus an unlocalized_list.txt for the primary assembly
* I created a folder on Uppmax (/proj/snic2022-6-208/nobackup/submission/T-triunguis/) and copied & gzipped manifest, assembly files, chromosome lists and unlocalised list there
* Then all files where submitted (first validation then submission) from Pelle on Uppmax using Webin-CLI:

    ```
    interactive -t 02:00:00 -A uppmax2025-2-58
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./rTriTgu1-manifest.txt -validate
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./rTriTgu1-manifest-mito.txt -validate
    ```
* Receipt primary:
    ```
    INFO : Your application version is 9.0.1
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/T-triunguis/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/T-triunguis/rTriTgu1_pri_20251013.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/T-triunguis/chromosome_list.txt.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/T-triunguis/unlocalized_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28541639
    ```
* Receipt mito:
    ```
    INFO : Your application version is 9.0.1
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/T-triunguis/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/T-triunguis/rTriTgu1_mito_20251013.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/T-triunguis/mito-chromosome_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28541640
    ```
* I added the accession number to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `Assembly submitted` to `Yes`, as well as set assembly as status `Submitted` in [Tracking_tool_Seq_centers](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/edit?pli=1&gid=0#gid=0)
* Accessioned:
    ```
    ASSEMBLY_NAME     | ASSEMBLY_ACC  | STUDY_ID    | SAMPLE_ID   | CONTIG_ACC                      | SCAFFOLD_ACC | CHROMOSOME_ACC

    ```
* Release study and check that it is shown under umbrella

### Umbrella project
For each of the BGE species, an **umbrella** project has to be created and linked to the main BGE project, [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

1. Release the child project via browser
1. Collect scientific name and tolId from the metadata template sheet
1. Go to [ENA browser](https://www.ebi.ac.uk/ena/browser/home) and enter the scientific name as search term
    1. To the left side, there should be a **Taxon** subheading, that gives the identifier
1. Copy experiment accession number from metadata in top of this README
* There is a CNAG script, that should do the deed of creating the xml file:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Trionyx triunguis" -t rTriTgu1 -p ERGA-BGE -c SCILIFELAB -a PRJEB96316 -x 101491
    ```
    Explanation of arguments:
    * -s: scientific name e.g. "Lithobius stygius"
    * -t: tolId e.g. qcLitStyg1
    * -a: the accession number of the raw reads project e.g. PRJEB76283
    * -x: NCBI taxonomy id e.g. 2750798

* Since I already have the project accession numbers for primary and mito assemblies (and they are submitted), I add these as children as well.
* Copy `submission-umbrella.xml` from any of the previous BGE species
* Submit using curl:
    ```
    curl -u Username:Password -F "SUBMISSION=@submission-umbrella.xml" -F "PROJECT=@umbrella.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-10-15T11:22:18.764+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB100764" alias="erga-bge-rTriTgu-study-umbrella-2025-10-15" status="PRIVATE" holdUntilDate="2027-10-15+01:00"/>
        <SUBMISSION accession="ERA35060985" alias="SUBMISSION-15-10-2025-11:22:18:408"/>
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
    <RECEIPT receiptDate="2025-10-15T11:24:57.986+01:00" submissionFile="submission-release-project.xml" success="true">
        <MESSAGES>
            <INFO>project accession "PRJEB100764" is set to public status.</INFO>
        </MESSAGES>
        <ACTIONS>RELEASE</ACTIONS>
    </RECEIPT>    
    ```
