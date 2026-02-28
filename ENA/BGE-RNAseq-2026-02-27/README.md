---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: RNAseq # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: Not applicable
---

# BGE - multiple species

## Submission task description
Submission of RNAseq raw reads for a mixture of species (45 in total) delivered 2026-02-27 to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). 

Submission will be done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [BGE RNAseq metadata](./data/RNAseq-delivery_202026-02-27.xlsx)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit RNAseq 
#### Preparations
* Data producer provided me with a list of sample identifiers, via slack
* Data was delivered in two rounds, where the first round contained 90 paired reads from 44 species, and the second round only contained 2 paired reads (labelled with CNAG) from one species.
* With the data delivery we received checksum.md5 files containing a list of all files and the md5 sums
    * I asked Gemini to create a script to put paired read md5 sum information on one row, tab separated, which resulted in [reformat_md5.sh](./scripts/reformat_md5.sh)
* All cleaned and transformed metadata was collected in `BGE_sheet` tab of the  .xlsx file, while semi-formatted metadata from different sources was put in the other tabs.  
* Sample ID gave BioSample ID via ERGA tracker portal

* All data files received in this batch were transferred using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz`. Given the time limitations before project ends, and that there were 45 species delivered, I did not follow previous procedures of adding ToLID to the files using rename function in FileZilla. Instead I double and triple checked that the correct files was connected to the correct sample, before creating any .xml files.

#### XML
* I created [RNAseq.tsv](./data/RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f RNAseq.tsv -p ERGA-BGE -o RNAseq
    ```
* Update RNAseq.exp.xml to reference accession number of previously registered studies (from `Species` tab in the .xlsx metadata file):
    ```
    <STUDY_REF accession=""/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title, since the other data types have the platform named
* All studies are already public, so submission.xml without hold date is used.
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@RNAseq.exp.xml" -F "RUN=@RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/) (if still available since project has ended)

