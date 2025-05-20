---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB77281 (umbrella), PRJEB76281 (experiment), PRJEB76282 (assembly), PRJEB89356 (mito assembly)
---

# BGE - *Astagobius angustatus*

## Submission task description
Submission of raw reads for *Astagobius angustatus* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Astagobius-angustatus-metadata.xlsx)
* [BGE HiFi metadata](./data/icAstAngu-hifi.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Collecting metadata
* I then looked at the delivery README for the HiFi dataset (on Uppmax) and extracted the Name (`ERGA_TD_5269_06`). I then went to [BioSamples](https://www.ebi.ac.uk/biosamples/samples?text=Astagobius+angustatus&page=2) and extracted the 2 samples that had this name as `specimen_id`. Since `SAMEA113399603` was the same as `SAMEA113399597`, I decided to use the latter. 
* I checked the [ERGA tracking portal](https://genomes.cnag.cat/erga-stream/samples/), using both the biosample accession number as well as the species name, but there was no hit. I guess in this case we will not have a tube or well id, so will use UGC user id (`pr_056_001`) instead.
### Submit HiFi
#### Creating xml
* I copied [submission.xml](./data/submission.xml) from BGE-Crayfish, using the same embargo date
* I updated the get_ENA_xml_files.py script so that library name and title also includes PacBio
* Running the script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icAstAngu-hifi.tsv -p ERGA-BGE -o icAstAngu-HiFi
    ```

#### Data transfer
* Create folder `bge-astagobius` at ENA upload area using Filezilla
* Using aspera from Uppmax to ENA upload area:
    ```
    interactive -t 03:00:00 -A naiss2023-5-307
    module load ascp
    export ASPERA_SCP_PASS='password'
    ascp -k 3 -d -q --mode=send -QT -l300M --host=webin.ebi.ac.uk --user=Webin-XXXX /proj/snic2021-6-194/INBOX/BGE_Astagobius_angustatus/pr_056/rawdata/pr_056_001/m84045_240223_153821_s3.hifi_reads.bc2053.bam /bge-astagobius/ &
    ```
* Keep track of progress using FileZilla

#### Programmatic submission
* Copy all xml files to Uppmax:
    ```
    scp submission.xml icAstAngu-HiFi*.xml yvonnek@rackham.uppmax.uu.se:/home/yvonnek/BGE-astagobius/
    ```
* Submit both projects and experiment in one go, i.e:
    ```
    interactive -t 03:00:00 -A naiss2023-5-307
    curl -u username:password -F "SUBMISSION=@submission.xml"  -F "PROJECT=@icAstAngu-HiFi.study.xml" -F "EXPERIMENT=@icAstAngu-HiFi.exp.xml" -F "RUN=@icAstAngu-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-06-04T08:22:25.192+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX12562212" alias="exp_icAstAngu6_HiFi_WGS_pr_056_001" status="PRIVATE"/>
        <RUN accession="ERR13191070" alias="run_icAstAngu6_HiFi_WGS_pr_056_001_bam_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB76281" alias="erga-bge-icAstAngu-study-rawdata-2024-06-04" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP160839" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB76282" alias="erga-bge-icAstAngu6_primary-2024-06-04" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP160840" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA30577665" alias="SUBMISSION-04-06-2024-08:22:23:482"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
* Update of submission status at [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/)

### Submit HiC
* 2 samples were used, so a virtual sample had to be registered, referring to:
    * SAMEA113399598, well id FS42595176, icAstAngu1
    * SAMEA113399599, well id FS42595225, icAstAngu2
    * create a [icAstAngu-virtual-sample.tsv](./data/icAstAngu-virtual-sample.tsv) based on what was done for RNAseq of [Hydroglyphus hamulatus](../BGE-Hydroglyphus-hamulatus/data/icHydHamu-virtual-sample.tsv)
    * Accession number received: ERS22139083
* However, as it turned out the HiC data was useless, and there's no more material to re-sequence, so this species will not have HiC.

### Submit RNA-Seq
* Data transfer to ENA upload area (folder /bge-rnaseq/) was done previously for all RNAseq data (first batch)
* Create [icAstAngu-RNAseq.tsv](./data/icAstAngu-RNAseq.tsv)
    * Note: Another biosample (compared to HiFi) will be referred to
* Create [submission-noHold.xml](./data/submission-noHold.xml), without any hold date since study is public already
* Run CNAG script
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icAstAngu-RNAseq.tsv -p ERGA-BGE -o icAstAngu-RNAseq
    ```
* Validate output (ignore the study xml)
* Update icAstAngu-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB76281"/>
    ```
* Copy xml files to Uppmax
    ```
    scp icAstAngu-RNAseq.exp.xml icAstAngu-RNAseq.runs.xml submission-noHold.xml yvonnek@rackham.uppmax.uu.se:/home/yvonnek/BGE-astagobius/
    ```
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission-noHold.xml" -F  "EXPERIMENT=@icAstAngu-RNAseq.exp.xml" -F "RUN=@icAstAngu-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"   
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-10-18T10:30:52.089+01:00" submissionFile="submission-noHold.xml" success="true">
        <EXPERIMENT accession="ERX13250204" alias="exp_icAstAngu_Illumina_RNA-Seq_FS42595226_RE019-1B" status="PRIVATE"/>
        <RUN accession="ERR13847438" alias="run_icAstAngu_Illumina_RNA-Seq_FS42595226_RE019-1B_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA30885809" alias="SUBMISSION-18-10-2024-10:30:51:779"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    </RECEIPT>
    ```

* Add recevied accession numbers to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `RNA-seq submitted` to `yes`

### Submit assembly
* Since HiC failed for this species, the assembly (and HiFi + RNAseq) should still be submitted and made public, but denoted as a draft:
    * *"BGE wants us to upload the assembly for Astagobius, which I guess means that they want the reads uploaded as well. However, it should be marked as draft! This is what Christian writes: "Could you please upload the draft genomes and make them public? Additionally, it would be helpful to include a label in the BioProject description indicating the draft nature of these genomes, rather than referring to them as BGE or using other terminology."*
    * In practice I'm guessing that we remove the BGE label/keyword on study level and instead add 'draft', but not sure about the description/abstract part.
        * Done for both the so far private assembly study (also included draft in title) as well as for the public raw data study
* Status note 2025-03-07: work is still done on the assembly, but has lower priority than the more promising species. The bioinformatician will let me know when to submit the assembly and if HiC also should be submitted.
* We will not submit HiC unless someone within ERGA tells us to, since it couldn't be used for the assembly.
* There is a contig assembly (so no chromosome list), and a mito assembly meaning I need to create a separate study for that one.

#### Primary assembly
* Created [icAstAngu6-manifest.txt](./data/icAstAngu6-manifest.txt), copied the fasta file to local laptop, gzipped, validated and then submitted using Webin-CLI:
    ```
    java -jar ~/webin-cli-8.2.0.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./icAstAngu6-manifest.txt -validate
    ```
* Receipt:
    ```
    INFO : Your application version is 8.2.0
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /home/yvonne/BGE/A-angustatus-assembly/././webin-cli.report
    INFO : Uploading file: /home/yvonne/BGE/A-angustatus-assembly/icAstAngu_pri_20250422.fasta.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ26867398
    ```
* I added the accession number to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `Assembly submitted` to `Yes`
* The assembly has been accessioned:
    ```
    ASSEMBLY_NAME | ASSEMBLY_ACC  | STUDY_ID   | SAMPLE_ID   | CONTIG_ACC                      | SCAFFOLD_ACC | CHROMOSOME_ACC
    icAstAngu6.1  | GCA_965278915 | PRJEB76282 | ERS15394745 | CBDIHG010000001-CBDIHG010002532 |              | 
    ```
* I manually updated the release date of the assembly study to 2025-05-16.

#### Mito assembly
* I manually created [icAstAngu-mito-study.xml](./data/icAstAngu-mito-study.xml) and submitted via curl (no embargo):
    ```
    curl -u username:password -F "SUBMISSION=@submission-noHold.xml" -F "PROJECT=@icAstAngu-mito-study.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-05-07T16:48:19.576+01:00" submissionFile="submission-noHold.xml" success="true">
        <PROJECT accession="PRJEB89356" alias="erga-bge-icAstAngu6_mito-2025-05-07" status="PRIVATE" holdUntilDate="2027-05-07+01:00">
            <EXT_ID accession="ERP172383" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA33120775" alias="SUBMISSION-07-05-2025-16:48:19:364"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    </RECEIPT>
    ```   

* I created [icAstAngu6-mito-manifest.txt](./data/icAstAngu6-mito-manifest.txt), copied the fasta file to local laptop, created [mito_chromosome_list.txt](./data/mito_chromosome_list.txt), gzipped, validated and then submitted using Webin-CLI:
    ```
    java -jar ~/webin-cli-8.2.0.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./icAstAngu6-mito-manifest.txt -validate
    ```
* Receipt:
    ```
    INFO : Your application version is 8.2.0
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /home/yvonne/BGE/A-angustatus-assembly/././webin-cli.report
    INFO : Uploading file: /home/yvonne/BGE/A-angustatus-assembly/icAstAngu_mito_20250422.fasta.gz
    INFO : Uploading file: /home/yvonne/BGE/A-angustatus-assembly/mito_chromosome_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ26867399
    ```

* I added the accession numbers to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `Assembly submitted` to `Yes`
* Mito has been accessioned:
    ```
    ASSEMBLY_NAME     | ASSEMBLY_ACC  | STUDY_ID   | SAMPLE_ID   | CONTIG_ACC | SCAFFOLD_ACC | CHROMOSOME_ACC
    icAstAngu-mito6.1 | GCA_965278905 | PRJEB89356 | ERS15394745 |            |              | OZ257121-OZ257121
    ```
* Not sure why the study didn't become public immediately, since I used the submission-noHold.xml, but I changed the release date via the browser to 2025-05-16.

### Register umbrella projekt

For each of the BGE species, an umbrella project has to be created and linked to the main BGE project, [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

* There is a CNAG script, that should do the deed of creating the xml file:
    ```
    ./script/get_umbrella_xml_ENA.py -s "Astagobius angustatus" -t icAstAngu6 -p ERGA-BGE -c SCILIFELAB -a PRJEB76281 -x 1457099
    ```
* Create a submission-umbrella.xml
* Submit using curl:
    ```
    curl -u Username:Password -F "SUBMISSION=@submission-umbrella.xml" -F "PROJECT=@umbrella.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-07-05T13:05:10.857+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB77281" alias="erga-bge-icAstAngu-study-umbrella-2024-07-05" status="PRIVATE" holdUntilDate="2024-07-07+01:00"/>
        <SUBMISSION accession="ERA30670050" alias="SUBMISSION-05-07-2024-13:05:10:663"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```

#### Add assemblies to umbrella
* Create [umbrella_modified.xml](./data/umbrella_modified.xml), adding assembly project `PRJEB76282`and mito assembly project `PRJEB89356` as children, update embargo to 2025-05-10 via [update.xml](./data/update.xml)
* Submit using curl:
    ```
    curl -u Username:Password -F "SUBMISSION=@update.xml" -F "PROJECT=@umbrella_modified.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-05-07T17:16:55.439+01:00" submissionFile="update.xml" success="true">
        <PROJECT accession="PRJEB77281" alias="erga-bge-icAstAngu-study-umbrella-2024-07-05" status="PUBLIC"/>
        <SUBMISSION accession="" alias="SUBMISSION-07-05-2025-17:16:55:182"/>
        <MESSAGES/>
        <ACTIONS>MODIFY</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
