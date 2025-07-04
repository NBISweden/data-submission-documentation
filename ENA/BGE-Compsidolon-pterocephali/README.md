---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB91436 (umbrella), PRJEB91095 (experiment), PRJEB91096 (assembly)
---

# BGE - *Compsidolon pterocephali*

## Submission task description
Submission of raw reads for *Compsidolon pterocephali* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Compsidolon-pterocephali-metadata.xlsx)
* [BGE HiFi metadata](./data/ihConPter-HiFi.tsv)
* [BGE HiC metadata](./data/ihConPter-HiC.tsv)
* [BGE RNAseq metadata](./data/ihConPter-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->
* If trimmed reads (due to ULI) is put in column named `file_name` (as it normally should when submitting) the scripts produces an empty run .xml file. However, when put in 'native_file_name' column, the scripts complains about the file ending. Hence, need to trick the script by putting the file in `native_file_name` and change ending to `.bam`, then afterwards change to appropriate values in run .xml (rows `<RUN ` and `<FILE `)

## Detailed step by step description

### Submit HiFi
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* ULI protocol, trimmed or untrimmed? It was decided that trimmed reads are most useful and hence should be submitted
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput *.bam` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [ihConPter-HiFi.tsv](./data/ihConPter-HiFi.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f ihConPter-HiFi.tsv -p ERGA-BGE -o ihConPter-HiFi
    ```
    * If trimmed reads (due to ULI) is put in column named `file_name` (as it normally should when submitting) the scripts produces an empty run .xml file. However, when put in 'native_file_name' column, the scripts complains about the file ending. Hence, need to trick the script by putting the file in `native_file_name` and change ending to `.bam`, then afterwards change to appropriate values in run .xml (rows `<RUN ` and `<FILE `)
    *
* Study is private, so submission.xml with hold date is used.

* Submit both projects and experiment in one go, i.e:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@ihConPter-HiFi.study.xml" -F "EXPERIMENT=@ihConPter-HiFi.exp.xml" -F "RUN=@ihConPter-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-26T10:17:42.822+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14566103" alias="exp_ihConPter_HiFi_WGS_LV6000912658_pr_221_001" status="PRIVATE"/>
        <RUN accession="ERR15160451" alias="run_ihConPter_HiFi_WGS_LV6000912658_pr_221_001_fastq_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB91095" alias="erga-bge-ihConPter-study-rawdata-2025-06-26" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP174087" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB91096" alias="erga-bge-ihConPter4_primary-2025-06-26" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP174088" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA33523625" alias="SUBMISSION-26-06-2025-10:17:42:482"/>
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
* I created [ihConPter-HiC.tsv](./data/ihConPter-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f ihConPter-HiC.tsv -p ERGA-BGE -o ihConPter-HiC
    ```
* Update -HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB91095"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study will be private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@ihConPter-HiC.exp.xml" -F "RUN=@ihConPter-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-27T09:02:03.568+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14570425" alias="exp_ihConPter_Hi-C_LV6000912650_HC042-1A1A" status="PRIVATE"/>
        <RUN accession="ERR15164702" alias="run_ihConPter_Hi-C_LV6000912650_HC042-1A1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA33527173" alias="SUBMISSION-27-06-2025-09:02:03:261"/>
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
* I created [ihConPter-RNAseq.tsv](./data/ihConPter-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f ihConPter-RNAseq.tsv -p ERGA-BGE -o ihConPter-RNAseq
    ```
* Update -RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB91095"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@ihConPter-RNAseq.exp.xml" -F "RUN=@ihConPter-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
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
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Compsidolon pterocephali" -t ihConPter -p ERGA-BGE -c SCILIFELAB -a PRJEB91095 -x 3229146
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
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-07-01T13:04:39.497+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB91436" alias="erga-bge-ihConPter-study-umbrella-2025-07-01" status="PRIVATE" holdUntilDate="2025-07-03+01:00"/>
        <SUBMISSION accession="ERA33545333" alias="SUBMISSION-01-07-2025-13:04:39:191"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>    
    ```
* **Note:** Add the assembly project `` when it has been submitted and made public, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.
