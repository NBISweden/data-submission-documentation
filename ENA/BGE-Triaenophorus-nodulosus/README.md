---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB80085 (umbrella), PRJEB79894 (experiment), PRJEB80032 (assembly), PRJEB104675 (mito assembly), PRJEB104676 (haplotype assembly)
---

# BGE - *Triaenophorus nodulosus*

## Submission task description
Submission of raw reads for *Triaenophorus nodulosus* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.

## Procedure overview and links to examples

* [ERGA-BGE_ReadData_Submission_Guide](https://github.com/ERGA-consortium/ERGA-submission/blob/main/BGE/ERGA-BGE_ReadData_Submission_Guide.md)

## Lessons learned
For this particular species it was not possible to identify an NGI tube or well ID. The BioSample used for sequencing (SAMEA115098039) is not referenced with a tube or well ID in the [ERGA portal](https://genomes.cnag.cat/erga-stream/). Actually, it is not referenced at all. To proceed with the submission the NGI delivery folder name was used (`pr_111`).


### Register study
* Title, abstract, and keyword for the study was set according to ERGA recommendations.
* Release date was set 2 years in the future. As we are still waiting for Hi-C data and only have HiFi data yet, we have decided in the DM team to delay making the data public for a while and allow for the other data types to be available. 
* The study was registered via the browser, using NBIS DM broker account, received accession number: `PRJEB79894`

### Submit HiFi
#### Collect metadata
* There were 18 BioSamples collected and registered for the species. The NGI tube register number was not possible to bridge (see above). After contact with NGI it was determined that the sample used (SAMEA115098039) was identified as TolID `heTriNodu1`, corresponding to the specimen ID `ERGA AV 5534 02`. 

* Information on experiment metadata was provided by NGI via Slack and entered into a [spreadsheet](./data/PRJEB79894-experiment.tsv).

* Sequence file was uploaded from Rackham to the ENA, after exporting the ENA broker password, using the command line:

```
ascp -k 3 -d -q --mode=send -QT -l300M --host=webin.ebi.ac.u
k -userName=Webin-39907 /proj/snic2022-6-208/INBOX/BGE_Triaenophorus_nodulosus/EBP_pr_111/files/pr_111/rawdata/pr_111_001/m84045_240818_005314_s2.hifi_reads.bc2118.bam /bge-triaenophorus/ &
```
Upload was slow to begin (~25 mins) but once begun it uploaded as expected.

* Manifests were made from the metadata spreadsheet by using a modified script [get_ENA_XML_files_yv.py](./scripts/get_ENA_XML_files_yv.py), generating XML files for Study (not used), [Experiment](./data/heTriNodu-HiFi.exp.xml) and [Runs](./data/heTriNodu-HiFi.runs.xml). Also, an md5 sum was calculated for each data file and included in the spreadsheet. 

* A [submission.xml](./data/submission.xml) file was made according to ENA specifications.

* Due to circumstances the manifests were submitted via the web portal this time without trouble, hence the separate registration of sequence and annotation projects.

* Received accession numbers: `ERX13023779`,`ERR13654568`

### Submit Hi-C
#### Preparations

* The sample identifier received, `2 (ID in minigrip: TN2.1)` was not possible to connect to a biosample either via biosamples database or ERGA tracking portal.
    * For HiFi we ended up using 'SAMEA115098039', after conferring with NGI, should we use the same for Hi-C?
    * There is another biosample, 'SAMEA115098038', which also seems to be an origin sample, from which other samples have been derived.
    * I asked NGI and we deduced that it should be `SAMEA115098038` for HiC since this one has 2's (specimen id is 'ERGA AV 5534 02' and ToLID is 'heTriNodu2')
    * Since this biosample isn't in ERGA tracking portal (only the derived samples are), I don't have a 'tube or well id' but will put the specimen id instead.

* First batch of HiC will be used, hence need to do data transfer (which I did for all first batch HiC in one go, but below is example of how to):
    ```
    interactive -t 08:00:00 -A uppmax2025-2-58
    cat sample_ATGTCAAG+GAGCTCTA_part*_R1.fastq.gz > ../to_ENA/triNodu_sample_ATGTCAAG+GAGCTCTA_R1.fastq.gz
    cat sample_ATGTCAAG+GAGCTCTA_part*_R2.fastq.gz > ../to_ENA/triNodu_sample_ATGTCAAG+GAGCTCTA_R2.fastq.gz
    cd ../to_ENA
    lftp webin2.ebi.ac.uk -u Webin-39907
    mput triNodu*.fastq.gz
    ```
#### XML
* I created [heTriNodu-HiC.tsv](./data/heTriNodu-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f heTriNodu-HiC.tsv -p ERGA-BGE -o heTriNodu-HiC
    ```
* Update heTriNodu-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB79894"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission-hold.xml with hold date 2026-09-09 is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission-hold.xml" -F "EXPERIMENT=@heTriNodu-HiC.exp.xml" -F "RUN=@heTriNodu-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-03-19T10:05:48.109Z" submissionFile="submission-hold.xml" success="true">
        <EXPERIMENT accession="ERX14162750" alias="exp_heTriNodu_Hi-C_ERGA_AV_5534_02_HC014_1A1A" status="PRIVATE"/>
        <RUN accession="ERR14758855" alias="run_heTriNodu_Hi-C_ERGA_AV_5534_02_HC014_1A1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA31211420" alias="SUBMISSION-19-03-2025-10:05:47:428"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### HiC version 2
* I created [heTriNodu-2-HiC.tsv](./data/heTriNodu-2-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f heTriNodu-2-HiC.tsv -p ERGA-BGE -o heTriNodu-2-HiC
    ```
* Update heTriNodu-2-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB79894"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission-hold.xml with hold date 2026-09-09 is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission-hold.xml" -F "EXPERIMENT=@heTriNodu-2-HiC.exp.xml" -F "RUN=@heTriNodu-2-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-07-04T11:07:37.921+01:00" submissionFile="submission-hold.xml" success="true">
        <EXPERIMENT accession="ERX14603648" alias="exp_heTriNodu_Hi-C_ERGA_AV_5534_02_HC014-2A1A" status="PRIVATE"/>
        <RUN accession="ERR15197992" alias="run_heTriNodu_Hi-C_ERGA_AV_5534_02_HC014-2A1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA33558458" alias="SUBMISSION-04-07-2025-11:07:37:678"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit RNAseq

### Submit assembly
* A study / project was created, receiving accession number `PRJEB80032`
* Yvonnes note: Not sure how it was registered, hence lack of information other than the accession number. 
* For this species both a haplotype and a mito assembly was identified, in addition to the primary assembly. Hence 2 more projects was needed:
    * I created [heTriNodu-hapMito-assembly-studies.xml](./data/heTriNodu-assembly-studies.xml) and submitted using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission-hold.xml"  -F "PROJECT=@heTriNodu-assembly-studies.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
    * Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-12-02T07:41:30.195Z" submissionFile="submission-hold.xml" success="true">
        <PROJECT accession="PRJEB104675" alias="erga-bge-heTriNodu1_mito-2025-12-02" status="PRIVATE" holdUntilDate="2026-09-09+01:00">
            <EXT_ID accession="ERP185931" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB104676" alias="erga-bge-heTriNodu1_haplo-2025-12-02" status="PRIVATE" holdUntilDate="2026-09-09+01:00">
            <EXT_ID accession="ERP185932" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA35288949" alias="SUBMISSION-02-12-2025-07:41:30:114"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
* I created 3 manifest files [heTriNodu1-hap1-manifest.txt](./data/heTriNodu1-hap1-manifest.txt), [heTriNodu1-hap2-manifest.txt](./data/heTriNodu1-hap2-manifest.txt), [heTriNodu1-mito-manifest.txt](./data/heTriNodu1-mito-manifest.txt) as well as chromosome lists and unlocalised lists (for haploids).
* I created a folder on Uppmax (/proj/snic2022-6-208/nobackup/submission/T-nodulosus) and copied & gzipped manifest, assembly file and chromosome list there
* Then all files where submitted (first validation then submission) from Pelle on Uppmax using Webin-CLI:

    ```
    interactive -t 08:00:00 -A uppmax2025-2-58
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./heTriNodu1-hap1-manifest.txt -validate
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./heTriNodu1-hap2-manifest.txt -validate
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./heTriNodu1-mito-manifest.txt -validate
    ```
* Receipt hap1:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/T-nodulosus/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/T-nodulosus/heTriNodu1_hap1_20251201.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/T-nodulosus/heTriNodu1-hap1-chromosome_list.txt.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/T-nodulosus/heTriNodu1-hap1-unlocalised_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28675713
    ```
* Receipt hap2:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/T-nodulosus/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/T-nodulosus/heTriNodu1_hap2_20251201.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/T-nodulosus/heTriNodu1-hap2-chromosome_list.txt.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/T-nodulosus/heTriNodu1-hap2-unlocalised_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28675714
    ```
* Receipt mito:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/T-nodulosus/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/T-nodulosus/heTriNodu1_mito_20251201.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/T-nodulosus/heTriNodu1-mito-chromosome_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28675715
    ```
* I added the accession number to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `Assembly submitted` to `Yes`, as well as set assembly as status `Submitted` in [Tracking_tool_Seq_centers](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/edit?pli=1&gid=0#gid=0)
* Accessioned:
    ```
    ASSEMBLY_NAME | ASSEMBLY_ACC  | STUDY_ID   | SAMPLE_ID   | CONTIG_ACC                      | SCAFFOLD_ACC | CHROMOSOME_ACC

    ```
* Release studies and check that they are shown under umbrella

#### Add assembly to umbrella
* Add the 3 assembly projects when they have been submitted, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.
* Create [update.xml](./data/update.xml) and [umbrella_modified.xml](./data/umbrella_modified.xml)
* Submit:
    ```
    curl -u Username:Password -F "SUBMISSION=@update.xml" -F "PROJECT=@umbrella_modified.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Received a weird error message about cyclic dependency:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-12-02T12:23:58.534Z" submissionFile="update.xml" success="false">
        <PROJECT alias="erga-bge-heTriNodu-study-umbrella-2024-09-12" status="PUBLIC"/>
        <SUBMISSION alias="SUBMISSION-02-12-2025-12:23:58:278"/>
        <MESSAGES>
            <ERROR>An exception occurred: Cyclic dependency error: there is an entry with parent: PRJEB80032 and child: PRJEB80085</ERROR>
        </MESSAGES>
        <ACTIONS>MODIFY</ACTIONS>
    </RECEIPT>
    ```
* Seems as if, when I created the umbrella initially, I added the assembly project as a parent instead of a child. Hence, I have to remove the umbrella from the assembly project, add umbrella to the BGE project, and then finally I can add all 3 assemblies to the umbrella. Not sure I'm able to fix this so I asked ENA support for help (2025-12-02).

### Create umbrella

For each of the BGE species, an umbrella project has to be created and linked to the main BGE project, [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

* Using the CNAG script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Triaenophorus nodulosus" -t heTriNodu1 -p ERGA-BGE -c SCILIFELAB -a PRJEB79894 -x 56557
    ```
* Create a [submission-umbrella.xml](./data/submission-umbrella.xml)

* Submit using curl:
    ```
    curl -u Username:Password -F "SUBMISSION=@submission-umbrella.xml" -F "PROJECT=@umbrella.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-09-12T14:41:48.893+01:00" submissionFile="submission-umbrella.xml" success="true">
     <PROJECT accession="PRJEB80085" alias="erga-bge-heTriNodu-study-umbrella-2024-09-12" status="PRIVATE" holdUntilDate="2026-09-12+01:00"/>
     <SUBMISSION accession="ERA30790827" alias="SUBMISSION-12-09-2024-14:41:48:346"/>
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
    <RECEIPT receiptDate="2025-08-27T12:56:53.738+01:00" submissionFile="submission-release-project.xml" success="true">
        <MESSAGES>
            <INFO>project accession "PRJEB80085" is set to public status.</INFO>
        </MESSAGES>
        <ACTIONS>RELEASE</ACTIONS>
    </RECEIPT>    
    ```

* **TODO:** Add the assembly study `PRJEB80032` as child to the umbrella project as well (currently only the genomic sequencing project is attached)
