---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB77283 (umbrella), PRJEB76283 (experiment), PRJEB76284 (assembly), PRJEB96884 (mito assembly)
---

# BGE - *Lithobius stygius*

## Submission task description
Submission of raw reads for *Lithobius stygius* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Lithobius-stygius-metadata.xlsx)
* [BGE HiFi metadata](./data/qcLitStyg-hifi.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Collecting metadata
* I went to [BioSamples](https://www.ebi.ac.uk/biosamples/samples?text=Lithobius+stygius) and extracted all samples for this species, where SCILIFELAB was the GAL. I then looked at the delivery README for the HiFi dataset (on Uppmax) and extracted the Name (`FS42595405`). This I then pasted as filter in `Tube or well id` field, in the [ERGA tracking portal](https://genomes.cnag.cat/erga-stream/samples/) which returned biosample [SAMEA115117740](https://www.ebi.ac.uk/biosamples/samples/SAMEA115117740).

### Submitting HiFi
#### Creating xml
* I copied [submission.xml](./data/submission.xml) from BGE-Crayfish, using the same embargo date
* Running the script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qcLitStyg-hifi.tsv -p ERGA-BGE -o qcLitStyg-HiFi
    ```

#### Data transfer
* Create folder `bge-lithobius` at ENA upload area using Filezilla
* Using aspera from Uppmax to ENA upload area:
    ```
    interactive -t 03:00:00 -A naiss2023-5-307
    module load ascp
    export ASPERA_SCP_PASS='password'
    ascp -k 3 -d -q --mode=send -QT -l300M --host=webin.ebi.ac.uk --user=Webin-XXXX /proj/snic2021-6-194/INBOX/BGE_Lithobius_stygius/EBP_pr_087/files/pr_087/rawdata/pr_087_001/m84045_240505_040448_s4.hifi_reads.bc2087.bam /bge-lithobius/ &
    ```
* Keep track of progress using FileZilla

#### Programmatic submission
* Copy all xml files to Uppmax:
    ```
    scp submission.xml qcLitStyg-HiFi*.xml yvonnek@rackham.uppmax.uu.se:/home/yvonnek/BGE-lithobius/
    ```
* Submit both projects and experiment in one go, i.e:
    ```
    interactive -t 03:00:00 -A naiss2023-5-307
    curl -u username:password -F "SUBMISSION=@submission.xml"  -F "PROJECT=@qcLitStyg-HiFi.study.xml" -F "EXPERIMENT=@qcLitStyg-HiFi.exp.xml" -F "RUN=@qcLitStyg-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-06-04T08:44:47.136+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX12562222" alias="exp_qcLitStyg1_HiFi_WGS_FS42595405" status="PRIVATE"/>
        <RUN accession="ERR13191080" alias="run_qcLitStyg1_HiFi_WGS_FS42595405_bam_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB76283" alias="erga-bge-qcLitStyg-study-rawdata-2024-06-04" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP160841" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB76284" alias="erga-bge-qcLitStyg1_primary-2024-06-04" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP160842" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA30577677" alias="SUBMISSION-04-06-2024-08:44:46:768"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
* Update of submission status at [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/)

### Submit HiC
#### Preparations
* For the sample data, `ERGA EB 5301 05` was given from NGI. I went to Biosample, and found 2 possible samples, SAMEA115117737 and SAMEA115117716
* In the ERGA tracking portal, only the first was found (which is derived/same as the second). Hence, SAMEA115117737 with tube id FS42595408, was used.
* First batch of HiC will be used, hence need to do data transfer (which I did for all first batch HiC in one go, but below is example of how to):
    ```
    interactive -t 08:00:00 -A uppmax2025-2-58
    cat sample_GCAGGTTC+TTGCTTCT_part*_R1.fastq.gz > ../to_ENA/litStyg_sample_GCAGGTTC+TTGCTTCT_R1.fastq.gz
    cat sample_GCAGGTTC+TTGCTTCT_part*_R2.fastq.gz > ../to_ENA/litStyg_sample_GCAGGTTC+TTGCTTCT_R2.fastq.gz
    cd ../to_ENA
    lftp webin2.ebi.ac.uk -u Webin-39907
    mput litStyg*.fastq.gz
    ```
* For this species we have a second round of HiC, I transferred all of them in one go (`mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species)
    * litStyg_XL-4185-HC011-2A1A_S79_L008_R1_001.fastq.gz
    * litStyg_XL-4185-HC011-2A1A_S79_L008_R2_001.fastq.gz
* We received another sample reference for this HiC

#### XML
* I created [qcLitStyg-HiC.tsv](./data/qcLitStyg-HiC.tsv) containing both 1st and 2nd round of HiC.
* I need to make sure that they appear in separate experiments.
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qcLitStyg-HiC.tsv -p ERGA-BGE -o qcLitStyg-HiC
    ```
* Update qcLitStyg-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB76283"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is already public, so submission.xml without hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission-noHold.xml" -F "EXPERIMENT=@qcLitStyg-HiC.exp.xml" -F "RUN=@qcLitStyg-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-03-18T11:52:20.435Z" submissionFile="submission-noHold.xml" success="true">
        <EXPERIMENT accession="ERX14155832" alias="exp_qcLitStyg_Hi-C_FS42595408_HC011_1A1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX14155833" alias="exp_qcLitStyg_Hi-C_FS42595409_HC011-2A1A" status="PRIVATE"/>
        <RUN accession="ERR14751971" alias="run_qcLitStyg_Hi-C_FS42595408_HC011_1A1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR14751972" alias="run_qcLitStyg_Hi-C_FS42595409_HC011-2A1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA31210463" alias="SUBMISSION-18-03-2025-11:52:18:172"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    </RECEIPT>
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit RNA-Seq
* Data transfer to ENA upload area (folder /bge-rnaseq/) was done previously for all RNAseq data (first batch)
* Create [qcLitStyg-RNAseq.tsv](./data/qcLitStyg-RNAseq.tsv)
    * Note: used biosample with well id `FS42595406` in erga tracking portal
* Create [submission-noHold.xml](./data/submission-noHold.xml), without any hold date since study is public already
* Run CNAG script
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qcLitStyg-RNAseq.tsv -p ERGA-BGE -o qcLitStyg-RNAseq
    ```
* Validate output (ignore the study xml)
* Update qcLitStyg-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB76283"/>
    ```
* Copy xml files to Uppmax
    ```
    scp qcLitStyg-RNAseq.exp.xml qcLitStyg-RNAseq.runs.xml submission-noHold.xml yvonnek@rackham.uppmax.uu.se:/home/yvonnek/BGE-lithobius/
    ```
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission-noHold.xml" -F "EXPERIMENT=@qcLitStyg-RNAseq.exp.xml" -F "RUN=@qcLitStyg-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"   
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-10-18T14:07:32.612+01:00" submissionFile="submission-noHold.xml" success="true">
        <EXPERIMENT accession="ERX13254552" alias="exp_qcLitStyg_Illumina_RNA-Seq_FS42595406_RE023-1A" status="PRIVATE"/>
        <RUN accession="ERR13851786" alias="run_qcLitStyg_Illumina_RNA-Seq_FS42595406_RE023-1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA30887149" alias="SUBMISSION-18-10-2024-14:07:32:414"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    </RECEIPT>
    ```

* Add recevied accession numbers to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `RNA-seq submitted` to `yes`

### Submit assembly
* There are 2 assemblies, one genome and one mitochondrial.

#### Genome assembly
* I created a manifest file [qcLitStyg-manifest.txt](./data/qcLitStyg-manifest.txt), as well as a chromosome and unlocalised list in tab delimited format.
* I created a folder on Uppmax (/proj/snic2022-6-208/nobackup/submission/BGE-L-stygius/)
* Then all files where gzipped and submitted (first validation then submission) from Uppmax using Webin-CLI:
    ```
    interactive -t 08:00:00 -A uppmax2025-2-58
    module load java/OpenJDK_24+36
    java -jar ~/webin-cli-8.2.0.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./qcLitStyg-manifest.txt -validate
    ```
    * I had issues with Java Runtime, that the one available at Uppmax/Rackham only supports up to version 52.0 while the webin-cli version was compiled by version 61.0. Solution is to add a newer version (module load java/OpenJDK_24+36)
* Receipt:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/BGE-L-stygius/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/BGE-L-stygius/qcLitStygr_priCur_29082025.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/BGE-L-stygius/chromosome_list.txt.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/BGE-L-stygius/unlocalised_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28435528
    ```
* I added the accession number to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `Assembly submitted` to `Yes`, as well as set assembly as status `Submitted` in [Tracking_tool_Seq_centers](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/edit?pli=1&gid=0#gid=0)
* Accessioned:
    ```
    ASSEMBLY_NAME | ASSEMBLY_ACC  | STUDY_ID   | SAMPLE_ID   | CONTIG_ACC                      | SCAFFOLD_ACC | CHROMOSOME_ACC
    qcLitStyg1.1  | GCA_976940485 | PRJEB76284 | ERS17759200 | CDRHXL010000001-CDRHXL010000108 |              | OZ325067-OZ325087    
    ```
* I made the assembly project public 2025-09-25

#### Mito assembly
* I manually created [qcLitStyg-mito-study.xml](./data/qcLitStyg-mito-study.xml) and submitted via curl (no embargo):
    ```
    curl -u username:password -F "SUBMISSION=@submission-noHold.xml" -F "PROJECT=@qcLitStyg-mito-study.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-09-02T13:55:05.622+01:00" submissionFile="submission-noHold.xml" success="true">
        <PROJECT accession="PRJEB96884" alias="erga-bge-qcLitStyg1-mito-2025-09-03" status="PRIVATE" holdUntilDate="2027-09-02+01:00">
            <EXT_ID accession="ERP179510" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA34865175" alias="SUBMISSION-02-09-2025-13:55:05:533"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    </RECEIPT>
    ```   
* Though no hold, it was visible from the receipt that hold date became 2 years from now, so I manually needed to release via browser (done 2025-09-25)

* I created [qcLitStyg-mito-manifest.txt](./data/qcLitStyg-mito-manifest.txt), copied the fasta file to Uppmax, created [mito_chromosome_list.txt](./data/mito_chromosome_list.txt), gzipped, validated and then submitted using Webin-CLI:
    ```
    interactive -t 08:00:00 -A uppmax2025-2-58
    module load java/OpenJDK_24+36
    java -jar --enable-native-access=ALL-UNNAMED ~/webin-cli-8.2.0.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./qcLitStyg-mito-manifest.txt -validate
    ```
* Receipt:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/BGE-L-stygius/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/BGE-L-stygius/qcLitStygr_mito_29082025.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/BGE-L-stygius/mito-chromosome_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28435529
    ```

* I added the accession numbers to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `Assembly submitted` to `Yes`
* Mito has been accessioned:
    ```
    ASSEMBLY_NAME     | ASSEMBLY_ACC  | STUDY_ID   | SAMPLE_ID   | CONTIG_ACC | SCAFFOLD_ACC | CHROMOSOME_ACC
    qcLitStyg1-mito.1 | GCA_976940495 | PRJEB96884 | ERS17759200 |            |              | OZ325014-OZ325014
    ```

#### Add assemblies to umbrella
* **Note:** Add the assembly projects `PRJEB76284` and `PRJEB96884` when they have been submitted and made public, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.
* Create [update.xml](./data/update.xml) and [umbrella_modified.xml](./data/umbrella_modified.xml)
* Submit:
    ```
    curl -u Username:Password -F "SUBMISSION=@update.xml" -F "PROJECT=@umbrella_modified.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-09-04T07:24:24.434+01:00" submissionFile="update.xml" success="true">
        <PROJECT accession="PRJEB77283" alias="erga-bge-qcLitStyg-study-umbrella-2024-07-05" status="PUBLIC"/>
        <SUBMISSION accession="" alias="SUBMISSION-04-09-2025-07:24:24:180"/>
        <MESSAGES/>
        <ACTIONS>MODIFY</ACTIONS>
    </RECEIPT>
    ```
* **Note:** The assembly studies are not visible in umbrella, is that due to them not being public yet? Need to check when they have been accessioned and made public.

## Umbrella project
For each of the BGE species, an umbrella project has to be created and linked to the main BGE project, [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

* There is a CNAG script, that should do the deed of creating the xml file:
    ```
    ./script/get_umbrella_xml_ENA.py -s "Lithobius stygius" -t qcLitStyg1 -p ERGA-BGE -c SCILIFELAB -a PRJEB76283 -x 2750798
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
    <RECEIPT receiptDate="2024-07-05T13:23:11.589+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB77283" alias="erga-bge-qcLitStyg-study-umbrella-2024-07-05" status="PRIVATE" holdUntilDate="2024-07-07+01:00"/>
        <SUBMISSION accession="ERA30670052" alias="SUBMISSION-05-07-2024-13:23:11:288"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
