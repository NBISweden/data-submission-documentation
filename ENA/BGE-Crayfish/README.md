---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: 
---

# BGE - *Austropotamobius torrentium* (stone crayfish)
## Submission task description
Submission of raw reads for *Austropotamobius torrentium* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Austropotamobius-torrentium-metadata.xlsx)
* [BGE metadata](./data/qmAusTorr-BGE.tsv)

## Lessons learned
* Trying programmatic submission, using CNAG scripts to produce xml files for studies and experiments
* There's been some struggle regarding HiFi sequencing on this species, has been done in several rounds, resulting in 3 separate deliveries from NGI. There was some uncertanties on which datasets to submit.

## Detailed step by step description

### Collect metadata
* Looking at BioSamples, 20 samples in total are candidates, 10 are same as one of the other 10.
* Looking at the HiFi deliveries, in the README files (there are 3 of them), all refer to 2(!) samples, ERGA_DS_328X_04_(01+02) as UGC_user_id (UGC_id is pr_047_001). Which sample do we submit the datasets to? Need to ask NGI/UGC
    * Answer from NGI is to use [SAMEA112878228](https://www.ebi.ac.uk/biosamples/samples/SAMEA112878228)
* Looking at the HiC delivery, they only have 8 'internal' samples, no indication on which BioSample might have been used. Need to ask NGI/SNP&SEQ.

### Create xml
* A [submission.xml](./data/submission.xml) needs to be created manually, which includes the action (ADD) and release date (HOLD).

While not complete information yet, I wanted to try using the script on this species:
```
../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qmAusTorr-BGE.tsv -p ERGA-BGE -o qmAusTorr
```
* Only run.xml for HiC data, why? 
    * Answer: I didn't have 'native_file_name' column name, only 'file_name'
* For Hi-C, there's an additional read type line, apart from PAIRED: `<READ_TYPE>sample_barcode</READ_TYPE>`, should it be there?
* There is not place to put insert_size in tsv, is it? But for paired reads it is mandatory, isn't it? When I did a trial submission (see below), I got no error so if it is not possible to get the insert size from NGI, at least programmatic submission is a way to escape.
* We received insert size for th HiC data, **this must be added manually** to the experiment xml:
    ```
    <LIBRARY_LAYOUT>
        <PAIRED NOMINAL_LENGTH=""/>
    </LIBRARY_LAYOUT>
    ```

### Upload sequences to ENA

* Use 2 subdirectories at ENA upload area, `bge-crayfish-HiFi` and `bge-crayfish-HiC` (create them previous to upload using FileZilla)
* Create a shell script, go-ascp-crayfish.sh with aspera commands, use the version that loggs transfers which can continue partial (failed) transfers:
    ```
    ascp -k 3 -d -q --mode=send -QT -l300M --host=webin.ebi.ac.uk --user=Webin-XXXX /path/to/*.bam /bge-crayfish-HiFi/ &
    ascp -k 3 -d -q --mode=send -QT -l300M --host=webin.ebi.ac.uk --user=Webin-XXXX /path/to/*.fastq /bge-crayfish-HiC/ &
    ```
* At Uppmax:
    ```
    tr -d '\r' < go-ascp-crayfish.sh.txt > go-ascp-crayfish.sh
    chmod 777 go-ascp-crayfish.sh
    interactive -t 08:00:00 -A naiss2023-5-307
    module load ascp
    export ASPERA_SCP_PASS='password'
    ./go-ascp-crayfish.sh &
    ```
* In the end I decided to remove the & ending each line, in order to run sequentially, and also divided HiC into one script and HiFi into another, and just run those in background (i.e. using &). 
* Keep track of upload success using FileZilla

### Programmatic submission
* Copy all xml files to Uppmax:
    ```
    scp submission.xml qmAusTorr.*.xml yvonnek@rackham.uppmax.uu.se:/home/yvonnek/BGE-crayfish/
    ```
* I think I will do a test drive, since I've never submitted programmatically, is it possible to submit both projects and experiment in one go, i.e:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml"  -F "PROJECT=@qmAusTorr.study.xml" -F "EXPERIMENT=@qmAusTorr.exp.xml" -F "RUN=@qmAusTorr.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```

### Test programmatic submission
* Copy all xml files to Uppmax:
    ```
    scp submission.xml qmAusTorr.*.xml yvonnek@rackham.uppmax.uu.se:/home/yvonnek/BGE-crayfish/
    ```
* I think I will do a test drive, since I've never submitted programmatically, is it possible to submit both projects and experiment in one go, i.e:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml"  -F "PROJECT=@qmAusTorr.study.xml" -F "EXPERIMENT=@qmAusTorr.exp.xml" -F "RUN=@qmAusTorr.runs.xml" "https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* If not possible to submit both levels of data, I will need to create another submission.xml file, without the release dat, for experiment submission.
* There's also a possibility to submit xmls via Webin Portal

```
<ERROR>Failed to validate run xml, error: string value 'BAM' is not a valid enumeration value for type of filetype attribute in type of FILE element in type of FILES element in type of DATA_BLOCK element in RunType</ERROR>
```
* I updated the code to output 'bam' instead, then it worked:
```
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
<RECEIPT receiptDate="2024-05-30T07:08:53.000+01:00" submissionFile="submission.xml" success="true">
     <EXPERIMENT accession="ERX12547823" alias="exp_qmAusTorr9_Hifi_WGS_pr_047_001" status="PRIVATE"/>
     <EXPERIMENT accession="ERX12547824" alias="exp_qmAusTorr9_Hi-C_XD-3967" status="PRIVATE"/>
     <RUN accession="ERR13176447" alias="run_qmAusTorr9_Hifi_WGS_pr_047_001_bam_1" status="PRIVATE"/>
     <RUN accession="ERR13176448" alias="run_qmAusTorr9_Hifi_WGS_pr_047_001_bam_2" status="PRIVATE"/>
     <RUN accession="ERR13176449" alias="run_qmAusTorr9_Hifi_WGS_pr_047_001_bam_3" status="PRIVATE"/>
     <RUN accession="ERR13176450" alias="run_qmAusTorr9_Hifi_WGS_pr_047_001_bam_4" status="PRIVATE"/>
     <RUN accession="ERR13176451" alias="run_qmAusTorr9_Hifi_WGS_pr_047_001_bam_5" status="PRIVATE"/>
     <RUN accession="ERR13176452" alias="run_qmAusTorr9_Hifi_WGS_pr_047_001_bam_6" status="PRIVATE"/>
     <RUN accession="ERR13176453" alias="run_qmAusTorr9_Hifi_WGS_pr_047_001_bam_7" status="PRIVATE"/>
     <RUN accession="ERR13176454" alias="run_qmAusTorr9_Hi-C_XD-3967_fastq_1" status="PRIVATE"/>
     <RUN accession="ERR13176455" alias="run_qmAusTorr9_Hi-C_XD-3967_fastq_2" status="PRIVATE"/>
     <RUN accession="ERR13176456" alias="run_qmAusTorr9_Hi-C_XD-3967_fastq_3" status="PRIVATE"/>
     <RUN accession="ERR13176457" alias="run_qmAusTorr9_Hi-C_XD-3967_fastq_4" status="PRIVATE"/>
     <RUN accession="ERR13176458" alias="run_qmAusTorr9_Hi-C_XD-3967_fastq_5" status="PRIVATE"/>
     <RUN accession="ERR13176459" alias="run_qmAusTorr9_Hi-C_XD-3967_fastq_6" status="PRIVATE"/>
     <RUN accession="ERR13176460" alias="run_qmAusTorr9_Hi-C_XD-3967_fastq_7" status="PRIVATE"/>
     <RUN accession="ERR13176461" alias="run_qmAusTorr9_Hi-C_XD-3967_fastq_8" status="PRIVATE"/>
     <PROJECT accession="PRJEB76181" alias="erga-bge-qmAusTorr-study-rawdata-2024-05-30" status="PRIVATE" holdUntilDate="2026-03-07Z">
          <EXT_ID accession="ERP160734" type="study"/>
     </PROJECT>
     <PROJECT accession="PRJEB76182" alias="erga-bge-qmAusTorr9_primary-2024-05-30" status="PRIVATE" holdUntilDate="2026-03-07Z">
          <EXT_ID accession="ERP160735" type="study"/>
     </PROJECT>
     <SUBMISSION accession="ERA30540703" alias="SUBMISSION-30-05-2024-07:08:51:258"/>
     <MESSAGES>
          <INFO>All objects in this submission are set to private status (HOLD).</INFO>
          <INFO>This submission is a TEST submission and will be discarded within 24 hours</INFO>
     </MESSAGES>
     <ACTIONS>ADD</ACTIONS>
     <ACTIONS>HOLD</ACTIONS>
```
* Since it *is* possible to submit all at once, I will wait until I have all HiC metadata before I submit for real.

* The xml script is not fully funtioning, insert size for paired reads is missing, and read_type 'sample_barcode' should likely be added to HiFi data, hence these needs to be added manually in the output run xmls for now.
