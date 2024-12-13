---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB77281 (umbrella), PRJEB76281 (experiment)
---

# BGE - *Astagobius angustatus*

## Submission task description
Submission of raw reads for *Astagobius angustatus* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Astagobius-angustatus-metadata.xlsx)
* [BGE HiFi metadata](./data/icAstAngu-hifi.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Collecting metadata
* I then looked at the delivery README for the HiFi dataset (on Uppmax) and extracted the Name (`ERGA_TD_5269_06`). I then went to [BioSamples](https://www.ebi.ac.uk/biosamples/samples?text=Astagobius+angustatus&page=2) and extracted the 2 samples that had this name as `specimen_id`. Since `SAMEA113399603` was the same as `SAMEA113399597`, I decided to use the latter. 
* I checked the [ERGA tracking portal](https://genomes.cnag.cat/erga-stream/samples/), using both the biosample accession number as well as the species name, but there was no hit. I guess in this case we will not have a tube or well id, so will use UGC user id (`pr_056_001`) instead.
### Submit HiFi
#### Creating xml
* I copied [submission.xml](./data/submission.xml) from BGE-Crayfish, using the same embargo date
* I updated the get_ENA_xml_files.py script so that library name and title also includes PacBio
* Running the script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icAstAngu-hifi.tsv -p ERGA-BGE -o icAstAngu-HiFi
    ```

#### Data transfer
* Create folder `bge-astagobius` at ENA upload area using Filezilla
* Using aspera from Uppmax to ENA upload area:
    ```
    interactive -t 03:00:00 -A naiss2023-5-307
    module load ascp
    export ASPERA_SCP_PASS='password'
    ascp -k 3 -d -q --mode=send -QT -l300M --host=webin.ebi.ac.uk --user=Webin-XXXX /proj/snic2021-6-194/INBOX/BGE_Astagobius_angustatus/pr_056/rawdata/pr_056_001/m84045_240223_153821_s3.hifi_reads.bc2053.bam /bge-astagobius/ &
    ```
* Keep track of progress using FileZilla

#### Programmatic submission
* Copy all xml files to Uppmax:
    ```
    scp submission.xml icAstAngu-HiFi*.xml yvonnek@rackham.uppmax.uu.se:/home/yvonnek/BGE-astagobius/
    ```
* Submit both projects and experiment in one go, i.e:
    ```
    interactive -t 03:00:00 -A naiss2023-5-307
    curl -u username:password -F "SUBMISSION=@submission.xml"  -F "PROJECT=@icAstAngu-HiFi.study.xml" -F "EXPERIMENT=@icAstAngu-HiFi.exp.xml" -F "RUN=@icAstAngu-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-06-04T08:22:25.192+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX12562212" alias="exp_icAstAngu6_HiFi_WGS_pr_056_001" status="PRIVATE"/>
        <RUN accession="ERR13191070" alias="run_icAstAngu6_HiFi_WGS_pr_056_001_bam_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB76281" alias="erga-bge-icAstAngu-study-rawdata-2024-06-04" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP160839" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB76282" alias="erga-bge-icAstAngu6_primary-2024-06-04" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP160840" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA30577665" alias="SUBMISSION-04-06-2024-08:22:23:482"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
* Update of submission status at [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/)

### Submit HiC
* 2 samples were used, so a virtual sample had to be registered, referring to:
    * SAMEA113399598, well id FS42595176, icAstAngu1
    * SAMEA113399599, well id FS42595225, icAstAngu2
    * create a [icAstAngu-virtual-sample.tsv](./data/icAstAngu-virtual-sample.tsv) based on what was done for RNAseq of [Hydroglyphus hamulatus](../BGE-Hydroglyphus-hamulatus/data/icHydHamu-virtual-sample.tsv)
    * Accession number received: ERS22139083
* However, as it turned out the HiC data was useless, and there's no more material to re-sequence, so this species will not have HiC.

### Submit RNA-Seq
* Data transfer to ENA upload area (folder /bge-rnaseq/) was done previously for all RNAseq data (first batch)
* Create [icAstAngu-RNAseq.tsv](./data/icAstAngu-RNAseq.tsv)
    * Note: Another biosample (compared to HiFi) will be referred to
* Create [submission-noHold.xml](./data/submission-noHold.xml), without any hold date since study is public already
* Run CNAG script
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icAstAngu-RNAseq.tsv -p ERGA-BGE -o icAstAngu-RNAseq
    ```
* Validate output (ignore the study xml)
* Update icAstAngu-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB76281"/>
    ```
* Copy xml files to Uppmax
    ```
    scp icAstAngu-RNAseq.exp.xml icAstAngu-RNAseq.runs.xml submission-noHold.xml yvonnek@rackham.uppmax.uu.se:/home/yvonnek/BGE-astagobius/
    ```
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission-noHold.xml" -F  "EXPERIMENT=@icAstAngu-RNAseq.exp.xml" -F "RUN=@icAstAngu-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"   
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-10-18T10:30:52.089+01:00" submissionFile="submission-noHold.xml" success="true">
        <EXPERIMENT accession="ERX13250204" alias="exp_icAstAngu_Illumina_RNA-Seq_FS42595226_RE019-1B" status="PRIVATE"/>
        <RUN accession="ERR13847438" alias="run_icAstAngu_Illumina_RNA-Seq_FS42595226_RE019-1B_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA30885809" alias="SUBMISSION-18-10-2024-10:30:51:779"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    </RECEIPT>
    ```

* Add recevied accession numbers to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `RNA-seq submitted` to `yes`

### Submit assembly
* Since HiC failed for this species, the assembly (and HiFi + RNAseq) should still be submitted and made public, but denoted as a draft:
    * *"BGE wants us to upload the assembly for Astagobius, which I guess means that they want the reads uploaded as well. However, it should be marked as draft! This is what Christian writes: "Could you please upload the draft genomes and make them public? Additionally, it would be helpful to include a label in the BioProject description indicating the draft nature of these genomes, rather than referring to them as BGE or using other terminology."*
    * In practice I'm guessing that we remove the BGE label/keyword on study level and instead add 'draft', but not sure about the description/abstract part.
        * Done for both the so far private assembly study (also included draft in title) as well as for the public raw data study

### Register umbrella projekt

For each of the BGE species, an umbrella project has to be created and linked to the main BGE project, [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

* There is a CNAG script, that should do the deed of creating the xml file:
    ```
    ./script/get_umbrella_xml_ENA.py -s "Astagobius angustatus" -t icAstAngu6 -p ERGA-BGE -c SCILIFELAB -a PRJEB76281 -x 1457099
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
    <RECEIPT receiptDate="2024-07-05T13:05:10.857+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB77281" alias="erga-bge-icAstAngu-study-umbrella-2024-07-05" status="PRIVATE" holdUntilDate="2024-07-07+01:00"/>
        <SUBMISSION accession="ERA30670050" alias="SUBMISSION-05-07-2024-13:05:10:663"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
* **Note:** Add the (draft) assembly project `PRJEB76282` when it has been submitted and made public, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update. Question is if also the umbrella labels should be changed (from `ERGA-BGE` to `draft`?)