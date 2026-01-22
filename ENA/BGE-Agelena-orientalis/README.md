---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB96485 (umbrella), PRJEB90605 (experiment), PRJEB90606 (assembly)
---

# BGE - *Agelena orientalis*

## Submission task description
Submission of raw reads for *Agelena orientalis* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.

## Procedure overview and links to examples

* [ERGA-BGE_ReadData_Submission_Guide](https://github.com/ERGA-consortium/ERGA-submission/blob/main/BGE/ERGA-BGE_ReadData_Submission_Guide.md)
* [BGE mRupRup umbrella project](https://www.ncbi.nlm.nih.gov/bioproject/1084634)

## Lessons learned
* How to change sample associated with an experiment after submission: use the browser to update both `SAMPLE_DESCRIPTOR` and `PRIMARY_ID` for the experiment(s) concerned.

## Detailed step by step description

### Submit HiFi

#### Preparations
* There are 2 bam files, need to make sure that the script produces the right output

#### XML
* I created [qqAgeOrie-HiFi.tsv](./data/qqAgeOrie-HiFi.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qqAgeOrie-HiFi.tsv -p ERGA-BGE -o qqAgeOrie-HiFi
    ```
    * Had to remove 1 experiment
* The study XML also needs to be submitted
* Submission.xml with hold date is used.
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission-hold.xml" -F "PROJECT=@qqAgeOrie-HiFi.study.xml" -F "EXPERIMENT=@qqAgeOrie-HiFi.exp.xml" -F "RUN=@qqAgeOrie-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-18T15:36:00.119+01:00" submissionFile="submission-hold.xml" success="true">
        <EXPERIMENT accession="ERX14538033" alias="exp_qqAgeOrie_HiFi_WGS_LV6000912393_pr_188" status="PRIVATE"/>
        <RUN accession="ERR15132793" alias="run_qqAgeOrie_HiFi_WGS_LV6000912393_pr_188_bam_1" status="PRIVATE"/>
        <RUN accession="ERR15132794" alias="run_qqAgeOrie_HiFi_WGS_LV6000912393_pr_188_bam_2" status="PRIVATE"/>
        <PROJECT accession="PRJEB90605" alias="erga-bge-qqAgeOrie-study-rawdata-2025-06-18" status="PRIVATE" holdUntilDate="2026-09-09+01:00">
            <EXT_ID accession="ERP173607" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB90606" alias="erga-bge-qqAgeOrie5_primary-2025-06-18" status="PRIVATE" holdUntilDate="2026-09-09+01:00">
            <EXT_ID accession="ERP173608" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA33332387" alias="SUBMISSION-18-06-2025-15:35:59:719"/>
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
* I received sample ID from [NGI](https://docs.google.com/spreadsheets/d/15kfYnhsCpNLNrYagwWZTcVBh9CSN-Ww1/), which I checked in the [ERGA tracking portal](https://genomes.cnag.cat/erga-stream/samples/) which returned biosample [SAMEA116289655](https://www.ebi.ac.uk/biosamples/samples/SAMEA116289655).

* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [qqAgeOrie-HiC.tsv](./data/qqAgeOrie-HiC.tsv)
* There are 2 libraries, need to make sure the .xml files are correct
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qqAgeOrie-HiC.tsv -p ERGA-BGE -o qqAgeOrie-HiC
    ```
* Update qqAgeOrie-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90605"/>
    ```

* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title, since the other data types have the platform named
* Study is public, so submission-noHold.xml is used.
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission-noHold.xml"  -F "EXPERIMENT=@qqAgeOrie-HiC.exp.xml" -F "RUN=@qqAgeOrie-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-09-25T10:06:48.825+01:00" submissionFile="submission-noHold.xml" success="true">
        <EXPERIMENT accession="ERX15053483" alias="exp_qqAgeOrie_Hi-C_LV6000912415_HC030-6A1B" status="PRIVATE"/>
        <EXPERIMENT accession="ERX15053484" alias="exp_qqAgeOrie_Hi-C_LV6000912415_HC030-6A2B" status="PRIVATE"/>
        <RUN accession="ERR15648920" alias="run_qqAgeOrie_Hi-C_LV6000912415_HC030-6A1B_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR15648921" alias="run_qqAgeOrie_Hi-C_LV6000912415_HC030-6A2B_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA35017347" alias="SUBMISSION-25-09-2025-10:06:48:448"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    </RECEIPT>
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)
* We received information that the sample associated with the HiC data was wrong, so I had to update the sample from SAMEA116289655 / ERS21333597 to SAMEA116289650 / ERS21333592.
    * This was done in the browser, updating both `SAMPLE_DESCRIPTOR` and `PRIMARY_ID` for the 2 experiments.

#### Additional HiC
* 2 more libraries were sequenced. Tube labels made it possible to identify biosample, and sequences were transferred to ENA in batch using lftp.
* I created [qqAgeOrie-2-HiC.tsv](./data/qqAgeOrie-2-HiC.tsv)
* There are 2 libraries, need to make sure the .xml files are correct
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qqAgeOrie-2-HiC.tsv -p ERGA-BGE -o qqAgeOrie-2-HiC
    ```
* Update qqAgeOrie-2-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90605"/>
    ```

* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title, since the other data types have the platform named
* Study is public, so submission-noHold.xml is used.
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission-noHold.xml"  -F "EXPERIMENT=@qqAgeOrie-2-HiC.exp.xml" -F "RUN=@qqAgeOrie-2-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-10-23T08:42:22.182+01:00" submissionFile="submission-noHold.xml" success="true">
        <EXPERIMENT accession="ERX15162329" alias="exp_qqAgeOrie_Hi-C_LV6000912424_HC030-7A1A-CL" status="PRIVATE"/>
        <EXPERIMENT accession="ERX15162330" alias="exp_qqAgeOrie_Hi-C_LV6000912424_HC030-7A2A" status="PRIVATE"/>
        <RUN accession="ERR15757805" alias="run_qqAgeOrie_Hi-C_LV6000912424_HC030-7A1A-CL_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR15757806" alias="run_qqAgeOrie_Hi-C_LV6000912424_HC030-7A2A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA35072606" alias="SUBMISSION-23-10-2025-08:42:21:866"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    </RECEIPT>
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)
### Submit RNAseq - **TODO**

#### Preparations

#### XML
* I created [qqAgeOrie-RNAseq.tsv](./data/qqAgeOrie-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qqAgeOrie-RNAseq.tsv -p ERGA-BGE -o qqAgeOrie-RNAseq
    ```
* Update qqAgeOrie-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90605"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission-hold.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission-hold.xml" -F "EXPERIMENT=@qqAgeOrie-RNAseq.exp.xml" -F "RUN=@qqAgeOrie-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit assembly

* I created a manifest file [qqAgeOrie5-manifest.txt](./data/qqAgeOrie5-manifest.txt)
* I created a folder on Uppmax (/proj/snic2022-6-208/nobackup/submission/A-orientalis) and copied & gzipped manifest, assembly file and chromosome list there
* Then all files where submitted (first validation then submission) from Pelle on Uppmax using Webin-CLI:

    ```
    interactive -t 08:00:00 -A uppmax2025-2-58
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./qqAgeOrie5-manifest.txt -validate
    ```
* Receipt:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/A-orientalis/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/A-orientalis/qqAgeOrie5_pri.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/A-orientalis/chromosome_list.txt.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/A-orientalis/unlocalised_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28786776
    ```
* I added the accession number to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `Assembly submitted` to `Yes`, as well as set assembly as status `Submitted` in [Tracking_tool_Seq_centers](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/edit?pli=1&gid=0#gid=0)
* Accessioned:
    ```
    ASSEMBLY_NAME | ASSEMBLY_ACC  | STUDY_ID   | SAMPLE_ID   | CONTIG_ACC                      | SCAFFOLD_ACC | CHROMOSOME_ACC
    qqAgeOrie5.1  | GCA_978045235 | PRJEB90606 | ERS21333585 | CDXHCA010000001-CDXHCA010000123 |              | OZ405000-OZ405022
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
    <RECEIPT receiptDate="2026-01-21T08:46:32.504Z" submissionFile="update.xml" success="true">
        <PROJECT accession="PRJEB96485" alias="erga-bge-qqAgeOrie-study-umbrella-2025-08-27" status="PUBLIC"/>
        <SUBMISSION accession="" alias="SUBMISSION-21-01-2026-08:46:32:339"/>
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
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Agelena orientalis" -t qqAgeOrie5 -p ERGA-BGE -c SCILIFELAB -a PRJEB90605 -x 293813
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
    <RECEIPT receiptDate="2025-08-27T09:07:04.879+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB96485" alias="erga-bge-qqAgeOrie-study-umbrella-2025-08-27" status="PRIVATE" holdUntilDate="2027-08-27+01:00"/>
        <SUBMISSION accession="ERA34838274" alias="SUBMISSION-27-08-2025-09:07:04:617"/>
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
    <RECEIPT receiptDate="2025-08-27T09:17:54.714+01:00" submissionFile="submission-release-project.xml" success="true">
        <MESSAGES>
            <INFO>project accession "PRJEB96485" is set to public status.</INFO>
        </MESSAGES>
        <ACTIONS>RELEASE</ACTIONS>
    </RECEIPT>    
    ```
