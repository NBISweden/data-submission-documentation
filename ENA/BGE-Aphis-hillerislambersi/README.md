---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB96486 (umbrella), PRJEB93933 (experiment), PRJEB93934 (assembly), PRJEB108460 (mito)
---

# BGE - *Aphis hillerislambersi*

## Submission task description
Submission of raw reads for *Aphis hillerislambersi* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Aphis-hillerislambersi-metadata.xlsx)
* [BGE HiFi metadata](./data/ihAphHill-HiFi.tsv)
* [BGE HiC metadata](./data/ihAphHill-HiC.tsv)
* [BGE RNAseq metadata](./data/ihAphHill-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiFi
#### Preparations
* There are 2 sample IDs -> a virtual sample is needed
    * There is a complication though, the two sample IDs has different ToLIDs. It shouldn't happen, I don't know how to handle it. To which id will/should the assembly be connected?
    * I've asked ERGA-BGE slack for advice, waiting for reply. The answer was to create a new one at https://id.tol.sanger.ac.uk/, referring to the original ToLID's and then create a virtual sample. I'm waiting for the new ToLID to become active (will keep an eye on the search page, https://id.tol.sanger.ac.uk/search-by-tolid, expecting `ihAphHill11`, specimenID `ERGA_PR_7524_0782;ERGA_PR_7524_0787`)
    * I created [ihAphHill-HiFi-virtual-sample.tsv](./data/ihAphHill-HiFi-virtual-sample.tsv) and registered the sample
    * Accession number received: `ERS25260761`  
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput *.bam` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.
#### XML
* I created [ihAphHill-HiFi.tsv](./data/ihAphHill-HiFi.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f ihAphHill-HiFi.tsv -p ERGA-BGE -o ihAphHill-HiFi
    ```

* Study is private, so submission.xml with hold date is used.

* Submit both projects and experiment in one go, i.e:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@ihAphHill-HiFi.study.xml" -F "EXPERIMENT=@ihAphHill-HiFi.exp.xml" -F "RUN=@ihAphHill-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-07-16T07:25:42.609+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14694880" alias="exp_ihAphHill_HiFi_WGS_LV6000904611_LV6000904600_pr_232_001" status="PRIVATE"/>
        <RUN accession="ERR15289046" alias="run_ihAphHill_HiFi_WGS_LV6000904611_LV6000904600_pr_232_001_bam_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB93933" alias="erga-bge-ihAphHill-study-rawdata-2025-07-16" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP176812" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB93934" alias="erga-bge-ihAphHill11_primary-2025-07-16" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP176813" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA33631455" alias="SUBMISSION-16-07-2025-07:25:42:253"/>
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
* Sample ID gave 4 BioSample ID:s via ERGA tracker portal, and 4 different ToLID:s --> Virtual sample is needed, and a new ToLID is needed.
    * New ToLID was requested by a colleague, received `ihAphHill12`
    * I created [ihAphHill-HiC-virtual-sample.tsv](./data/ihAphHill-HiC-virtual-sample.tsv) and registered the sample
    * Accession number received: `ERS26920718`
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [ihAphHill-HiC.tsv](./data/ihAphHill-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f ihAphHill-HiC.tsv -p ERGA-BGE -o ihAphHill-HiC
    ```
* Update ihAphHill-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB93933"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title, since the other data types have the platform named
* Study is pulic, so submission-noHold.xml is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission-noHold.xml" -F "EXPERIMENT=@ihAphHill-HiC.exp.xml" -F "RUN=@ihAphHill-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-09-25T13:02:29.261+01:00" submissionFile="submission-noHold.xml" success="true">
        <EXPERIMENT accession="ERX15056023" alias="exp_ihAphHill_Hi-C_LV6000904610_LV6000904599_ LV6000902952_LV6000904603_HC050-1A1A" status="PRIVATE"/>
        <RUN accession="ERR15651460" alias="run_ihAphHill_Hi-C_LV6000904610_LV6000904599_ LV6000902952_LV6000904603_HC050-1A1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA35018351" alias="SUBMISSION-25-09-2025-13:02:28:992"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    </RECEIPT>
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit RNAseq
* See [README RNAseq submission](../BGE-RNAseq-2026-02-27/README.md)

### Submit assembly
* There is also a separate mito assembly, so I needed another project for that:
    * I created [ihAphHill-mito.study.xml](./data/ihAphHill-mito.study.xml) and submitted using curl:
        ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@ihAphHill-mito.study.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
        ```
    * Receipt:
        ```
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2026-02-18T08:13:10.858Z" submissionFile="submission.xml" success="true">
        <PROJECT accession="PRJEB108460" alias="erga-bge-ihAphHill11-study-mito-2026-02-18" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP189294" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA35776792" alias="SUBMISSION-18-02-2026-08:13:10:768"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
        ```
* I created manifest files [ihAphHill11-manifest.txt](./data/ihAphHill11-manifest.txt) and [ihAphHill11-mito-manifest.txt](./data/ihAphHill11-mito-manifest.txt)
* I created a folder on Uppmax (/proj/snic2022-6-208/nobackup/submission/A-hillerislambersi) and copied & gzipped manifest, assembly file and chromosome list there
* Then all files where submitted (first validation then submission) from Pelle on Uppmax using Webin-CLI:

    ```
    interactive -t 01:00:00 -A uppmax2025-2-58
    java -jar ~/webin-cli-9.0.1.jar -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./ihAphHill11-manifest.txt -validate
    java -jar ~/webin-cli-9.0.1.jar -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./ihAphHill11-mito-manifest.txt -validate    
    ```
    **Note:** I had the flag `-ascp` set and the submit command failed. Once removed the file uploaded successfully.
* Receipt:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/A-hillerislambersi/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/A-hillerislambersi/ihAphHill11.priCur.20260216.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/A-hillerislambersi/chromosome_list.txt.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/A-hillerislambersi/unlocalised_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ29061737

    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/A-hillerislambersi/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/A-hillerislambersi/ihAphHill11.mito.20260216.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/A-hillerislambersi/mito-chromosome_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ29061760    
    ```
* I added the accession number to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `Assembly submitted` to `Yes`, as well as set assembly as status `Submitted` in [Tracking_tool_Seq_centers](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/edit?pli=1&gid=0#gid=0)
* Accessioned:
    ```
    ASSEMBLY_NAME      | ASSEMBLY_ACC  | STUDY_ID    | SAMPLE_ID   | CONTIG_ACC                      | SCAFFOLD_ACC | CHROMOSOME_ACC
    ihAphHill11.1      | GCA_980628925 | PRJEB93934  | ERS25260761 | CELYDT010000001-CELYDT010000009 |              | OZ413322-OZ413325
    ihAphHill11-mito.1 | GCA_980634235 | PRJEB108460 | ERS25260761 |                                 |              | OZ413326-OZ413326
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
    <RECEIPT receiptDate="2026-02-18T10:22:41.333Z" submissionFile="update.xml" success="true">
        <PROJECT accession="PRJEB96486" alias="erga-bge-ihAphHill-study-umbrella-2025-08-27" status="PUBLIC"/>
        <SUBMISSION accession="" alias="SUBMISSION-18-02-2026-10:22:41:133"/>
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
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Aphis hillerislambersi" -t ihAphHill11 -p ERGA-BGE -c SCILIFELAB -a PRJEB93933 -x 3350012
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
    <RECEIPT receiptDate="2025-08-27T09:32:38.862+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB96486" alias="erga-bge-ihAphHill-study-umbrella-2025-08-27" status="PRIVATE" holdUntilDate="2027-08-27+01:00"/>
        <SUBMISSION accession="ERA34838284" alias="SUBMISSION-27-08-2025-09:32:38:564"/>
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
    <RECEIPT receiptDate="2025-08-27T09:33:25.903+01:00" submissionFile="submission-release-project.xml" success="true">
        <MESSAGES>
            <INFO>project accession "PRJEB96486" is set to public status.</INFO>
        </MESSAGES>
        <ACTIONS>RELEASE</ACTIONS>
    </RECEIPT>    
    ```

* **Note:** Add the assembly project `` when it has been submitted and made public, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.
