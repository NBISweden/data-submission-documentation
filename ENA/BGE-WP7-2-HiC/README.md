---
Redmine_issue: https://projects.nbis.se/issues/8259
Repository: ENA
Submission_type: Hi-C
Data_generating_platforms:
- NGI
Top_level_acccession: 
---

# BGE Task 7.2 Lab course in advanced HiC methodology

## Submission task description
Submission of HiC raw reads for *Clupea harengus* and *Meganyctiphanes norvegica* to facilitate BGE Task 7.2 Lab course in advanced HiC methodology, as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). 

8 samples, 6 herring and 2 krill, with 8 experiments is submitted and put under the BGE umbrella project [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

Submission will be done by the data producer's (NGI) ENA account.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-WP7.2-HiC-course-metadata.xlsx)
* [BGE HiC metadata](./data/WP7-2-HiC.tsv)

* Idea is to do a programmatic submission of the study, then register the samples via browser, and finally do a programmatic submission of the experiments.

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit study - **TODO**
The idea is to submit a project and attach to the BGE umbrella at the same time, but if it doesn't work, the attachment has to be done afterwards (possibly with help from central BGE).

* Create [project.xml](./data/project.xml) with the same structure as in [Create study xml](https://ena-docs.readthedocs.io/en/latest/submit/study/programmatic.html#create-the-study-xml)
* Copy the `RELATED_PROJECTS` and `PROJECT_ATTRIBUTES` sections from an umbrella.xml from one of the other BGE submissions
* Add metadata from the Excel sheet
* Create [submission-project.xml](./data/submission-project.xml) with the release date 2025-08-31
* Submit using curl (to wwwdev first, since 1st time trying to add to a parent umbrella while creating a project that is not an umbrella):
    ```
    curl -u username:password -F "SUBMISSION=@submission-project.xml" -F "PROJECT=@project.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"   
    ```
* Receipt:
    ```

    ```
### Submit samples
We don't have the metadata for the krill, so the samples (and experiments) will be submitted in 2 rounds

#### Herring
* Create [herring-samples.tsv](./data/herring-samples.tsv)
* Copy the metadata from the google metadata sheet (copying from the downloaded sheet caused problems e.g. removing decimals in geographic coordinates)
* Upload via browser, using NGI ENA account - **TODO**
* Accession numbers:

#### Krill - **TODO when metadata is available**
* Create [krill-samples.tsv](./data/krill-samples.tsv)
* Copy the metadata from the google metadata sheet (copying from the downloaded sheet caused problems e.g. removing decimals in geographic coordinates)
* Upload via browser, using NGI ENA account
* Accession numbers:

### Submit HiC - **TODO**
* The data files are transferred by NGI to ENA upload area.
* Since it is likely that the krill metadata samples are not available by the time of submission of experiments, only the herring HiC will be submitted before release of project to public (due to vacations)
* **Note:** need to create a BGE-sheet tab from the ENA_experiment tab, so that  the .tsv's will work with the CNAG script

#### Herring XML
* I created [herring-HiC.tsv](./data/herring-HiC.tsv) and added metadata from BGE sheet tab
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f herring-HiC.tsv -p ERGA-BGE -o herring-HiC
    ```
* Update herring-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession=""/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title, since the other data types have the platform named
* Study will be private, so submission-experiment.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission-experiment.xml" -F "EXPERIMENT=@herring-HiC.exp.xml" -F "RUN=@herring-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```

#### Krill XML
* I created [krill-HiC.tsv](./data/krill-HiC.tsv) and added metadata from BGE sheet tab
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f krill-HiC.tsv -p ERGA-BGE -o krill-HiC
    ```
* Update krill-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession=""/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title, since the other data types have the platform named
* Study will be private, so submission-experiment.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission-experiment.xml" -F "EXPERIMENT=@krill-HiC.exp.xml" -F "RUN=@krill-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
