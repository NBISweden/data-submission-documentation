---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB81311 (umbrella), PRJEB81307 (experiment), PRJEB81308 (assembly), PRJEB98993 (mito)
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

### Submit HiFi
#### Preparations
* I looked at the delivery README for the HiFi dataset (on Uppmax) and extracted the following:
  ```
  Name    UGC_ID  Barcode Comments
  FS42595244+45 / ERGA_DS_382X_05 pr_124_001      bc2135  -
  ```
* I went to [BioSamples](https://www.ebi.ac.uk/biosamples/samples?text=Cladocora+caespitosa) (adding filter that the organism had to be C. ceaspitosa since there were several metagenome samples as well), looking for a match in the 'Name' above. It resulted in 2 samples that weren't derived from another sample, [SAMEA112878230](https://www.ebi.ac.uk/biosamples/samples/SAMEA112878230) (TolId jaClaCaes1) and [SAMEA112878231](https://www.ebi.ac.uk/biosamples/samples/SAMEA112878231) (TolId jaClaCaes2)

* Then I went to the [ERGA tracking portal](https://genomes.cnag.cat/erga-stream/samples/) and pasted `FS42595244` as filter in `Tube or well id` field, which returned biosample [SAMEA113399591](https://www.ebi.ac.uk/biosamples/samples/SAMEA113399591) (which is derived from SAMEA112878230). Then I searched for `FS42595245` instead, returning biosample [SAMEA112878240](https://www.ebi.ac.uk/biosamples/samples/SAMEA112878240) (which is derived from SAMEA112878231)

* Now what? Which of the samples do I use? Need to confere with UGC bioinformatician... I got the advice to use the lowest number, hence biosample [SAMEA113399591](https://www.ebi.ac.uk/biosamples/samples/SAMEA113399591) with TolId `jaClaCaes1` will be used

* I filled the tab BGE-sheet with the information and created a tsv file: [jaClaCaes-hifi.tsv](./data/jaClaCaes-hifi.tsv)

* Create folder `bge-cladocora` at ENA upload area using Filezilla
* Using aspera from Uppmax to ENA upload area:
    ```
    interactive -t 03:00:00 -A naiss2024-22-345
    module load ascp
    export ASPERA_SCP_PASS='password'
    ascp -k 3 -d -q --mode=send -QT -l300M --host=webin.ebi.ac.uk --user=Webin-XXXX /proj/snic2022-6-208/INBOX/BGE_Cladocora_caespitosa/EBP_pr_124/files/pr_124/rawdata/pr_124_001/m84045_240925_162103_s2.hifi_reads.bc2135.bam /bge-cladocora/ &
    ```
* Keep track of progress using FileZilla

#### HiFi xml
* I copied [submission.xml](./data/submission.xml) from BGE-Crayfish, using the same embargo date
* Running the script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f jaClaCaes-hifi.tsv -p ERGA-BGE -o jaClaCaes-HiFi
    ```
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

### Submit HiC
#### Preparations
* Sample ID has the same 'issues' as for HiFi, I will use the same sample here 
* There are 2 libraries, using the same sample but one is with old formaldehyde and one is with new / freshly opened
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [jaClaCaes-HiC.tsv](./data/jaClaCaes-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f jaClaCaes-HiC.tsv -p ERGA-BGE -o jaClaCaes-HiC
    ```
* Update jaClaCaes-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB81307"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title, since the other data types have the platform named
* Study is public, so submission-noHold.xml is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission-noHold.xml" -F "EXPERIMENT=@jaClaCaes-HiC.exp.xml" -F "RUN=@jaClaCaes-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-10-10T09:04:36.756+01:00" submissionFile="submission-noHold.xml" success="true">
        <EXPERIMENT accession="ERX15093300" alias="exp_jaClaCaes_Hi-C_FS42595244_HC008-3C1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX15093301" alias="exp_jaClaCaes_Hi-C_FS42595244_HC008-3D1A" status="PRIVATE"/>
        <RUN accession="ERR15688615" alias="run_jaClaCaes_Hi-C_FS42595244_HC008-3C1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR15688616" alias="run_jaClaCaes_Hi-C_FS42595244_HC008-3D1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA35055533" alias="SUBMISSION-10-10-2025-09:04:36:354"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    </RECEIPT>
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit RNAseq - **TODO**
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [jaClaCaes-RNAseq.tsv](./data/jaClaCaes-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f jaClaCaes-RNAseq.tsv -p ERGA-BGE -o jaClaCaes-RNAseq
    ```
* Update jaClaCaes-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB81307"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@jaClaCaes-RNAseq.exp.xml" -F "RUN=@jaClaCaes-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit assembly

* There are one primary and one mitochondrial assembly, need to create a project for the mito.
    * I created [jaClaes-mito.study.xml](./data/jaClaes-mito.study.xml) and submitted using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@jaClaes-mito.study.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
    * Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-10-10T10:37:10.898+01:00" submissionFile="submission.xml" success="true">
        <PROJECT accession="PRJEB98993" alias="erga-bge-jaClaCaes-study-mito-2025-10-10" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP181339" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA35055599" alias="SUBMISSION-10-10-2025-10:37:10:787"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
* I created manifest files [jaClaCaes1-manifest.txt](./data/jaClaCaes1-manifest.txt) and [jaClaCaes1-mito-manifest.txt](./data/jaClaCaes1-mito-manifest.txt)
* I created [chromosome_list.txt](./data/chromosome_list.txt) and [chromosome_list_mito.txt](./data/chromosome_list_mito.txt), and [unlocalised_list.txt](./data/unlocalised_list.txt)
* I created a folder on Uppmax (/proj/snic2022-6-208/nobackup/submission/C-caespitosa) and copied & gzipped manifests, assembly file and chromosome list there
* Then all files where submitted (first validation then submission) from Pelle on Uppmax using Webin-CLI:

    ```
    interactive -t 02:00:00 -A uppmax2025-2-58
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./jaClaCaes1-manifest.txt -validate
    ```
* Receipt primary:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/C-caespitosa/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/C-caespitosa/jaClaCaes1_pri_20251009_noMito.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/C-caespitosa/chromosome_list.txt.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/C-caespitosa/unlocalised_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28536405
    ```
* Receipt mito:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/C-caespitosa/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/C-caespitosa/jaClaCaes1_mito_20251009.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/C-caespitosa/chromosome_list_mito.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28536406
    ```
* I added the accession number to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `Assembly submitted` to `Yes`, as well as set assembly as status `Submitted` in [Tracking_tool_Seq_centers](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/edit?pli=1&gid=0#gid=0)
* Accessioned:
    ```
    ASSEMBLY_NAME | ASSEMBLY_ACC  | STUDY_ID   | SAMPLE_ID   | CONTIG_ACC                      | SCAFFOLD_ACC | CHROMOSOME_ACC

    ```
* Release studies and check that they are shown under umbrella

#### Add assembly to umbrella
* Add the assembly project when it has been submitted, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.
* Create [update.xml](./data/update.xml) and [umbrella_modified.xml](./data/umbrella_modified.xml)
* Submit:
    ```
    curl -u Username:Password -F "SUBMISSION=@update.xml" -F "PROJECT=@umbrella_modified.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```

### Umbrella project
For each of the BGE species, an **umbrella** project has to be created and linked to the main BGE project, [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

* There is a CNAG script, that should do the deed of creating the umbrella.xml file:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Cladocora caespitosa" -t jaClaCaes1 -p ERGA-BGE -c SCILIFELAB -a PRJEB81307 -x 130055
    ```
    Explanation of arguments:
    * -s: scientific name e.g. "Lithobius stygius"
    * -t: tolId e.g. qcLitStyg1
    * -a: the accession number of the raw reads project e.g. PRJEB76283
    * -x: NCBI taxonomy id e.g. 2750798

* Copy `submission-umbrella.xml` from any of the previous BGE species, check that the hold date is as wanted.

* Submit using curl (can be done from laptop):
    ```
    curl -u Username:Password -F "SUBMISSION=@submission-umbrella.xml" -F "PROJECT=@umbrella.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-10-15T14:45:12.569+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB81311" alias="erga-bge-jaClaCaes-study-umbrella-2024-10-15" status="PRIVATE" holdUntilDate="2026-03-07Z"/>
        <SUBMISSION accession="ERA30876363" alias="SUBMISSION-15-10-2024-14:45:12:356"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
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
    <RECEIPT receiptDate="2025-08-27T10:02:37.507+01:00" submissionFile="submission-release-project.xml" success="true">
        <MESSAGES>
            <INFO>project accession "PRJEB81311" is set to public status.</INFO>
        </MESSAGES>
        <ACTIONS>RELEASE</ACTIONS>
    </RECEIPT>    
    ```

* **Note:** Add the assembly project `PRJEB81308` when it has been submitted and made public, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.
