---
Redmine_issue: https://projects.nbis.se/issues/6793
Repository: ENA
Submission_type: RNAseq # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: https://www.ebi.ac.uk/ena/browser/view/PRJEB63328
---

# 6793 - Data submission of RNAseq data from potato

## Submission task description
The task is to submit RNAseq data for 18 potato samples to ENA. Analysis was done in a previous project ([#4573](http://projects.nbis.se/issues/4573)), and now reviewers of the paper requires that raw data is deposited at a public repository. PI contacted us for help with the submission. Unfortunately the Uppmax project was closed, and PI couldn't find a local copy, so PI first had to contact Uppmax and see if they still had the data (thankfully they did).

## Procedure overview and links to examples
* Decide on checklist to be used
* Decide way of submission
* Prepare all files necessary
* Upload files from Uppmax to ENA, using Aspera on interactive node
* Submit via Webin Portal

## Lessons learned

* Uppmax managed to find a closed project's sequence-data even if older project
* Researcher chose checklist, and decided that the default checklist was the best option since a few of the mandatory fields were missing data.
* I needed input from Bioinformatician in order to find out if index files should be submitted as well, and learned: Index-files are not always useful, if sequence data is de-multiplexed already.
* DS should add themselves as contributors of the ENA account temporarily, in order to obtain study-specific emails from ENA. 
* Insert size (required field for paired reads) isn't always found in report from NGI but can sometimes be found from standard protocols from instrument provider.

## Detailed step by step description

### Accounts and access
* PI adds me to Uppmax project
* PI creates account at ENA and shares credentials with me
* I added myself as contributor and adviced PI to remove me, and change password, when the submission process is complete and the dataset is public. Being a contributor allows me to get study-specific emails from ENA.

### Checklist
* PI identifies appropriate ENA checklist
  * ENA default checklist (ERC000011) with addition of a selection of the recommended fields from plant checklist (ERC000037) will be used for submission
* A metadata template was created and put on google drive: [6793_metadata_template_default_ERC000011](./data/6793_metadata_template_default_ERC000011.xlsx), and PI was asked to fill in the missing information.

### Raw reads preparation
* I decided on doing submission via **Webin Portal** for both samples and raw reads
* This requires that md5 **checksums** are available and put into the tsv experiment template:
  * Checksums were calculated using script: 
    ```
    interactive -A naiss2023-22-289

    /scripts/go-calc-md5.sh > /data/checksums_md5_6793.txt
    ```
* The raw reads are stored at Uppmax, and there are **index files** (I) for each sequence file (both forward and reverse). I don't know how to handle this so I will ask NBIS bioinformaticians if they should be submitted as well, and how.
  * Is this to be submitted as [multi-fastq](https://ena-docs.readthedocs.io/en/latest/submit/reads/webin-cli.html#json-manifest-file-format)?
  * Or as a separate row in the .tsv?
  * [About index files](https://bioinformatics.stackexchange.com/questions/5178/what-is-the-index-fastq-file-sample-i-fastq-gz-generated-when-demultiplexing)
  * Or convert to bam? [10x Genomics info at ENA](https://ena-docs.readthedocs.io/en/latest/submit/fileprep/reads.html#x-genomics)
  * After conferring with a bioinformatician, it was concluded that the index files are of no use since:
    * The information within them had no value (all of them looked alike)
    * What was delivered from NGI was already de-multiplexed data (which is the format ENA wants) and the index files would only have been informative if we had the fastq files from before this step
    * The subsequent analysis (done by NBIS), where the reads were aligned to genome, only used the reads and not the index files
* The **insert siz**e field, required when submitting paired reads, wasn't found in the sequencing report from NGI. In another submission project I found the values explicit as insert_size, in the html report from facility, but the report for this project looks different. A [standard protocol from TruSeq](https://support.illumina.com/content/dam/illumina-support/documents/documentation/chemistry_documentation/samplepreps_truseq/truseq-stranded-mrna-workflow/truseq-stranded-mrna-workflow-reference-1000000040498-00.pdf) was used, and there it says that the average insert size is 150.

### Transfer fastq files
1. Fastq files are then uploaded to ENA, via an interactive node on Uppmax  
    1. I created a tsv file (with all fastq files) with the ascp command, where the fastq files resides on uppmax and where I want it to upload on ENA, e.g. `ascp -QT -l300M -L- /folder/path/uppmax/RF-1896/181012_A00181_0053_AH3J3KDRXX/BjCoR1-1_S9_L002_R1_001.fastq.gz Webin-XXXXX@webin.ebi.ac.uk:/BjCoR1-1_S9_L002_R1_001.fastq.gz
`
    1. Copied to Visual Studio (go-ascp-fastq.sh) where `#!/bin/sh` was added as first line, and all tabs where replaced with space.
    1. Transferred to Uppmax using WinSCP
    1. might not be needed, but was before, so remove all '\r' in the script (i.e. Windows line breaks):
    >tr -d '\r' < go-ascp-fastq.sh > go-ascp-fastq.sh.tmp  
    >mv go-ascp-fastq.sh.tmp go-ascp-fastq.sh
    1. Make script executable: `chmod 777 go-ascp-fastq.sh`
    1. Execute the script using interactive mode
    > interactive -A naiss2023-22-289  
    > module load ascp/4.2.0.183804
    1. Put password in memory (change password to the actual one) and execute the script:
    > export ASPERA_SCP_PASS='password'  
    >./go-ascp-fastq.sh &
    1. Kept an eye using FileZilla to see what had been uploaded to ENA.

### Submission
Although the [6793_metadata_template_default_ERC000011.xlsx](./data/6793_metadata_template_default_ERC000011.xlsx) was used to gather all levels of information (metadata), the samples and experiments were submitted by first downloading tsv templates and then copy the information (using Visual Studio) from the main, excel, template into the respective tsv files. This in order to not introduce submission failures due to different interpretations of what a tsv file is btw ENA and Excel. Not sure if required but has helped in previous submissions.

Files uploaded:
* Samples - [Checklist_ENA-default-sample-checklist_1687266943468.tsv](./data/Checklist_ENA-default-sample-checklist_1687266943468.tsv)
* Experiments - [fastq2_template_1687268941886.tsv](./data/fastq2_template_1687268941886.tsv)

