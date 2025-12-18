---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: 
---

# BGE - batch10 CNAG

## Submission task description
Submission of HiC data for a handful of species, to be added to existing projects created by another node.
* Agrilus gianassoi
* Brachydesmus stygivagus
* Eumannia arenbergeri
* Maniola cypricola
* Troglophilus ovuliformis
* Chaetopelma olivaceum
* Mesochaetopterus rogeri (2 libraries)

## Procedure overview and links to examples

* [Metadata template](./data/BGE-batch10-CNAG-metadata.xlsx)
* [BGE HiC metadata](./data/batch10-CNAG-HiC.tsv)


## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiC
#### Preparations
* Sample IDs given in the [metadata template from NGI](https://docs.google.com/spreadsheets/d/1_z1vymhI-dxpIJUFkKlZQNjGUmRYTJ4C) gave BioSample IDs via ERGA tracker portal. For M rogeri, the metadata is found in [another delivery's template](https://docs.google.com/spreadsheets/d/1BKR3odQjKmh3YP6DGzbkCe2s_aRh6Trf/)
* The data files were transferred together with other species received in this batch, from /proj/snic2022-6-208/INBOX/BGE_HiC_20251022/DataDelivery_2025-10-22_13-24-11_snpseq01422_download/files/YH-4400/20251003_LH00179_0370_A233NMNLT4, and (for M rogeri) /proj/snic2022-6-208/INBOX/BGE_HiC_20251119/DataDelivery_2025-11-19_10-12-11_snpseq01469_download/files/YJ-4442/20251030_LH00179_0385_A237T2CLT4/, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.
* For M rogeri, there is an issue with which project to attach to, there are 2 projects: PRJEB96374
 and PRJEB77795. I chose PRJEB96374 since it is the one with the existing HiFi data from Oslo, but on the other hand the other project has an umbrella with assembly submitted. I think that that assembly failed, was sent to Oslo (in WP 7.2, i.e. a continuation after all sequencing was supposed to have been done), then oslo sent us sample for the HiC. Might be wrong but it is the working theory I used as basis for my decision.

#### XML
* I created [batch10-CNAG-HiC-1.tsv](./data/batch10-CNAG-HiC-1.tsv), but not including Agrilus gianassoi, Eumannia arenbergeri and Maniola cypricola, since I could not find any public ENA project for them to link to. CNAG will create projects for these species, and then I can submit them (prepared in [batch10-CNAG-HiC-2.tsv](./data/batch10-CNAG-HiC-2.tsv)).
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f batch10-CNAG-HiC-1.tsv -p ERGA-BGE -o batch10-CNAG-HiC-1
    ```
* Update batch10-CNAG-HiC-1.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB96037"/> - Brachydesmus stygivagus, HC061-1A1A-CL
    <STUDY_REF accession="PRJEB96082"/> - Troglophilus ovuliformis, HC064-1A1A
    <STUDY_REF accession="PRJEB89645"/> - Chaetopelma olivaceum, HC065-1A1A
    <STUDY_REF accession="PRJEB96374"/> - Mesochaetopterus rogeri, HC059-4A4-NI-CL
   <STUDY_REF accession="PRJEB96374"/> - Mesochaetopterus rogeri, HC059-5A-NI-CL
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library names and titles, since the other data types have the platform named
* Study is public, so submission.xml without hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@batch10-CNAG-HiC-1.exp.xml" -F "RUN=@batch10-CNAG-HiC-1.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-12-17T14:58:53.313Z" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX15430109" alias="exp_qdBraStyg_Hi-C_LV6000914154_HC061-1A1A-CL" status="PRIVATE"/>
        <EXPERIMENT accession="ERX15430110" alias="exp_iqTroOvul_Hi-C_ERGA_NT_0292_00001_HC064-1A1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX15430111" alias="exp_qqChaOliv_Hi-C_ERGA_AP_4894_00294_HC065-1A1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX15430112" alias="exp_wdMesRoge_Hi-C_ERGA_DM_7384_04_HC059-4A4-NI-CL" status="PRIVATE"/>
        <EXPERIMENT accession="ERX15430113" alias="exp_wdMesRoge_Hi-C_ERGA_DM_7384_03_HC059-5A-NI-CL" status="PRIVATE"/>
        <RUN accession="ERR16039416" alias="run_qdBraStyg_Hi-C_LV6000914154_HC061-1A1A-CL_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16039417" alias="run_iqTroOvul_Hi-C_ERGA_NT_0292_00001_HC064-1A1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16039418" alias="run_qqChaOliv_Hi-C_ERGA_AP_4894_00294_HC065-1A1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16039419" alias="run_wdMesRoge_Hi-C_ERGA_DM_7384_04_HC059-4A4-NI-CL_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16039420" alias="run_wdMesRoge_Hi-C_ERGA_DM_7384_03_HC059-5A-NI-CL_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA35407969" alias="SUBMISSION-17-12-2025-14:58:52:895"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    </RECEIPT>
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

* One of the files had wrong checksum, `wdMesRoge_YJ-4442-HC059-5A-NI-CL_S817_L008_R1_001.fastq.gz`, which is really weird since I see the correct checksum in .xlsx and tsv file, but not in the run file... Anyway, I changed it in run xml file, and updated the checksum via the browser.

### Submit RNAseq - **TODO** (perhaps)
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [batch10-CNAG-RNAseq.tsv](./data/batch10-CNAG-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f batch10-CNAG-RNAseq.tsv -p ERGA-BGE -o batch10-CNAG-RNAseq
    ```
* Update batch10-CNAG-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB96037"/> - Brachydesmus stygivagus, HC061-1A1A-CL
    <STUDY_REF accession="PRJEB96082"/> - Troglophilus ovuliformis, HC064-1A1A
    <STUDY_REF accession="PRJEB89645"/> - Chaetopelma olivaceum, HC065-1A1A
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library names and titles, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@batch10-CNAG-RNAseq.exp.xml" -F "RUN=@batch10-CNAG-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)
