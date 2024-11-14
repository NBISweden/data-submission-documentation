---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: 
---

# BGE - *Wirenia argentea*

## Submission task description
Submission of raw reads for *Wirenia argentea* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Wirenia-argentea-metadata.xlsx)
* [BGE HiFi metadata](./data/xoWirArge-hifi.tsv)
* [BGE HiC metadata](./data/xoWirArge-hic.tsv)
* [BGE RNAseq metadata](./data/xoWirArge-rnaseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Collecting metadata
* I went to [BioSamples](https://www.ebi.ac.uk/biosamples/samples?text=) and extracted all samples for this species, where SCILIFELAB was the GAL. * I then went to the [ERGA tracking portal](https://genomes.cnag.cat/erga-stream/samples/) and filtered on the species name, collecting `Tube or well id` fields.
* I noticed that one of the GAL/sample collector id's seems to have a typo. 
    * It says `warg ad3 erga MYC 2023` but I think it should be `warg ad2 erga MYC 2023` for biosamples `SAMEA114530803` and `SAMEA114530802` 
    * Since the specimen id is `ERGA MYC 9212 02` and ToLID is `xoWirArge2` (and the other GAL and collector ids seems to be based on specimen id and ToLID)

### Data transfer
**To be done**
* Create folder `bge-wirenia-argentea` at ENA upload area using Filezilla
* Using aspera from Uppmax to ENA upload area:
    ```
    interactive -t 03:00:00 -A naiss2024-22-345
    module load ascp
    export ASPERA_SCP_PASS='password'
    ascp -k 3 -d -q --mode=send -QT -l300M --host=webin.ebi.ac.uk --user=Webin-XXXX /proj/snic2021-6-194/INBOX/BGE_.bam /bge-wirenia-argentea/ &
    ```
* Keep track of progress using FileZilla

### Submit Hi-C
**To be done**
* This is the first dataset for this species, so both study and experiment needs to be created.
* For the sample, I received the label `wargBGO23-4`, and I'm unable to connect this to a biosample, specimen id or ToLID, so I've asked NGI for assistance.

* Copy a [submission.xml](./data/submission.xml) with hold date, from earlier submission

* Running the script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f xoWirArge-hic.tsv -p ERGA-BGE -o xoWirArge-HiC
    ```

* Copy all xml files to Uppmax:
    ```
    scp submission.xml xoWirArge-HiC*.xml yvonnek@rackham.uppmax.uu.se:/home/yvonnek/BGE-Wirenia-argentea/
    ```
* Submit both project and experiment in one go, i.e:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml"  -F "PROJECT=@xoWirArge-HiC.study.xml" -F "EXPERIMENT=@xoWirArge-HiC.exp.xml" -F "RUN=@xoWirArge-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    
    ```
* Update of submission status at [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/)

### Submit HiFi
**To be done**
* Identify the sample

* Running the script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f xoWirArge-hifi.tsv -p ERGA-BGE -o xoWirArge-HiFi
    ```
* Validate output (ignore the study xml)
* Update xoWirArge-HiFi.exp.xml to reference accession number of previously registered study (HiC):
    ```
    <STUDY_REF accession=""/>
    ```
* Copy all xml files to Uppmax:
    ```
    scp submission.xml xoWirArge-HiFi*.xml yvonnek@rackham.uppmax.uu.se:/home/yvonnek/BGE-Wirenia-argentea/
    ```
* Submit only experiment:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml"  -F "EXPERIMENT=@xoWirArge-HiFi.exp.xml" -F "RUN=@xoWirArge-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    
    ```
* Update of submission status at [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/)

### Submit RNAseq
**To be done**
* Identify which sample

* Run CNAG script
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f xoWirArge-RNAseq.tsv -p ERGA-BGE -o xoWirArge-RNAseq
    ```
* Validate output (ignore the study xml)
* Update xoWirArge-RNAseq.exp.xml to reference accession number of previously registered study (HiC):
    ```
    <STUDY_REF accession=""/>
    ```

* Copy all xml files to Uppmax:
    ```
    scp submission.xml xoWirArge-RNAseq*.xml yvonnek@rackham.uppmax.uu.se:/home/yvonnek/BGE-Wirenia-argentea/
    ```
* Submit only experiment:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml"  -F "EXPERIMENT=@xoWirArge-RNAseq.exp.xml" -F "RUN=@xoWirArge-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    
    ```
* Update of submission status at [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/)


### Umbrella project
**To be done, add project number**

For each of the BGE species, an **umbrella** project has to be created and linked to the main BGE project, [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

* There is a CNAG script, that should do the deed of creating the xml file:
    ```
    ./script/get_umbrella_xml_ENA.py -s "Wirenia argentea" -t  -p ERGA-BGE -c SCILIFELAB -a  -x 669229
    ```
    Explanation of arguments:
    * -s: scientific name e.g. "Lithobius stygius"
    * -t: tolId e.g. qcLitStyg1
    * -a: the accession number of the raw reads project e.g. PRJEB76283
    * -x: NCBI taxonomy id e.g. 2750798

* Copy `submission-umbrella.xml` from any of the previous BGE species, check that the hold date is as wanted. (**done**)
* Submit using curl:
    ```
    curl -u Username:Password -F "SUBMISSION=@submission-umbrella.xml" -F "PROJECT=@umbrella.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    
    ```
* **Note:** Add the assembly project `` when it has been submitted and made public, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.
