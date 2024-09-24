---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB77280, PRJEB77106, PRJEB77107 
---

# BGE - *Austropotamobius torrentium* (stone crayfish)
## Submission task description
Submission of raw reads for *Austropotamobius torrentium* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Austropotamobius-torrentium-metadata.xlsx)
* [BGE metadata](./data/qmAusTorr-BGE.tsv)

## Lessons learned
* Trying programmatic submission, using CNAG script to produce xml files for studies and experiments
* The script had to be updated in several places in order to produce the wanted and expected output xml's
* There's been some struggle regarding HiFi sequencing on this species, has been done in several rounds, resulting in 3 separate deliveries from NGI. There was some uncertanties on which datasets to submit.
* The Hi-C data came with a necessary update of the script (by CNAG) and update of mandatory fields in the tsv file, in order to accomodate that sometimes the runs for a datatype needs to be submitted to separate experiments, e.g. due to varying insert sizes.

## Detailed step by step description

### Collect metadata
* Looking at BioSamples, 20 samples in total are candidates, 10 are same as one of the other 10.
* Looking at the HiFi deliveries, in the README files (there are 3 of them), all refer to 2(!) samples, ERGA_DS_328X_04_(01+02) as UGC_user_id (UGC_id is pr_047_001). Which sample do we submit the datasets to? Need to ask NGI/UGC
    * Answer from NGI is to use [SAMEA112878228](https://www.ebi.ac.uk/biosamples/samples/SAMEA112878228)
* Looking at the HiC delivery, they only have 8 'internal' samples, no indication on which BioSample might have been used. Need to ask NGI/SNP&SEQ.
* There are still some missing metadata for the HiC, but HiFi is complete.

### Upload sequences to ENA

* Use 2 subdirectories at ENA upload area, `bge-crayfish-HiFi` and `bge-crayfish-HiC` (create them previous to upload using FileZilla)
* Create a shell script, go-ascp-crayfish.sh with aspera commands, use the version that logs transfers which can continue partial (failed) transfers:
    ```
    ascp -k 3 -d -q --mode=send -QT -l300M --host=webin.ebi.ac.uk --user=Webin-XXXX /path/to/*.bam /bge-crayfish-HiFi/ &
    ascp -k 3 -d -q --mode=send -QT -l300M --host=webin.ebi.ac.uk --user=Webin-XXXX /path/to/*.fastq /bge-crayfish-HiC/ &
    ```
* At Uppmax:
    ```
    tr -d '\r' < go-ascp-crayfish.sh.txt > go-ascp-crayfish.sh
    chmod 777 go-ascp-crayfish.sh
    interactive -t 08:00:00 -A naiss2023-5-307
    module load ascp
    export ASPERA_SCP_PASS='password'
    ./go-ascp-crayfish.sh &
    ```
* In the end I decided to remove the & ending each line, in order to run sequentially, and also divided HiC into one script and HiFi into another, and just run those in background (i.e. using &). 
* Keep track of upload success using FileZilla.

### Create xml

#### Submission xml
* [submission.xml](./data/submission.xml) needs to be created manually, which includes the action (ADD) and release date (HOLD)

    * **Note:** The projects should be released to public as soon as there is at least one dataset registered within it, in order to be able to show progress for milestones within the BGE project. Hence, while not ideal, we will use an embargo of the raw data project only until the HiFi is uploaded. Thus, the HiFi and RNA-seq datasets will become public directly, since we will receive this data at a later stage (well, we do have HiC for this species, but not the metadata, and a deadline of July 15 is approaching fast).The assembly project however, will still be under embargo until an assembly has been registered.

#### HiFi xml
* I started doing some [Tests](#tests) of the CNAG script using this species. Since I didn't have all the metadata, I did some (programmatic) submissions of other species before returning to this one. Hence, the original CNAG script has been edited several times. What remained, when returning back to this species, was the following:

    * Project attributes (Keyword:ERGA-BGE) are not registered if written in the xml as original script. I had to edit the script so that it is written on 2 rows insead of compact form
    * Library construction protocol has to be put in the lib_attr column of the tsv file, in the form `LIBRARY_CONSTRUCTION_PROTOCOL:Preparing HiFi SMRTbell® Libraries using the SMRTbell Express Template Prep Kit 3.0`

* I've put  my updates to CNAG scripts in a forked repository [YvonneKallberg/ERGA-submission](https://github.com/YvonneKallberg/ERGA-submission), along with the notes I've made and the original xml file(s) (though the original will not be updated when upstream/main changes). This version works for the [qmAusTorr-HiFi-BGE.tsv](./data/qmAusTorr-HiFi-BGE.tsv) file, but might not work for the Hi-C data (for which I haven't received the full metadata yet).
    ```
    ../../.././ERGA-submission/get_submission_xmls/get_ENA_xml_files.py/get_ENA_xml_files.py  -f qmAusTorr-HiFi-BGE.tsv -p ERGA-BGE -o qmAusTorr-HiFi
    ```
#### Hi-C xml

* Figure out what needs to be done in order to create HiC and RNA-seq xml's so that it they correctly are added to the existing study. 
* Figure out a way to avoid adding insert size for paired reads manually
    ```
    <LIBRARY_LAYOUT>
        <PAIRED NOMINAL_LENGTH="insert_size_value"/>
    </LIBRARY_LAYOUT>
    ```
     * CNAG says it *should* be possible to put it in “Library_attributes” column, but how will the script know where to add it (i.e. to the PAIRED row in library layout section), compared to the library construction protocol, which is also put in the lib_attr column but added after the library layout section?
* Initial attempt, where I've added both insert size and library construction protocol (separated by semicolon) in the lib_attr column of [qmAusTorr-HiC-BGE.tsv](./data/qmAusTorr-HiC-BGE.tsv):
    ```
    conda deactivate
     ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py  -f qmAusTorr-HiC-BGE.tsv -p ERGA-BGE -o qmAusTorr-HiC
    ```

    * The resulting qmAusTorr-HiC.exp.xml refers to the **wrong study** (the script creates a study.xml, can this be avoided? check arguments of the script). Hence, need to manually change the STUDY_REF to `accession="PRJEB77106"` instead of `refname="erga-bge-qmAusTorr-study-rawdata-2024-09-02"`
    * There are 8 paired reads, but **only 1 experiment** (meaning there will be only one insert_size although they differe btw the pairs). Is it supposed to be 8 experiments or only 1?
    * The **insert sizes** are added in **wrong place**

* I asked CNAG for help:  
    * For now, the study needs to be manually updated in order to refer to an existing one.  
    * Regarding the 8 paired reads, the get_ENA_xml_files.py has now been updated, so that it requries a field `library_name`. I have no instructions on how to populate that field, so I created my own convention:  
        * Copy the value from `sample_tube_or_well_id` 
        * *If* it is required with separate experiments for the runs, add a dash (`-`) and an incremental index
        * E.g in this case `XD-3967-1`, `XD-3967-2`, etc
    * Insert sizes we have to add in right place manually, at least until I can figure out how to fix the script myself.
* A rerun with updated script was made, but the library names didn't look good, e.g. `XD-3967 Hi-C XD-3967-1` where I would have liked it to be `XD-3967-1 Hi-C`. Question is if I should accept the script and instead change my naming convention, or if I should change the script?  
    * I decided to change the script, wherever 'flowcell' was mentioned, i replaced it with 'library_id' (and removed the trailing library_id that was introduced with the update)
    * Seems to work for this case, but I need to be aware that it might look odd for RNA-seq or HiFi in future runs of the script
* With some help of a colleague, I managed to fix so that insert_size is put in the right place. However, the solution requires an additional column in the tsv file. I've updated the template accordingly.
* Manual update of study reference is still required for all experiments.
* A final rerun of the [script](./scripts/) produced:
    * [qmAusTorr-HiC.study.xml](./data/qmAusTorr-HiC.study.xml) (not to be used)
    * [qmAusTorr-HiC.exp.xml](./data/qmAusTorr-HiC.exp.xml)
    * [qmAusTorr-HiC.runs.xml](./data/qmAusTorr-HiC.runs.xml)
* `qmAusTorr-HiC.exp.xml` was manually updated, replacing 8 occurences of `<STUDY_REF refname="erga-bge-qmAusTorr-study-rawdata-2024-09-24"/>` with `<STUDY_REF accession="PRJEB77106"/>`

#### RNA-seq xml

### Programmatic submission HiFi

* Copy all xml files to Uppmax:
    ```
    scp submission.xml qmAusTorr-HiFi.*.xml yvonnek@rackham.uppmax.uu.se:/home/yvonnek/BGE-crayfish/
    ```
* Submit:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml"  -F "PROJECT=@qmAusTorr-HiFi.study.xml" -F "EXPERIMENT=@qmAusTorr-HiFi.exp.xml" -F "RUN=@qmAusTorr-HiFi.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-07-03T06:04:43.956+01:00" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX12711150" alias="exp_qmAusTorr_HiFi_WGS_pr_047_001" status="PRIVATE"/>
        <RUN accession="ERR13340176" alias="run_qmAusTorr_HiFi_WGS_pr_047_001_bam_1" status="PRIVATE"/>
        <RUN accession="ERR13340177" alias="run_qmAusTorr_HiFi_WGS_pr_047_001_bam_2" status="PRIVATE"/>
        <RUN accession="ERR13340178" alias="run_qmAusTorr_HiFi_WGS_pr_047_001_bam_3" status="PRIVATE"/>
        <RUN accession="ERR13340179" alias="run_qmAusTorr_HiFi_WGS_pr_047_001_bam_4" status="PRIVATE"/>
        <RUN accession="ERR13340180" alias="run_qmAusTorr_HiFi_WGS_pr_047_001_bam_5" status="PRIVATE"/>
        <RUN accession="ERR13340181" alias="run_qmAusTorr_HiFi_WGS_pr_047_001_bam_6" status="PRIVATE"/>
        <RUN accession="ERR13340182" alias="run_qmAusTorr_HiFi_WGS_pr_047_001_bam_7" status="PRIVATE"/>
        <PROJECT accession="PRJEB77106" alias="erga-bge-qmAusTorr-study-rawdata-2024-07-02" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP161588" type="study"/>
        </PROJECT>
        <PROJECT accession="PRJEB77107" alias="erga-bge-qmAusTorr9_primary-2024-07-02" status="PRIVATE" holdUntilDate="2026-03-07Z">
            <EXT_ID accession="ERP161589" type="study"/>
        </PROJECT>
        <SUBMISSION accession="ERA30663094" alias="SUBMISSION-03-07-2024-06:04:43:289"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
* When the Hifi runs were to become public, there were errors on 2 of them regarding the checksums. Apparently I had switched them when copy-pasting.
 
### Programmatic submission HiC

### Programmatic submission RNAseq

## Tests

### Test create xml
* A [submission.xml](./data/submission.xml) needs to be created manually, which includes the action (ADD) and release date (HOLD).

While not complete information yet, I wanted to try using the script on this species:
```
../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f qmAusTorr-BGE.tsv -p ERGA-BGE -o qmAusTorr
```
* Only run.xml for HiC data, why? 
    * Answer: I didn't have 'native_file_name' column name, only 'file_name'
* For Hi-C, there's an additional read type line, apart from PAIRED: `<READ_TYPE>sample_barcode</READ_TYPE>`, should it be there?
* There is not place to put insert_size in tsv, is it? But for paired reads it is mandatory, isn't it? When I did a trial submission (see below), I got no error so if it is not possible to get the insert size from NGI, at least programmatic submission is a way to escape.
* We received insert size for th HiC data, **this must be added manually** to the experiment xml:
    ```
    <LIBRARY_LAYOUT>
        <PAIRED NOMINAL_LENGTH=""/>
    </LIBRARY_LAYOUT>
    ```
### Test programmatic submission
* Copy all xml files to Uppmax:
    ```
    scp submission.xml qmAusTorr.*.xml yvonnek@rackham.uppmax.uu.se:/home/yvonnek/BGE-crayfish/
    ```
* I think I will do a test drive, since I've never submitted programmatically, is it possible to submit both projects and experiment in one go, i.e:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml"  -F "PROJECT=@qmAusTorr.study.xml" -F "EXPERIMENT=@qmAusTorr.exp.xml" -F "RUN=@qmAusTorr.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```

* If not possible to submit both levels of data, I will need to create another submission.xml file, without the release date, for experiment submission.
* There's also a possibility to submit xmls via Webin Portal

```
<ERROR>Failed to validate run xml, error: string value 'BAM' is not a valid enumeration value for type of filetype attribute in type of FILE element in type of FILES element in type of DATA_BLOCK element in RunType</ERROR>
```
* I updated the code to output 'bam' instead, then it worked:
```
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
<RECEIPT receiptDate="2024-05-30T07:08:53.000+01:00" submissionFile="submission.xml" success="true">
     <EXPERIMENT accession="ERX12547823" alias="exp_qmAusTorr9_Hifi_WGS_pr_047_001" status="PRIVATE"/>
     <EXPERIMENT accession="ERX12547824" alias="exp_qmAusTorr9_Hi-C_XD-3967" status="PRIVATE"/>
     <RUN accession="ERR13176447" alias="run_qmAusTorr9_Hifi_WGS_pr_047_001_bam_1" status="PRIVATE"/>
     <RUN accession="ERR13176448" alias="run_qmAusTorr9_Hifi_WGS_pr_047_001_bam_2" status="PRIVATE"/>
     <RUN accession="ERR13176449" alias="run_qmAusTorr9_Hifi_WGS_pr_047_001_bam_3" status="PRIVATE"/>
     <RUN accession="ERR13176450" alias="run_qmAusTorr9_Hifi_WGS_pr_047_001_bam_4" status="PRIVATE"/>
     <RUN accession="ERR13176451" alias="run_qmAusTorr9_Hifi_WGS_pr_047_001_bam_5" status="PRIVATE"/>
     <RUN accession="ERR13176452" alias="run_qmAusTorr9_Hifi_WGS_pr_047_001_bam_6" status="PRIVATE"/>
     <RUN accession="ERR13176453" alias="run_qmAusTorr9_Hifi_WGS_pr_047_001_bam_7" status="PRIVATE"/>
     <RUN accession="ERR13176454" alias="run_qmAusTorr9_Hi-C_XD-3967_fastq_1" status="PRIVATE"/>
     <RUN accession="ERR13176455" alias="run_qmAusTorr9_Hi-C_XD-3967_fastq_2" status="PRIVATE"/>
     <RUN accession="ERR13176456" alias="run_qmAusTorr9_Hi-C_XD-3967_fastq_3" status="PRIVATE"/>
     <RUN accession="ERR13176457" alias="run_qmAusTorr9_Hi-C_XD-3967_fastq_4" status="PRIVATE"/>
     <RUN accession="ERR13176458" alias="run_qmAusTorr9_Hi-C_XD-3967_fastq_5" status="PRIVATE"/>
     <RUN accession="ERR13176459" alias="run_qmAusTorr9_Hi-C_XD-3967_fastq_6" status="PRIVATE"/>
     <RUN accession="ERR13176460" alias="run_qmAusTorr9_Hi-C_XD-3967_fastq_7" status="PRIVATE"/>
     <RUN accession="ERR13176461" alias="run_qmAusTorr9_Hi-C_XD-3967_fastq_8" status="PRIVATE"/>
     <PROJECT accession="PRJEB76181" alias="erga-bge-qmAusTorr-study-rawdata-2024-05-30" status="PRIVATE" holdUntilDate="2026-03-07Z">
          <EXT_ID accession="ERP160734" type="study"/>
     </PROJECT>
     <PROJECT accession="PRJEB76182" alias="erga-bge-qmAusTorr9_primary-2024-05-30" status="PRIVATE" holdUntilDate="2026-03-07Z">
          <EXT_ID accession="ERP160735" type="study"/>
     </PROJECT>
     <SUBMISSION accession="ERA30540703" alias="SUBMISSION-30-05-2024-07:08:51:258"/>
     <MESSAGES>
          <INFO>All objects in this submission are set to private status (HOLD).</INFO>
          <INFO>This submission is a TEST submission and will be discarded within 24 hours</INFO>
     </MESSAGES>
     <ACTIONS>ADD</ACTIONS>
     <ACTIONS>HOLD</ACTIONS>
```
* Since it *is* possible to submit all at once, I will wait until I have all HiC metadata before I submit for real.

* The xml script is not fully functioning, insert size for paired reads is missing, and read_type 'sample_barcode' should likely be added to HiFi data, hence these needs to be added manually in the output run xmls for now.

### Register umbrella projekt

For each of the BGE species, an umbrella project has to be created and linked to the main BGE project, [PRJEB61747](https://www.ebi.ac.uk/ena/browser/view/PRJEB61747).

* There is a CNAG script, that should do the deed of creating the xml file:
    ```
    ./script/get_umbrella_xml_ENA.py -s "Austropotamobius torrentium" -t qmAusTorr9 -p ERGA-BGE -c SCILIFELAB -a PRJEB77106 -x 94942
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
    <RECEIPT receiptDate="2024-07-05T12:58:43.699+01:00" submissionFile="submission-umbrella.xml" success="true">
        <PROJECT accession="PRJEB77280" alias="erga-bge-qmAusTorr-study-umbrella-2024-07-05" status="PRIVATE" holdUntilDate="2024-07-07+01:00"/>
        <SUBMISSION accession="ERA30670049" alias="SUBMISSION-05-07-2024-12:58:42:488"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    ```
* **Note:** Add the assembly project `PRJEB77107` when it has been submitted and made public, see [ENA docs](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella) on how to update.
