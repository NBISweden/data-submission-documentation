---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB77286 (umbrella), PRJEB74038 (experiment)
---

# BGE - *Siphonaria pectinata*

## Submission task description
Submission of raw reads for *Siphonaria pectinata* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Siphonaria-pectinata-metadata.xlsx)
* [ERGA-BGE_ReadData_Submission_Guide](https://github.com/ERGA-consortium/ERGA-submission/blob/main/BGE/ERGA-BGE_ReadData_Submission_Guide.md)
* [BGE mRupRup umbrella project](https://www.ncbi.nlm.nih.gov/bioproject/1084634)

## Lessons learned
* When it comes to preregistered samples, done via COPO, there is a struggle to identify which sample has been used for sequencing. Ideally the data producer would use the BioSample accession number instead of an identifier that is found in several of the registered samples.

## Detailed step by step description

### Collect metadata
* There were 2 BioSamples that matched the label provided by NGI (ERGA_KE_1616_002) in their README file, [SAMEA113595500](https://www.ebi.ac.uk/biosamples/samples/SAMEA113595500) and [SAMEA113595495](https://www.ebi.ac.uk/biosamples/samples/SAMEA113595495). NGI confirmed that it was the latter that should be used (the former is derived from the latter). 

### Register study
* Title and abstract for the study was decided together with a colleague.
* Release date was set 2 years in the future, 2026-03-07, but it is likely that the study will be released as soon as the rest of the sequencing datasets have been produced and submitted. At the latest, we expect the datasets to be public when the assembly has been submitted as well.
* The study was registered via the browser, using NBIS DM broker account, received accession number: `PRJEB74038`
* Study was updated according to instructions in ERGA-BGE submission guide, with new title, name, and description. Also, added a study attribute (keyword, ERGA-BGE).
* By looking at actual examples of submission, study name was changed (index removed, ToLID with index is used for study name of assembly).

### Submit HiFi
* NGI filled and checked the experiment metadata
* Both fastq and bam files were available. Together with a colleague, it was decided to submit the bam file.
* A [HiFi manifest](./data/reads-PacBio-HiFi-manifest.txt) was created by downloading a manifest template from [NBIS DM>Data publication>ENA>ERGA_VR-EBP](https://drive.google.com/drive/folders/1VOXZot7ji1Ea5KZFvmb2Pbm9YGtHwy99) google drive
* The submission was validated and submitted at Uppmax using Webin-CLI:
```
  interactive -t 03:00:00 -A naiss2023-5-307
  module load ascp
  java -jar ../webin-cli-7.0.1.jar -ascp -context reads -userName $1 -password $2 -manifest reads-PacBio-HiFi-manifest.txt -outputDir Webin_output/ -submit
```
* Note on validation: I first tried using the study alias (SipPec1) in the manifest file but received an error that it was unknown. Hence, always use the study accession number.
* Received accession number: `ERX12137308`, `ERR12764099`

### Submit Hi-C

### Submit RNA-Seq
* Data transfer to ENA upload area (folder /bge-rnaseq/) was done previously for all RNAseq data (first batch)
* Create [xgSipPect-RNAseq.tsv](./data/xgSipPect-RNAseq.tsv)
    * Note: used biosample with well id `Spec-3` in erga tracking portal
* Create [submission-noHold.xml](./data/submission-noHold.xml), without any hold date since study is public already
* Run CNAG script
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f xgSipPect-RNAseq.tsv -p ERGA-BGE -o xgSipPect-RNAseq
    ```
* Validate output (ignore the study xml)
* Update xgSipPect-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB74038"/>
    ```
* Copy xml files to Uppmax
    ```
    scp xgSipPect-RNAseq.exp.xml xgSipPect-RNAseq.runs.xml submission-noHold.xml yvonnek@rackham.uppmax.uu.se:/home/yvonnek/BGE-siphonaria/
    ```
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission-noHold.xml" -F "EXPERIMENT=@xgSipPect-RNAseq.exp.xml" -F "RUN=@xgSipPect-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"   
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-10-18T12:59:13.489+01:00" submissionFile="submission-noHold.xml" success="true">
        <EXPERIMENT accession="ERX13251380" alias="exp_xgSipPect_Illumina_RNA-Seq_Spec-3_RE018-2B" status="PRIVATE"/>
        <RUN accession="ERR13848614" alias="run_xgSipPect_Illumina_RNA-Seq_Spec-3_RE018-2B_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA30886728" alias="SUBMISSION-18-10-2024-12:59:13:167"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    </RECEIPT>
    ```

* Add recevied accession numbers to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `RNA-seq submitted` to `yes`

### Submit assembly

### Umbrella project
For each of the BGE species, an umbrella project has to be created and linked to the main BGE project, [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

* There is a CNAG script, that should do the deed of creating the xml file:
    ```
    ./script/get_umbrella_xml_ENA.py -s "Siphonaria pectinata" -t xgSipPect2 -p ERGA-BGE -c SCILIFELAB -a PRJEB74038 -x 57642
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
    <RECEIPT receiptDate="2024-07-05T13:32:34.259+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB77286" alias="erga-bge-xgSipPect-study-umbrella-2024-07-05" status="PRIVATE" holdUntilDate="2024-07-07+01:00"/>
        <SUBMISSION accession="ERA30670067" alias="SUBMISSION-05-07-2024-13:32:34:071"/>
        <MESSAGES>
              <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
* **Note:** Add the assembly project when it has been created and submitted and made public, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.
