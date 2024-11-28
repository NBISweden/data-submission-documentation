---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: 
---

# BGE - *Laparocerus anagae*

## Submission task description
Submission of raw reads for *Laparocerus anagae* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample(s) used for sequencing has already been submitted via COPO.
Submission will be done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Laparocerus-anagae-metadata.xlsx)
* [BGE HiFi metadata](./data/-hifi.tsv)
* [BGE HiC metadata](./data/-hic.tsv)
* [BGE RNAseq metadata](./data/-rnaseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Data transfer
* Create folder `bge-laparocerus-anagae` at ENA upload area using Filezilla
* Using aspera from Uppmax didn't work:
    ```
    interactive -t 03:00:00 -A naiss2024-22-345
    module load ascp
    export ASPERA_SCP_PASS='password'
    ascp -k 3 -d -q --mode=send -QT -l300M --host=webin.ebi.ac.uk --user=Webin-XXXX /proj/snic2022-6-208/INBOX/BGE_Laparocerus-anagae/...bam /bge-laparocerus-anagae/ &
    ```
* Instead I used lftp:
    ```
    cd /proj/snic2022-6-208/INBOX/BGE_Laparocerus-anagae/...
    lftp webin2.ebi.ac.uk -u Webin-XXX
    cd bge-laparocerus-anagae
    mput *.bam
    ```
* Keep track of progress using FileZilla

### HiFi submission
#### Collecting metadata
* I looked at the delivery README for the HiFi dataset (on Uppmax) and extracted the Name (`FS38819783`). I looked in the [ERGA tracking portal](https://genomes.cnag.cat/erga-stream/samples/), filtered on the organism, and saw that the Name was registered with biosample [SAMEA115808865](https://www.ebi.ac.uk/biosamples/samples/SAMEA115808865).
* I copied the sample metadata (tube id, ToLID, BioSample id, species name) into the BGE-sheet of the metadata template.
* Need to check the experimental metadata with NGI.

#### HiFi xml
* **Note:** There are 2 bam files, need to make sure that the script works
* I copied [submission.xml](./data/submission.xml) from BGE-Crayfish, using the same embargo date
* Running the script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icLapAnag-hifi.tsv -p ERGA-BGE -o icLapAnag-HiFi
    ```

### Programmatic submission HiFi
* Copy all xml files to Uppmax:
    ```
    scp submission.xml icLapAnag-HiFi*.xml yvonnek@rackham.uppmax.uu.se:/home/yvonnek/BGE-Laparocerus-anagae/
    ```
* Submit both projects and experiment in one go, i.e:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml"  -F "PROJECT=@icLapAnag-HiFi.study.xml" -F "EXPERIMENT=@icLapAnag-HiFi.exp.xml" -F "RUN=@icLapAnag-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    
    ```
* Update of submission status at [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/)

### HiC submission
#### Collect metadata
#### Create xml
#### Submission

### RNAseq submission
#### Collect metadata
#### Create xml
#### Submission

### Umbrella project
* **TODO**
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
