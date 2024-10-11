---
Redmine_issue: https://projects.nbis.se/issues/7700
Repository: ENA
Submission_type: exome # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB80839
---

# 7700 Carum carvi

## Submission task description
Assistance with submitting raw sequence reads from 207 individuals of *Carum carvi* sampled from various locations in Europe, in .bam format to ENA.

Researcher filled in the checklist as .xlsx file and sent by email. The ENA account credentials were sent using www.privnote.com and stored locally on laptop. 

## Procedure overview and links to examples

* Metadata was collected from PI using the ENA default [template](./data/7700-carum-metadata_template_default_ERC000011.xlsx)
* Data was transfered from directory on Rackham to ENA using Aspera. File transfer status was checked using FileZilla 
* Register study at ENA
* Submit samples to ENA
* Submit experiments to ENA

### Data transfer

All files are in .bam format. Instead of using Webin-CLI, which allows transfer of only a single .bam file at a time, all files were uploaded from Rackham to ENA using the commands:

```
interactive -t 08:00:00 -A naiss[XXXX-XX-XX]
module load ascp
export ASPERA_SCP_PASS='PASSWORD'
ascp -k 3 -d -q --mode=send -QT -l300M --host=webin2.ebi.ac.uk --user=Webin-XXXXX /proj/cwr_stor-bhr_2022/carum_paper/*.bam / &
```

File transfer required approximately three minutes in total.

### Submit samples

Samples were extracted from the spreadsheet in .tsv format and submitted via the ENA portal. The PI had included more samples than used in experiments, which was only discovered after samples submission was complete. It was decided the extra samples would be of no problem for the study since they were not referenced.

### Submit experiments

Experiments were saved in .tsv format with sample aliases transfered from the samples tab. Md5 checksums were calculated for the set of files on Rackham and entered in the spreadsheet. The .tsv was uploaded in the ENA online portal, and files were ingested overnight. 

## Lessons learned
Upon submitting the samples, all letters related to nordic alphabets rendered as question marks in the ENA portal. It could probably have been avoided by making sure the .tsv was formatted as UTF-8 prior to submission. 

Post submission bulk edits of sample records at ENA can only be made programmatically using xml-files.

This required two steps:

* The [samples](./data/Carum_samples.tsv) had to be transformed from .tsv into xml format, and encoded in UTF-8.

* Make an associated [submission update-file in xml](./data/submission.xml).

For the first step a DS colleague [assisted in adapting an already available script](https://github.com/NBISweden/nbisdm-ena-xml-generator) that was used to generate correctly updated samples in xml-format.

The two files, [samples.xml](./data/samples.xml) and [submission]((./data/submission.xml).xml, was then uploaded programmatically in the samples section in the ENA online portal and confirmed. 

