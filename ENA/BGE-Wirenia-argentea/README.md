---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB83554 (experiment), PRJEB83555 (assembly)
---

# BGE - *Wirenia argentea*

## Submission task description
Submission of raw reads for *Wirenia argentea* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample(s) used for sequencing has already been submitted via COPO.
Submission will be done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Wirenia-argentea-metadata.xlsx)
* [BGE HiFi metadata](./data/xoWirArge-hifi.tsv)
* [BGE HiC metadata](./data/xoWirArge-hic.tsv)
* [BGE RNAseq metadata](./data/xoWirArge-rnaseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Data transfer
* Create folder `bge-wirenia-argentea` at ENA upload area using Filezilla
* Using aspera from Uppmax didn't work, used lftp:
    ```
    interactive -t 05:00:00 -A naiss2024-22-345
    lftp webin2.ebi.ac.uk -u Webin-XXX
    cd bge-wirenia-argentea
    mput /proj/snic2022-6-208/INBOX/BGE_Wirenia-argentea/EBP_pr_123/files/pr_123/rawdata/pr_123_001/*.bam
    ```
* Keep track of progress using FileZilla

### HiFi submission
#### Collecting metadata
* I looked at the delivery README for the HiFi dataset (on Uppmax) and extracted the Name (`FS42595739`). I looked in the [ERGA tracking portal](https://genomes.cnag.cat/erga-stream/samples/), filtered on the organism, and saw that the Name was registered with biosample [SAMEA114530807](https://www.ebi.ac.uk/biosamples/samples/SAMEA114530807).
* I copied the sample metadata (tube id, ToLID, BioSample id, species name) into the BGE-sheet of the metadata template.
* NGI says that the experimental metadata is the same as previous HiFi datasets.
* Created the tsv file [xoWirArge-hifi.tsv](./data/xoWirArge-hifi.tsv)

#### HiFi xml
* I copied [submission.xml](./data/submission.xml) from BGE-Crayfish, using the same embargo date

* Running the script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f xoWirArge-hifi.tsv -p ERGA-BGE -o xoWirArge-HiFi
    ```
    * The script wrongly adds `<SINGLE>NOMINAL_LENGTH</SINGLE>` in LIBRARY_LAYOUT. I changed the layout to `</SINGLE>`, but as with Laparocerus anagae I then get error upon submission.
    * If I copy L. anagae xml file and change to the values of W. argentea, and then calculate checksums on both exp xml files, they differ.
    * I changed the CNAG script so that it handles single vs paired layouts differently, and the resulting xml file could be submitted without errors.

#### Programmatic submission HiFi
* Submit both projects and experiment in one go, i.e:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml"  -F "PROJECT=@xoWirArge-HiFi.study.xml" -F "EXPERIMENT=@xoWirArge-HiFi.exp.xml" -F "RUN=@xoWirArge-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```

* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-12-13T07:06:35.951Z" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX13464201" alias="exp_xoWirArge_HiFi_WGS_FS42595739_pr_123" status="PRIVATE"/>
        <RUN accession="ERR14061198" alias="run_xoWirArge_HiFi_WGS_FS42595739_pr_123_bam_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB83554" alias="erga-bge-xoWirArge-study-rawdata-2024-12-13" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP167144" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB83555" alias="erga-bge-xoWirArge3_primary-2024-12-13" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP167145" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA31041431" alias="SUBMISSION-13-12-2024-07:06:35:336"/>
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
* I went to [BioSamples](https://www.ebi.ac.uk/biosamples/samples?text=Wirena+argentea) and extracted all samples for this species, where SCILIFELAB was the GAL. 
* I then went to the [ERGA tracking portal](https://genomes.cnag.cat/erga-stream/samples/) and filtered on the species name, collecting `Tube or well id` fields.
* I noticed that one of the GAL/sample collector id's seems to have a typo. 
    * It says `warg ad3 erga MYC 2023` but I think it should be `warg ad2 erga MYC 2023` for biosamples `SAMEA114530803` and `SAMEA114530802` 
    * Since the specimen id is `ERGA MYC 9212 02` and ToLID is `xoWirArge2` (and the other GAL and collector ids seems to be based on specimen id and ToLID)
* For the sample, I received the label `wargBGO23-4` (from an excel sheet via slack), and I'm unable to connect this to a biosample, specimen id or ToLID, so I've asked NGI for assistance.
    * Turns out that the samples for the material used haven't been registered in COPO (and hence does not exist in BioSamples). Only 3 samples are listed in the tracking tool, and SciLifeLab received 18 in total.
    * BGE has contacted sample provider, but no response yet. Once she uploads the updated Manifest, it will appear in the Tracking tool.
* The HiC sequencing failed, and new library has been ordered. Since I don't know which samples to use, I will let the text above remain until new HiC dataset arrives.

#### Create xml
**To be done**

* Running the script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f xoWirArge-hic.tsv -p ERGA-BGE -o xoWirArge-HiC
    ```
* Validate output (ignore the study xml)
* Update xoWirArge-HiC.exp.xml to reference accession number of previously registered study (HiFi):
    ```
    <STUDY_REF accession=""/>
    ```

#### Submission
**To be done**
* Submit:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@xoWirArge-HiC.exp.xml" -F "RUN=@xoWirArge-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
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
