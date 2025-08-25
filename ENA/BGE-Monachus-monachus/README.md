---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB96355 (umbrella), PRJEB90634 (experiment), PRJEB90635 (assembly)
---

# BGE - *Monachus monachus*

## Submission task description
Submission of raw reads for *Monachus monachus* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Monachus-monachus-metadata.xlsx)
* [BGE HiFi metadata](./data/mMonMoa-HiFi.tsv)
* [BGE HiC metadata](./data/mMonMoa-HiC.tsv)
* [BGE RNAseq metadata](./data/mMonMoa-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiFi

#### Preparations
* Data transfer:
    ´´´
    interactive -t 08:00:00 -A uppmax2025-2-58
    lftp webin2.ebi.ac.uk -u Webin-39907
    mput cell*/*.bam
    ```
* Add TolID `mMonMoa` in the beginning of the file name using FileZilla
* The README in delivery folder from NGI gave me sample id `FS42549312`
* Looking it up in the ERGA tracker portal gave me BioSample `SAMEA117387583`

#### XML
* I created [mMonMoa-HiFi.tsv](./data/mMonMoa-HiFi.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f mMonMoa-HiFi.tsv -p ERGA-BGE -o mMonMoa-HiFi
    ``` 
* Note: There are 2 bam files, and the script creates 2 experiments so I had to remove one of them in the exp.xml file (runs.xml file is correct though, since I used the same library_name which is what the script makes use of when creating alias)
* The study XML also needs to be submitted, hence need to check that study xml looks ok
    
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@mMonMoa-HiFi.study.xml" -F "EXPERIMENT=@mMonMoa-HiFi.exp.xml" -F "RUN=@mMonMoa-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-19T07:16:50.097+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14538616" alias="exp_mMonMoa_HiFi_WGS_FS42549312_pr_177_001" status="PRIVATE"/>
        <RUN accession="ERR15133378" alias="run_mMonMoa_HiFi_WGS_FS42549312_pr_177_001_bam_1" status="PRIVATE"/>
        <RUN accession="ERR15133379" alias="run_mMonMoa_HiFi_WGS_FS42549312_pr_177_001_bam_2" status="PRIVATE"/>
        <PROJECT accession="PRJEB90634" alias="erga-bge-mMonMoa-study-rawdata-2025-06-19" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP173639" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB90635" alias="erga-bge-mMonMoa1_primary-2025-06-19" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP173640" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA33373631" alias="SUBMISSION-19-06-2025-07:16:49:860"/>
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
* I received sample ID from [NGI](https://docs.google.com/spreadsheets/d/10ZPAhkp1fCmpqR9GAZMRJ9wdXa8m-1G_/), which I checked in the [ERGA tracking portal](https://genomes.cnag.cat/erga-stream/samples/) which returned biosample [SAMEA117387581](https://www.ebi.ac.uk/biosamples/samples/SAMEA117387581).

* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [mMonMoa-HiC.tsv](./data/mMonMoa-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f mMonMoa-HiC.tsv -p ERGA-BGE -o mMonMoa-HiC
    ```   
* Update mMonMoa-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90634"/>
    ```

* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study will be private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@mMonMoa-HiC.exp.xml" -F "RUN=@mMonMoa-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-08-25T07:50:53.840+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14869051" alias="exp_mMonMoa_Hi-C_FS42549314_HC055-1B3A" status="PRIVATE"/>
        <RUN accession="ERR15465156" alias="run_mMonMoa_Hi-C_FS42549314_HC055-1B3A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA34642495" alias="SUBMISSION-25-08-2025-07:50:53:527"/>
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

#### XML
* I created [mMonMoa-RNAseq.tsv](./data/mMonMoa-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f mMonMoa-RNAseq.tsv -p ERGA-BGE -o mMonMoa-RNAseq
    ```
* Update mMonMoa-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90634"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@mMonMoa-RNAseq.exp.xml" -F "RUN=@mMonMoa-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Umbrella project - **TODO**
For each of the BGE species, an **umbrella** project has to be created and linked to the main BGE project, [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

1. Release the child project via browser
1. Collect scientific name and tolId from the metadata template sheet
1. Go to [ENA browser](https://www.ebi.ac.uk/ena/browser/home) and enter the scientific name as search term
    1. To the left side, there should be a **Taxon** subheading, that gives the identifier
1. Copy experiment accession number from metadata in top of this README
* There is a CNAG script, that should do the deed of creating the xml file:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Monachus monachus" -t mMonMoa1 -p ERGA-BGE -c SCILIFELAB -a PRJEB90634 -x 248254
    ```
    Explanation of arguments:
    * -s: scientific name e.g. "Lithobius stygius"
    * -t: tolId e.g. qcLitStyg1
    * -a: the accession number of the raw reads project e.g. PRJEB76283
    * -x: NCBI taxonomy id e.g. 2750798

* Copy `submission-umbrella.xml` from any of the previous BGE species
* Submit using curl:
    ```
    curl -u Username:Password -F "SUBMISSION=@submission-umbrella.xml" -F "PROJECT=@umbrella.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-08-25T13:17:49.116+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB96355" alias="erga-bge-mMonMoa-study-umbrella-2025-08-25" status="PRIVATE" holdUntilDate="2027-08-25+01:00"/>
        <SUBMISSION accession="ERA34668920" alias="SUBMISSION-25-08-2025-13:17:48:965"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    </RECEIPT>    
    ```
* Release the umbrella by adding the umbrella project accession number from the receipt above in file [submission-release-project.xml](./data/submission-release-project.xml)
* Submit using curl:
    ```
    curl -u Username:Password -F "SUBMISSION=@submission-release-project.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-08-25T13:23:44.416+01:00" submissionFile="submission-release-project.xml" success="true">
        <MESSAGES>
            <INFO>project accession "PRJEB96355" is set to public status.</INFO>
        </MESSAGES>
        <ACTIONS>RELEASE</ACTIONS>
    </RECEIPT>    
    ```

* **Note:** Add the assembly project `` when it has been submitted and made public, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.
