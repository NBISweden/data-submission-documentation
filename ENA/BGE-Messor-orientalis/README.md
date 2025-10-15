---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB100781 (experiment), PRJEB100782 (assembly)
---

# BGE - *Messor orientalis*

## Submission task description
Submission of raw reads for *Messor orientalis* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Messor-orientalis-metadata.xlsx)
* [BGE HiFi metadata](./data/iyMesOrie-HiFi.tsv)
* [BGE HiC metadata](./data/iyMesOrie-HiC.tsv)
* [BGE RNAseq metadata](./data/iyMesOrie-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiFi
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data HiFi data has library prep using AmpliFi protocol, thus the trimmed reads are to be submitted. This file has been provided as a .fastq file (not .bam as is usual for this data type), hence I need to make sure that the .xml file will look ok (and that script works). The data file was transferred  using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput *.fastq.gz` and added ToLID to the file using rename function in FileZilla, to make it easier to see that right file will be submitted.
#### XML
* I created [iyMesOrie-HiFi.tsv](./data/iyMesOrie-HiFi.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iyMesOrie-HiFi.tsv -p ERGA-BGE -o iyMesOrie-HiFi
    ```
* Didn't work due to expecting .bam file so I shifted column from `native_file` to `file_name` but then the .run.xml is largely empty. Hence, need to trick the script by putting the file in `native_file_name` and change ending to `.bam`, then afterwards change to appropriate values in run .xml (rows `<RUN ` and `<FILE `)
* Study is private, so submission.xml with hold date is used.

* Submit both projects and experiment in one go, i.e:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@iyMesOrie-HiFi.study.xml" -F "EXPERIMENT=@iyMesOrie-HiFi.exp.xml" -F "RUN=@iyMesOrie-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-10-15T13:45:21.571+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX15106038" alias="exp_iyMesOrie_HiFi_WGS_LV6000912094_pr_261_003" status="PRIVATE"/>
        <RUN accession="ERR15701808" alias="run_iyMesOrie_HiFi_WGS_LV6000912094_pr_261_003_fastq_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB100781" alias="erga-bge-iyMesOrie-study-rawdata-2025-10-15" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP182226" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB100782" alias="erga-bge-iyMesOrie12_primary-2025-10-15" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP182227" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA35061088" alias="SUBMISSION-15-10-2025-13:45:21:324"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>    
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit HiC
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [iyMesOrie-HiC.tsv](./data/iyMesOrie-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iyMesOrie-HiC.tsv -p ERGA-BGE -o iyMesOrie-HiC
    ```
* Update iyMesOrie-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB100781"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title, since the other data types have the platform named
* Study will be private, so submission.xml with hold date is used.
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@iyMesOrie-HiC.exp.xml" -F "RUN=@iyMesOrie-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-10-15T14:53:15.411+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX15107902" alias="exp_iyMesOrie_Hi-C_LV6000912093_HC048-1A1A" status="PRIVATE"/>
        <RUN accession="ERR15703066" alias="run_iyMesOrie_Hi-C_LV6000912093_HC048-1A1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA35061186" alias="SUBMISSION-15-10-2025-14:53:15:241"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit RNAseq - **TODO**
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [iyMesOrie-RNAseq.tsv](./data/iyMesOrie-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iyMesOrie-RNAseq.tsv -p ERGA-BGE -o iyMesOrie-RNAseq
    ```
* Update -RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB100781"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@iyMesOrie-RNAseq.exp.xml" -F "RUN=@iyMesOrie-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Umbrella project
For each of the BGE species, an **umbrella** project has to be created and linked to the main BGE project, [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

1. Release the child project via browser
1. Collect scientific name and tolId from the metadata template sheet
1. Go to [ENA browser](https://www.ebi.ac.uk/ena/browser/home) and enter the scientific name as search term
    1. To the left side, there should be a **Taxon** subheading, that gives the identifier
1. Copy experiment accession number from metadata in top of this README
* There is a CNAG script, that should do the deed of creating the xml file:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "" -t  -p ERGA-BGE -c SCILIFELAB -a  -x 
    ```
    Explanation of arguments:
    * -s: scientific name e.g. "Lithobius stygius"
    * -t: tolId e.g. qcLitStyg1
    * -a: the accession number of the raw reads project e.g. PRJEB76283
    * -x: NCBI taxonomy id e.g. 2750798

* Copy `submission-umbrella.xml` from any of the previous BGE species, check that the hold date is as wanted.
* Submit using curl:
    ```
    curl -u Username:Password -F "SUBMISSION=@submission-umbrella.xml" -F "PROJECT=@umbrella.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    
    ```
* **Note:** Add the assembly project `` when it has been submitted and made public, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.
