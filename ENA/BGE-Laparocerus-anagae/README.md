---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB96495 (umbrella), PRJEB83457 (experiment), PRJEB83458 (assembly), PRJEB98920 (haploid), PRJEB98919 (mito)
---

# BGE - *Laparocerus anagae*

## Submission task description
Submission of raw reads for *Laparocerus anagae* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample(s) used for sequencing has already been submitted via COPO.
Submission will be done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Laparocerus-anagae-metadata.xlsx)
* [BGE HiFi metadata](./data/icLapAnag-hifi.tsv)
* [BGE HiC metadata](./data/icLapAnag-hic.tsv)
* [BGE RNAseq metadata](./data/icLapAnag-rnaseq.tsv)

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
* Need to check the experimental metadata with NGI. Answer: The same as previous HiFi datasets.

#### HiFi xml
* I copied [submission.xml](./data/submission.xml) from BGE-Crayfish, using the same embargo date
* **Note:** There are 2 bam files, need to make sure that the script works
* Running the script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icLapAnag-hifi.tsv -p ERGA-BGE -o icLapAnag-HiFi
    ```
    * As suspected, the script now creates 2 experiments and also wrongly adds `<SINGLE>NOMINAL_LENGTH</SINGLE>` in LIBRARY_LAYOUT. I guess we need 2 versions of the script now... For now, I will manually edit the exp .xml file, remove the second experiment and change the layout to `</SINGLE>`.

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
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-12-12T14:38:38.308Z" success="false">
        <MESSAGES>
            <ERROR>experiment xml is not valid, error parsing the file: "icLapAnag-HiFi.exp.xml".</ERROR>
        </MESSAGES>
    </RECEIPT>
    ```
    * I have no idea why it didn't work, and what to do. I've compared to e.g. crayfish HiFi submission, and they are similar. Would like a better explanation, the only difference is that I now submitted from laptop and not from Uppmax, but that cannot be why.
    * I tried submitting the xml files via browser, thinking it might produce better error messages, but it didn't.
    * I then copied the rows from Cladocora caespitosa experiment xml file, and edited only what differed, and for some reason this worked...
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-12-12T15:30:57.930Z" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX13461187" alias="exp_icLapAnag_HiFi_WGS_FS38819783_pr_136" status="PRIVATE"/>
        <RUN accession="ERR14058183" alias="run_icLapAnag_HiFi_WGS_FS38819783_pr_136_bam_1" status="PRIVATE"/>
        <RUN accession="ERR14058184" alias="run_icLapAnag_HiFi_WGS_FS38819783_pr_136_bam_2" status="PRIVATE"/>
        <PROJECT accession="PRJEB83457" alias="erga-bge-icLapAnag-study-rawdata-2024-12-12" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP167091" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB83458" alias="erga-bge-icLapAnag1_primary-2024-12-12" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP167092" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA31041307" alias="SUBMISSION-12-12-2024-15:30:57:279"/>
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
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [icLapAnag-HiC.tsv](./data/icLapAnag-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icLapAnag-HiC.tsv -p ERGA-BGE -o icLapAnag-HiC
    ```
* Update icLapAnag-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB83457"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title, since the other data types have the platform named
* Study will be private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@icLapAnag-HiC.exp.xml" -F "RUN=@icLapAnag-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-07-04T10:37:15.320+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14602199" alias="exp_icLapAnag_Hi-C_FS38819792_HC020-2A1A" status="PRIVATE"/>
        <RUN accession="ERR15196543" alias="run_icLapAnag_Hi-C_FS38819792_HC020-2A1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA33558434" alias="SUBMISSION-04-07-2025-10:37:15:011"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit RNAseq - **TODO**
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [icLapAnag-RNAseq.tsv](./data/icLapAnag-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f icLapAnag-RNAseq.tsv -p ERGA-BGE -o icLapAnag-RNAseq
    ```
* Update icLapAnag-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB83457"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@icLapAnag-RNAseq.exp.xml" -F "RUN=@icLapAnag-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit assembly

* For this species we have 3 assemblies to submit, 2 haplotypes and 1 mito. This means we need 2 additional studies
    * I created [icLapAnag-assembly-studies.xml](./data/icLapAnag-assembly-studies.xml) and submitted using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml"  -F "PROJECT=@icLapAnag-assembly-studies.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
    * Receipt:
    ```
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-10-09T13:49:52.632+01:00" submissionFile="submission.xml" success="true">
        <PROJECT accession="PRJEB98919" alias="erga-bge-icLapAnag-study-mito-2025-10-09" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP181275" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB98920" alias="erga-bge-icLapAnag1_haplo-2025-10-09" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP181276" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA35054634" alias="SUBMISSION-09-10-2025-13:49:52:531"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
ls
* I created 3 manifest files [icLapAnag1-hap1-manifest.txt](./data/icLapAnag1-hap1-manifest.txt), [icLapAnag1-hap2-manifest.txt](./data/icLapAnag1-hap2-manifest.txt), and [icLapAnag1-mito-manifest.txt](./data/icLapAnag1-mito-manifest.txt)
* I also created 3 chromosome_lists: [chromosome_list_hap1.txt](./data/chromosome_list_hap1.txt), [chromosome_list_hap2.txt](./data/chromosome_list_hap2.txt), [chromosome_list_mito.txt](./data/chromosome_list_mito.txt)
* I created a folder on Uppmax (/proj/snic2022-6-208/nobackup/submission/L-anagae/) and copied & gzipped manifests, assembly files and chromosome list theres
* Then all files where submitted (first validation then submission) from Pelle on Uppmax using Webin-CLI:

    ```
    interactive -t 08:00:00 -A uppmax2025-2-58
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./icLapAnag1-hap1-manifest.txt -validate
    ```
* Receipt hap1:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/L-anagae/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/L-anagae/icLapAnag1_hap1_20250930_noMito.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/L-anagae/chromosome_list_hap1.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28534160
    ```
* Receipt hap2:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/L-anagae/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/L-anagae/icLapAnag1_hap2_20250930_noMito.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/L-anagae/chromosome_list_hap2.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28534161
    ```
* Receipt mito:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/L-anagae/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/L-anagae/icLapAnag1_mito_20251009.fasta.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/L-anagae/chromosome_list_mito.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28534162
    ```
* I added the accession numbers to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `Assembly submitted` to `Yes`, as well as set assembly as status `Submitted` in [Tracking_tool_Seq_centers](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/edit?pli=1&gid=0#gid=0)
* Accessioned:
    ```
    ASSEMBLY_NAME | ASSEMBLY_ACC  | STUDY_ID   | SAMPLE_ID   | CONTIG_ACC                      | SCAFFOLD_ACC | CHROMOSOME_ACC

    ```
* Release study and check that it is shown under umbrella

#### Add assembly to umbrella
* Add the assembly projects when they have been submitted, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.
* Create [update.xml](./data/update.xml) and [umbrella_modified.xml](./data/umbrella_modified.xml)
* Submit:
    ```
    curl -u Username:Password -F "SUBMISSION=@update.xml" -F "PROJECT=@umbrella_modified.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```


* **Note:** Add the assembly project `` when it has been submitted and made public, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.

### Umbrella project
* For each of the BGE species, an **umbrella** project has to be created and linked to the main BGE project, [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

1. Release the child project via browser
1. Collect scientific name and tolId from the metadata template sheet
1. Go to [ENA browser](https://www.ebi.ac.uk/ena/browser/home) and enter the scientific name as search term
    1. To the left side, there should be a **Taxon** subheading, that gives the identifier
1. Copy experiment accession number from metadata in top of this README
* There is a CNAG script, that should do the deed of creating the xml file:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Laparocerus anagae" -t icLapAnag1 -p ERGA-BGE -c SCILIFELAB -a PRJEB83457 -x 1963931
    ```
    Explanation of arguments:
    * -s: scientific name e.g. "Lithobius stygius"
    * -t: tolId e.g. qcLitStyg1
    * -a: the accession number of the raw reads project e.g. PRJEB76283
    * -x: NCBI taxonomy id e.g. 2750798

* Copy `submission-umbrella.xml` from any of the previous BGE species
* Submit using curl:
    ```
    curl -u Username:Password -F "SUBMISSION=@submission-umbrella.xml" -F "PROJECT=@umbrella.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-08-27T11:08:14.502+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB96495" alias="erga-bge-icLapAnag-study-umbrella-2025-08-27" status="PRIVATE" holdUntilDate="2027-08-27+01:00"/>
        <SUBMISSION accession="ERA34838329" alias="SUBMISSION-27-08-2025-11:08:14:166"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
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
    <RECEIPT receiptDate="2025-08-27T11:09:51.680+01:00" submissionFile="submission-release-project.xml" success="true">
        <MESSAGES>
            <INFO>project accession "PRJEB96495" is set to public status.</INFO>
        </MESSAGES>
        <ACTIONS>RELEASE</ACTIONS>
    </RECEIPT>    
    ```
