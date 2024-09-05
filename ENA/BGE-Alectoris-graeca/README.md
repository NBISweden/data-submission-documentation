---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB79726 PRJEB79727
---

# BGE - *Alectoris graeca*
## Submission task description
Submission of raw reads for *Alectoris graeca* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Alectoris-graeca-metadata.xlsx)
* [BGE metadata](./data/bAleGra1-BGE.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->
* Went all in on xml submission, and only filled in minimum of metadata in our BGE-metadata-template.xlsx. Saved a lot of time.
* Also, saving time as well, this time the sample info name in the NGI delivery README provided enough information to fairly easy (via ERGA tracking portal) identifying which of the 20 BioSamples should be used.

## Detailed step by step description
### Collect metadata
* [BioSample query](https://www.ebi.ac.uk/biosamples/samples?text=Alectoris+graeca) resulted in 11 ERGA-related samples
* NGI README (in /proj/snic2022-6-208/INBOX/BGE_Alectoris_graeca/EBP_pr_106/files/pr_106/README) say Sample info name `FS42595433`, and UGC ID `pr_106_001`.
* Searching in [ERGA tracking portal Samples](https://genomes.cnag.cat/erga-stream/samples/) with the name as `Tube or well id`, gave [SAMEA115117745](https://www.ebi.ac.uk/biosamples/samples/SAMEA115117745) as result
* I checked BioSamples and it seems valid
* This time I only filled in BGE-sheet and ENA_run tabs in metadata template, to save time
* Once filled in, I copied the BGE-sheet into [bAleGra1-BGE.tsv](./data/bAleGra1-BGE.tsv)

### Create xml
* A [submission.xml](./data/submission.xml) needs to be created manually, which includes the action (ADD) and release date (HOLD). A release date of 2026-03-07 is set.
* Command to create submission xml:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f bAleGra1-BGE.tsv -p ERGA-BGE -o bAleGra1-hifi
    ```
* Checked the output files, bAleGra1-hifi.study.xml, bAleGra1-hifi.exp.xml and bAleGra1-hifi.runs.xml, looked okay

### Submit HiFi
* Created a subdirectory at ENA upload area, `bge-alectoris-graeca` using FileZilla
* At Uppmax:
    ```
    cd /proj/naiss2024-22-345/nobackup/yvonnek/
    interactive -t 08:00:00 -A naiss2024-22-345
    module load ascp
    export ASPERA_SCP_PASS='password'
    ascp -k 3 -d -q --mode=send -QT -l300M --host=webin.ebi.ac.uk --user=Webin-XXXX /proj/snic2022-6-208/INBOX/BGE_Alectoris_graeca/EBP_pr_106/files/pr_106/rawdata/pr_106_001/m84045_240717_194654_s3.hifi_reads.bc2086.bam /bge-alectoris-graeca/
    ```

    **Note:** A colleague experienced that it was faster upload at nobackup compared to home directory, even though it shouldn't matter (Uppmax people said it could be due to parts of crex not feeling so well), so I used the same.

* Transfer xml files to Uppmax no backup:
    * Create a folder `/proj/naiss2024-22-345/nobackup/yvonnek/BGE-Alectoris/`
    * Copy the files using scp: `scp *.xml yvonnek@rackham.uppmax.uu.se:/proj/naiss2024-22-345/nobackup/yvonnek/BGE-Alectoris/`
* Do the acutal submission:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml"  -F "PROJECT=@bAleGra1-hifi.study.xml" -F "EXPERIMENT=@bAleGra1-hifi.exp.xml" -F "RUN=@bAleGra1-hifi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-09-05T08:24:23.589+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX13002328" alias="exp_bAleGra_HiFi_WGS_FS42595433" status="PRIVATE"/>
        <RUN accession="ERR13631396" alias="run_bAleGra_HiFi_WGS_FS42595433_bam_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB79726" alias="erga-bge-bAleGra-study-rawdata-2024-09-05" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP163841" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB79727" alias="erga-bge-bAleGra1_primary-2024-09-05" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP163842" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA30781837" alias="SUBMISSION-05-09-2024-08:24:23:241"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
* Add recevied accession numbers to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/)

### Register umbrella project

For each of the BGE species, an umbrella project has to be created and linked to the main BGE project, [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

* There is a CNAG script, that should do the deed of creating the xml file:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Alectoris graeca" -t bAleGra1 -p ERGA-BGE -c SCILIFELAB -a PRJEB79726 -x 173051
    ```
    * Got error message: `ImportError: No module named jinja2`
    * Had to update 1st line of python script to `#!/usr/bin/env python3` instead of `#!/usr/bin/env python` 
* Create a [submission-umbrella.xml](./data/submission-umbrella.xml). I put a release date of 2026-03-07, but this might not be necessary, if we wait with submitting the umbrella until at least the HiFi data is public.
* **TODO**: Submit using curl:
    ```
    curl -u Username:Password -F "SUBMISSION=@submission-umbrella.xml" -F "PROJECT=@umbrella.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    ```
* **Note:** Add the assembly project `PRJEB79727` when it has been submitted and made public, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.

### Submit Hi-C

### Submit RNAseq

### Submit assembly

