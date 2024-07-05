---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB77287, PRJEB74039
---

# BGE - *Tetrastemma melanocephalum*

## Submission task description
Submission of raw reads for *Tetrastemma melanocephalum* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Tetrastemma-melanocephalum-metadata.xlsx)
* [ERGA-BGE_ReadData_Submission_Guide](https://github.com/ERGA-consortium/ERGA-submission/blob/main/BGE/ERGA-BGE_ReadData_Submission_Guide.md)
* [BGE mRupRup umbrella project](https://www.ncbi.nlm.nih.gov/bioproject/1084634)

## Lessons learned

## Detailed step by step description

### Collect metadata
* There were 2 BioSamples that matched the label provided by NGI (ERGA_FAFA_7377_007) in their README file, [SAMEA113595490](https://www.ebi.ac.uk/biosamples/samples/SAMEA113595490) and [SAMEA113595480](https://www.ebi.ac.uk/biosamples/samples/SAMEA113595480). NGI confirmed that it was the latter that should be used (the former is derived from the latter). 

### Register study
* Title and abstract for the study was decided together with a colleague.
* Release date was set 2 years in the future, 2026-03-07, but it is likely that the study will be released as soon as the rest of the sequencing datasets have been produced and submitted. At the latest, we expect the datasets to be public when the assembly has been submitted as well.
* The study was registered via the browser, using NBIS DM broker account, received accession number: `PRJEB74039`
* Study was updated according to instructions in ERGA-BGE submission guide, with new title, name, and description. Also, added a study attribute (keyword, ERGA-BGE).
* By looking at actual examples of submission, study name was changed (index removed, ToLID with index is used for study name of assembly).

### Submit HiFi
* NGI filled and checked the experiment metadata
* A [HiFi manifest](./data/reads-PacBio-HiFi-manifest.txt) was created by downloading a manifest template from [NBIS DM>Data publication>ENA>ERGA_VR-EBP](https://drive.google.com/drive/folders/1VOXZot7ji1Ea5KZFvmb2Pbm9YGtHwy99) google drive
* The submission was validated and submitted at Uppmax using Webin-CLI:
```
  interactive -t 03:00:00 -A naiss2023-5-307
  module load ascp
  java -jar ../webin-cli-7.0.1.jar -ascp -context reads -userName $1 -password $2 -manifest reads-PacBio-HiFi-manifest.txt -outputDir Webin_output/ -submit
```
* Received accession number: `ERX12137345`, `ERR12764136`

### Submit Hi-C

### Submit RNAseq

### Submit assembly

For each of the BGE species, an umbrella project has to be created and linked to the main BGE project, [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

* There is a CNAG script, that should do the deed of creating the xml file:
    ```
    ./script/get_umbrella_xml_ENA.py -s "Tetrastemma melanocephalum" -t tnTetMela7 -p ERGA-BGE -c SCILIFELAB -a PRJEB74039 -x 307678
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
    <RECEIPT receiptDate="2024-07-05T13:37:05.023+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB77287" alias="erga-bge-tnTetMela-study-umbrella-2024-07-05" status="PRIVATE" holdUntilDate="2024-07-07+01:00"/>
        <SUBMISSION accession="ERA30670089" alias="SUBMISSION-05-07-2024-13:37:04:733"/>
        <MESSAGES>
              <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
* **Note:** Add the assembly project when it has been created and submitted and made public, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.
