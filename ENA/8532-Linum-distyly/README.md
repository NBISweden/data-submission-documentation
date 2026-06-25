---
Redmine_issue: https://projects.nbis.se/issues/8532
Repository: ENA
Submission_type: WGS, assembly, target sequences # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB108317
---

# 8532 - Evolutionary consequences of repeated loss of distyly in Linum

## Submission task description
Research group contacted NBIS for assistance with submission of various data in a project to ENA, including WGS reads, RNA-seq, target sequences, and assemblies for a total of 18 species of Linum. 

## Procedure overview and links to examples

* Research group and DS had an initial meeting and decided on expected timeframe and amounts of data to be submitted. The exptected time was short, and it was therefore decided to prioritize registering a study and get a PID to be referenced in the article, and then fill with data.
* After discussion with the research group it was decided to use the ENA default checklist (ERC000011) for the WGS data. A separate spreadsheet was used for the targeted sequences, available through the ENA portal (`Data Analyses` -> `Generate Annotated Sequence Spreadsheet`).
* The [WGS spreadsheet](./data/Linum_distyly_metadata_template_default_ERC000011.xlsx) was put on Google Drive and populated by metadata by the research group.
* After consultation with the research group, three studies were registered.
  * A general study for the 17 species of Linum with annotated chloroplast assemblies.
  * A separate study for the species Linum leonii with an annotated nuclear genome assembly.
  * An umbrella study to define a common entry point for the two studies above.

## Lessons learned
When identifying data files for submission, a few paths contained misspelled folder names. These were identified and corrected based on error messages in the ENA submission process.

For the chloroplast assemblies the fasta headers did not align with the name in the first column in the corresponding gff's. This throws the following error:

```
WARNING EMBLmyGFF3: Sequence id <[xyz]> from the gff file not found within the fasta file. Are you sure to provide the correct fasta file? The tool will create a string of ???? as sequence (its length will be the end position of the last feature).
```
Solution: Changing the header of the fasta files to the column one term in the gff's.

# Detailed step by step description

* Studies were registered in the ENA portal using information in the [ENA spreadsheet](./data/Linum_distyly_metadata_template_default_ERC000011.xlsx).
  * PRJEB108304 - Raw sequences for the nuclear assembly of *Linum leonii*, together with the targeted sequence reads. One locus tag registered.
  * PRJEB108312 - Raw seqeunces for the chloroplast of 16 species of Linum (*L. bienne* not included, see above), together with the chloroplast assemblies. 17 locus tags registered.
  
* An umbrella study (PRJEB108317) was registered via command line in terminal by preparing a [submission.xml](./data/submission.xml) file and an [umbrella.xml](./data/umbrella.xml) file. Both were then submitted using the command:
```
curl -u Webin-XXXXX:[password] -F "SUBMISSION=@submission.xml" -F "PROJECT=@umbrella.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
```
  * A successful registration was confirmed in [the xml receipt](./data/umbrella_submit_receipt.txt)

## Sample registration
Samples for the study was registered by extracting the sample information in the spreadsheet to [a tsv file](./data/linum_samples.tsv), and submitting it via the portal by uploading it in the Samples section under `Samples` -> `Register samples` -> `Upload filled spreadsheet to register samples`.

## Preparation of embl files for annotated assemblies
The project contains a total of 17 annotated chloroplast assemblies and 1 annotated nuclear assembly. For the species *Linum bienne*, no novel data was generated (re-use of NCBI:SRR1592607).

Files were small, and for convenience all were downloaded locally from Dardel before conversion to embl flat file format.

Conversions for chloroplast assemblies were done with the input:

```
EMBLmyGFF3 -i [LOCUS TAG] -p PRJEB108312 -r 1 -s 'Linum [SPECIES]' -t circular -g plastid:chloroplast -m 'genomic DNA' [FILENAME].gff3 [FILENAME].fasta -o Linum_[SPECIES]_chloroplast_assembly.embl
```
Information on Locus tags and file names were taken from the [metadata spreadsheet](./data/Linum_distyly_metadata_template_default_ERC000011.xlsx).

Conversion for the nuclear assembly was done with the input:

```
EMBLmyGFF3 -i LINLEO -p PRJEB108304 -r 1 -s 'Linum leonii' -t linear -m 'genomic DNA' L_leonii_v1_nuclear_Rmo.gff L_leonii_v1_nuclear.fasta -o Linum_leonii_nuclear_assembly.embl
```
Note! The nuclear and chloroplast locus tags for the species *Linum leonii* were not identical (LINLEO and LLEOCHL, respectively).

Finished .embl files were gzipped using the command line:

```
gzip -k *.embl
``` 
(The -k flag assures the original file is not deleted when creating the zip file)

For each chloroplast assembly a corresponding chromosome list file was made:

```
_Laustriacum CHL     Circular-Chromosome       Chloroplast
```

Values were separated by tabs, with term in the first column corresponding to the header in the fasta file. Chromosome list files were saved in .txt format and gzipped.



An initial attempt to submit one of the chloroplast assemblies resulted in several errors relating to feature duplications, e.g:

``` 
ERROR: "gene" Features with locations "complement(6548..9339)" are duplicated - consider merging qualifiers. [ line: 145 of L_austriacum_chloroplast_assembly.embl.gz,  line: 123 of L_austriacum_chloroplast_assembly.embl.gz]
ERROR: "intron" Features with locations "complement(8156..8907)" are duplicated - consider merging qualifiers. [ line: 152 of L_austriacum_chloroplast_assembly.embl.gz,  line: 140 of L_austriacum_chloroplast_assembly.embl.gz]

```
This could be traced back to the gff features:

```
Laustriacum	Chloe	gene	6548	9339	.	-	.	ID=nbis-gene-79;gbkey=CDS;gene=rpoC1
Laustriacum	Chloe	mRNA	6548	9339	.	-	.	ID=gene-chloe_rpoC1_1_2;Parent=nbis-gene-79;gbkey=CDS;gene=rpoC1
Laustriacum	Chloe	exon	6548	8155	.	-	1	ID=chloe_rpoC1_1_5;Parent=gene-chloe_rpoC1_1_2;gbkey=exon;gene=rpoC1
Laustriacum	Chloe	exon	8908	9339	.	-	1	ID=chloe_rpoC1_1_3;Parent=gene-chloe_rpoC1_1_2;gbkey=exon;gene=rpoC1
Laustriacum	Chloe	CDS	6548	8155	.	-	1	ID=cds-chloe_rpoC1_1_2;Parent=gene-chloe_rpoC1_1_2;gbkey=CDS;gene=rpoC1
Laustriacum	Chloe	CDS	8908	9339	.	-	1	ID=cds-chloe_rpoC1_1_2;Parent=gene-chloe_rpoC1_1_2;gbkey=CDS;gene=rpoC1
Laustriacum	Chloe	intron	8156	8907	.	-	1	ID=chloe_rpoC1_1_4;Parent=gene-chloe_rpoC1_1_2;gbkey=intron;gene=rpoC1
Laustriacum	blatX	gene	6548	9339	86.8	-	1	ID=nbis-gene-199;Note=blatX_hit_rpoC1_Rcommunis_GeSeq-SRS_v6%2C_position_1_-_2043%2C_psl_score_86.8%2C_coverage_99.85%25%2C_match_87.32%25;gbkey=gene;gene=rpoC1;gene_biotype=protein_coding
Laustriacum	blatX	RNA	6548	9339	86.8	-	1	ID=gene-blatx_rpoC1_1;Parent=nbis-gene-199;Note=blatX_hit_rpoC1_Rcommunis_GeSeq-SRS_v6%2C_position_1_-_2043%2C_psl_score_86.8%2C_coverage_99.85%25%2C_match_87.32%25;gbkey=gene;gene=rpoC1;gene_biotype=protein_coding
Laustriacum	blatX	exon	6548	8155	.	-	1	ID=blatx_rpoC1_1_exon_2;Parent=gene-blatx_rpoC1_1;gbkey=exon;gene=rpoC1
Laustriacum	blatX	exon	8908	9339	.	-	1	ID=blatx_rpoC1_1_exon_1;Parent=gene-blatx_rpoC1_1;gbkey=exon;gene=rpoC1
Laustriacum	blatX	intron	8156	8907	.	-	1	ID=blatx_rpoC1_1_intron_1;Parent=gene-blatx_rpoC1_1;gbkey`intron;gene=rpoC1
```
The Problem was due to a conflicting setting in the [GeSeq 2.03 online pipeline](https://chlorobox.mpimp-golm.mpg.de/geseq.html) used for annotaion. It allowed for using separate modules (i.e. blatX and Chloe) to annotate the same features (CDS, tRNA and rRNA), effectively doubling the information in the gff, which the ENA validaton interpreted as duplication of features. Resolving the duplication issues using `agat_sp_fix_features_locations_duplicated.pl` and `(agat_convert_sp_gxf2gxf.pl)` in AGAT did not work.

The solution was to re-run the pipeline with non-overlapping annotation features for blatX (tRNA and rRNA) and Chloe (CDS).


## Submisson of annotated assemblies to ENA
### Nuclear assembly for *Linum leonii* 
The nuclear annotated assembly for *Linum leonii* was submitted with Webin-CLI:

```
java -jar webin-cli-9.0.3.jar -username Webin-[XXXXX] -password [PASSWORD] -context genome -manifest Manifest_leonii_nuc.txt -validate
```
After confirmed validation the assembly was submitted changing to the `-submit` flag, with the receipt:

```
INFO : Your application version is 9.0.3
INFO : Connecting to FTP server : webin2.ebi.ac.uk
INFO : Creating report file: [PATH]/./webin-cli.report
INFO : Uploading file: [PATH]/Linum_leonii_nuclear_assembly.embl.gz
INFO : Files have been uploaded to webin2.ebi.ac.uk. 
INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ29265154

```

## Submission of targeted reads
Target reads must be submitted in a separate spreadsheet, available in the portal via `Data Analyses` -> `Generate Annotated Sequence Spreadsheet`. For this submission the ERT000029 list was selected (Single CDS genomic DNA) and downloaded.

The dowloaded checklist was sent to the research group, and populated for the genes TSS1 and WDR44, along with the relevant metadata. The checklist was then [converted to tsv format](./data/Single-CDS_genomic_DNA_ERT000029_1771326273165.tsv) and g-zipped.

Submission was done by preparing a [manifest file](./data/Target_seq_manifest.txt) and then submitting the checklist to ENA project PRJEB108312 by runnning Webi-CLI from the same directory as the manifest and tsv files with the command:

``` 
java -jar webin-cli-9.0.1.jar -username Webin-[XXXXX] -password [PASSWORD] -context sequence -manifest Target_seq_manifest.txt -submit
```
Successful submission was confirmed in the Webin-CLI [output](./data/receipt_target_seq_Linum_disyly_2.txt), with assigned analysis accession ERZ29221441.

## Continuing and unresolved issues at ENA
For two species, *L. leonii* and *L. bienne*, the chloroplast assemblies failed ENA validation with the same type of error:

```
ERROR: organism classified. Submitted /transl_table "11" conflicts with translation table "1" recruited from taxonomy. Please check submitted /transl_table, /organelle and /organism for agreement. Contact us if necessary. [ line: 1 of [File].embl.gz]

```
Curiously, the two species experiencing this issue are the only two species where the chloroplast is derived from WGS data, and in the case of *L. bienne*, from data downloaded from the NCBI.
The cases are still active issues for the ENA helpdesk.

Additionally, all submitted chloroplast annotations passed validation, but seem have encountered processing errors in the ENA internal validation pipeline. 
These cases are also active issues for the ENA helpdesk.