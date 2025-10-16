---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB91434 (umbrella), PRJEB90612 (experiment), PRJEB90613 (assembly)
---

# BGE - *Clavelina lepadiformis*

## Submission task description
Submission of raw reads for *Clavelina lepadiformis* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Clavelina-lepadiformis-metadata.xlsx)
* [BGE HiFi metadata](./data/kaClaLepa-HiFi.tsv)
* [BGE HiC metadata](./data/kaClaLepa-HiC.tsv)
* [BGE RNAseq metadata](./data/kaClaLepa-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiFi

#### Preparations
* Data transfer:
    ```
    interactive -t 08:00:00 -A uppmax2025-2-58
    lftp webin2.ebi.ac.uk -u Webin-39907
    mput m84045_250225_172119_s3.hifi_reads.bc2046.bam
    ```
* Add TolID in the beginning of the file name using FileZilla
* The README in delivery folder from NGI gave me sample id `FS42549325`
* Looking it up in the ERGA tracker portal gave me BioSample `SAMEA115782298`

#### XML
* I created [kaClaLepa-HiFi.tsv](./data/kaClaLepa-HiFi.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f kaClaLepa-HiFi.tsv -p ERGA-BGE -o kaClaLepa-HiFi
    ```
* The study XML also needs to be submitted, hence need to check that kaClaLepa-HiC.study.xml seems ok

* Study will be private, so submission.xml with hold date is used.
* Submit using curl: 
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@kaClaLepa-HiFi.study.xml" -F "EXPERIMENT=@kaClaLepa-HiFi.exp.xml" -F "RUN=@kaClaLepa-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-18T15:55:32.445+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14538047" alias="exp_kaClaLepa_HiFi_WGS_FS42549325_pr_168_001" status="PRIVATE"/>
        <RUN accession="ERR15132814" alias="run_kaClaLepa_HiFi_WGS_FS42549325_pr_168_001_bam_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB90612" alias="erga-bge-kaClaLepa-study-rawdata-2025-06-18" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP173614" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB90613" alias="erga-bge-kaClaLepa18_primary-2025-06-18" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP173615" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA33333139" alias="SUBMISSION-18-06-2025-15:55:32:237"/>
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
* I received sample ID from [NGI](https://docs.google.com/spreadsheets/d/10ZPAhkp1fCmpqR9GAZMRJ9wdXa8m-1G_/), which I checked in the [ERGA tracking portal](https://genomes.cnag.cat/erga-stream/samples/) which returned biosample [SAMEA115782300](https://www.ebi.ac.uk/biosamples/samples/SAMEA115782300).

* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [kaClaLepa-HiC.tsv](./data/kaClaLepa-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f kaClaLepa-HiC.tsv -p ERGA-BGE -o kaClaLepa-HiC
    ```
* Update kaClaLepa-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90612"/>
    ```
* Study is private, so submission.xml with hold date is used.

* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study will be private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@kaClaLepa-HiC.exp.xml" -F "RUN=@kaClaLepa-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-07-01T06:16:50.533+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14577974" alias="exp_kaClaLepa_Hi-C_FS42549323_HC018-2A1A" status="PRIVATE"/>
        <RUN accession="ERR15172550" alias="run_kaClaLepa_Hi-C_FS42549323_HC018-2A1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA33544628" alias="SUBMISSION-01-07-2025-06:16:50:247"/>
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
* I created [kaClaLepa-RNAseq.tsv](./data/kaClaLepa-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f kaClaLepa-RNAseq.tsv -p ERGA-BGE -o kaClaLepa-RNAseq
    ```
* Update kaClaLepa-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90612"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@kaClaLepa-RNAseq.exp.xml" -F "RUN=@kaClaLepa-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
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
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Clavelina lepadiformis" -t kaClaLepa -p ERGA-BGE -c SCILIFELAB -a PRJEB90612 -x 159417
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
    <RECEIPT receiptDate="2025-07-01T12:55:58.756+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB91434" alias="erga-bge-kaClaLepa-study-umbrella-2025-07-01" status="PRIVATE" holdUntilDate="2026-03-07Z"/>
        <SUBMISSION accession="ERA33545318" alias="SUBMISSION-01-07-2025-12:55:58:457"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
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
    <RECEIPT receiptDate="2025-10-16T09:44:07.731+01:00" submissionFile="submission-release-project.xml" success="true">
        <MESSAGES>
            <INFO>project accession "PRJEB91434" is set to public status.</INFO>
        </MESSAGES>
        <ACTIONS>RELEASE</ACTIONS>
    </RECEIPT>    
    ```

* **Note:** Add the assembly project `` when it has been submitted and made public, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.
