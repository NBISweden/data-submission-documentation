# How to submit targeted sequences
Targeted sequences are typically short assembled and annotated sequences representing interesting features or gene/intron regions. These are submitted as analyses, linked to a project but not necessarily linked to samples. Submission can either be an [EMBL flatfile](https://ena-docs.readthedocs.io/en/latest/submit/sequence/webin-cli-flatfile.html) or using a [checklist](https://ena-docs.readthedocs.io/en/latest/submit/sequence/webin-cli-spreadsheet.html). This SOP covers the latter.

* ENA docs [How to submit targeted sequences](https://ena-docs.readthedocs.io/en/latest/submit/sequence.html#how-to-submit-targeted-sequences)
* ENA docs [Annotation checklists](https://ena-docs.readthedocs.io/en/latest/submit/sequence/annotation-checklists.html)

## Steps
1. Select a suitable checklist by logging in to the portal and go to `Data Analyses` -> `Generate Annotated Sequence Spreadsheet`.
1. Ask research group to populate the spreadsheet with metadata.
1. Convert the filled spreadsheet to a .tsv file and gzip it.
1. Create a manifest referencing the `STUDY` accession number, a unique `NAME`, an optional `DESCRIPTION` of what is submitted, and the file with the spreadsheet in `TAB` field:
    ```
    STUDY        
    NAME         
    DESCRIPTION    
    TAB         
    ```
1. Validate and submit using Webin-CLI, note the context being `sequence`:
    ``` 
    java -jar webin-cli-9.0.1.jar -username Webin-[XXXXX] -password [PASSWORD] -context sequence -manifest manifest.txt -validate
    ```
1. Just as with assembly submissions, you  will receive an email with accession numbers for each of the targeted sequences, once ENA has processed them.

## Lessons learned
Note that you need to know the reading frame for each included sequence. If incorrect, the submission will fail with an error message. The reading frame is specified in the metadata template indicated by the numbers 0, 1, and 2, indicating the number of leading bases before the first entire codon. Also, the ENA validation steps include a check if the reading frame contains unexpected stop codons.