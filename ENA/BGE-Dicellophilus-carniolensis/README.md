---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB77282 (umbrella), PRJEB77038 (experiment), PRJEB77039 (assembly)
---

# BGE - *Dicellophilus carniolensis*
## Submission task description
Submission of raw reads for *Dicellophilus carniolensis* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Dicellophilus-carniolensis-metadata.xlsx)
* [BGE metadata](./data/qcDicCarn-BGE.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->
* Went all in on xml submission, and only filled in minimum of metadata in our BGE-metadata-template.xlsx. Saved a lot of time.
* Also, saving time as well, this time the sample info name in the NGI delivery README provided enough information to fairly easy (via ERGA tracking portal) identifying which of the 20 BioSamples should be used.

## Detailed step by step description
### Collect metadata
* [BioSample query](https://www.ebi.ac.uk/biosamples/samples?text=Dicellophilus+carniolensis) resulted in 20 samples
* NGI README (in /proj/snic2022-6-208/INBOX/BGE_Dicellophilus_carniolensis/EBP_pr_088/files/pr_088/README) say Sample info name `FS42595415`, and UGC ID `pr_088_001`.
* Searching in [ERGA tracking portal Samples](https://genomes.cnag.cat/erga-stream/samples/) with the name as `Tube or well id`, gave [SAMEA115117730](https://www.ebi.ac.uk/biosamples/samples/SAMEA115117730) as result
* I checked BioSamples and it seems valid
* This time I only filled in BGE-sheet and ENA_run tabs in metadata template, to save time
* Once filled in, I copied the BGE-sheet into [qcDicCarn-BGE.tsv](./data/qcDicCarn-BGE.tsv)

### Create xml
* A [submission.xml](./data/submission.xml) needs to be created manually, which includes the action (ADD) and release date (HOLD).
* Command to create submission xml:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qcDicCarn-BGE.tsv -p ERGA-BGE -o qcDicCarn-hifi
    ```
* Checked the output files, qcDicCarn-hifi.study.xml, qcDicCarn-hifi.exp.xml and qcDicCarn-hifi.runs.xml, looked okay

### Submit HiFi
* Created a subdirectory at ENA upload area, `bge-dicellophilus-HiFi` using FileZilla
* At Uppmax:
    ```
    cd /proj/naiss2024-22-345/nobackup/yvonnek/
    interactive -t 08:00:00 -A naiss2024-22-345
    module load ascp
    export ASPERA_SCP_PASS='password'
    ascp -k 3 -d -q --mode=send -QT -l300M --host=webin.ebi.ac.uk --user=Webin-XXXX /proj/snic2022-6-208/INBOX/BGE_Dicellophilus_carniolensis/EBP_pr_088/files/pr_088/rawdata/pr_088_001/m84045_240531_164906_s1.hifi_reads.bc2040.bam /bge-dicellophilus-HiFi/
    ```

    **Note:** A colleague experienced that it was faster upload at nobackup compared to home directory, even though it shouldn't matter (Uppmax people said it could be due to parts of crex not feeling so well), so I used the same.

* Transfer xml files to Uppmax no backup using MobaXterm:
    * Start the app and connect to Rackham using 2FA
    * Start a local terminal session in the app, and write the scp command as usual, `scp *.xml yvonnek@rackham.uppmax.uu.se:/proj/naiss2024-22-345/nobackup/yvonnek/BGE-Dicellophilus/`
* Do the acutal submission:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml"  -F "PROJECT=@qcDicCarn-hifi.study.xml" -F "EXPERIMENT=@qcDicCarn-hifi.exp.xml" -F "RUN=@qcDicCarn-hifi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-06-28T14:47:57.023+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX12704040" alias="exp_qcDicCarn1_HiFi_WGS_FS42595415" status="PRIVATE"/>
        <RUN accession="ERR13333054" alias="run_qcDicCarn1_HiFi_WGS_FS42595415_bam_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB77038" alias="erga-bge-qcDicCarn-study-rawdata-2024-06-28" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP161518" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB77039" alias="erga-bge-qcDicCarn1_primary-2024-06-28" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP161519" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA30654581" alias="SUBMISSION-28-06-2024-14:47:56:763"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
    
### Submit Hi-C
#### Preparations
* Recieved sample label `FS42595418` from NGI, looking it up in the ERGA tracking portal, it leads to biosample `SAMEA115117727`, from which I collected the ToLID.
* First batch of HiC will be used, hence need to do data transfer (which I did for all first batch HiC in one go, but below is example of how to):
    ```
    interactive -t 08:00:00 -A uppmax2025-2-58
    cat sample_TAGACCAA+TCACCTTG_part*_R1.fastq.gz > ../to_ENA/dicCarn_sample_TAGACCAA+TCACCTTG_R1.fastq.gz
    cat sample_TAGACCAA+TCACCTTG_part*_R2.fastq.gz > ../to_ENA/dicCarn_sample_TAGACCAA+TCACCTTG_R2.fastq.gz
    cd ../to_ENA
    lftp webin2.ebi.ac.uk -u Webin-39907
    mput dicCarn*.fastq.gz
    ```
#### XML
* I created [qcDicCarn-HiC.tsv](./data/qcDicCarn-HiC.tsv).
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qcDicCarn-HiC.tsv -p ERGA-BGE -o qcDicCarn-HiC
    ```
* Update qcDicCarn-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB77038"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is already public, so submission.xml without hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission-noHold.xml" -F "EXPERIMENT=@qcDicCarn-HiC.exp.xml" -F "RUN=@qcDicCarn-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-03-19T10:59:34.738Z" submissionFile="submission-noHold.xml" success="true">
        <EXPERIMENT accession="ERX14162836" alias="exp_qcDicCarn_Hi-C_FS42595418_HC012-1A1A" status="PRIVATE"/>
        <RUN accession="ERR14758876" alias="run_qcDicCarn_Hi-C_FS42595418_HC012-1A1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA31211466" alias="SUBMISSION-19-03-2025-10:59:33:592"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    </RECEIPT>
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

#### Additional HiC
* Additional sequencing was made for library `HC012-2A1A-CL`. Sample is the same and sequences was transferred in batch to ENA using lftp. (**Note:** The text assumes that I had already submitted HC012-2A1A, but in reality I had not, that is done below this submission)
#### XML
* I created [qcDicCarn-2-HiC.tsv](./data/qcDicCarn-2-HiC.tsv).
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qcDicCarn-2-HiC.tsv -p ERGA-BGE -o qcDicCarn-2-HiC
    ```
* Update qcDicCarn-2-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB77038"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title, since the other data types have the platform named
* Study is already public, so submission.xml without hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission-noHold.xml" -F "EXPERIMENT=@qcDicCarn-2-HiC.exp.xml" -F "RUN=@qcDicCarn-2-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-10-23T07:50:07.156+01:00" submissionFile="submission-noHold.xml" success="true">
        <EXPERIMENT accession="ERX15162305" alias="exp_qcDicCarn_Hi-C_FS42595417_HC012-2A1A-CL" status="PRIVATE"/>
        <RUN accession="ERR15757781" alias="run_qcDicCarn_Hi-C_FS42595417_HC012-2A1A-CL_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA35072585" alias="SUBMISSION-23-10-2025-07:50:06:754"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    </RECEIPT>
    ```

* **Note 2025-11-13**: I missed to submit one of the HiC datasets earlier, `HC012-2A1A`
* I created [qcDicCarn-3-HiC.tsv](./data/qcDicCarn-3-HiC.tsv).
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qcDicCarn-3-HiC.tsv -p ERGA-BGE -o qcDicCarn-3-HiC
    ```
* Update qcDicCarn-3-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB77038"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title, since the other data types have the platform named
* Study is already public, so submission.xml without hold date is used.
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission-noHold.xml" -F "EXPERIMENT=@qcDicCarn-3-HiC.exp.xml" -F "RUN=@qcDicCarn-3-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-11-13T15:37:18.796Z" submissionFile="submission-noHold.xml" success="true">
        <EXPERIMENT accession="ERX15266298" alias="exp_qcDicCarn_Hi-C_FS42595417_HC012-2A1A" status="PRIVATE"/>
        <RUN accession="ERR15866510" alias="run_qcDicCarn_Hi-C_FS42595417_HC012-2A1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA35139231" alias="SUBMISSION-13-11-2025-15:37:18:510"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    </RECEIPT>
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit RNA-Seq
* Data transfer to ENA upload area (folder /bge-rnaseq/) was done previously for all RNAseq data (first batch)
* Create [qcDicCarn-RNAseq.tsv](./data/qcDicCarn-RNAseq.tsv)
    * Note: used biosample with well id `FS42595422` in erga tracking portal
* Create [submission-noHold.xml](./data/submission-noHold.xml), without any hold date since study is public already
* Run CNAG script
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qcDicCarn-RNAseq.tsv -p ERGA-BGE -o qcDicCarn-RNAseq
    ```
* Validate output (ignore the study xml)
* Update qcDicCarn-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB77038"/>
    ```
* Copy xml files to Uppmax
    ```
    scp qcDicCarn-RNAseq.exp.xml qcDicCarn-RNAseq.runs.xml submission-noHold.xml yvonnek@rackham.uppmax.uu.se:/home/yvonnek/BGE-dicellophilus/
    ```
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission-noHold.xml" -F "EXPERIMENT=@qcDicCarn-RNAseq.exp.xml" -F "RUN=@qcDicCarn-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"   
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-10-18T13:50:05.928+01:00" submissionFile="submission-noHold.xml" success="true">
        <EXPERIMENT accession="ERX13254455" alias="exp_qcDicCarn_Illumina_RNA-Seq_FS42595422_RE024-2A" status="PRIVATE"/>
        <RUN accession="ERR13851689" alias="run_qcDicCarn_Illumina_RNA-Seq_FS42595422_RE024-2A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA30886877" alias="SUBMISSION-18-10-2024-13:50:05:690"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    </RECEIPT>
    ```

* Add recevied accession numbers to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `RNA-seq submitted` to `yes`

### Submit assembly
* I created a manifest file [qcDicCarn1-manifest.txt](./data/qcDicCarn1-manifest.txt)
* I created a folder on Uppmax (/proj/snic2022-6-208/nobackup/submission/D-carniolensis) and copied & gzipped manifest, assembly file and chromosome list there
* Then all files where submitted (first validation then submission) from Pelle on Uppmax using Webin-CLI:

    ```
    interactive -t 01:00:00 -A uppmax2025-2-58
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./qcDicCarn1-manifest.txt -validate
    ```
* Receipt:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/D-carniolensis/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/D-carniolensis/qcDicCarn1_pri.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/D-carniolensis/chromosome_list.txt.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/D-carniolensis/unlocalised_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28562917
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
    <RECEIPT receiptDate="2025-11-14T09:08:16.070Z" submissionFile="update.xml" success="true">
        <PROJECT accession="PRJEB77282" alias="erga-bge-qcDicCarn-study-umbrella-2024-07-05" status="PUBLIC"/>
        <SUBMISSION accession="" alias="SUBMISSION-14-11-2025-09:08:15:858"/>
        <MESSAGES/>
        <ACTIONS>MODIFY</ACTIONS>
    </RECEIPT>
    ```

### Register umbrella projekt

For each of the BGE species, an umbrella project has to be created and linked to the main BGE project, [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

1. Release the child project via browser
1. Collect scientific name and tolId from the metadata template sheet
1. Go to [ENA browser](https://www.ebi.ac.uk/ena/browser/home) and enter the scientific name as search term
    1. To the left side, there should be a **Taxon** subheading, that gives the identifier
1. Copy experiment accession number from metadata in top of this README
* There is a CNAG script, that should do the deed of creating the xml file:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Dicellophilus carniolensis" -t qcDicCarn1 -p ERGA-BGE -c SCILIFELAB -a PRJEB77038 -x 173051
    ```
* Create a submission-umbrella.xml
* Submit using curl:
    ```
    curl -u Username:Password -F "SUBMISSION=@submission-umbrella.xml" -F "PROJECT=@umbrella.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-07-05T13:17:55.454+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB77282" alias="erga-bge-qcDicCarn-study-umbrella-2024-07-05" status="PRIVATE" holdUntilDate="2024-07-07+01:00"/>
        <SUBMISSION accession="ERA30670051" alias="SUBMISSION-05-07-2024-13:17:54:586"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
