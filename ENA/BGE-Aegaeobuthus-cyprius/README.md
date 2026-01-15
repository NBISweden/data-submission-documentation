---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB91378 (umbrella), PRJEB90592 (experiment), PRJEB90593 (assembly)
---

# BGE - *Aegaeobuthus cyprius*

## Submission task description
Submission of raw reads for *Aegaeobuthus cyprius* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Aegaeobuthus-cyprius-metadata.xlsx)
* [BGE HiFi metadata](./data/qqAegCypr-HiFi.tsv)
* [BGE HiC metadata](./data/qqAegCypr-HiC.tsv)
* [BGE RNAseq metadata](./data/qqAegCypr-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiFi
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal. However, there are 2 samples, hence, a virtual sample needs to be created
    * I created [qqAegCypr-HiFi-virtual-sample.tsv](./data/qqAegCypr-HiFi-virtual-sample.tsv) and registered the sample
    * Accession number received: `ERS25056508`

* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput *.bam` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [qqAegCypr-HiFi.tsv](./data/qqAegCypr-HiFi.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qqAegCypr-HiFi.tsv -p ERGA-BGE -o qqAegCypr-HiFi
    ```

* Study is private, so submission.xml with hold date is used.

* Submit both projects and experiment in one go, i.e:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@qqAegCypr-HiFi.study.xml" -F "EXPERIMENT=@qqAegCypr-HiFi.exp.xml" -F "RUN=@qqAegCypr-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-18T14:46:18.873+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14537775" alias="exp_qqAegCypr_HiFi_WGS_LV6000912378_LV6000912346_pr_203" status="PRIVATE"/>
        <RUN accession="ERR15132530" alias="run_qqAegCypr_HiFi_WGS_LV6000912378_LV6000912346_pr_203_bam_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB90592" alias="erga-bge-qqAegCypr-study-rawdata-2025-06-18" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP173594" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB90593" alias="erga-bge-qqAegCypr1_primary-2025-06-18" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP173595" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA33330201" alias="SUBMISSION-18-06-2025-14:46:18:477"/>
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
* I created [qqAegCypr-HiC.tsv](./data/qqAegCypr-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qqAegCypr-HiC.tsv -p ERGA-BGE -o qqAegCypr-HiC
    ```
* Update -HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90592"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study will be private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@qqAegCypr-HiC.exp.xml" -F "RUN=@qqAegCypr-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-30T07:29:56.905+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14574825" alias="exp_qqAegCypr_Hi-C_LV6000912336_HC029-1A1A" status="PRIVATE"/>
        <RUN accession="ERR15169094" alias="run_qqAegCypr_Hi-C_LV6000912336_HC029-1A1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA33538450" alias="SUBMISSION-30-06-2025-07:29:56:725"/>
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
* I created [qqAegCypr-RNAseq.tsv](./data/qqAegCypr-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qqAegCypr-RNAseq.tsv -p ERGA-BGE -o qqAegCypr-RNAseq
    ```
* Update -RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90592"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@qqAegCypr-RNAseq.exp.xml" -F "RUN=@qqAegCypr-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit assembly

* I created a manifest file [qqAegCypr1-manifest.txt](./data/qqAegCypr1-manifest.txt)
* I created a folder on Uppmax (/proj/snic2022-6-208/nobackup/submission/A-cyprius/) and copied & gzipped manifest, assembly file and chromosome list there
* Then all files where submitted (first validation then submission) from Pelle on Uppmax using Webin-CLI:

    ```
    interactive -t 08:00:00 -A uppmax2025-2-58
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./qqAegCypr1-manifest.txt -validate
    ```
* Receipt:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/A-cyprius/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/A-cyprius/qqAegCypr1_pri.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/A-cyprius/chromosome_list.txt.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/A-cyprius/unlocalised_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28783855
    ```
* I added the accession number to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `Assembly submitted` to `Yes`, as well as set assembly as status `Submitted` in [Tracking_tool_Seq_centers](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/edit?pli=1&gid=0#gid=0)
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
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2026-01-15T15:23:59.778Z" submissionFile="update.xml" success="true">
        <PROJECT accession="PRJEB91378" alias="erga-bge-qqAegCypr-study-umbrella-2025-07-01" status="PUBLIC"/>
        <SUBMISSION accession="" alias="SUBMISSION-15-01-2026-15:23:59:593"/>
        <MESSAGES/>
        <ACTIONS>MODIFY</ACTIONS>
    </RECEIPT>
    ```

### Umbrella project
For each of the BGE species, an **umbrella** project has to be created and linked to the main BGE project, [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

* What is the best way of collecting the data, since it is even the taxonomy ID that is needed?
    1. Collect scientific name and tolId from the metadata template sheet
    1. Go to [ENA browser](https://www.ebi.ac.uk/ena/browser/home) and enter the scientific name as search term
        1. To the left side, there should be a **Taxon** subheading, that gives the identifier
    1. Copy experiment accession number from metadata in top of this README
* There is a CNAG script, that should do the deed of creating the xml file:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Aegaeobuthus cyprius" -t qqAegCypr -p ERGA-BGE -c SCILIFELAB -a PRJEB90592 -x 3229104
    ```
    Explanation of arguments:
    * -s: scientific name e.g. "Lithobius stygius"
    * -t: tolId e.g. qcLitStyg1
    * -a: the accession number of the raw reads project e.g. PRJEB76283
    * -x: NCBI taxonomy id e.g. 2750798
* Do I have to release the experiment study via browser, i.e. if no hold date on umbrella, will the attached children automagically be released?
    * ENA read the docs:
        * It is good practice to provide a specific release date for an umbrella project using the HOLD action in the submission XML. When this date arrives, the umbrella project will become public automatically. 
        However, this is optional and **if not provided, the release date defaults to two years after registration**.

        * Each **child project is released independently** and they each have their own hold date which is determined on registration, the **umbrella** project release **does not determine** the child project(s) release.
    * Question is if I should add also assembly project already now, even though it is not yet submitted? However, since there's always a risk that the assembly needs to be a draft, and thus should not be 'ERGA-BGE' tagged (see e.g. Astagobius angustatus), I think it's safest to add afterwards, when ready
    * Hence
        1. **Set hold date ~2 days ahead of registration** (guess it could be today's date as well)
        1. **Release the child project via browser**

* Copy `submission-umbrella.xml` from any of the previous BGE species, set the hold date as desired.
* Submit using curl:
    ```
    curl -u Username:Password -F "SUBMISSION=@submission-umbrella.xml" -F "PROJECT=@umbrella.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-07-01T10:21:13.641+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB91378" alias="erga-bge-qqAegCypr-study-umbrella-2025-07-01" status="PRIVATE" holdUntilDate="2025-07-03+01:00"/>
        <SUBMISSION accession="ERA33545029" alias="SUBMISSION-01-07-2025-10:21:13:397"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>    
    ```
* Add received accession number in top of this page, in the NBIS tracking sheet, ERGA tracking sheet, and update status to public
