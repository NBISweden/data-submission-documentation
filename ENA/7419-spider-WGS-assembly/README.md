---
Redmine_issue: https://projects.nbis.se/issues/7419
Repository: ENA
Submission_type: WGS, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB74310, PRJEB74311, PRJEB74494, PRJEB74312
---

# 7419 - Spider WGS & assembly

## Submission task description
The Spider partner project has produced several datasets of which this documentation describes the submission to ENA of 4 datasets: 3 whole genome sequencing datasets (PacBio long reads, Chromium 10X short reads, and PacBio Iso-seq) and 1 annotated assembly. The WGS datasets were used to create the annotated assembly.

## Procedure overview and links to examples

Metadata templates
* [PacBio metadata template](./data/PacBio-metadata_template_default_ERC000011.xlsx)
* [Chromium 10x metadata template](./data/chromium10x-metadata_template_default_ERC000011.xlsx)
* [PacBio Iso-seq metadata template](./data/PacBio_Iso-seq-metadata_template_default_ERC000011.xlsx)
* [Assembly metadata template](./data/assembly-metadata_template_default_ERC000011.xlsx)

Internal links
* [PacBio dataset](#pacbio-dataset)
* [Chromium 10x dataset](#chromium-10x-dataset)
* [PacBio Iso-seq dataset](#pacbio-iso-seq-long-transcript-reads-dataset)
* [Assembly dataset](#assembly-dataset)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->
* Due to lack of time, the submission process started a bit too late, resulting in all hands on deck since there are several datasets to be published.
* Aspera isn't always the best/fastest way, sometimes it is better to submit reads using manifests and Webin_CLI.
* When transferring many files to ENA, add logging to the aspera command so that the upload can continue where kicked out instead of starting from the beginning.

## Detailed step by step description

Research group registered an ENA account, and added also data stewards.

### PacBio dataset
* All metadata was collected in [PacBio-metadata_template_default_ERC000011.xlsx](./data/PacBio-metadata_template_default_ERC000011.xlsx)
* I added whatever metadata I found from the manuscript, and asked NGI and research group to confirm and provide missing values
* Study was registered interactively via browser, received accession number: `PRJEB74310`
* One sample was registered interactively by uploading [pacbio-sample.tsv](./data/pacbio-sample.tsv), received accession number: `ERS18607825`

#### Experiment

* I decided to submit this dataset interactively, via the Webin Portal / browser. Hence, I needed to transfer 60 bam files to ENA upload area from Uppmax:
  * Create a script that do the transfer using aspera
    * Create a tsv file with the ascp command in first column, all the bam files on Uppmax in second, where they should land on ENA in the third column. Then copy the columns to Visual Studio ([go-ascp-pacbio.sh.txt](./scripts/go-ascp-pacbio.sh.txt)), add `#!/bin/sh` on first line and replace all tabs with space. E.g. `ascp -d -QT -l300M -L- /uppstore/path/m54032_190126_061335.subreads.bam Webin-XXXXX@webin.ebi.ac.uk:/PacBio-WGS/m54032_190126_061335.subreads.bam
    * Copy to Uppmax using `scp -p ./scripts/go-ascp-pacbio.sh.txt yvonnek@rackham.uppmax.uu.se:/home/yvonnek/Spider/`

  * Execute the transfer
    * Do I use our general NAISS project? I ended up doing that
    ```
    tr -d '\r' < go-ascp-pacbio.sh.txt > go-ascp-pacbio.sh
    chmod 777 go-ascp-pacbio.sh
    interactive -t 08:00:00 -A naiss2023-22-289
    module load ascp
    export ASPERA_SCP_PASS='password'
    ./go-ascp-pacbio.sh &
    ```
  * I had huge issues with data transfer, was stalled or got Exit error messages. I consulted with a DS colleague and updated the aspera command so that it logged the transfers and could continue partial (failed) transfers:
  ```
  ascp -k 3 -d -q --mode=send -QT -l300M --host=webin.ebi.ac.uk --user=Webin-XXXX /path/to/*.bam /PacBio-WGS/ &
  ```
  * I transferred sometimes one bam file at a time, and some using groups (i.e. the script above wasn't used at all), and kept an eye on transfer using FileZilla.

* It took some time to get the metadata from NGI, but eventually the experiment was submitted using [pacbio-experiment.tsv](./data/pacbio-experiment.tsv).
* Received accession numbers: [PacBio-run-experiment-accessions.txt](./data/PacBio-run-experiment-accessions.txt), also divided into comma separated files [PacBio-experiment-accessions.txt](./data/PacBio-experiment-accessions.txt) and [PacBio-run-accessions.txt](./data/PacBio-run-accessions.txt).

### Chromium 10x dataset

* All metadata was collected in [chromium10x-metadata_template_default_ERC000011.xlsx](./data/chromium10x-metadata_template_default_ERC000011.xlsx)
* I added whatever metadata I found from the manuscript, and asked NGI and research group to confirm and provide missing values
* Study was registered interactively via browser, received accession number: `PRJEB74311`
* One sample was registered interactively by uploading [chromium10x-sample.tsv](./data/chromium10x-sample.tsv), received accession number: `ERS18607826`
* **Note:** The NGI sample info indicates that the species is Araneus diadematus (user id is 'Araneus diadematus 1'). *Answer: Initially there was uncertanties as of which species it was, but later it was confirmed that indeed it is Larinioides sclopetarius*

#### Experiment

* I found 2 fastq files and one index file. I asked responsible bioinformatician which files to submit, and they confirmed that indeed it was the sequence pair I found, and that the index file found in the same folder should not be submitted.

* I decided to do an interactive submission for this dataset as well, and prepared [chromium10x-experiment.tsv](./data/chromium10x-experiment.tsv).

* Hence, I needed to transfer the 2 fastq  files to ENA upload area from Uppmax. However, when trying I was kicked out immediately. Thinking this might be due to the 60 bam files already uploaded, that I might have reached a limit, I deided to try after PacBio submission was completed.

  ```
  interactive -t 08:00:00 -A naiss2024-22-345
  module load ascp
  export ASPERA_SCP_PASS='password'
  cd /uppstore/path/
  ascp -k 3 -d -q --mode=send -QT -l300M --host=webin.ebi.ac.uk --user=Webin-XXXXX P11453_101_S1_L001_R1_001.fastq.gz /Chromium_10x-WGS/ &
  ascp -k 3 -d -q --mode=send -QT -l300M --host=webin.ebi.ac.uk --user=Webin-XXXXX P11453_101_S1_L001_R2_001.fastq.gz /Chromium_10x-WGS/ &
  ```
* I got kicked out even though upload area was empty, trying with Webin-CLI instead, by submitting [chromium10x-experiment-manifest.txt](./data/chromium10x-experiment-manifest.txt):
  ```
  mkdir Webin_output
  java -jar ../webin-cli-7.0.1.jar -ascp -context reads -userName Webin-XXXXX -password 'my_password' -manifest chromium10x-experiment-manifest.txt -outputDir Webin_output/ -validate
  java -jar ../webin-cli-7.0.1.jar -ascp -context reads -userName Webin-XXXXX -password 'my_password' -manifest chromium10x-experiment-manifest.txt -outputDir Webin_output/ -submit
  ```
* Received accession numbers: `ERX12204293`, `ERR12831479`

### PacBio Iso-Seq long transcript reads dataset

* All metadata was collected from the draft journal article and entered into [PacBio_Iso-seq-metadata_template_default_ERC000011.xlsx](./data/PacBio_Iso-seq-metadata_template_default_ERC000011.xlsx)
* Study was registered interactively via browser, received accession number: `PRJEB74494`
* Sample was registered by modification of an aldready registered sample by uploading [PacBio_Iso-seq_sample.tsv](.data/PacBio_Iso-seq_sample.tsv). Received accession number: `SAMEA115465569`

#### Experiment

Data consisted of a single bam-file, and due to the presumed size (>50Gb) it was decided to submit the file directly from storage (Uppmax) to ENA using Webin-CLI.

Java client for Webin-CLI v7.1.1 was uploaded to the Uppmax data folder along with the text manifest using standard `scp`.

The submission command line was initially run with a `-validate` flag before submission - `java -jar ../webin-cli-7.1.1.jar -ascp -context reads -userName Webin-XXXXX -password 'my_password' -manifest PacBio_Iso-seq_manifest.txt -validate`

This resulted in extremly long initial handshakes with the ENA server, and several attempts were made over several days without success. Eventually it was discovered the .bam-file was extremely large (~950 Gb), and communication with the researcher and Bioinformatician revealed the file to be a [consensus full reads version](https://ngisweden.scilifelab.se/bioinformatics/pacbio-isoseq-analysis/). After more communication a more polished and re-useable friendly file version (demultiplexed flnc) was settled on as more publication friendly, bringning the file size down to ~7 Gb.

The flnc file was validated and then submitted to ENA without further issues.

### Assembly dataset

* All metadata was collected in [assembly-metadata_template_default_ERC000011.xlsx](./data/assembly-metadata_template_default_ERC000011.xlsx)
* The assembly bioinformatician completed the metadata template.
* The PacBio sample (ERS18607825) will be main, since assembly was made from that dataset.
* A project was registered interactively, asking for locus tag `LARSCL`, received accession number: `PRJEB74312`

* I received a set of files:
  * LSc.v1.1.fa
  * Lsc.v1.1.gff

* I copied both of them to nac-login and created a runscript /home/yvonnek/Spider/[run_emblmygff3_spider.sh](./scripts/run_emblmygff3_spider.sh)
* I copied expose_translation json files from previous runs, into the folder
* I started the script using `sbatch run_emblmygff3_spider.sh`

* There were some errors, (AssertionError), that an assembly bioinformatician helped solve by removing offending lines (rather truncating some lines to remove unnecessary additions) in the gff file.

* New, cleaned files (copied to nac-login cluster):
  * LSc.v1.2.fa
  * Lsc.v1.2.gff

* [assembly-manifest.txt](./data/assembly-manifest.txt) was validated using Webin-CLI:
  ```
  java -jar ../../../Downloads/webin-cli-7.1.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./assembly-manifest.txt -validate     
  ```

* Validation errors:
  ```
  ERROR: Feature Qualifier "product" has invalid value 3,5-cyclic"" /product=" 1" /product=" nucleotide" /product=" phosphodiesterase" /product="Calcium/calmodulin-dependent" /standard_name="pde1c_2. [ line: 4376826]
  ERROR: Feature Qualifier "product" has invalid value 2-O-methyltransferase"" /product=" fibrillarin" /product="rRNA" /standard_name="fib. [ line: 14022661]
  ERROR: Feature Qualifier "product" has invalid value 5-AMP-activated"" /standard_name="prkaa2_iso2. [ line: 14023856]
  ERROR: Feature Qualifier "product" has invalid value 5-AMP-activated"" /standard_name="prkaa2_iso1. [ line: 14023913]
  ERROR: Feature Qualifier "product" has invalid value 5-AMP-activated"" /standard_name="prkab1_2. [ line: 15938751]
  ERROR: Feature Qualifier "product" has invalid value 5"" /standard_name="dclre1b. [ line: 21691346]
  ```
* I gunzipped the embl file and looked at the offending lines. The errors were due to extra `"`, once removed it worked.
* [assembly-manifest.txt](./data/assembly-manifest.txt) was re-validated and submitted using Webin-CLI:
  ```
  java -jar ../../../Downloads/webin-cli-7.1.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./assembly-manifest.txt -validate
  java -jar ../../../Downloads/webin-cli-7.1.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./assembly-manifest.txt -submit      
  ```

* Received accession number: `ERZ23875418`