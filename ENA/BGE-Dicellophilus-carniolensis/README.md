---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB77282, PRJEB77038, PRJEB77039
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

### Submit RNAseq

### Submit assembly

### Register umbrella projekt

For each of the BGE species, an umbrella project has to be created and linked to the main BGE project, [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

* There is a CNAG script, that should do the deed of creating the xml file:
    ```
    ./script/get_umbrella_xml_ENA.py -s "Dicellophilus carniolensis" -t qcDicCarn1 -p ERGA-BGE -c SCILIFELAB -a PRJEB77038 -x 173051
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
* **Note:** Add the assembly project `PRJEB77039` when it has been submitted and made public, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.
