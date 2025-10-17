---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB96490 (umbrella), PRJEB90601 (experiment), PRJEB90602 (assembly)
---

# BGE - *Dactylopius coccus*

## Submission task description
Submission of raw reads for *Dactylopius coccus* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Dactylopius-coccus-metadata.xlsx)
* [BGE HiFi metadata](./data/ihDacCocc-HiFi.tsv)
* [BGE HiC metadata](./data/ihDacCocc-HiC.tsv)
* [BGE RNAseq metadata](./data/ihDacCocc-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiFi
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput *.bam` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.
#### XML
* I created [ihDacCocc-HiFi.tsv](./data/ihDacCocc-HiFi.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f ihDacCocc-HiFi.tsv -p ERGA-BGE -o ihDacCocc-HiFi
    ```

* Study is private, so submission.xml with hold date is used.

* Submit both projects and experiment in one go, i.e:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@ihDacCocc-HiFi.study.xml" -F "EXPERIMENT=@ihDacCocc-HiFi.exp.xml" -F "RUN=@ihDacCocc-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-18T15:14:23.162+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14537947" alias="exp_ihDacCocc_HiFi_WGS_LV6000903717_pr_222" status="PRIVATE"/>
        <RUN accession="ERR15132702" alias="run_ihDacCocc_HiFi_WGS_LV6000903717_pr_222_bam_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB90601" alias="erga-bge-ihDacCocc-study-rawdata-2025-06-18" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP173603" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB90602" alias="erga-bge-ihDacCocc15_primary-2025-06-18" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP173604" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA33331594" alias="SUBMISSION-18-06-2025-15:14:22:915"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>    
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit HiC
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [ihDacCocc-HiC.tsv](./data/ihDacCocc-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f ihDacCocc-HiC.tsv -p ERGA-BGE -o ihDacCocc-HiC
    ```
* Update ihDacCocc-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90601"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title, since the other data types have the platform named
* Study is public, so submission-noHold.xml is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission-noHold.xml" -F "EXPERIMENT=@ihDacCocc-HiC.exp.xml" -F "RUN=@ihDacCocc-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-09-25T13:57:56.610+01:00" submissionFile="submission-noHold.xml" success="true">
        <EXPERIMENT accession="ERX15056354" alias="exp_ihDacCocc_Hi-C_LV6000903715_HC052-2A1B" status="PRIVATE"/>
        <RUN accession="ERR15651791" alias="run_ihDacCocc_Hi-C_LV6000903715_HC052-2A1B_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA35018373" alias="SUBMISSION-25-09-2025-13:57:56:281"/>
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
* I created [ihDacCocc-RNAseq.tsv](./data/ihDacCocc-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f ihDacCocc-RNAseq.tsv -p ERGA-BGE -o ihDacCocc-RNAseq
    ```
* Update ihDacCocc-RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90601"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@ihDacCocc-RNAseq.exp.xml" -F "RUN=@ihDacCocc-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit assembly

* I created a manifest file [ihDacCocc15-manifest.txt](./data/ihDacCocc15-manifest.txt)
* I added a note in the description that the quality of the HiC data is low. I also added this note to the library_construction protocol of the HiC experiment.
* I created a folder on Uppmax (/proj/snic2022-6-208/nobackup/submission/D-coccus/) and copied & gzipped manifest, assembly file and chromosome list there
* Then all files where submitted (first validation then submission) from Pelle on Uppmax using Webin-CLI:

    ```
    interactive -t 08:00:00 -A uppmax2025-2-58
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./ihDacCocc15-manifest.txt -validate
    ```
* Receipt:
    ```
    INFO : Your application version is 9.0.1
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/D-coccus/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/D-coccus/ihDacCocc15_pri_20251008.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/D-coccus/chromosome_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28541641
    ```
* I added the accession number to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `Assembly submitted` to `Yes`, as well as set assembly as status `Submitted` in [Tracking_tool_Seq_centers](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/edit?pli=1&gid=0#gid=0)
* Accessioned:
    ```
    ASSEMBLY_NAME | ASSEMBLY_ACC  | STUDY_ID   | SAMPLE_ID   | CONTIG_ACC                      | SCAFFOLD_ACC | CHROMOSOME_ACC
    ihDacCocc15.1 | GCA_977009245 | PRJEB90602 | ERS21327155 | CDRMXH010000001-CDRMXH010000004 |              | OZ346538-OZ346545
    ```
* Release study and check that it is shown under umbrella

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

### Submit 2 endosymbionts
* Submit Spiroplasma and Wolbachia endosymbionts, see [Stylops ater README](../ERGA-Stylops-ater/README.md/#submission-symbionts) how it was done there.

#### Suggested steps

1. Register new taxonomies
1. Register 2 projects/studies
1. Register 2 samples with fields `sample symbiont of` (with the sample accession of host) and `symbiont` (set to 'Y')
1. Submit assemblies
1. Add to umbrella of host

#### Register new taxonomies
* The fields to fill:
    ```
    proposed_name: the organism name (mandatory). We will check if there is a taxa registered with the given name.
    name_type: allowed taxon name types are
        Environmental Name
        Synthetic Name
        Novel Species
        Unidentified Species
        Published Name
    host: host associated with the taxon, if applicable
    project_id: project associated with the taxa, if applicable
    description: a short description of the taxon, please provide an authority or publication where available, or any other information describing the organism
    ```

* In the [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/taxonomy_requests.html#creating-taxon-requests) they state *"If you have multiple names to request, please do this as a single request"*. Hence, I logged in to ENA and went to [Register taxonomy](https://www.ebi.ac.uk/ena/submit/webin/taxonomy) in the Samples menu and downloaded a [taxonomy template](./data/taxonomy_template.tsv). After filling it in, it was uploaded to ENA (2025-10-16). It is expected to take quite a while before it is granted.
* As it turns out, there is already a taxon for Wolbachia ([Taxon:1605993](https://www.ebi.ac.uk/ena/browser/view/Taxon:1605993)), so only the Spriroplasma is necessary to apply for


#### Register study
* While not necessary, since there are 2 samples, I decided to create 2 separate studies
* I registered the them via browser, set release dates to 2026-03-07 
    ```
    title:          Wolbachia endosymbiont of Dactylopius coccus genome assembly
    study_name:     Wolbachia-ihDacCocc15
    study_abstract: This project provides the genome assembly of Wolbachia endosymbiont of Dactylopius coccus.	
    ```
    ```
    title:          Spiroplasma endosymbiont of Dactylopius coccus genome assembly
    study_name:     Spiroplasma-ihDacCocc15
    study_abstract: This project provides the genome assembly of Spiroplasma endosymbiont of Dactylopius coccus.	
    ```
* Accession numbers: `PRJEB100832` for Wolbachia and `PRJEB100833` for Spiroplasma
* I added the accession numbers to SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/)

#### Register samples
**Wolbachia**
* I submitted 1 samples, by uploading the sheet [wolbachia-sample.tsv](./data/wolbachia-sample.tsv)
* Accession number received: `ERS27074074`

**Spiroplasma** **TODO**
* I had to wait until the taxonomy request was approved
* I then submitted 1 sample, by uploading the sheet [spiroplasma-sample.tsv](./data/spiroplasma-sample.tsv)
* Accession number received: `` 

#### Submit assemblies

**Wolbachia**
* I created 2 manifest files [wolbachia-manifest.txt](./data/wolbachia-manifest.txt) and a chromosome_list file
* I copied them to Uppmax (/proj/snic2022-6-208/nobackup/submission/D-coccus) 
* Then all files were submitted (first validation then submission) from Pelle on Uppmax using Webin-CLI:

    ```
    interactive -t 02:00:00 -A uppmax2025-2-58
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./wolbachia-manifest.txt -validate    
    ```
* Receipts:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/D-coccus/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/D-coccus/ihDacCocc15_contaminations_Wolbachia_endosymbiont.fasta.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/D-coccus/wolbachia-chromosome_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28545900
    ```
* I added the accession number to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/)
* Accessioned:
    ```

    ```

**Spiroplasma**   **TODO**
* I created [spiroplasma-manifest.txt](./data/spiroplasma-manifest.txt) and a chromosome_list file
* I copied them to Uppmax (/proj/snic2022-6-208/nobackup/submission/D-coccus)
* Then all files were submitted (first validation then submission) from Pelle on Uppmax using Webin-CLI:

    ```
    interactive -t 02:00:00 -A uppmax2025-2-58
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./spiroplasma-manifest.txt -validate    
    ```
* Receipt:
    ```

    ```

* I added the accession number to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/)
* Accessioned:
    ```

    ```
#### Add to umbrella
**Wolbachia**
* I reused [update.xml](./data/update.xml) and created [umbrella_wolbachia.xml](./data/umbrella__wolbachia.xml)
* Submit:
    ```
    curl -u Username:Password -F "SUBMISSION=@update.xml" -F "PROJECT=@umbrella_wolbachia.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-10-17T14:53:16.917+01:00" submissionFile="update.xml" success="true">
        <PROJECT accession="PRJEB96490" alias="erga-bge-ihDacCocc-study-umbrella-2025-08-27" status="PUBLIC"/>
        <SUBMISSION accession="" alias="SUBMISSION-17-10-2025-14:53:16:793"/>
        <MESSAGES/>
        <ACTIONS>MODIFY</ACTIONS>
    </RECEIPT>
    ```
**Spiroplasma** **TODO**
* I reused [update.xml](./data/update.xml) and created [umbrella_spiroplasma.xml](./data/umbrella_spiroplasma.xml)
* Submit:
    ```
    curl -u Username:Password -F "SUBMISSION=@update.xml" -F "PROJECT=@umbrella_spiroplasma.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
 
### Umbrella project
For each of the BGE species, an **umbrella** project has to be created and linked to the main BGE project, [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

1. Release the child project via browser
1. Collect scientific name and tolId from the metadata template sheet
1. Go to [ENA browser](https://www.ebi.ac.uk/ena/browser/home) and enter the scientific name as search term
    1. To the left side, there should be a **Taxon** subheading, that gives the identifier
1. Copy experiment accession number from metadata in top of this README
* There is a CNAG script, that should do the deed of creating the xml file:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Dactylopius coccus" -t ihDacCocc15 -p ERGA-BGE -c SCILIFELAB -a PRJEB90601 -x 765876
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
    <RECEIPT receiptDate="2025-08-27T10:12:43.626+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB96490" alias="erga-bge-ihDacCocc-study-umbrella-2025-08-27" status="PRIVATE" holdUntilDate="2026-03-07Z"/>
        <SUBMISSION accession="ERA34838311" alias="SUBMISSION-27-08-2025-10:12:43:439"/>
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
    <RECEIPT receiptDate="2025-08-27T10:15:05.090+01:00" submissionFile="submission-release-project.xml" success="true">
        <MESSAGES>
            <INFO>project accession "PRJEB96490" is set to public status.</INFO>
        </MESSAGES>
        <ACTIONS>RELEASE</ACTIONS>
    </RECEIPT>    
    ```
