---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB96372 (umbrella), PRJEB91079 (experiment), PRJEB91080 (assembly)
---

# BGE - *Megachile posti*

## Submission task description
Submission of raw reads for *Megachile posti* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Megachile-posti-metadata.xlsx)
* [BGE HiFi metadata](./data/iyMegPost-HiFi.tsv)
* [BGE HiC metadata](./data/iyMegPost-HiC.tsv)
* [BGE RNAseq metadata](./data/iyMegPost-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiFi
#### Preparations
* 2 sample ID's -> virtual sample needed
    * I created [iyMegPost-HiFi-virtual-sample.tsv](./data/iyMegPost-HiFi-virtual-sample.tsv) and registered the sample
    * Accession number received: `ERS25084907` 
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput *.bam` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.
#### XML
* I created [iyMegPost-HiFi.tsv](./data/iyMegPost-HiFi.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iyMegPost-HiFi.tsv -p ERGA-BGE -o iyMegPost-HiFi
    ```

* Study is private, so submission.xml with hold date is used.

* Submit both projects and experiment in one go, i.e:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@iyMegPost-HiFi.study.xml" -F "EXPERIMENT=@iyMegPost-HiFi.exp.xml" -F "RUN=@iyMegPost-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-26T08:37:44.282+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14565488" alias="exp_iyMegPost_HiFi_WGS_LV6000912629_LV6000912621_pr_253_001" status="PRIVATE"/>
        <RUN accession="ERR15159836" alias="run_iyMegPost_HiFi_WGS_LV6000912629_LV6000912621_pr_253_001_bam_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB91079" alias="erga-bge-iyMegPost-study-rawdata-2025-06-26" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP174075" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB91080" alias="erga-bge-iyMegPost4_primary-2025-06-26" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP174076" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA33523440" alias="SUBMISSION-26-06-2025-08:37:43:912"/>
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
* I created [iyMegPost-HiC.tsv](./data/iyMegPost-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iyMegPost-HiC.tsv -p ERGA-BGE -o iyMegPost-HiC
    ```
* Update iyMegPost-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB91079"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study will be private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@iyMegPost-HiC.exp.xml" -F "RUN=@iyMegPost-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <RECEIPT receiptDate="2025-08-25T13:55:47.692+01:00" submissionFile="submission.xml" success="true">
     <EXPERIMENT accession="ERX14869356" alias="exp_iyMegPost_Hi-C_LV6000912653_HC046-1A1A" status="PRIVATE"/>
     <RUN accession="ERR15465461" alias="run_iyMegPost_Hi-C_LV6000912653_HC046-1A1A_fastq_1" status="PRIVATE"/>
     <SUBMISSION accession="ERA34672664" alias="SUBMISSION-25-08-2025-13:55:47:561"/>
     <MESSAGES>
          <INFO>All objects in this submission are set to private status (HOLD).</INFO>
     </MESSAGES>
     <ACTIONS>ADD</ACTIONS>
     <ACTIONS>HOLD</ACTIONS>
     <RECEIPT/>
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit RNAseq - **TODO**
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [iyMegPost-RNAseq.tsv](./data/iyMegPost-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iyMegPost-RNAseq.tsv -p ERGA-BGE -o iyMegPost-RNAseq
    ```
* Update iyMegPost-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession=""/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@iyMegPost-RNAseq.exp.xml" -F "RUN=@iyMegPost-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit assembly **TODO**

* I created a manifest file [iyMegPost4-manifest.txt](./data/iyMegPost4-manifest.txt)
* I created a folder on Uppmax (/proj/snic2022-6-208/nobackup/submission/BGE-M-posti/) and copied & gzipped manifest, assembly file and chromosome list there
* Then all files where submitted (first validation then submission) from Pelle Uppmax using Webin-CLI:
    ```
    interactive -t 08:00:00 -A uppmax2025-2-58
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./iyMegPost4-manifest.txt -validate
    ```
* Receipt:
    ```

    ```
* I added the accession number to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `Assembly submitted` to `Yes`, as well as set assembly as status `Submitted` in [Tracking_tool_Seq_centers](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/edit?pli=1&gid=0#gid=0)
* Accessioned:
    ```

    ```
* Release study and check that it is shown under umbrella

#### Add assembly to umbrella
* Add the assembly project when it has been submitted, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.
* Create [update.xml](./data/update.xml) and [umbrella_modified.xml](./data/umbrella_modified.xml)
* Submit: **TODO**
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
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Megachile posti" -t iyMegPost4 -p ERGA-BGE -c SCILIFELAB -a PRJEB91079 -x 3229175
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
    <RECEIPT receiptDate="2025-08-25T15:47:17.814+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB96372" alias="erga-bge-iyMegPost-study-umbrella-2025-08-25" status="PRIVATE" holdUntilDate="2026-03-07Z"/>
        <SUBMISSION accession="ERA34685281" alias="SUBMISSION-25-08-2025-15:47:17:664"/>
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
    <RECEIPT receiptDate="2025-08-25T15:48:01.697+01:00" submissionFile="submission-release-project.xml" success="true">
        <MESSAGES>
            <INFO>project accession "PRJEB96372" is set to public status.</INFO>
        </MESSAGES>
        <ACTIONS>RELEASE</ACTIONS>
    </RECEIPT>    
    ```
