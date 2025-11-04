---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB96371 (umbrella), PRJEB96314 (experiment), PRJEB96315 (assembly), PRJEB102190 (mito)
---

# BGE - *Eucera mavromoustakisi*

## Submission task description
Submission of raw reads for *Eucera mavromoustakisi* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Eucera-mavromoustakisi-metadata.xlsx)
* [BGE HiFi metadata](./data/iyEucMavr-HiFi.tsv)
* [BGE HiC metadata](./data/iyEucMavr-HiC.tsv)
* [BGE RNAseq metadata](./data/iyEucMavr-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiFi
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput *.bam` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.
#### XML
* I created [iyEucMavr-HiFi.tsv](./data/iyEucMavr-HiFi.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iyEucMavr-HiFi.tsv -p ERGA-BGE -o iyEucMavr-HiFi
    ```

* Study is private, so submission.xml with hold date is used.

* Submit both projects and experiment in one go, i.e:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@iyEucMavr-HiFi.study.xml" -F "EXPERIMENT=@iyEucMavr-HiFi.exp.xml" -F "RUN=@iyEucMavr-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-08-24T11:04:09.936+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14868744" alias="exp_iyEucMavr_HiFi_WGS_LV6000911946_pr_256_001" status="PRIVATE"/>
        <RUN accession="ERR15464848" alias="run_iyEucMavr_HiFi_WGS_LV6000911946_pr_256_001_bam_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB96314" alias="erga-bge-iyEucMavr-study-rawdata-2025-08-22" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP179057" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB96315" alias="erga-bge-iyEucMavr2_primary-2025-08-22" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP179058" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA34527093" alias="SUBMISSION-24-08-2025-11:04:09:759"/>
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
* I created [iyEucMavr-HiC.tsv](./data/iyEucMavr-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iyEucMavr-HiC.tsv -p ERGA-BGE -o iyEucMavr-HiC
    ```
* Update -HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB96314"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study will be private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@iyEucMavr-HiC.exp.xml" -F "RUN=@iyEucMavr-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <RECEIPT receiptDate="2025-08-25T13:48:25.781+01:00" submissionFile="submission.xml" success="true">
     <EXPERIMENT accession="ERX14869354" alias="exp_iyEucMavr_Hi-C_LV6000911938_HC043-1A1A" status="PRIVATE"/>
     <RUN accession="ERR15465459" alias="run_iyEucMavr_Hi-C_LV6000911938_HC043-1A1A_fastq_1" status="PRIVATE"/>
     <SUBMISSION accession="ERA34671933" alias="SUBMISSION-25-08-2025-13:48:25:635"/>
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
* I created [iyEucMavr-RNAseq.tsv](./data/iyEucMavr-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iyEucMavr-RNAseq.tsv -p ERGA-BGE -o iyEucMavr-RNAseq
    ```
* Update -RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB96314"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@iyEucMavr-RNAseq.exp.xml" -F "RUN=@iyEucMavr-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit assembly
* Apart from the primary assembly, a mitochondrial assembly has also been produced for this species, so another project needs to be created.
    * I created [iyEucMavr-mito.study.xml](./data/iyEucMavr-mito.study.xml) and submitted using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission-hold.xml" -F "PROJECT=@iyEucMavr-mito.study.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
    * Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-11-03T14:54:55.180Z" submissionFile="submission-hold.xml" success="true">
        <PROJECT accession="PRJEB102190" alias="erga-bge-iyEucMavr2_mito-2025-11-03" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP183591" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA35101724" alias="SUBMISSION-03-11-2025-14:54:55:115"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
    
* I created a manifest file [iyEucMavr2-manifest.txt](./data/iyEucMavr2-manifest.txt) and [iyEucMavr2-manifest-mito.txt](./data/iyEucMavr2-manifest.txt) and chromosome_list.txt for both primary and mito assembly, plus an unlocalised_list.txt for the primary assembly
* I created a folder on Uppmax (/proj/snic2022-6-208/nobackup/submission/E-mavromoustakisi) and copied & gzipped manifests, assembly file and chromosome list there
* Then all files where submitted (first validation then submission) from Pelle on Uppmax using Webin-CLI:

    ```
    interactive -t 08:00:00 -A uppmax2025-2-58
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./iyEucMavr2-manifest.txt -validate
    ```
* Receipt primary:
    ```
    INFO : Your application version is 9.0.1
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/E-mavromoustakisi/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/E-mavromoustakisi/iyEucMavr2_pri_20251020.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/E-mavromoustakisi/chromosome_list.txt.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/E-mavromoustakisi/unlocalised_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28549506
    ```
* Receipt mito:
    ```
    INFO : Your application version is 9.0.1
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/E-mavromoustakisi/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/E-mavromoustakisi/iyEucMavr2_mito_20251020.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/E-mavromoustakisi/mito-chromosome_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28549507
    ```    
* I added the accession number to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `Assembly submitted` to `Yes`, as well as set assembly as status `Submitted` in [Tracking_tool_Seq_centers](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/edit?pli=1&gid=0#gid=0)
* Accessioned:
    ```
    ASSEMBLY_NAME     | ASSEMBLY_ACC  | STUDY_ID    | SAMPLE_ID   | CONTIG_ACC                      | SCAFFOLD_ACC | CHROMOSOME_ACC
    iyEucMavr2.1      | GCA_977019085 | PRJEB96315  | ERS21344149 | CDRNYJ010000001-CDRNYJ010005275 |              | OZ362827-OZ362848
    iyEucMavr2-mito.1 | GCA_977019075 | PRJEB102190 | ERS21344149 |                                 |              | OZ362826-OZ362826
    ```
* Release study and check that it is shown under umbrella

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
    <RECEIPT receiptDate="2025-11-03T16:00:59.155Z" submissionFile="update.xml" success="true">
        <PROJECT accession="PRJEB96371" alias="erga-bge-iyEucMavr-study-umbrella-2025-08-25" status="PUBLIC"/>
        <SUBMISSION accession="" alias="SUBMISSION-03-11-2025-16:00:58:934"/>
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
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Eucera mavromoustakisi" -t iyEucMavr2 -p ERGA-BGE -c SCILIFELAB -a PRJEB96314 -x 3229266
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
    <RECEIPT receiptDate="2025-08-25T15:38:51.150+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB96371" alias="erga-bge-iyEucMavr-study-umbrella-2025-08-25" status="PRIVATE" holdUntilDate="2026-03-07Z"/>
        <SUBMISSION accession="ERA34684305" alias="SUBMISSION-25-08-2025-15:38:51:009"/>
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
    <RECEIPT receiptDate="2025-08-25T15:39:27.218+01:00" submissionFile="submission-release-project.xml" success="true">
        <MESSAGES>
            <INFO>project accession "PRJEB96371" is set to public status.</INFO>
        </MESSAGES>
        <ACTIONS>RELEASE</ACTIONS>
    </RECEIPT>    
    ```
