---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB80085 (umbrella), PRJEB79894 (experiment), PRJEB80032 (assembly)
---

# BGE - *Triaenophorus nodulosus*

## Submission task description
Submission of raw reads for *Triaenophorus nodulosus* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.

## Procedure overview and links to examples

* [ERGA-BGE_ReadData_Submission_Guide](https://github.com/ERGA-consortium/ERGA-submission/blob/main/BGE/ERGA-BGE_ReadData_Submission_Guide.md)

## Lessons learned
For this particular species it was not possible to identify an NGI tube or well ID. The BioSample used for sequencing (SAMEA115098039) is not referenced with a tube or well ID in the [ERGA portal](https://genomes.cnag.cat/erga-stream/). Actually, it is not referenced at all. To proceed with the submission the NGI delivery folder name was used (`pr_111`).

### Collect metadata
* There were 18 BioSamples collected and registered for the species. The NGI tube register number was not possible to bridge (see above). After contact with NGI it was determined that the sample used ((SAMEA115098039) was identified as TolID `heTriNodu1`, corresponding to the specimen ID `ERGA AV 5534 02`. 

### Register study
* Title, abstract, and keyword for the study was set according to ERGA recommendations.
* Release date was set 2 years in the future. As we are still waiting for Hi-C data and only have HiFi data yet, we have decided in the DM team to delay making the data public for a while and allow for the other data types to be available. 
* The study was registered via the browser, using NBIS DM broker account, received accession number: `PRJEB79894`

### Submit HiFi
* Information on experiment metadata was provided by NGI via Slack and entered into a [spreadsheet](./data/PRJEB79894-experiment.tsv).

* Sequence file was uploaded from Rackham to the ENA, after exporting the ENA broker password, using the command line:

```
ascp -k 3 -d -q --mode=send -QT -l300M --host=webin.ebi.ac.u
k -userName=Webin-39907 /proj/snic2022-6-208/INBOX/BGE_Triaenophorus_nodulosus/EBP_pr_111/files/pr_111/rawdata/pr_111_001/m84045_240818_005314_s2.hifi_reads.bc2118.bam /bge-triaenophorus/ &
```
Upload was slow to begin (~25 mins) but once begun it uploaded as expected.

* Manifests were made from the metadata spreadsheet by using a modified script [get_ENA_XML_files_yv.py](./scripts/get_ENA_XML_files_yv.py), generating XML files for Study (not used), [Experiment](./data/heTriNodu-HiFi.exp.xml) and [Runs](./data/heTriNodu-HiFi.runs.xml). Also, an md5 sum was calculated for each data file and included in the spreadsheet. 

* A [submission.xml](./data/submission.xml) file was made according to ENA specifications.

* Due to circumstances the manifests were submitted via the web portal this time without trouble, hence the separate registration of sequence and annotation projects.

* Received accession numbers: `ERX13023779`,`ERR13654568`

### Submit Hi-C

### Submit RNAseq

### Submit assembly

* A study / project was created, receiving accession number `PRJEB80032`
* Yvonnes note: Not sure how it was registered, hence lack of information other than the accession number. 

### Create umbrella

For each of the BGE species, an umbrella project has to be created and linked to the main BGE project, [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

* Using the CNAG script:
    ```
    ./script/get_umbrella_xml_ENA.py -s "Triaenophorus nodulosus" -t heTriNodu1 -p ERGA-BGE -c SCILIFELAB -a PRJEB79894 -x 56557
    ```
* Create a [submission-umbrella.xml](./scripts/submission-umbrella.xml)

* Submit using curl:
    ```
    curl -u Username:Password -F "SUBMISSION=@submission-umbrella.xml" -F "PROJECT=@umbrella.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-09-12T14:41:48.893+01:00" submissionFile="submission-umbrella.xml" success="true">
     <PROJECT accession="PRJEB80085" alias="erga-bge-heTriNodu-study-umbrella-2024-09-12" status="PRIVATE" holdUntilDate="2026-09-12+01:00"/>
     <SUBMISSION accession="ERA30790827" alias="SUBMISSION-12-09-2024-14:41:48:346"/>
     <MESSAGES>
          <INFO>All objects in this submission are set to private status (HOLD).</INFO>
     </MESSAGES>
     <ACTIONS>ADD</ACTIONS>
     <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>  
    ```
* **TODO:** Add the assembly study `PRJEB80032` as child to the umbrella project as well (currently only the genomic sequencing project is attached)
