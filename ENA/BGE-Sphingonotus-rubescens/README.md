---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB91541 (umbrella), PRJEB90653 (experiment), PRJEB90654 (assembly), PRJEB101048 (haplo), PRJEB101047 (mito)
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

### Submit assembly
* There are 2 haploids and 1 mito assembly to submit. Hence, need 2 more projects:
    * I created [iqSphRube1-assembly-studies.xml](./data/iqSphRube1-assembly-studies.xml) and submitted using curl:
        ```
        curl -u username:password -F "SUBMISSION=@submission.xml"  -F "PROJECT=@iqSphRube-assembly-studies.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
        ```
        * Receipt:
        ```
        <?xml version="1.0" encoding="UTF-8"?>
        <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
        <RECEIPT receiptDate="2025-10-20T09:11:39.447+01:00" submissionFile="submission.xml" success="true">
            <PROJECT accession="PRJEB101047" alias="erga-bge-iqSphRube1_mito-2025-10-20" status="PRIVATE" holdUntilDate="2026-03-07Z">
                <EXT_ID accession="ERP182474" type="study"/>
            </PROJECT>
            <PROJECT accession="PRJEB101048" alias="erga-bge-iqSphRube1_haplo-2025-10-20" status="PRIVATE" holdUntilDate="2026-03-07Z">
                <EXT_ID accession="ERP182475" type="study"/>
            </PROJECT>
            <SUBMISSION accession="ERA35065957" alias="SUBMISSION-20-10-2025-09:11:39:341"/>
            <MESSAGES>
                <INFO>All objects in this submission are set to private status (HOLD).</INFO>
            </MESSAGES>
            <ACTIONS>ADD</ACTIONS>
            <ACTIONS>HOLD</ACTIONS>
        </RECEIPT>
        ```
    
* I created 3 manifest files [iqSphRube1-hap1-manifest.txt](./data/iqSphRube1-hap1-manifest.txt), [iqSphRube1-hap2-manifest.txt](./data/iqSphRube1-hap2-manifest.txt), and [iqSphRube1-mito-manifest.txt](./data/iqSphRube1-mito-manifest.txt)
* I also created 3 chromosome_lists: [chromosome_list_hap1.txt](./data/chromosome_list_hap1.txt), [chromosome_list_hap2.txt](./data/chromosome_list_hap2.txt), [chromosome_list_mito.txt](./data/chromosome_list_mito.txt)
* The haploids also has unlocalised lists: [unlocalised_list_hap1.txt](./data/unlocalised_list_hap1.txt) and [unlocalised_list_hap2.txt](./data/unlocalised_list_hap2.txt)
* I created a folder on Uppmax (/proj/snic2022-6-208/nobackup/submission/S-rubescens/) and copied & gzipped manifests, assembly files, chromosome and unlocalised lists there
* Then all files where submitted (first validation then submission) from Pelle on Uppmax using Webin-CLI:

    ```
    interactive -t 08:00:00 -A uppmax2025-2-58
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./iqSphRube1-hap1-manifest.txt -validate
    ```
* Receipt hap1:
    ```
    INFO : Your application version is 9.0.1
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/S-rubescens/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/S-rubescens/iqSphRube1_hap1_20250930.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/S-rubescens/chromosome_list_hap1.txt.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/S-rubescens/unlocalised_list_hap1.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28546098
    ```
* Receipt hap2:
    ```
    INFO : Your application version is 9.0.1
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/S-rubescens/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/S-rubescens/iqSphRube1_hap2_20250930.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/S-rubescens/chromosome_list_hap2.txt.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/S-rubescens/unlocalised_list_hap2.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28546099
    ```
* Receipt mito:
    ```
    INFO : Your application version is 9.0.1
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/S-rubescens/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/S-rubescens/iqSphRube1_mito_20250930.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/S-rubescens/chromosome_list_mito.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28546100
    ```
* I added the accession numbers to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `Assembly submitted` to `Yes`, as well as set assembly as status `Submitted` in [Tracking_tool_Seq_centers](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/edit?pli=1&gid=0#gid=0)

* Accessioned:
    ```
    ASSEMBLY_NAME | ASSEMBLY_ACC  | STUDY_ID   | SAMPLE_ID   | CONTIG_ACC                      | SCAFFOLD_ACC | CHROMOSOME_ACC

    ```
* Release studies and check that they are shown under umbrella

#### Add assemblies to umbrella
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
    <RECEIPT receiptDate="2025-10-20T13:48:25.725+01:00" submissionFile="update.xml" success="true">
        <PROJECT accession="PRJEB91541" alias="erga-bge-iqSphRube-study-umbrella-2025-07-02" status="PUBLIC"/>
        <SUBMISSION accession="" alias="SUBMISSION-20-10-2025-13:48:25:387"/>
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
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Sphingonotus rubescens" -t iqSphRube -p ERGA-BGE -c SCILIFELAB -a PRJEB90653 -x 499837
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
    <RECEIPT receiptDate="2025-07-02T09:23:21.237+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB91541" alias="erga-bge-iqSphRube-study-umbrella-2025-07-02" status="PRIVATE" holdUntilDate="2025-07-04+01:00"/>
        <SUBMISSION accession="ERA33548826" alias="SUBMISSION-02-07-2025-09:23:21:049"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>    
    ```
