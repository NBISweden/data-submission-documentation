---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB96500 (umbrella), PRJEB91089 (experiment), PRJEB91090 (assembly), PRJEB110036 (haploid), PRJEB110037 (mito)
---

# BGE - *Scarites abbreviatus*

## Submission task description
Submission of raw reads for *Scarites abbreviatus* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Scarites-abbreviatus-metadata.xlsx)
* [BGE HiFi metadata](./data/icScaAbbr-HiFi.tsv)
* [BGE HiC metadata](./data/icScaAbbr-HiC.tsv)
* [BGE RNAseq metadata](./data/icScaAbbr-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiFi
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput *.bam` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.
#### XML
* I created [icScaAbbr-HiFi.tsv](./data/icScaAbbr-HiFi.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icScaAbbr-HiFi.tsv -p ERGA-BGE -o icScaAbbr-HiFi
    ```

* Study is private, so submission.xml with hold date is used.

* Submit both projects and experiment in one go, i.e:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@icScaAbbr-HiFi.study.xml" -F "EXPERIMENT=@icScaAbbr-HiFi.exp.xml" -F "RUN=@icScaAbbr-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-26T08:59:17.227+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14565496" alias="exp_icScaAbbr_HiFi_WGS_LV6000905036_pr_255_001" status="PRIVATE"/>
        <RUN accession="ERR15159844" alias="run_icScaAbbr_HiFi_WGS_LV6000905036_pr_255_001_bam_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB91089" alias="erga-bge-icScaAbbr-study-rawdata-2025-06-26" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP174081" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB91090" alias="erga-bge-icScaAbbr5_primary-2025-06-26" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP174082" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA33523486" alias="SUBMISSION-26-06-2025-08:59:16:801"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>    
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)
    * **Note:** Status in Tracking sheet is 'TopUp', if valid it means that more material is needed

### Submit HiC
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [icScaAbbr-HiC.tsv](./data/icScaAbbr-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icScaAbbr-HiC.tsv -p ERGA-BGE -o icScaAbbr-HiC
    ```
* Update icScaAbbr-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB91089"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title, since the other data types have the platform named
* Study is public, so submission-noHold.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission-noHold.xml" -F "EXPERIMENT=@icScaAbbr-HiC.exp.xml" -F "RUN=@icScaAbbr-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-09-25T14:09:47.036+01:00" submissionFile="submission-noHold.xml" success="true">
        <EXPERIMENT accession="ERX15056356" alias="exp_icScaAbbr_Hi-C_LV6000905035_HC054-1A1A" status="PRIVATE"/>
        <RUN accession="ERR15651793" alias="run_icScaAbbr_Hi-C_LV6000905035_HC054-1A1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA35019374" alias="SUBMISSION-25-09-2025-14:09:46:598"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    </RECEIPT>
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit RNAseq
* See [README RNAseq submission](../BGE-RNAseq-2026-02-27/README.md)

### Submit assembly
* For this species there was 2 haploid assemblies as well as a mito assembly. Hence I needed to create 2 additional projects:
    * I created [icScaAbbr-assembly-studies.xml](./data/icScaAbbr-assembly-studies.xml) and submitted via curl:
        ```
        curl -u username:password -F "SUBMISSION=@submission.xml"  -F "PROJECT=@icScaAbbr-assembly-studies.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
        ```
    * Receipt:
        ```
        <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
        <RECEIPT receiptDate="2026-03-13T09:32:47.051Z" submissionFile="submission.xml" success="true">
            <PROJECT accession="PRJEB110036" alias="erga-bge-icScaAbbr5_haplo-2026-03-13" status="PRIVATE" holdUntilDate="2026-03-07Z">
                <EXT_ID accession="ERP190761" type="study"/>
            </PROJECT>
            <PROJECT accession="PRJEB110037" alias="erga-bge-icScaAbbr5_mito-2026-03-13" status="PRIVATE" holdUntilDate="2026-03-07Z">
                <EXT_ID accession="ERP190762" type="study"/>
            </PROJECT>
            <SUBMISSION accession="ERA36000231" alias="SUBMISSION-13-03-2026-09:32:46:955"/>
            <MESSAGES>
                <INFO>All objects in this submission are set to private status (HOLD).</INFO>
            </MESSAGES>
            <ACTIONS>ADD</ACTIONS>
            <ACTIONS>HOLD</ACTIONS>
        </RECEIPT>
        ```
* I created 3 manifest files [icScaAbbr5-manifest.txt](./data/icScaAbbr5-manifest.txt)
* I created a folder on Uppmax (/proj/snic2022-6-208/nobackup/submission/S-abbreviatus) and copied & gzipped manifest, assembly file and chromosome list there
* Then all files where submitted (first validation then submission) from Pelle on Uppmax using Webin-CLI:

    ```
    interactive -t 08:00:00 -A uppmax2025-2-58
    java -jar ~/webin-cli-9.0.1.jar -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./icScaAbbr5-hap1-manifest.txt -validate
    java -jar ~/webin-cli-9.0.1.jar -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./icScaAbbr5-hap2-manifest.txt -validate
    java -jar ~/webin-cli-9.0.1.jar -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./icScaAbbr5-mito-manifest.txt -validate    
    ```
* Receipt hap1:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/S-abbreviatus/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/S-abbreviatus/icScaAbbr5_curated_20260216.hap1.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/S-abbreviatus/hap1-chromosome_list.txt.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/S-abbreviatus/hap1-unlocalised_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ29236969
    ```
* Receipt hap2:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/S-abbreviatus/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/S-abbreviatus/icScaAbbr5_curated_20260216.hap2.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/S-abbreviatus/hap2-chromosome_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ29236970
    ```
* Receipt mito:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/S-abbreviatus/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/S-abbreviatus/icScaAbbr5_mito_20251022.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/S-abbreviatus/mito-chromosome_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ29236971
    ```

* I added the accession number to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `Assembly submitted` to `Yes`, as well as set assembly as status `Submitted` in [Tracking_tool_Seq_centers](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/edit?pli=1&gid=0#gid=0)
* Accessioned:
    ```
    ASSEMBLY_NAME | ASSEMBLY_ACC  | STUDY_ID   | SAMPLE_ID   | CONTIG_ACC                      | SCAFFOLD_ACC | CHROMOSOME_ACC

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
    <RECEIPT receiptDate="2026-03-13T10:26:44.932Z" submissionFile="update.xml" success="true">
        <PROJECT accession="PRJEB96500" alias="erga-bge-icScaAbbr-study-umbrella-2025-08-27" status="PUBLIC"/>
        <SUBMISSION accession="" alias="SUBMISSION-13-03-2026-10:26:44:619"/>
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
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Scarites abbreviatus" -t icScaAbbr5 -p ERGA-BGE -c SCILIFELAB -a PRJEB91089 -x 3349997
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
    <RECEIPT receiptDate="2025-08-27T11:46:10.586+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB96500" alias="erga-bge-icScaAbbr-study-umbrella-2025-08-27" status="PRIVATE" holdUntilDate="2027-08-27+01:00"/>
        <SUBMISSION accession="ERA34838339" alias="SUBMISSION-27-08-2025-11:46:10:419"/>
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
    <RECEIPT receiptDate="2025-08-27T11:46:46.463+01:00" submissionFile="submission-release-project.xml" success="true">
        <MESSAGES>
            <INFO>project accession "PRJEB96500" is set to public status.</INFO>
        </MESSAGES>
        <ACTIONS>RELEASE</ACTIONS>
    </RECEIPT>    
    ```

* **Note:** Add the assembly project `` when it has been submitted and made public, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.
