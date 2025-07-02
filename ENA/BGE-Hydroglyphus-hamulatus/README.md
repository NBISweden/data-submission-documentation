---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB77288 (umbrella), PRJEB76972 (experiment)
---

# BGE - *Hydropglyphus hamulatus*

## Submission task description
Submission of raw reads for *Hydropglyphus hamulatus* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.

## Procedure overview and links to examples

* [ERGA-BGE_ReadData_Submission_Guide](https://github.com/ERGA-consortium/ERGA-submission/blob/main/BGE/ERGA-BGE_ReadData_Submission_Guide.md)
* [BGE mRupRup umbrella project](https://www.ncbi.nlm.nih.gov/bioproject/1084634)

## Lessons learned

* Create a virtual sample, when 2 (or more) biosamples have been used in order to create enough material

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

* Manifests were made from the metadata spreadsheet by using a modified script [get_ENA_XML_files_yv.py](./scripts/get_ENA_XML_files_yv.py), generating XML files for Study (not used), [Experiment](./data/PRJEB76972.exp.xml) and [Runs](./data/PRJEB76972.runs.xml). Also, md5 sums had calculated for each data file and included in the spreadsheet. 

* Since the scripts automatically separated the two datasets into separate Studies, the XML's were modified to include both datasets in the already registered Study. Also, since the Study was already registered via the ENA portal, the referencing line was changed to:

  `<STUDY_REF accession="PRJEB76972"/>`

* A [submission.xml](./data/submission.xml) file was made according to ENA specifications.

* Manifests were submitted to ENA via curl:

```
curl -u Webin-39907:<password> -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@PRJEB76972.exp.xml" -F "RUN=@PRJEB76972.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
```

* Received accession numbers: `ERX12708954`, `ERR13337980`, `ERX12708955`, `ERR13337981`

* **Note:** I was unaware that this was ULI when submitting HiFi reads. Hence, when trimmed fastq reads are available, these should be uploaded and replace .bam (or add barcode info in metadata i.e. in library_construction_protocol)

### Submit Hi-C

#### Preparations

* 4 samples were used, hence a virtual sample was needed:
    * Biosamples: SAMEA114554682, SAMEA114554684, SAMEA114554685, SAMEA114554686
    * Biosamples were deduced given the 'tube or well id's' received from UGC and looked up in the ERGA tracking portal
    * [icHydHamu-HiC-virtual-sample.tsv](./data/icHydHamu-HiC-virtual-sample.tsv)
    * Accession number received: ERS22139701
* First batch of HiC will be used, hence need to do data transfer (which I did for all first batch HiC in one go, but below is example of how to):
    ```
    interactive -t 08:00:00 -A uppmax2025-2-58
    cat sample_TAGAGCTC+TTCGGTAG_part*_R1.fastq.gz > ../to_ENA/hydHamu_sample_TAGAGCTC+TTCGGTAG_R1.fastq.gz
    cat sample_TAGAGCTC+TTCGGTAG_part*_R2.fastq.gz > ../to_ENA/hydHamu_sample_TAGAGCTC+TTCGGTAG_R2.fastq.gz
    cd ../to_ENA
    lftp webin2.ebi.ac.uk -u Webin-39907
    mput hydHamu*.fastq.gz
    ```
#### XML
* I created [icHydHamu-HiC.tsv](./data/icHydHamu-HiC.tsv).
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icHydHamu-HiC.tsv -p ERGA-BGE -o icHydHamu-HiC
    ```
* Update icHydHamu-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB76972"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is already public, so submission-noHold.xml without hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission-noHold.xml" -F "EXPERIMENT=@icHydHamu-HiC.exp.xml" -F "RUN=@icHydHamu-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-03-19T10:25:55.090Z" submissionFile="submission-noHold.xml" success="true">
        <EXPERIMENT accession="ERX14162757" alias="exp_icHydHamu_Hi-C_FS55571885_FS55571887-89_HC009-1A1A" status="PRIVATE"/>
        <RUN accession="ERR14758863" alias="run_icHydHamu_Hi-C_FS55571885_FS55571887-89_HC009-1A1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA31211438" alias="SUBMISSION-19-03-2025-10:25:53:396"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    </RECEIPT>
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit RNA-Seq
* Data transfer to ENA upload area (folder /bge-rnaseq/) was done previously for all RNAseq data (first batch)
* Create [icHydHamu-RNAseq.tsv](./data/icHydHamu-RNAseq.tsv)
    * Note: the RNAsheet delivered by SNP&SEQ indicates 2 tube or well id's `FS55571879+FS55571880`. In erga tracking portal, these point to 2 different biosamples which in turn are derived from 2 different original samples: `FS55571879 -> SAMEA114554676 -> SAMEA114554658`, `FS55571880 -> SAMEA114554677 -> SAMEA114554659`. The ToLId's varies as well, what to do? On both of these it states that they are extra sequencing exemplars of specimen id `ERGA JB 4431 00001` (`SAMEA114554670`), should I use that one instead? It is ToLId icHydHamu1, tube or well id `FS55571873`. I've asked NGI coordinators (in dedicated #bge_ngi_metadata slack channel)
    * I had to create a virtual sample, that refers to them both, and submit to ENA: [icHydHamu-RNA-virtual-sample.tsv](./data/icHydHamu-RNA-virtual-sample.tsv)
    * Accession number received: ERS21379198
* Create [submission-noHold.xml](./data/submission-noHold.xml), without any hold date since study is public already
* Run CNAG script
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icHydHamu-RNAseq.tsv -p ERGA-BGE -o icHydHamu-RNAseq
    ```
* Validate output (ignore the study xml)
* Update icHydHamu-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB76972"/>
    ```
* Copy xml files to Uppmax
    ```
    scp icHydHamu-RNAseq.exp.xml icHydHamu-RNAseq.runs.xml submission-noHold.xml yvonnek@rackham.uppmax.uu.se:/home/yvonnek/BGE-hydroglyphus/
    ```
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission-noHold.xml" -F "EXPERIMENT=@icHydHamu-RNAseq.exp.xml" -F "RUN=@icHydHamu-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"   
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-10-29T13:29:23.215Z" submissionFile="submission-noHold.xml" success="true">
        <EXPERIMENT accession="ERX13311160" alias="exp_icHydHamu_Illumina_RNA-Seq_FS55571879_FS55571880_RE021-2A" status="PRIVATE"/>
        <RUN accession="ERR13909341" alias="run_icHydHamu_Illumina_RNA-Seq_FS55571879_FS55571880_RE021-2A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA30918368" alias="SUBMISSION-29-10-2024-13:29:22:983"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    </RECEIPT>
    ```

* Add recevied accession numbers to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `RNA-seq submitted` to `yes`

### Submit assembly

### Create umbrella

For each of the BGE species, an umbrella project has to be created and linked to the main BGE project, [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

* There is a CNAG script, that should do the deed of creating the xml file:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Hydroglyphus hamulatus" -t icHydHamu2 -p ERGA-BGE -c SCILIFELAB -a PRJEB76972 -x 3078427
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



