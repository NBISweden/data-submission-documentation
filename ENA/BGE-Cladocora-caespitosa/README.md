---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: 
---

# BGE - *Cladocora caespitosa*

## Submission task description
Submission of raw reads for *Cladocora caespitosa* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Cladocora-caespitosa-metadata.xlsx)
* [BGE HiFi metadata](./data/jaClaCaes-hifi.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Collecting metadata

* I looked at the delivery README for the HiFi dataset (on Uppmax) and extracted the following:
  ```
  Name    UGC_ID  Barcode Comments
  FS42595244+45 / ERGA_DS_382X_05 pr_124_001      bc2135  -
  ```
* I went to [BioSamples](https://www.ebi.ac.uk/biosamples/samples?text=Cladocora+caespitosa) (adding filter that the organism had to be C. ceaspitosa since there were several metagenome samples as well), looking for a match in the 'Name' above. It resulted in 2 samples that weren't derived from another sample, [SAMEA112878230](https://www.ebi.ac.uk/biosamples/samples/SAMEA112878230) (TolId jaClaCaes1) and [SAMEA112878231](https://www.ebi.ac.uk/biosamples/samples/SAMEA112878231) (TolId jaClaCaes2)

* Then I went to the [ERGA tracking portal](https://genomes.cnag.cat/erga-stream/samples/) and pasted `FS42595244` as filter in `Tube or well id` field, which returned biosample [SAMEA113399591](https://www.ebi.ac.uk/biosamples/samples/SAMEA113399591) (which is derived from SAMEA112878230). Then I searched for `FS42595245` instead, returning biosample [SAMEA112878240](https://www.ebi.ac.uk/biosamples/samples/SAMEA112878240) (which is derived from SAMEA112878231)

* Now what? Which of the samples do I use? Need to confere with UGC bioinformatician... I got the advice to use the lowest number, hence biosample [SAMEA113399591](https://www.ebi.ac.uk/biosamples/samples/SAMEA113399591) with TolId `jaClaCaes1` will be used

* I filled the tab BGE-sheet with the information and created a tsv file: [jaClaCaes-hifi.tsv](./data/jaClaCaes-hifi.tsv)

### Creating xml
#### HiFi xml
* I copied [submission.xml](./data/submission.xml) from BGE-Crayfish, using the same embargo date
* Running the script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f jaClaCaes-hifi.tsv -p ERGA-BGE -o jaClaCaes-HiFi
    ```
#### HiC xml

#### RNAseq xml

### Data transfer
#### HiFi
* Create folder `bge-cladocora` at ENA upload area using Filezilla
* Using aspera from Uppmax to ENA upload area:
    ```
    interactive -t 03:00:00 -A naiss2024-22-345
    module load ascp
    export ASPERA_SCP_PASS='password'
    ascp -k 3 -d -q --mode=send -QT -l300M --host=webin.ebi.ac.uk --user=Webin-XXXX /proj/snic2022-6-208/INBOX/BGE_Cladocora_caespitosa/EBP_pr_124/files/pr_124/rawdata/pr_124_001/m84045_240925_162103_s2.hifi_reads.bc2135.bam /bge-cladocora/ &
    ```
* Keep track of progress using FileZilla

### Programmatic submission HiFi
* Copy all xml files to Uppmax (create a folder there BGE-Cladocora-caespitosa):
    ```
    scp submission.xml jaClaCaes-HiFi*.xml yvonnek@rackham.uppmax.uu.se:/home/yvonnek/BGE-Cladocora-caespitosa/
    ```
* Submit both projects and experiment in one go, i.e:
    ```
    interactive -t 03:00:00 -A naiss2024-22-345
    curl -u username:password -F "SUBMISSION=@submission.xml"  -F "PROJECT=@jaClaCaes-HiFi.study.xml" -F "EXPERIMENT=@jaClaCaes-HiFi.exp.xml" -F "RUN=@jaClaCaes-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
    * `<ERROR>Failed to validate experiment xml, error: Element 'SINGLE' with empty content type cannot have text or element content.</ERROR>`
    * Looking at the experiment xml I realise that there is a mentioning of NOMINAL_LENGTH but this should of course not be written since it is not a paired read. Hence, my version of the CNAG script doesn't work for HiFi now that I've changed it to accomodate HiC reads...
    * I manually edited the xml file, replacing `<SINGLE>NOMINAL_LENGTH</SINGLE>` with `<SINGLE/>`
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-10-15T13:53:10.832+01:00" submissionFile="submission.xml" success="true">
     <EXPERIMENT accession="ERX13203815" alias="exp_jaClaCaes_HiFi_WGS_FS42595244_FS42595244" status="PRIVATE"/>
     <RUN accession="ERR13803063" alias="run_jaClaCaes_HiFi_WGS_FS42595244_FS42595244_bam_1" status="PRIVATE"/>
     <PROJECT accession="PRJEB81307" alias="erga-bge-jaClaCaes-study-rawdata-2024-10-15" status="PRIVATE" holdUntilDate="2026-03-07Z">
          <EXT_ID accession="ERP165156" type="study"/>
     </PROJECT>
     <PROJECT accession="PRJEB81308" alias="erga-bge-jaClaCaes1_primary-2024-10-15" status="PRIVATE" holdUntilDate="2026-03-07Z">
          <EXT_ID accession="ERP165157" type="study"/>
     </PROJECT>
     <SUBMISSION accession="ERA30875987" alias="SUBMISSION-15-10-2024-13:53:10:521"/>
     <MESSAGES>
          <INFO>All objects in this submission are set to private status (HOLD).</INFO>
     </MESSAGES>
     <ACTIONS>ADD</ACTIONS>
     <ACTIONS>HOLD</ACTIONS>
    ```
* Update of submission status at [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/)

### Programmatic submission HiC

### Programmatic submission RNAseq

### Umbrella Project (TODO)
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
