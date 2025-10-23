---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB96534 (umbrella), PRJEB96532 (experiment), PRJEB96533 (assembly)
---

# BGE - *Messor bucephalus*

## Submission task description
Submission of raw reads for *Messor bucephalus* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Messor-bucephalus-metadata.xlsx)
* [BGE HiFi metadata](./data/iyMesBuce-HiFi.tsv)
* [BGE HiC metadata](./data/iyMesBuce-HiC.tsv)
* [BGE RNAseq metadata](./data/iyMesBuce-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiFi
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput *.bam` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.
#### XML
* I created [iyMesBuce-HiFi.tsv](./data/iyMesBuce-HiFi.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iyMesBuce-HiFi.tsv -p ERGA-BGE -o iyMesBuce-HiFi
    ```

* Study will be public directly, so submission.xml without hold date is used.

* Submit both projects and experiment in one go, i.e:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@iyMesBuce-HiFi.study.xml" -F "EXPERIMENT=@iyMesBuce-HiFi.exp.xml" -F "RUN=@iyMesBuce-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-08-27T15:06:09.338+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14882872" alias="exp_iyMesBuce_HiFi_WGS_LV6000912053_pr_260_001" status="PRIVATE"/>
        <RUN accession="ERR15478975" alias="run_iyMesBuce_HiFi_WGS_LV6000912053_pr_260_001_bam_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB96532" alias="erga-bge-iyMesBuce-study-rawdata-2025-08-27" status="PRIVATE" holdUntilDate="2027-08-27+01:00">
            <EXT_ID accession="ERP179237" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB96533" alias="erga-bge-iyMesBuce7_primary-2025-08-27" status="PRIVATE" holdUntilDate="2027-08-27+01:00">
            <EXT_ID accession="ERP179238" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA34838469" alias="SUBMISSION-27-08-2025-15:06:09:021"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    </RECEIPT>    
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit HiC - **TODO**
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* **Issue:** Deliveries batch 8 and 9 has same library name. I have asked about this in slack, if correct. I suggest not to submit any HiC before this has been clarified.
    * Answer from NGI: *It's the same library sequenced in the two different pools. We needed to fill the second pool in batch 9 with a library containing a certain primer pair for colour balancing reasons as the library we had planned for this failed. (Should you feel that you have enough data with the first library and don't want more of Messor bucephalus, you can likely just leave it out of the analysis.)*
    * Should we submit or not, and if so, should we wait until we get batch 9 delivery so that we can submit both runs to same experiment?
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [iyMesBuce-HiC.tsv](./data/iyMesBuce-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iyMesBuce-HiC.tsv -p ERGA-BGE -o iyMesBuce-HiC
    ```
* Update iyMesBuce-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB96532"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title, since the other data types have the platform named
* Study is public, so submission.xml without hold date is used.
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@iyMesBuce-HiC.exp.xml" -F "RUN=@iyMesBuce-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-08-27T15:15:35.956+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14882873" alias="exp_iyMesBuce_Hi-C_LV6000912132_HC047-1A1A" status="PRIVATE"/>
        <RUN accession="ERR15478976" alias="run_iyMesBuce_Hi-C_LV6000912132_HC047-1A1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA34838477" alias="SUBMISSION-27-08-2025-15:15:35:517"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    </RECEIPT>
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit RNAseq - **TODO**
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [iyMesBuce-RNAseq.tsv](./data/iyMesBuce-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iyMesBuce-RNAseq.tsv -p ERGA-BGE -o iyMesBuce-RNAseq
    ```
* Update iyMesBuce-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB96532"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study public, so submission.xml without hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@iyMesBuce-RNAseq.exp.xml" -F "RUN=@iyMesBuce-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit assembly
* I created a manifest file [iyMesBuce7-manifest.txt](./data/iyMesBuce7-manifest.txt)
* I created a folder on Uppmax (/proj/snic2022-6-208/nobackup/submission/M-bucephalus/) and copied & gzipped manifest, assembly file and chromosome + unlocalised list there
* Then all files where submitted (first validation then submission) from Pelle Uppmax using Webin-CLI:
    ```
    interactive -t 08:00:00 -A uppmax2025-2-58
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./iyMesBuce7-manifest.txt -validate
    ```
* Receipt:
    ```
    INFO : Your application version is 9.0.1
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/M-bucephalus/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/M-bucephalus/iyMesBuce7_pri.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/M-bucephalus/chromosome_list.txt.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/M-bucephalus/unlocalised_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28547240
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
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Messor bucephalus" -t iyMesBuce7 -p ERGA-BGE -c SCILIFELAB -a PRJEB96532 -x 3229181
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
    <RECEIPT receiptDate="2025-08-27T15:19:24.976+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB96534" alias="erga-bge-iyMesBuce-study-umbrella-2025-08-27" status="PRIVATE" holdUntilDate="2027-08-27+01:00"/>
        <SUBMISSION accession="ERA34838483" alias="SUBMISSION-27-08-2025-15:19:24:818"/>
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
    <RECEIPT receiptDate="2025-08-27T15:21:49.379+01:00" submissionFile="submission-release-project.xml" success="true">
        <MESSAGES>
            <INFO>project accession "PRJEB96534" is set to public status.</INFO>
        </MESSAGES>
        <ACTIONS>RELEASE</ACTIONS>
    </RECEIPT>    
    ```
