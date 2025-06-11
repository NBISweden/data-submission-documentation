---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: 
---

# BGE - *Niphargus gammariformis*

## Submission task description
Submission of raw reads for *Niphargus gammariformis* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Niphargus-gammariformis-metadata.xlsx)
* [BGE HiFi metadata](./data/qmNipGamm-HiFi.tsv)
* [BGE HiC metadata](./data/qmNipGamm-HiC.tsv)
* [BGE RNAseq metadata](./data/qmNipGamm-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiFi - **TODO**

#### Preparations

#### XML

* Update qmNipGamm-HiFi.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession=""/>
    ```
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@qmNipGamm-HiFi.exp.xml" -F "RUN=@qmNipGamm-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit HiC **TODO**

#### Preparations
* I received sample IDs from [NGI](https://docs.google.com/spreadsheets/d/15BObG5Z8CExbTa2bu4h8qvsr6xn8M0MT/), which I checked in the [ERGA tracking portal](https://genomes.cnag.cat/erga-stream/samples/) which returned biosample [SAMEA115536145](https://www.ebi.ac.uk/biosamples/samples/SAMEA115536145).

* The data files where transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

* 2 more data sets has been produced, based on biosample SAMEA115536142
* Note to self, need to make sure that the xmls are correct since separate samples and library names

#### XML
* I created [qmNipGamm-HiC.tsv](./data/qmNipGamm-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qmNipGamm-HiC.tsv -p ERGA-BGE -o qmNipGamm-HiC
    ```
* The study XML also needs to be submitted, since HiC is the first data type we have received.
    * I will not create the study for the assembly, since I don't yet know (no HiFi data yet, where we usually start, only HiC) which ToLID should be used (the script took `qmNipGamm10`)
    * Hence, removed that project from qmNipGamm-HiC.study.xml

* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study will be private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@qmNipGamm-HiC.study.xml" -F "EXPERIMENT=@qmNipGamm-HiC.exp.xml" -F "RUN=@qmNipGamm-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)


### Submit RNAseq - **TODO**

#### Preparations

#### XML
* I created [qmNipGamm-RNAseq.tsv](./data/qmNipGamm-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qmNipGamm-RNAseq.tsv -p ERGA-BGE -o qmNipGamm-RNAseq
    ```
* Update qmNipGamm-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession=""/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@qmNipGamm-RNAseq.exp.xml" -F "RUN=@qmNipGamm-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Umbrella project - **TODO**
For each of the BGE species, an **umbrella** project has to be created and linked to the main BGE project, [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

* There is a CNAG script, that should do the deed of creating the xml file:
    ```
    ./script/get_umbrella_xml_ENA.py -s "" -t  -p ERGA-BGE -c SCILIFELAB -a  -x 
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
