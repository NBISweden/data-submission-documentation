---
Redmine_issue: https://projects.nbis.se/issues/8347
Repository: ENA
Submission_type: WGS # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB107427
---

# 8347 - Comparative genomics at the re­birth of a sustainable fibre crop

## Submission task description
Support issue on brokering sequence data for the nettle project to be uploaded to the ENA, as an early submission, on behalf of the research group. Small dataset (46 files, ~300Gb data). 

## Procedure overview and links to examples

* Consult with research group and decide on scope and approximate/reasonable timeline for the entire process
* Decide together with research group on appropriate checklist (ENA000053 - ENA plant sample checklist)), and which optional metadata fields (columns) to include in the submission.
* Research group provided metadata for samples and runs in the template
* DS registered Study in the ENA portal using information from the [metadata template](./data/8347-Nettle.xlsx) (PRJEB107427)
* DS registered [sample information](./data/nettle_samples.tsv) via the ENA portal based on the metadata template
* Research group provided a list of all included files and added DS to SNIC project. 
* DS upploaded the [file list](./data/nettle_for_submission.txt) to Dardel using `scp`
```
scp nettle_for_submission.txt -i ~/.ssh/id-ed25519-pdc stenyl@dardel.pdc.kth.se:/cfs/klemming/home/s/stenyl/
```  
and then transfered files from Dardel to the ENA servers using Aspera with command `ascp`
```
ascp -D -v -k2 --mode=send --file-list=nettle_for_submission.txt --host=webin2.ebi.ac.uk --user=[Webin-XXXXX] /.
```
* File names and md5sums were added to the run tabs in the spreadsheet. 
* Submission of files was done via the ENA portal using the sequence type run files extracted from the checklist in .tsv format; ([DNA](./data/DNA_bam.tsv), [RNA](./data/RNA_fastq.tsv), [HiC](./data/HiC_fastq.tsv) and [miRNA](./data/miRNA_fastq.tsv))
* Successful submissions were confirmed via receipts for each sequence type; [DNA](./data/DNA_bam_receipt.xml), [RNA](./data/RNA_fastq_receipt.xml), [HiC](./data/HiC_fastq_receipt.xml), and [miRNA](./data/miRNA_fastq_receipt.xml)

## Lessons learned
Upload speeds from Dardel to ENA varied by a large 
factor within and betweeen days, in spite of using the Aspera protocol. Transfers were made from the Dardel login node.

For samples, the checklist ERC000037 (ENA plant sample checklist) was noted to refer to a depricated [link for ontology of plant growth medium](http://purl.obolibrary.org/obo/EO_0007147). After communication, we decided to replace it with [PECO (Plant Experimental Conditions Ontology)](https://www.ebi.ac.uk/ols4/ontologies/peco/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FPECO_0007049?lang=en) as a suitable replacement. 

For some reason, when uploading the sequence files to ENA, using the command line:

```
ascp -D -v -k2 --mode=send --file-list=nettle_for_submission.txt --host=webin2.ebi.ac.uk --user=[Webin-XXXXX] /.
```
Aspera ended the transfer with the message:

```
Completed: 89860628K bytes transferred in 4732 seconds
 (155556K bits/sec), in 46 files; 15 files skipped or empty.
```
Retrying the transfer did not resolve the issue. Transferring the files one by one did not resolve it either. Curiously, checking again the day after all files had actually been transfered to ENA. 
