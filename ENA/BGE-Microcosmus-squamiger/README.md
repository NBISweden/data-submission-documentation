---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB91533 (umbrella), PRJEB83563 (experiment), PRJEB83564 (assembly), PRJEB104483 (mito)
---

# BGE - *Microcosmus squamiger*

## Submission task description
Submission of raw reads for *Microcosmus squamiger* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample(s) used for sequencing has already been submitted via COPO.
Submission will be done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Microcosmus-squamiger-metadata.xlsx)
* [BGE HiFi metadata](./data/kaMicSqua-hifi.tsv)
* [BGE HiC metadata](./data/kaMicSqua-hic.tsv)
* [BGE RNAseq metadata](./data/kaMicSqua-rnaseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Data transfer
* Create folder `bge-microcosmus-squamiger` at ENA upload area using Filezilla
* Using aspera from Uppmax didn't work, used lftp:
    ```
    interactive -t 06:00:00 -A naiss2024-22-345
    lftp webin2.ebi.ac.uk -u Webin-XXX
    cd bge-microcosmus-squamiger
    mput /proj/snic2022-6-208/INBOX/BGE_Microcosmus-squamiger/EBP_pr_144/files/pr_144/rawdata/pr_144_001/cell*/*.bam
    ```
* Keep track of progress using FileZilla

### HiFi submission
#### Collecting metadata
* I looked at the delivery README for the HiFi dataset (on Uppmax) and extracted the Name (`FS42549340`). I looked in the [ERGA tracking portal](https://genomes.cnag.cat/erga-stream/samples/), filtered on the organism, and saw that the Name was registered with biosample [SAMEA115808870](https://www.ebi.ac.uk/biosamples/samples/SAMEA115808870).
* I copied the sample metadata (tube id, ToLID, BioSample id, species name) into the BGE-sheet of the metadata template.
* NGI says that the experimental metadata is the same as previous HiFi datasets.
* Created the tsv file [kaMicSqua-hifi.tsv](./data/kaMicSqua-hifi.tsv)

#### HiFi xml
* I copied [submission.xml](./data/submission.xml) from BGE-Crayfish, using the same embargo date

* Running the script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f kaMicSqua-hifi.tsv -p ERGA-BGE -o kaMicSqua-HiFi
    ```
    * The script creates 2 experiments (due to 2 files), but this is wrong, so the 2nd needs to be deleted.

### Programmatic submission HiFi
* Submit both projects and experiment in one go, i.e:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml"  -F "PROJECT=@kaMicSqua-HiFi.study.xml" -F "EXPERIMENT=@kaMicSqua-HiFi.exp.xml" -F "RUN=@kaMicSqua-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```

* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-12-13T08:01:13.952Z" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX13464586" alias="exp_kaMicSqua_HiFi_WGS_FS42549340_pr_144" status="PRIVATE"/>
        <RUN accession="ERR14061583" alias="run_kaMicSqua_HiFi_WGS_FS42549340_pr_144_bam_1" status="PRIVATE"/>
        <RUN accession="ERR14061584" alias="run_kaMicSqua_HiFi_WGS_FS42549340_pr_144_bam_2" status="PRIVATE"/>
        <PROJECT accession="PRJEB83563" alias="erga-bge-kaMicSqua-study-rawdata-2024-12-13" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP167153" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB83564" alias="erga-bge-kaMicSqua1_primary-2024-12-13" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP167154" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA31041443" alias="SUBMISSION-13-12-2024-08:01:12:500"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```

* Update of submission status at [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/)

### Submit HiC
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [kaMicSqua-HiC.tsv](./data/kaMicSqua-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f kaMicSqua-HiC.tsv -p ERGA-BGE -o kaMicSqua-HiC
    ```
* Update kaMicSqua-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB83563"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title, since the other data types have the platform named
* Study will be private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@kaMicSqua-HiC.exp.xml" -F "RUN=@kaMicSqua-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-07-01T14:15:33.198+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14588543" alias="exp_kaMicSqua_Hi-C_FS42549338_HC019-2A1A" status="PRIVATE"/>
        <RUN accession="ERR15183153" alias="run_kaMicSqua_Hi-C_FS42549338_HC019-2A1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA33545416" alias="SUBMISSION-01-07-2025-14:15:32:922"/>
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
* I created [kaMicSqua-RNAseq.tsv](./data/kaMicSqua-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f kaMicSqua-RNAseq.tsv -p ERGA-BGE -o kaMicSqua-RNAseq
    ```
* Update kaMicSqua-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB83563"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@kaMicSqua-RNAseq.exp.xml" -F "RUN=@kaMicSqua-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit assembly
* There is a separate mitochondrial assembly:
    * I FORGOT TO ADD MITO TO A SEPARATE PROJECT!!!
    * I created [kaMicSqua-mito.study.xml](./data/kaMicSqua-mito.study.xml) and submitted it separately
    * Command and Receipt:
        ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@kaMicSqua-mito.study.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"

        <?xml version="1.0" encoding="UTF-8"?>
        <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
        <RECEIPT receiptDate="2025-11-28T09:08:02.998Z" submissionFile="submission.xml" success="true">
            <PROJECT accession="PRJEB104483" alias="erga-bge-kaMicSqua1_mito-2025-11-28" status="PRIVATE" holdUntilDate="2026-03-07Z">
                <EXT_ID accession="ERP185776" type="study"/>
            </PROJECT>
            <SUBMISSION accession="ERA35282209" alias="SUBMISSION-28-11-2025-09:08:02:817"/>
            <MESSAGES>
                <INFO>All objects in this submission are set to private status (HOLD).</INFO>
            </MESSAGES>
            <ACTIONS>ADD</ACTIONS>
            <ACTIONS>HOLD</ACTIONS>
        </RECEIPT>
        ```
    * I then updated the .xml file for the mito assembly to reference the newly created study accession instead of the primary assembly study. Fingers crossed that it works, it was accepted and looks ok in the analysis list... 
        ```
        <STUDY_REF accession="ERP185776">
        <IDENTIFIERS>
            <PRIMARY_ID>ERP185776</PRIMARY_ID>
            <SECONDARY_ID>PRJEB104483</SECONDARY_ID>
        </IDENTIFIERS>
        </STUDY_REF>
        ```
    * I added also this mito assembly to the umbrella:
        * Created [umbrella_modified-mito.xml](./data/umbrella_modified-mito.xml)
        * Submitted:
            ```
            curl -u Username:Password -F "SUBMISSION=@update.xml" -F "PROJECT=@umbrella_modified-mito.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
            ```
        * Receipt:
            ```
            <?xml version="1.0" encoding="UTF-8"?>
            <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
            <RECEIPT receiptDate="2025-11-28T09:21:57.716Z" submissionFile="update.xml" success="true">
                <PROJECT accession="PRJEB91533" alias="erga-bge-kaMicSqua-study-umbrella-2025-07-02" status="PUBLIC"/>
                <SUBMISSION accession="" alias="SUBMISSION-28-11-2025-09:21:57:613"/>
                <MESSAGES>
                    <INFO>The XML md5 checksum for the object being updated has not changed. No update required for PRJEB91533.</INFO>
                </MESSAGES>
                <ACTIONS>MODIFY</ACTIONS>
            </RECEIPT>
            ```
* I created manifest files [kaMicSqua1-manifest.txt](./data/kaMicSqua1-manifest.txt) and [kaMicSqua1-mito-manifest.txt](./data/kaMicSqua1-mito-manifest.txt)
* I created a folder on Uppmax (/proj/snic2022-6-208/nobackup/submission/M-squamiger) and copied & gzipped manifests, assembly file unlocalised_list and chromosome lists there
* Then all files where submitted (first validation then submission) from Pelle on Uppmax using Webin-CLI:

    ```
    interactive -t 08:00:00 -A uppmax2025-2-58
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./kaMicSqua1-manifest.txt -validate
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./kaMicSqua1-mito-manifest.txt -validate
    ```
* Receipt primary:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/M-squamiger/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/M-squamiger/kaMicSqua1_pri_20251126.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/M-squamiger/chromosome_list.txt.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/M-squamiger/unlocalised_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28674135    
    ```
* Receipt mito:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/M-squamiger/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/M-squamiger/kaMicSqua1_mito_20251126.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/M-squamiger/mito-chromosome_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28674132
    ```
* I added the accession number to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `Assembly submitted` to `Yes`, as well as set assembly as status `Submitted` in [Tracking_tool_Seq_centers](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/edit?pli=1&gid=0#gid=0)
* Accessioned:
    ```
    ASSEMBLY_NAME | ASSEMBLY_ACC  | STUDY_ID   | SAMPLE_ID   | CONTIG_ACC                      | SCAFFOLD_ACC | CHROMOSOME_ACC
    kaMicSqua1.1  | GCA_977109195 | PRJEB83564 | ERS20534881 | CDSAWO010000001-CDSAWO010000098 |              | OZ372786-OZ372795
    ```
* NOTE: Mito assembly processing failed, I don't know if it has to do that I forgot to create a separate project for it before submission. I will wait and see if it gets accession numbers, if not I will contact ENA support.
* Release studies and check that they are shown under umbrella **TODO** (when I know that mito assembly worked)

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
    <RECEIPT receiptDate="2025-11-28T08:08:34.184Z" submissionFile="update.xml" success="true">
        <PROJECT accession="PRJEB91533" alias="erga-bge-kaMicSqua-study-umbrella-2025-07-02" status="PUBLIC"/>
        <SUBMISSION accession="" alias="SUBMISSION-28-11-2025-08:08:34:007"/>
        <MESSAGES/>
        <ACTIONS>MODIFY</ACTIONS>
    </RECEIPT>
    ```

### Umbrella project
* For each of the BGE species, an **umbrella** project has to be created and linked to the main BGE project, [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

1. Release the child project via browser
1. Collect scientific name and tolId from the metadata template sheet
1. Go to [ENA browser](https://www.ebi.ac.uk/ena/browser/home) and enter the scientific name as search term
    1. To the left side, there should be a **Taxon** subheading, that gives the identifier
1. Copy experiment accession number from metadata in top of this README
* There is a CNAG script, that should do the deed of creating the xml file:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Microcosmus squamiger" -t kaMicSqua -p ERGA-BGE -c SCILIFELAB -a PRJEB83563 -x 439822
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
    <RECEIPT receiptDate="2025-07-02T08:12:19.938+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB91533" alias="erga-bge-kaMicSqua-study-umbrella-2025-07-02" status="PRIVATE" holdUntilDate="2025-07-04+01:00"/>
        <SUBMISSION accession="ERA33548724" alias="SUBMISSION-02-07-2025-08:12:19:640"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>    
    ```
