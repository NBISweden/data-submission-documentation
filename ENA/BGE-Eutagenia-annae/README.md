---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB96492 (umbrella), PRJEB93959 (experiment), PRJEB93960 (assembly)
---

# BGE - *Eutagenia annae*

## Submission task description
Submission of raw reads for *Eutagenia annae* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Eutagenia-annae-metadata.xlsx)
* [BGE HiFi metadata](./data/icEutAnna-HiFi.tsv)
* [BGE HiC metadata](./data/icEutAnna-HiC.tsv)
* [BGE RNAseq metadata](./data/icEutAnna-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiFi
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput *.bam` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.
* **Note:** Data is delivered but bioinformatician says: *"Please skip Eutagenia annae for now. Due to some mislabeling of the tubes 2 individuals were sequenced with PacBio, i.e. we have a tetraploid problem and HiC is most probably from a 3rd individual. Lets focus on the easier species first."*. 
  * The 2 samples also has different ToLID's so I have no idea which one to use. Asked for a new one, `icEutAnna36`
  * Virtual sample is needed
    * I created [icEutAnna-HiFi-virtual-sample.tsv](./data/icEutAnna-HiFi-virtual-sample.tsv)
    * Accession number received: `ERS25260776`
  * Data sheet is updated and data is transferred to ENA
  * I asked BGE for assistance of how to handle multiple ToLID's and the answer was to create a new one at https://id.tol.sanger.ac.uk/, referring to the original ToLID's and then create a virtual sample. I'm waiting for the new ToLID to become active (will keep an eye on the search page, https://id.tol.sanger.ac.uk/search-by-tolid, expecting `icEauAnna36`, specimenID `ERGA_AP_4894_00518;ERGA_AP_4894_00519`)
  
#### XML
* I created [icEutAnna-HiFi.tsv](./data/icEutAnna-HiFi.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icEutAnna-HiFi.tsv -p ERGA-BGE -o icEutAnna-HiFi
    ```

* Study is private, so submission.xml with hold date is used.

* Submit both projects and experiment in one go, i.e:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@icEutAnna-HiFi.study.xml" -F "EXPERIMENT=@icEutAnna-HiFi.exp.xml" -F "RUN=@icEutAnna-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-07-16T08:37:13.696+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14695223" alias="exp_icEutAnna_HiFi_WGS_LV6000912019_LV6000912027_pr_229_001" status="PRIVATE"/>
        <RUN accession="ERR15289389" alias="run_icEutAnna_HiFi_WGS_LV6000912019_LV6000912027_pr_229_001_bam_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB93959" alias="erga-bge-icEutAnna-study-rawdata-2025-07-16" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP176838" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB93960" alias="erga-bge-icEutAnna36_primary-2025-07-16" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP176839" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA33631670" alias="SUBMISSION-16-07-2025-08:37:13:404"/>
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
* Virtual sample had to be created and submitted via ENA browser:
    * [icEutAnna-HiC-virtual-sample.tsv](./data/icEutAnna-HiC-virtual-sample.tsv)
    * Accession number received: `ERS24618733`
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [icEutAnna-HiC.tsv](./data/icEutAnna-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icEutAnna-HiC.tsv -p ERGA-BGE -o icEutAnna-HiC
    ```
* Update -HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB93959"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the title and library name, since the other data types have the platform named
* Study will be private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@icEutAnna-HiC.exp.xml" -F "RUN=@icEutAnna-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-07-16T08:48:16.803+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14695257" alias="exp_icEutAnna_Hi-C_LV6000912034_LV6000912018_HC044-1A1A" status="PRIVATE"/>
        <RUN accession="ERR15289423" alias="run_icEutAnna_Hi-C_LV6000912034_LV6000912018_HC044-1A1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA33631691" alias="SUBMISSION-16-07-2025-08:48:16:526"/>
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
* I created [icEutAnna-RNAseq.tsv](./data/icEutAnna-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icEutAnna-RNAseq.tsv -p ERGA-BGE -o icEutAnna-RNAseq
    ```
* Update -RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB93959"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@icEutAnna-RNAseq.exp.xml" -F "RUN=@icEutAnna-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
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
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Eutagenia annae" -t icEutAnna36 -p ERGA-BGE -c SCILIFELAB -a PRJEB93959 -x 3229158
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
    <RECEIPT receiptDate="2025-08-27T10:27:16.233+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB96492" alias="erga-bge-icEutAnna-study-umbrella-2025-08-27" status="PRIVATE" holdUntilDate="2027-08-27+01:00"/>
        <SUBMISSION accession="ERA34838314" alias="SUBMISSION-27-08-2025-10:27:16:018"/>
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
    <RECEIPT receiptDate="2025-08-27T10:27:58.343+01:00" submissionFile="submission-release-project.xml" success="true">
        <MESSAGES>
            <INFO>project accession "PRJEB96492" is set to public status.</INFO>
        </MESSAGES>
        <ACTIONS>RELEASE</ACTIONS>
    </RECEIPT>    
    ```

* **Note:** Add the assembly project `` when it has been submitted and made public, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.
