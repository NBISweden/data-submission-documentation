---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB83563 (experiment), PRJEB83564 (assembly)
---

# BGE - *Microcosmus squamiger*

## Submission task description
Submission of raw reads for *Microcosmus squamiger* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample(s) used for sequencing has already been submitted via COPO.
Submission will be done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Microcosmus-squamiger-metadata.xlsx)
* [BGE HiFi metadata](./data/kaMicSqua-hifi.tsv)
* [BGE HiC metadata](./data/TOLID-hic.tsv)
* [BGE RNAseq metadata](./data/TOLID-rnaseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Data transfer
* Create folder `bge-microcosmus-squamiger` at ENA upload area using Filezilla
* Using aspera from Uppmax didn't work, used lftp:
    ```
    interactive -t 06:00:00 -A naiss2024-22-345
    lftp webin2.ebi.ac.uk -u Webin-XXX
    cd bge-microcosmus-squamiger
    mput /proj/snic2022-6-208/INBOX/BGE_Microcosmus-squamiger/EBP_pr_144/files/pr_144/rawdata/pr_144_001/cell*/*.bam
    ```
* Keep track of progress using FileZilla

### HiFi submission
#### Collecting metadata
* I looked at the delivery README for the HiFi dataset (on Uppmax) and extracted the Name (`FS42549340`). I looked in the [ERGA tracking portal](https://genomes.cnag.cat/erga-stream/samples/), filtered on the organism, and saw that the Name was registered with biosample [SAMEA115808870](https://www.ebi.ac.uk/biosamples/samples/SAMEA115808870).
* I copied the sample metadata (tube id, ToLID, BioSample id, species name) into the BGE-sheet of the metadata template.
* NGI says that the experimental metadata is the same as previous HiFi datasets.
* Created the tsv file [kaMicSqua-hifi.tsv](./data/kaMicSqua-hifi.tsv)

#### HiFi xml
* I copied [submission.xml](./data/submission.xml) from BGE-Crayfish, using the same embargo date

* Running the script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f kaMicSqua-hifi.tsv -p ERGA-BGE -o kaMicSqua-HiFi
    ```
    * The script creates 2 experiments (due to 2 files), but this is wrong, so the 2nd needs to be deleted.

### Programmatic submission HiFi
* Submit both projects and experiment in one go, i.e:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml"  -F "PROJECT=@kaMicSqua-HiFi.study.xml" -F "EXPERIMENT=@kaMicSqua-HiFi.exp.xml" -F "RUN=@kaMicSqua-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```

* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-12-13T08:01:13.952Z" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX13464586" alias="exp_kaMicSqua_HiFi_WGS_FS42549340_pr_144" status="PRIVATE"/>
        <RUN accession="ERR14061583" alias="run_kaMicSqua_HiFi_WGS_FS42549340_pr_144_bam_1" status="PRIVATE"/>
        <RUN accession="ERR14061584" alias="run_kaMicSqua_HiFi_WGS_FS42549340_pr_144_bam_2" status="PRIVATE"/>
        <PROJECT accession="PRJEB83563" alias="erga-bge-kaMicSqua-study-rawdata-2024-12-13" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP167153" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB83564" alias="erga-bge-kaMicSqua1_primary-2024-12-13" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP167154" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA31041443" alias="SUBMISSION-13-12-2024-08:01:12:500"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
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
