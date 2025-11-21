---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB91438 (umbrella), PRJEB91102 (experiment), PRJEB91103 (assembly)
---

# BGE - *Cryptotrichosporon brontae*

## Submission task description
Submission of raw reads for *Cryptotrichosporon brontae* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.

## Procedure overview and links to examples

* [ERGA-BGE_ReadData_Submission_Guide](https://github.com/ERGA-consortium/ERGA-submission/blob/main/BGE/ERGA-BGE_ReadData_Submission_Guide.md)
* [BGE mRupRup umbrella project](https://www.ncbi.nlm.nih.gov/bioproject/1084634)

## Lessons learned

## Detailed step by step description

### Submit HiFi

#### Preparations
* 2 samples were used hence a virtual sample had to be registered:
    * Biosamples were deduced given the 'tube or well id's' received from UGC (via slack) and looked up in the ERGA tracking portal: SAMEA115344702, SAMEA115344703
    * I registered the sample via browser, uploading [gfCryBron-HiFi-virtual-sample.tsv](./data/gfCryBron-HiFi-virtual-sample.tsv)
    * Accession number received: `ERS24610775`
* Note: Ultra-low DNA input protocol has been used, and for those it is the trimmed reads that has to be submitted, not the original .bam file

#### XML
* I created [gfCryBron-HiFi.tsv](./data/gfCryBron-HiFi.tsv), and added `.bam` to file name
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f gfCryBron-HiFi.tsv -p ERGA-BGE -o gfCryBron-HiFi
    ```
    * Edit run .xml and change to `fastq` (2 rows)
* The study XML also needs to be submitted
* Submission.xml with hold date is used.
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission-hold.xml" -F "PROJECT=@gfCryBron-HiFi.study.xml" -F "EXPERIMENT=@gfCryBron-HiFi.exp.xml" -F "RUN=@gfCryBron-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-26T11:38:04.032+01:00" submissionFile="submission-hold.xml" success="true">
        <EXPERIMENT accession="ERX14566145" alias="exp_gfCryBron_HiFi_WGS_DSM_104551_14-DSM_104551_15_pr_159" status="PRIVATE"/>
        <RUN accession="ERR15160492" alias="run_gfCryBron_HiFi_WGS_DSM_104551_14-DSM_104551_15_pr_159_fastq_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB91102" alias="erga-bge-gfCryBron-study-rawdata-2025-06-26" status="PRIVATE" holdUntilDate="2026-09-09+01:00">
            <EXT_ID accession="ERP174093" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB91103" alias="erga-bge-gfCryBron1_primary-2025-06-26" status="PRIVATE" holdUntilDate="2026-09-09+01:00">
            <EXT_ID accession="ERP174094" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA33523696" alias="SUBMISSION-26-06-2025-11:38:03:685"/>
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
* I received sample ID from [NGI](https://docs.google.com/spreadsheets/d/1z22KvtncVnJI-53qq-we5J6kC6ytuX9g/), which I checked in the [ERGA tracking portal](https://genomes.cnag.cat/erga-stream/samples/) which returned biosample [SAMEA116283198](https://www.ebi.ac.uk/biosamples/samples/SAMEA116283198).

* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [gfCryBron-HiC.tsv](./data/gfCryBron-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f gfCryBron-HiC.tsv -p ERGA-BGE -o gfCryBron-HiC
    ```
* Update gfCryBron-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB91102"/>
    ```

* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title, since the other data types have the platform named
* Study is private, so submission-hold.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission-hold.xml"  -F "EXPERIMENT=@gfCryBron-HiC.exp.xml" -F "RUN=@gfCryBron-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-27T08:34:23.426+01:00" submissionFile="submission-hold.xml" success="true">
        <EXPERIMENT accession="ERX14570414" alias="exp_gfCryBron_Hi-C_DSM_104551_17_HC015-1A1A" status="PRIVATE"/>
        <RUN accession="ERR15164691" alias="run_gfCryBron_Hi-C_DSM_104551_17_HC015-1A1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA33527091" alias="SUBMISSION-27-06-2025-08:34:23:089"/>
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
* I created [gfCryBron-RNAseq.tsv](./data/gfCryBron-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f gfCryBron-RNAseq.tsv -p ERGA-BGE -o gfCryBron-RNAseq
    ```
* Update gfCryBron-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB91102"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission-hold.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission-hold.xml" -F "EXPERIMENT=@gfCryBron-RNAseq.exp.xml" -F "RUN=@gfCryBron-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit assembly

* I created a manifest file [gfCryBron1-manifest.txt](./data/gfCryBron1-manifest.txt)
* I created a folder on Uppmax (/proj/snic2022-6-208/nobackup/submission/C-brontae) and copied & gzipped manifest, assembly file and chromosome list there
* Then all files where submitted (first validation then submission) from Pelle on Uppmax using Webin-CLI:

    ```
    interactive -t 08:00:00 -A uppmax2025-2-58
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./gfCryBron1-manifest.txt -validate
    ```
* Receipt:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/C-brontae/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/C-brontae/gfCryBron.1.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/C-brontae/chromosome_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28668755
    ```
* I added the accession number to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `Assembly submitted` to `Yes`, as well as set assembly as status `Submitted` in [Tracking_tool_Seq_centers](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/edit?pli=1&gid=0#gid=0)
* Accessioned:
    ```
    ASSEMBLY_NAME | ASSEMBLY_ACC  | STUDY_ID   | SAMPLE_ID   | CONTIG_ACC                      | SCAFFOLD_ACC | CHROMOSOME_ACC
    gfCryBron1.1  | GCA_977066725 | PRJEB91103 | ERS24610775 | CDRURE010000001-CDRURE010000004 |              | OZ370660-OZ370672
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
    <RECEIPT receiptDate="2025-11-19T13:38:26.773Z" submissionFile="update.xml" success="true">
        <PROJECT accession="PRJEB91438" alias="erga-bge-gfCryBron-study-umbrella-2025-07-01" status="PUBLIC"/>
        <SUBMISSION accession="" alias="SUBMISSION-19-11-2025-13:38:26:646"/>
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
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Cryptotrichosporon brontae" -t gfCryBron -p ERGA-BGE -c SCILIFELAB -a PRJEB91102 -x 1890680
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
    <RECEIPT receiptDate="2025-07-01T13:11:54.719+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB91438" alias="erga-bge-gfCryBron-study-umbrella-2025-07-01" status="PRIVATE" holdUntilDate="2025-07-03+01:00"/>
        <SUBMISSION accession="ERA33545342" alias="SUBMISSION-01-07-2025-13:11:54:538"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>    
