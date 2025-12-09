---
Redmine_issue: https://projects.nbis.se/issues/<id>
Repository: ENA
Submission_type: WGS, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB89226
---

# 8061 - Data publication of Songbird RNA-Seq data

## Submission task description
Support issue on brokering sequence data and assembly to ENA on behalf of research group. Large dataset (~450 files, ~3Tb data). Occasionally multiple runs from same experiment that needs to be solved in submisson.

## Procedure overview and links to examples

* Consult with research group and decide on scope and timeline
* Consultation on suitable ENA checklist. Decided on ToL (ERC000053)
* Research group provided metadata in template
* DS registered Study at ENA using information from metadata template (PRJEB89226)
* Research group provided list of files with md5 sums and added DS to SNIC project
* File list was uploaded to Dardel
* DS transferred sequence files from Dardel to ENA using Aspera (see Lessons learned)
* Due to number of files and total amount of data, submission was decided to be done programatically to ENA
* A submission.xml was made with release date set to 2027-11-09
* An xml file was made for the experiments ([Songbird_experiments.xml](./data/Songbird_experiments.xml))
* Another xml file was made for the run files ([Songbird_runs_files.xml](./data/Songbird_runs_files.xml))
* Submission of files was done using the curl command:

```
curl -u [Username]:[password] -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@Songbird_experiments.xml" -F "RUN=@Songbird_runs_files.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
```
Several things were problematic. See Lessons learned below.

Successful submission was confirmed in the [xml receipt](./data/receipt.xml). 

## Submission of assembly and HiFi data

* Paths to assembly fasta file and PacBio Revio bam-file was provided by researchers.
* Bam file was uploaded from Dardel to ENA staging using Aspera
* A submission.xml file was made identical to the previously used
* An XML file was made for the experiment ([Songbird_experiments_HiFi.xml](./data/Songbird_experiments_HiFi.xml))
* The bam file was referenced in a [Songbird_runs_files_HiFi.xml](./data/Songbird_runs_files_HiFi.xml)
* Submission was done using the curl command:

```
curl -u [user]:[password] -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@Songbird_experiments_HiFi.xml" -F "RUN=@Songbird_runs_files_HiFi.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
```
* Successful ingestion was confirmed by the receipt containing `success="true"`.

* The assembly file (not annotated) was uploaded using Webin-CLI v9.0.1 and a manifest file with the proper metadata, referencing the bam file:

```
java -jar -Xmx10G webin-cli-9.0.1.jar -ascp -context=genome -manifest=songbird_manifest.txt -userName=Webin-XXXXX -password=[password] -validate
```

* After successful validation the assembly was submitted by changing the flag to -submit.

## Lessons learned
### Transfer of data from Dardel to ENA
Data transfer was done using the Aspera protocol. Due to the large amounts of data, the transfer had to be made in several steps. All transfer was made from the Dardel transfer node.

* Login to Dardel transfer node
  
    ```
    ssh -i ~/.ssh/id-ed25519-pdc [username]@dardel-ftn01.pdc.kth.se
    ```
* Load the Aspera module
    ```
    ml aspera-cli/3.9.6.1467.159c5b1
    ```
* Initiate file transfer
    ```
    ascp -D -v -QT -l300M -k2 --mode=send --file-list=file_list.txt --host=webin2.ebi.ac.uk --user=Webin-XXXXX /.
    ```
    In the above example the resume flag `-k2` was used to save time on md5 checks (~2 min per file). Total time for transfer was ~1 week due to fluctuating upload times, probably due to ENA bottlenecks.

* After ingestion, four files were flagged by ENA for having deviant md5sums. Sums were checked on Dardel, and files were then re-uploaded to ENA, and then checked again using Aspera with `-k3` flag.

File ingestion is automatically attempted once per day per file not passing auto-validation.

### Submitting multiple runs per experiment to ENA
The ENA guidelines states that only a single kind of data can be submitted per experiment. Each experiment can support several sets of files, though. The solution was:

* Programmatic submission with all experiments referenced in a [Songbird_experiments.xml](./data/Songbird_experiments.xml), and all files (runs) specified in a [Songbird_runs_files.xml](./data/Songbird_runs_files.xml).
* Songbird_experiments.xml was populated with information from the metadata spreadsheet.
* Songbird_runs_files.xml was set up such that each set of paired reads of an experiment was referenced by a unique RUN alias, the same EXPERIMENT_REF, in separate DATA_BLOCKs.
* A [submission.xml](./data/submission.xml) with the ADD and RELEASE functions was made.
* Ingest of data was done by submitting the XML files by curl to ENA:
    ```
    curl -u Webin-XXXXX:[password] -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@Songbird_experiments.xml" -F "RUN=@Songbird_runs_files.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Successful ingestion was confirmed by the receipt containing `success="true"`
  
#### Encountered caveats
It is not stated clearly in the ENA submission guides how to reference multiple runs using the same experiment. Unsuccessful attempts were made including:

* Listing all files under a single DATA_BLOCK
* Clustering paired reads under the same DATA_BLOCK
* Cluster paired reads into separate DATA_BLOCKs but with the same RUN alias

The error messages when doing the above does not indicate what the actual error is, i.e. that paired reads need to be clustered in separate DATA_BLOCKs under different RUN aliases. 

