---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB76972
---

# BGE - *Hydropglyphus hamulatus*

## Submission task description
Submission of raw reads for *Hydropglyphus hamulatus* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.

## Procedure overview and links to examples

* [ERGA-BGE_ReadData_Submission_Guide](https://github.com/ERGA-consortium/ERGA-submission/blob/main/BGE/ERGA-BGE_ReadData_Submission_Guide.md)
* [BGE mRupRup umbrella project](https://www.ncbi.nlm.nih.gov/bioproject/1084634)

## Lessons learned

## Detailed step by step description

### Collect metadata
* There were 36 BioSamples collected and registered for the species. From NGI the sample tube register number FS55571874 bridged via the ERGA reporting portal to the specific sample [SAMEA114554671](https://www.ebi.ac.uk/biosamples/samples/SAMEA114554671) that was used for sequencing (corresponding to specimen ID - ERGA JB 4431 00002). 

### Register study
* Title, abstract, and keyword for the study was set according to ERGA recommendations.
* Release date was initially set 2 years in the future, but as it was decided that all raw data should be released immediately, the date was soon changed to release the same week. 
* The study was registered via the browser, using NBIS DM broker account, received accession number: `PRJEB76972`

### Submit HiFi
* Information on experiment metadata was provided by NGI via Slack and entered into a [spreadsheet](./data/PRJEB76972-experiment.tsv). Staff at NGI also told that the genome size was smaller than initially anticipated, and that sufficient coverage was reached with a single HiFi run (two were produced). It was decided that both raw data files (.bam) would be published even if these were to be joined by the Bioinformatician working with the data. 

* Sequence files were ingested to the ENA via terminal from the file directory Rackham using the command line: 
```
ascp -QT -l300M -k 1 m84045_240620_060113_s4.hifi_reads.bc205[2/3].bam Webin-39907@webin.ebi.ac.uk:.
```

Since upload speeds were very low, a solution was to copy the files to `nobackup` on Rackham where upload speeds were significantly higher (for some reason).

* Manifests were made from the metadata spreadsheet by using a modified script [get_ENA_XML_files_yv.py](scripts/get_ENA_XML_files_yv.py), generating XML files for Study (not used), [Experiment](ENA/BGE-Hydroglyphus-hamulatus/data/PRJEB76972.exp.xml) and [Runs](ENA/BGE-Hydroglyphus-hamulatus/data/PRJEB76972.runs.xml). Also, md5 sums had calculated for each data file and included in the spreadsheet. 

* Since the scripts automatically separated the two datasets into separate Studies, the XML's were modified to include both datasets in the already registered Study. Also, since the Study was already registered via the ENA portal, the referencing line was changed to:

  `<STUDY_REF accession="PRJEB76972"/>`

* A [submission.xml](ENA/BGE-Hydroglyphus-hamulatus/data/submission.xml) file was made according to ENA specifications.

* Manifests were submitted to ENA via curl:

```
curl -u Webin-39907:<password> -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@PRJEB76972.exp.xml" -F "RUN=@PRJEB76972.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
```

* Received accession numbers: `ERX12708954`, `ERR13337980`, `ERX12708955`, `ERR13337981`

### Submit Hi-C

### Submit RNAseq

### Submit assembly

### Create umbrella

For each of the BGE species, an umbrella project has to be created and linked to the main BGE project, [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

* There is a CNAG script, that should do the deed of creating the xml file:
    ```
    ./script/get_umbrella_xml_ENA.py -s "Hydroglyphus hamulatus" -t icHydHamu2 -p ERGA-BGE -c SCILIFELAB -a PRJEB76972 -x 3078427
    ```
* Create a [submission-umbrella.xml](ENA/BGE-Hydroglyphus-hamulatus/data/submission-umbrella.xml)
* Submit using curl:
    ```
    curl -u Username:Password -F "SUBMISSION=@submission-umbrella.xml" -F "PROJECT=@umbrella.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
   <RECEIPT receiptDate="2024-07-05T13:49:57.156+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB77288" alias="erga-bge-icHydHamu-study-umbrella-2024-07-05" status="PRIVATE" holdUntilDate="2024-07-07+01:00"/>
        <SUBMISSION accession="ERA30670091" alias="SUBMISSION-05-07-2024-13:49:56:891"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>

 
 
 
                                                                                                                                                                                                                   
    ```



