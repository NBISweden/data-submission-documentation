---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: 
---

# BGE - **

## Submission task description
Submission of raw reads for ** to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE--metadata.xlsx)
* [BGE HiFi metadata](./data/-hifi.tsv)
* [BGE HiC metadata](./data/-hic.tsv)
* [BGE RNAseq metadata](./data/-rnaseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Collecting metadata
* I went to [BioSamples](https://www.ebi.ac.uk/biosamples/samples?text=) and extracted all samples for this species, where SCILIFELAB was the GAL. I then looked at the delivery README for the HiFi dataset (on Uppmax) and extracted the Name (``). This I then pasted as filter in `Tube or well id` field, in the [ERGA tracking portal](https://genomes.cnag.cat/erga-stream/samples/) which returned biosample [](https://www.ebi.ac.uk/biosamples/samples/).

### Creating xml
* I copied [submission.xml](./data/submission.xml) from BGE-Crayfish, using the same embargo date
* Running the script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f -hifi.tsv -p ERGA-BGE -o -HiFi
    ```

### Data transfer
* Create folder `bge-` at ENA upload area using Filezilla
* Using aspera from Uppmax to ENA upload area:
    ```
    interactive -t 03:00:00 -A naiss2023-5-307
    module load ascp
    export ASPERA_SCP_PASS='password'
    ascp -k 3 -d -q --mode=send -QT -l300M --host=webin.ebi.ac.uk --user=Webin-XXXX /proj/snic2021-6-194/INBOX/BGE_.bam /bge-/ &
    ```
* Keep track of progress using FileZilla

### Programmatic submission
* Copy all xml files to Uppmax:
    ```
    scp submission.xml -HiFi*.xml yvonnek@rackham.uppmax.uu.se:/home/yvonnek/BGE-/
    ```
* Submit both projects and experiment in one go, i.e:
    ```
    interactive -t 03:00:00 -A naiss2023-5-307
    curl -u username:password -F "SUBMISSION=@submission.xml"  -F "PROJECT=@-HiFi.study.xml" -F "EXPERIMENT=@-HiFi.exp.xml" -F "RUN=@-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    
    ```
* Update of submission status at [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/)

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
