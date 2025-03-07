---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB77283 (umbrella), PRJEB76283 (experiment), PRJEB76284 (assembly)
---

# BGE - *Lithobius stygius*

## Submission task description
Submission of raw reads for *Lithobius stygius* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Lithobius-stygius-metadata.xlsx)
* [BGE HiFi metadata](./data/qcLitStyg-hifi.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Collecting metadata
* I went to [BioSamples](https://www.ebi.ac.uk/biosamples/samples?text=Lithobius+stygius) and extracted all samples for this species, where SCILIFELAB was the GAL. I then looked at the delivery README for the HiFi dataset (on Uppmax) and extracted the Name (`FS42595405`). This I then pasted as filter in `Tube or well id` field, in the [ERGA tracking portal](https://genomes.cnag.cat/erga-stream/samples/) which returned biosample [SAMEA115117740](https://www.ebi.ac.uk/biosamples/samples/SAMEA115117740).

### Submitting HiFi
#### Creating xml
* I copied [submission.xml](./data/submission.xml) from BGE-Crayfish, using the same embargo date
* Running the script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qcLitStyg-hifi.tsv -p ERGA-BGE -o qcLitStyg-HiFi
    ```

#### Data transfer
* Create folder `bge-lithobius` at ENA upload area using Filezilla
* Using aspera from Uppmax to ENA upload area:
    ```
    interactive -t 03:00:00 -A naiss2023-5-307
    module load ascp
    export ASPERA_SCP_PASS='password'
    ascp -k 3 -d -q --mode=send -QT -l300M --host=webin.ebi.ac.uk --user=Webin-XXXX /proj/snic2021-6-194/INBOX/BGE_Lithobius_stygius/EBP_pr_087/files/pr_087/rawdata/pr_087_001/m84045_240505_040448_s4.hifi_reads.bc2087.bam /bge-lithobius/ &
    ```
* Keep track of progress using FileZilla

#### Programmatic submission
* Copy all xml files to Uppmax:
    ```
    scp submission.xml qcLitStyg-HiFi*.xml yvonnek@rackham.uppmax.uu.se:/home/yvonnek/BGE-lithobius/
    ```
* Submit both projects and experiment in one go, i.e:
    ```
    interactive -t 03:00:00 -A naiss2023-5-307
    curl -u username:password -F "SUBMISSION=@submission.xml"  -F "PROJECT=@qcLitStyg-HiFi.study.xml" -F "EXPERIMENT=@qcLitStyg-HiFi.exp.xml" -F "RUN=@qcLitStyg-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-06-04T08:44:47.136+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX12562222" alias="exp_qcLitStyg1_HiFi_WGS_FS42595405" status="PRIVATE"/>
        <RUN accession="ERR13191080" alias="run_qcLitStyg1_HiFi_WGS_FS42595405_bam_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB76283" alias="erga-bge-qcLitStyg-study-rawdata-2024-06-04" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP160841" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB76284" alias="erga-bge-qcLitStyg1_primary-2024-06-04" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP160842" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA30577677" alias="SUBMISSION-04-06-2024-08:44:46:768"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
* Update of submission status at [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/)

### Submit HiC
* For the sample data, `ERGA EB 5301 05` was given from NGI. I went to Biosample, and found 2 possible samples, SAMEA115117737 and SAMEA115117716
* In the ERGA tracking portal, only the first was found (which is derived/same as the second). Hence, SAMEA115117737 with tube id FS42595408, was used.
* First batch of HiC will be used, hence need to do data transfer (which I did for all first batch HiC in one go, but below is xample of how to):
    ```
    interactive -t 08:00:00 -A uppmax2025-2-58
    cat sample_GCAGGTTC+TTGCTTCT_part*_R1.fastq.gz > ../to_ENA/litStyg_sample_GCAGGTTC+TTGCTTCT_R1.fastq.gz
    cat sample_GCAGGTTC+TTGCTTCT_part*_R2.fastq.gz > ../to_ENA/litStyg_sample_GCAGGTTC+TTGCTTCT_R2.fastq.gz
    cd ../to_ENA
    lftp webin2.ebi.ac.uk -u Webin-39907
    mput litStyg*.fastq.gz
    ```

### Submit RNA-Seq
* Data transfer to ENA upload area (folder /bge-rnaseq/) was done previously for all RNAseq data (first batch)
* Create [qcLitStyg-RNAseq.tsv](./data/qcLitStyg-RNAseq.tsv)
    * Note: used biosample with well id `FS42595406` in erga tracking portal
* Create [submission-noHold.xml](./data/submission-noHold.xml), without any hold date since study is public already
* Run CNAG script
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qcLitStyg-RNAseq.tsv -p ERGA-BGE -o qcLitStyg-RNAseq
    ```
* Validate output (ignore the study xml)
* Update qcLitStyg-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB76283"/>
    ```
* Copy xml files to Uppmax
    ```
    scp qcLitStyg-RNAseq.exp.xml qcLitStyg-RNAseq.runs.xml submission-noHold.xml yvonnek@rackham.uppmax.uu.se:/home/yvonnek/BGE-lithobius/
    ```
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission-noHold.xml" -F "EXPERIMENT=@qcLitStyg-RNAseq.exp.xml" -F "RUN=@qcLitStyg-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"   
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-10-18T14:07:32.612+01:00" submissionFile="submission-noHold.xml" success="true">
        <EXPERIMENT accession="ERX13254552" alias="exp_qcLitStyg_Illumina_RNA-Seq_FS42595406_RE023-1A" status="PRIVATE"/>
        <RUN accession="ERR13851786" alias="run_qcLitStyg_Illumina_RNA-Seq_FS42595406_RE023-1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA30887149" alias="SUBMISSION-18-10-2024-14:07:32:414"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    </RECEIPT>
    ```

* Add recevied accession numbers to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `RNA-seq submitted` to `yes`

## Umbrella project
For each of the BGE species, an umbrella project has to be created and linked to the main BGE project, [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

* There is a CNAG script, that should do the deed of creating the xml file:
    ```
    ./script/get_umbrella_xml_ENA.py -s "Lithobius stygius" -t qcLitStyg1 -p ERGA-BGE -c SCILIFELAB -a PRJEB76283 -x 2750798
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
    <RECEIPT receiptDate="2024-07-05T13:23:11.589+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB77283" alias="erga-bge-qcLitStyg-study-umbrella-2024-07-05" status="PRIVATE" holdUntilDate="2024-07-07+01:00"/>
        <SUBMISSION accession="ERA30670052" alias="SUBMISSION-05-07-2024-13:23:11:288"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
* **Note:** Add the assembly project `PRJEB76284` when it has been submitted and made public, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.
