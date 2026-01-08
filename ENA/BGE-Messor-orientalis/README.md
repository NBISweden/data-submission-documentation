---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB101764 (umbrella), PRJEB100781 (experiment), PRJEB100782 (assembly), PRJEB106245 (mito)
---

# BGE - *Messor orientalis*

## Submission task description
Submission of raw reads for *Messor orientalis* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Messor-orientalis-metadata.xlsx)
* [BGE HiFi metadata](./data/iyMesOrie-HiFi.tsv)
* [BGE HiC metadata](./data/iyMesOrie-HiC.tsv)
* [BGE RNAseq metadata](./data/iyMesOrie-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiFi
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data HiFi data has library prep using AmpliFi protocol, thus the trimmed reads are to be submitted. This file has been provided as a .fastq file (not .bam as is usual for this data type), hence I need to make sure that the .xml file will look ok (and that script works). The data file was transferred  using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput *.fastq.gz` and added ToLID to the file using rename function in FileZilla, to make it easier to see that right file will be submitted.
#### XML
* I created [iyMesOrie-HiFi.tsv](./data/iyMesOrie-HiFi.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iyMesOrie-HiFi.tsv -p ERGA-BGE -o iyMesOrie-HiFi
    ```
* Didn't work due to expecting .bam file so I shifted column from `native_file` to `file_name` but then the .run.xml is largely empty. Hence, need to trick the script by putting the file in `native_file_name` and change ending to `.bam`, then afterwards change to appropriate values in run .xml (rows `<RUN ` and `<FILE `)
* Study is private, so submission.xml with hold date is used.

* Submit both projects and experiment in one go, i.e:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@iyMesOrie-HiFi.study.xml" -F "EXPERIMENT=@iyMesOrie-HiFi.exp.xml" -F "RUN=@iyMesOrie-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-10-15T13:45:21.571+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX15106038" alias="exp_iyMesOrie_HiFi_WGS_LV6000912094_pr_261_003" status="PRIVATE"/>
        <RUN accession="ERR15701808" alias="run_iyMesOrie_HiFi_WGS_LV6000912094_pr_261_003_fastq_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB100781" alias="erga-bge-iyMesOrie-study-rawdata-2025-10-15" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP182226" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB100782" alias="erga-bge-iyMesOrie12_primary-2025-10-15" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP182227" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA35061088" alias="SUBMISSION-15-10-2025-13:45:21:324"/>
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
* I created [iyMesOrie-HiC.tsv](./data/iyMesOrie-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iyMesOrie-HiC.tsv -p ERGA-BGE -o iyMesOrie-HiC
    ```
* Update iyMesOrie-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB100781"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title, since the other data types have the platform named
* Study will be private, so submission.xml with hold date is used.
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@iyMesOrie-HiC.exp.xml" -F "RUN=@iyMesOrie-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-10-15T14:53:15.411+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX15107902" alias="exp_iyMesOrie_Hi-C_LV6000912093_HC048-1A1A" status="PRIVATE"/>
        <RUN accession="ERR15703066" alias="run_iyMesOrie_Hi-C_LV6000912093_HC048-1A1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA35061186" alias="SUBMISSION-15-10-2025-14:53:15:241"/>
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
* I created [iyMesOrie-RNAseq.tsv](./data/iyMesOrie-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iyMesOrie-RNAseq.tsv -p ERGA-BGE -o iyMesOrie-RNAseq
    ```
* Update iyMesOrie-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB100781"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@iyMesOrie-RNAseq.exp.xml" -F "RUN=@iyMesOrie-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit assembly
* There is a separate mito assembly, hence need to create an additional project:
    * I created [iyMesOrie-mito.study.xml](./data/iyMesOrie-mito.study.xml) and submitted using curl:
        ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@iyMesOrie-mito.study.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
        ```
        * Receipt:
        ```
        <?xml version="1.0" encoding="UTF-8"?>
        <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
        <RECEIPT receiptDate="2026-01-07T09:51:31.225Z" submissionFile="submission.xml" success="true">
            <PROJECT accession="PRJEB106245" alias="erga-bge-iyMesOrie12_mito-2026-01-07" status="PRIVATE" holdUntilDate="2026-03-07Z">
                <EXT_ID accession="ERP187339" type="study"/>
            </PROJECT>
            <SUBMISSION accession="ERA35440762" alias="SUBMISSION-07-01-2026-09:51:31:139"/>
            <MESSAGES>
                <INFO>All objects in this submission are set to private status (HOLD).</INFO>
            </MESSAGES>
            <ACTIONS>ADD</ACTIONS>
            <ACTIONS>HOLD</ACTIONS>
        </RECEIPT>
        ```
* I created a manifest files [iyMesOrie-manifest.txt](./data/iyMesOrie-manifest.txt) and [iyMesOrie-mito-manifest.txt](./data/iyMesOrie-mito-manifest.txt)
* I created a folder on Uppmax (/proj/snic2022-6-208/nobackup/submission/M-orientalis) and copied & gzipped manifests, assembly file and chromosome list there
* Then all files where submitted (first validation then submission) from Pelle on Uppmax using Webin-CLI:

    ```
    interactive -t 08:00:00 -A uppmax2025-2-58
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./iyMesOrie-manifest.txt -validate
    ```
* Receipt mito:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/M-orientalis/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/M-orientalis/iyMesOrie12.mito.20251219.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/M-orientalis/mito-chromosome_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28782833
    ```
* Receipt primary:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/M-orientalis/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/M-orientalis/iyMesOrie12.pri.20251219.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/M-orientalis/chromosome_list.txt.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/M-orientalis/unlocalised_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28782834
    ```
* I added the accession number to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `Assembly submitted` to `Yes`, as well as set assembly as status `Submitted` in [Tracking_tool_Seq_centers](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/edit?pli=1&gid=0#gid=0)
* Accessioned:
    ```
    ASSEMBLY_NAME      | ASSEMBLY_ACC  | STUDY_ID    | SAMPLE_ID   | CONTIG_ACC                      | SCAFFOLD_ACC | CHROMOSOME_ACC
    iyMesOrie12-mito.1 | GCA_978018215 | PRJEB106245 | ERS21344432 |                                 |              | OZ389535-OZ389535
    iyMesOrie12.1      | GCA_978018205 | PRJEB100782 | ERS21344432 | CDXDGT010000001-CDXDGT010000087 |              | OZ389536-OZ389556

    ```
* Release studies and check that they are shown under umbrella

#### Add assembly to umbrella
* Add the assembly projects when they have been submitted, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.
* Create [update.xml](./data/update.xml) and [umbrella_modified.xml](./data/umbrella_modified.xml)
* Submit:
    ```
    curl -u Username:Password -F "SUBMISSION=@update.xml" -F "PROJECT=@umbrella_modified.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2026-01-07T10:06:31.323Z" submissionFile="update.xml" success="true">
        <PROJECT accession="PRJEB101764" alias="erga-bge-iyMesOrie-study-umbrella-2025-10-28" status="PUBLIC"/>
        <SUBMISSION accession="" alias="SUBMISSION-07-01-2026-10:06:31:129"/>
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
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "" -t  -p ERGA-BGE -c SCILIFELAB -a  -x 
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
    <RECEIPT receiptDate="2025-10-28T07:53:34.154Z" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB101764" alias="erga-bge-iyMesOrie-study-umbrella-2025-10-28" status="PRIVATE" holdUntilDate="2027-10-28+01:00"/>
        <SUBMISSION accession="ERA35078353" alias="SUBMISSION-28-10-2025-07:53:33:888"/>
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
    <RECEIPT receiptDate="2025-10-28T08:45:28.107Z" submissionFile="submission-release-project.xml" success="true">
        <MESSAGES>
            <INFO>project accession "PRJEB101764" is set to public status.</INFO>
        </MESSAGES>
        <ACTIONS>RELEASE</ACTIONS>
    </RECEIPT>  
    ```
