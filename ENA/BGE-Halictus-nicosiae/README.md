---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB96354 (umbrella), PRJEB90995 (experiment), PRJEB90996 (assembly), PRJEB106249 (Wolbachia), PRJEB106249 (Spiroplasma)
---

# BGE - *Halictus nicosiae*

## Submission task description
Submission of raw reads for *Halictus nicosiae* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Halictus-nicosiae-metadata.xlsx)
* [BGE HiFi metadata](./data/iyHalNico-HiFi.tsv)
* [BGE HiC metadata](./data/iyHalNico-HiC.tsv)
* [BGE RNAseq metadata](./data/iyHalNico-RNAseq.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit HiFi
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput *.bam` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.
#### XML
* I created [iyHalNico-HiFi.tsv](./data/iyHalNico-HiFi.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iyHalNico-HiFi.tsv -p ERGA-BGE -o iyHalNico-HiFi
    ```

* Study is private, so submission.xml with hold date is used.

* Submit both projects and experiment in one go, i.e:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "PROJECT=@iyHalNico-HiFi.study.xml" -F "EXPERIMENT=@iyHalNico-HiFi.exp.xml" -F "RUN=@iyHalNico-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-06-25T10:22:27.503+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14562399" alias="exp_iyHalNico_HiFi_WGS_LV6000911885_pr_230_001" status="PRIVATE"/>
        <RUN accession="ERR15157107" alias="run_iyHalNico_HiFi_WGS_LV6000911885_pr_230_001_bam_1" status="PRIVATE"/>
        <PROJECT accession="PRJEB90995" alias="erga-bge-iyHalNico-study-rawdata-2025-06-25" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP173990" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB90996" alias="erga-bge-iyHalNico6_primary-2025-06-25" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP173991" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA33518804" alias="SUBMISSION-25-06-2025-10:22:27:224"/>
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
* I created [iyHalNico-HiC.tsv](./data/iyHalNico-HiC.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iyHalNico-HiC.tsv -p ERGA-BGE -o iyHalNico-HiC
    ```
* Update iyHalNico-HiC.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90995"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name and title, since the other data types have the platform named
* Study will be private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@iyHalNico-HiC.exp.xml" -F "RUN=@iyHalNico-HiC.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-08-24T11:50:39.469+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX14868749" alias="exp_iyHalNico_Hi-C_LV6000911877_HC045-1A1A" status="PRIVATE"/>
        <RUN accession="ERR15464854" alias="run_iyHalNico_Hi-C_LV6000911877_HC045-1A1A_fastq_1" status="PRIVATE"/>
        <SUBMISSION accession="ERA34531124" alias="SUBMISSION-24-08-2025-11:50:39:317"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

* Data producer told me that there had been a mix up regarding samples, and that 
`LV6000911869` was correct, not `LV6000911877`. 
    * I changed the sample descriptor and primary id, of the experiment .xml file via the browser, from SAMEA116299217 / ERS21344134 to SAMEA116299218 / ERS21344135 (i.e. I used the ERS identifier).

### Submit RNAseq - **TODO**
#### Preparations
* Sample ID gave BioSample ID via ERGA tracker portal
* The data files were transferred together with other species received in this batch, using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz` and added ToLID to the files using rename function in FileZilla, to make it easier to see that right files will be submitted per species.

#### XML
* I created [iyHalNico-RNAseq.tsv](./data/iyHalNico-RNAseq.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f iyHalNico-RNAseq.tsv -p ERGA-BGE -o iyHalNico-RNAseq
    ```
* Update -RNAseq.exp.xml to reference accession number of previously registered study:
    ```
    <STUDY_REF accession="PRJEB90995"/>
    ```
* Remove row `<PAIRED/>` (error in script)
* I added 'Illumina' to the library name, since the other data types have the platform named
* Study is private, so submission.xml with hold date is used.
* Submit using curl:
    ```
        curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@iyHalNico-RNAseq.exp.xml" -F "RUN=@iyHalNico-RNAseq.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```

    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/), update status in BGE [tracking sheet](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/)

### Submit assembly

* I created a manifest file [iyHalNico6-manifest.txt](./data/iyHalNico6-manifest.txt)
* I created a folder on Uppmax (/proj/snic2022-6-208/nobackup/submission/H-nicosiae/) and copied & gzipped manifest, assembly file and chromosome list there
* Then all files where submitted (first validation then submission) from Pelle on Uppmax using Webin-CLI:

    ```
    interactive -t 08:00:00 -A uppmax2025-2-58
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./iyHalNico6-manifest.txt -validate
    ```
* Receipt:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/H-nicosiae/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/H-nicosiae/iyHalNico6_pri.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/H-nicosiae/chromosome_list.txt.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/H-nicosiae/unlocalised_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28514738
    ```
* I added the accession number to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) and set `Assembly submitted` to `Yes`, as well as set assembly as status `Submitted` in [Tracking_tool_Seq_centers](https://docs.google.com/spreadsheets/d/1IXEyg-XZfwKOtXBHAyJhJIqkmwHhaMn5uXd8GyXHSpY/edit?pli=1&gid=0#gid=0)
* Accessioned:
    ```
    ASSEMBLY_NAME | ASSEMBLY_ACC  | STUDY_ID   | SAMPLE_ID   | CONTIG_ACC                      | SCAFFOLD_ACC | CHROMOSOME_ACC
    iyHalNico6.1  | GCA_976986675 | PRJEB90996 | ERS21344133 | CDRKBY010000001-CDRKBY010000045 |              | OZ336067-OZ336074
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
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2025-10-03T10:49:22.069+01:00" submissionFile="update.xml" success="true">
        <PROJECT accession="PRJEB96354" alias="erga-bge-iyHalNico-study-umbrella-2025-08-25" status="PUBLIC"/>
        <SUBMISSION accession="" alias="SUBMISSION-03-10-2025-10:49:21:949"/>
        <MESSAGES/>
        <ACTIONS>MODIFY</ACTIONS>
    </RECEIPT>
    ```

### Submit 2 endosymbionts
* Submit Spiroplasma and Wolbachia endosymbionts, see [Stylops ater README](../ERGA-Stylops-ater/README.md/#submission-symbionts) how it was done there.

#### Suggested steps

1. Register new taxonomies
1. Register project/study - 1 or perhaps 2 since different species?
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
    * I did a free text search at ENA and *Halictus nicosiae* has no taxon registered for endosymbionts, hence proposed names `Wolbachia endosymbiont of Halictus nicosiae` and `Spiroplasma endosymbiont of Halictus nicosiae` should work
    * For Stylops we referred to the raw reads study as `project_id` but should it be the study created for the symbionts' assemblies or the umbrella that will refer to both? Decision was made to use the umbrella.
    * The description field is not obvious how to fill either, I asked colleagues for help and received a reference to use for Spiroplasma
* In the [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/taxonomy_requests.html#creating-taxon-requests) they state *"If you have multiple names to request, please do this as a single request"*. Hence, I logged in to ENA and went to [Register taxonomy](https://www.ebi.ac.uk/ena/submit/webin/taxonomy) in the Samples menu and downloaded a [taxonomy template](./data/taxonomy_template_1759492490477.tsv). After filling it in, it was uploaded to ENA (2025-10-09). It is expected to take quite a while before it is granted.
* Recieved taxon ids:
    * Wolbachia endosymbiont of Halictus nicosiae: `3473539`
    * Spiroplasma endosymbiont of Halictus nicosiae: `3473538`

#### Register study
* While not necessary, since there are 2 samples, I decided to create 2 separate studies
* I registered the them via browser, using 2026-02-02 as release dates
    ```
    title:          Wolbachia endosymbiont of Halictus nicosiae genome assembly
    study_name:     Wolbachia-iyHalNico6
    study_abstract: This project provides the genome assembly of Wolbachia endosymbiont of Halictus nicosiae.
    ```
    ```
    title:          Spiroplasma endosymbiont of Halictus nicosiae genome assembly
    study_name:     Spiroplasma-iyHalNico6
    study_abstract: This project provides the genome assembly of Spiroplasma endosymbiont of Halictus nicosiae.
    ```
* Accession numbers: `PRJEB106248` for Wolbachia and `PRJEB106249` for Spiroplasma
* I added the accession numbers to SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/)

#### Register samples
* I had to wait until the taxonomy request was approved
* I then submitted 2 samples, by uploading the sheet [symbiont-samples.tsv](./data/symbiont-samples.tsv)
* Accession numbers received: `ERS28446548` (alias w-HalNico) for Wolbachia and `ERS28446549` (alias s-HalNico) for Spiroplasma

#### Submit assemblies
* I created 2 manifest files [wolbachia-manifest.txt](./data/wolbachia-manifest.txt) and [spiroplasma-manifest.txt](./data/spiroplasma-manifest.txt)
* I copied them to separate subfolders on Uppmax (/proj/snic2022-6-208/nobackup/submission/H-nicosiae/) together with the chromosome lists and fasta assembly files
* Then all files where submitted (first validation then submission) from Pelle on Uppmax using Webin-CLI:

    ```
    interactive -t 08:00:00 -A uppmax2025-2-58
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./wolbachia-manifest.txt -validate
    java -jar ~/webin-cli-9.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./spiroplasma-manifest.txt -validate    
    ```
* Receipts:
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/H-nicosiae/Wolbachia/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/H-nicosiae/Wolbachia/ptg000024c_wolbachia.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/H-nicosiae/Wolbachia/chromosome_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28782859
    ```
    ```
    INFO : Connecting to FTP server : webin2.ebi.ac.uk
    INFO : Creating report file: /crex/proj/snic2021-6-194/nobackup/submission/H-nicosiae/Spiroplasma/././webin-cli.report
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/H-nicosiae/Spiroplasma/ptg000017c_spiroplasma.fa.gz
    INFO : Uploading file: /crex/proj/snic2021-6-194/nobackup/submission/H-nicosiae/Spiroplasma/chromosome_list.txt.gz
    INFO : Files have been uploaded to webin2.ebi.ac.uk.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ28782860
    ```
* I added the accession number to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/) 
* Accessioned:
    ```

    ```
#### Add to umbrella
* I reused [update.xml](./data/update.xml) and created [umbrella_symbionts.xml](./data/umbrella_modified.xml)
* Submit:
    ```
    curl -u Username:Password -F "SUBMISSION=@update.xml" -F "PROJECT=@umbrella_symbionts.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2026-01-07T11:19:56.603Z" submissionFile="update.xml" success="true">
        <PROJECT accession="PRJEB96354" alias="erga-bge-iyHalNico-study-umbrella-2025-08-25" status="PUBLIC"/>
        <SUBMISSION accession="" alias="SUBMISSION-07-01-2026-11:19:56:424"/>
        <MESSAGES>
            <INFO>The XML md5 checksum for the object being updated has not changed. No update required for PRJEB96354.</INFO>
        </MESSAGES>
        <ACTIONS>MODIFY</ACTIONS>
    </RECEIPT>
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
    ../../../../ERGA-submission/get_submission_xmls/get_umbrella_xml_ENA.py -s "Halictus nicosiae" -t iyHalNico6 -p ERGA-BGE -c SCILIFELAB -a PRJEB90995 -x 3229267
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
    <RECEIPT receiptDate="2025-08-25T13:06:21.833+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB96354" alias="erga-bge-iyHalNico-study-umbrella-2025-08-25" status="PRIVATE" holdUntilDate="2027-08-25+01:00"/>
        <SUBMISSION accession="ERA34667764" alias="SUBMISSION-25-08-2025-13:06:21:679"/>
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
    <RECEIPT receiptDate="2025-08-25T13:09:02.543+01:00" submissionFile="submission-release-project.xml" success="true">
        <MESSAGES>
            <INFO>project accession "PRJEB96354" is set to public status.</INFO>
        </MESSAGES>
        <ACTIONS>RELEASE</ACTIONS>
    </RECEIPT>    
    ```
