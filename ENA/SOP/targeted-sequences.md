# How to submit targeted sequences
Targeted sequences are typically short assembled and annotated sequences representing interesting features or gene regions. These are submitted as analyses, linked to a project but not necessarily linked to samples. Submission can either be an [EMBL flatfile](https://ena-docs.readthedocs.io/en/latest/submit/sequence/webin-cli-flatfile.html) or using a [checklist](https://ena-docs.readthedocs.io/en/latest/submit/sequence/webin-cli-spreadsheet.html). This SOP covers the latter.

* ENA docs [How to submit targeted sequences](https://ena-docs.readthedocs.io/en/latest/submit/sequence.html#how-to-submit-targeted-sequences)
* ENA docs [Annotation checklists](https://ena-docs.readthedocs.io/en/latest/submit/sequence/annotation-checklists.html)

## Steps
1. Select a suitable checklist by logging in to the portal and go to `Data Analyses` -> `Generate Annotated Sequence Spreadsheet`.
1. Ask research group to populate the spreadsheet.
1. Convert the filled spreadsheet to a .tsv file and gzip.
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
