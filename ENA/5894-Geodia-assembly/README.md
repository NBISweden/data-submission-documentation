---
Redmine_issue: https://projects.nbis.se/issues/5894
Repository: ENA
Submission_type: <type> # e.g. WGS, assembly, mito
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB58046 
---

# geodia-data-submission-22-12-to-23-03
Description of data submission process of Sponge (Geodia) data in NBIS LTS project to ENA.

# 1. Project Orientation

Contact was made by Bioinformatician in November 2022 to include DM in data submission request by researchers. 

Data types were listed as:

Raw data:
  - Illumina HiSeqX
  - PacBio RSII reads
  - PacBio Sequel reads
     
Assemblies:
  - Annotated nuclear genome
  - Annotated Mitochondrial genome

Data was generated in 2017-2018. PacBio reads were the basis of the assembly, with HiSeqX data used to refine the assmebly and increase quality.

# 2. First scheduled meeting

First meeting between Data Steward (DS) and researchers on 2022-12-02 via Zoom. This was followed up in the week after with communication between Bioinformaticians and researchers on which files to submit, resulting in a list of files for submission consisting of:

  - 1 file of PacBio RSII filtered subreads in .FASTQ format (1.02G zipped)
  - 4 files of PacBio Sequel reads in .BAM format (3.74G + 4.05G + 2.6G + 2.43G unzipped)
  - 2 files of HiSeqX reads in .FASTQ format (37.58G + 42.99G zipped)

  - 1 annotated nuclear assembly in .GFF format prepared for ENA by Bioinfomratician (351M unzipped)
  - 1 corresponding nuclear genome .FASTA file (147M)
  - 1 annotated mitochondrial assembly in .GFF format prepared for ENA by researchers (8kb unzipped)
  - 1 corresponding mitochondrial genome .FASTA file (18k)

# 3. ENA account - Registration of project and study 

Resarchers created account in ENA and registered project and study on 2022-12-05. Provided DS with ENA login information to act as broker.

Data Steward decided to begin submission with the PacBio RSII sequel reads. Single file, small file size.

  - Submission to be done using the ENA webin-cli client due to the various file formats in the projects. Keeping all submissions to a single solution makes trouble shooting easier. Further, the client java executable, e.g. `webin-cli-6.1.0.jar` was not installed and put in PATH, but was kept in the active submission folder and executed in the Terminal in the respective folder.
  - Researchers provided DS with access to project folder at UPPMAX, for brokering purposes.
  - DS provided with paths to respective files
> Note: The file tree was rather complex and not easy to navigate. Printed a tree topology to store locally on laptop to facilitate orientation.

# 4. Locus tags

To prepare the assembly data for submission, proper locus tags had to be decided. After consultation the researchers decided on the abbreviation GBAR for the species under study (Geodia BARretti). The locus tag is essential to perform the conversion of .GFF to .EMBL using EMBLmyGFF3 later on.

# 5. Raw data submissions to ENA

## 5.1 Preparing for first submission of data incl. creating the manifest file

The PacBio RSII .FASTQ file was downloaded from UPPMAX and verified. After verification the same file was gzipped using the command line with `-k` flag to retain the original file after zipping:

```gzip -k pb_387_filtered_subreads.fastq > pb_387_filtered_subreads.fastq.gz```

A manifest file was first attempted in .JSON format, but the configuration of the file was difficult to figure out, and a change to simple .TXT format was made, naming the file `manifest_RSII.txt`. 

```
STUDY PRJEB58046
SAMPLE ERS14471852
NAME pb_387
INSTRUMENT PacBio RS II
INSERT_SIZE 4500
LIBRARY_SOURCE METAGENOMIC
LIBRARY_SELECTION RANDOM
LIBRARY_STRATEGY WGS
FASTQ pb_387_filtered_subreads.fastq.gz
```

Information for `INSTRUMENT` was taken from the ENA web help pages. Information for `INSERT SIZE`, `LIBRARY SOURCE`, `LIBRARY SELECTION`, and `LIBRARY STRATEGY` was provided by the researchers. Information for `NAME` was decided by DS in consultation with colleague. ENA website provided very few suggestions on format and what type of information `NAME` should allude to. It was eventually decided to let `NAME` reference the library name.

## 5.2 First submission round (PacBio RSII reads)

Using the webin-cli client (version 5.2.0) the submission was first validated using the command line:

```java -jar webin-cli-5.2.0.jar -context=reads -manifest=manifest_RSII.txt -userName=[username] -password=[password] -validate```

After validation pass the command line was changed to: 

```java -jar webin-cli-5.2.0.jar -context=reads -manifest=manifest_RSII.txt -userName=[username] -password=[password] -submit```

A successful submission was verified by command line output.

## 5.3 Second submission round (PacBio Sequel reads)

Similar to the previous submission of RSII reads (# 5.1 and # 5.2) the four .BAM files were downloaded from UPPMAX, validated, and zipped like above. A new manifest file was made in .TXT format (manifest_Sequel_reads.txt) as:

```
STUDY PRJEB58046
SAMPLE ERS14471852
NAME Sequel-4
INSTRUMENT Sequel
INSERT_SIZE 7000
LIBRARY_SOURCE METAGENOMIC
LIBRARY_SELECTION RANDOM
LIBRARY_STRATEGY WGS
BAM m54032_171020_230022.subreads.bam
```

Specifications were provided as above, with the last line `BAM` changed to match each of the files, respectively. 

> Note Submission of .BAM files can only be made one at a time.

Using the webin-cli client (version 5.2.0) the submission was first validated, as before, using the command line:

```java -jar webin-cli-5.2.0.jar -context=reads -manifest=manifest_Sequel_reads.txt -userName=[username] -password=[password] -validate```

After validation pass the command line was changed to:

```java -jar webin-cli-5.2.0.jar -context=reads -manifest=manifest_Sequel_reads.txt -userName=[username] -password=[password] -submit```

## 5.4 Third submission round (HiSeqX reads)

For the two larger HiSeqX files they were, just as before, downloaded from UPPMAX, validated, and zipped. The manifest (manifest_HiSeqX.txt) was defined as:

```
STUDY PRJEB58046
SAMPLE ERS14471852
NAME HISEQ-RC-1780
INSTRUMENT HiSeq X Ten
INSERT_SIZE 350
LIBRARY_SOURCE METAGENOMIC
LIBRARY_SELECTION RANDOM
LIBRARY_STRATEGY WGS
FASTQ RC-1780-Geodia-barretti_S1_L001_R1_001.fastq.gz
FASTQ RC-1780-Geodia-barretti_S1_L001_R2_001.fastq.gz
```

Using the webin-cli client (version 5.2.0) the submission was first validated, as before, using the command line:

```java -jar webin-cli-5.2.0.jar -context=reads -manifest=manifest_HiSeqX.txt -userName=[username] -password=[password] -validate```

After validation pass the command line was changed to:

```java -jar webin-cli-5.2.0.jar -context=reads -manifest=manifest_HiSeqX.txt -userName=[username] -password=[password] -submit```

However! Executing the command line resulted in a standy prompt, not seemingly gettting anywhere. Waiting for an extended time (1-6 hours) did not help. Any time the laptop was interrupted by energy save mode the file upload was terminated with an error message.

> Note: It seems very large files makes the webin-cli client get stuck in a silent or non-verbose submission loop!

After consultation with DS colleagues the solution was to apply the IBM Aspera client as recommended by ENA. Installation of the client did not work immediately as it seemed the webin-cli client could not call the functions in spite of using the `-ascp` flag.

> Note: The not so obvious solution was to make sure the Aspera binary `ascp` was in PATH **toghter with the corresponding `ascp-license` file**! Without the license file in the same PATH as the binary, the client fails to execute. However, the error messages running the webin-cli client without correct PATH to `ascp` and `ascp-license` does not revreal what is wrong! The solution was eventually found by making Aspera uploads to their test server using dummy data.

Once the Apera client executed as excpected the final raw reads could eventually be uploaded to ENA (2023-02-15) with the command line:

```java -jar webin-cli-5.2.0.jar -ascp -context=reads -manifest=manifest_HiSeqX.txt -userName=[username] -password=[password] -validate```

and

```java -jar webin-cli-5.2.0.jar -ascp -context=reads -manifest=manifest_HiSeqX.txt -userName=[username] -password=[password] -submit```

> Note: It seems certain uploads in webin-cli using the Aspera flag results in failed file uploads due to system errors. In case this happens, try the same upload but witout the `-ascp` flag. 

# 6. Assembly submissions to ENA

Once the raw reads were submitted and accepted to the ENA, the Assemblies were next. As these referenced the raw data all raw datafiles were required to have assigned accession numbers before assembly submissions could begin.

Two assemblies were scheduled:

  - Annotated nuclear genome (made by Bioinfomraticians at NBIS)
  - Annotated mitochondrial genome (made by researchers in the software Geneious, based on data provided by NBIS Bioinformaticians)

As ENA does not (Early spring 2023) accept .GFF files for annotations a conversion to the EMBL flat file format was made using the emblmygff3 application (REF). The NBIS Bioinformaticians provided file paths to the proper .GFF files prepared for ENA submissions.

> Note: The file tree in the project folder on UPPMAX contained multiple .GFF files with various names. Crucial for the project that responsible Bioinformaticians not only pointed out the correct files with paths, but also labelled the files accordingly.

## 6.1 .GFF to .EMBL conversion

For conversions to .EMBL flat file format the application requires two files:

  - A .GFF file
  - The corresponding .FASTA file

> Note: The .FASTA file header needs to correspond to the label on the .EMBL `AC * ` line.

Conversion was done using the command line:
```EMBLmyGFF3 -i GBAR -p [ENA project] -r 1 -s 'Geodia barretti' -t linear -m 'genomic DNA' [input ENA gff file].gff [fastq file].fa -o [output file].embl```

THe resulting .EMBL flat file was then zipped as above. 

## 6.2 The manifest file

A manifest file in .TXT format was prepared as follows:

```
STUDY           PRJEB58046
SAMPLE          ERS14471852
ASSEMBLYNAME    Geodia_barretti_n_2022_12
ASSEMBLY_TYPE   isolate
COVERAGE        19
PROGRAM         Flye
PLATFORM        HiSeq X Ten, PacBio RS II, Sequel-4
MINGAPLENGTH    100
MOLECULETYPE    genomic DNA
DESCRIPTION     'PacBio data was assembled with Flye using the ‘-meta’ flag (Kolmogorov et al. 2020) and polished with the short reads using Pilon (Walker et al. 2014). RNA sequencing data of the same specimen sequenced here and six other G. barretti individuals were used for identification of sponge contigs and gene annotation. These seven poly-A selected transcriptomes (bioproject: PRJNA603347, SRA: SRS6083072) include four individuals from the Norwegian and Barents Sea, sequenced with Scriptseqv2 (ROV6_3, trawl_5, trawl_6, trawl_8) and three individuals from Sweden sequenced with Trueseqv2 (Geodia_01 (UPSZMC 184975), Geodia_02 (UPSZMC 184976), Geodia_03 (UPSZMC 184977)) (Koutsouveli, Cárdenas, Conejero, et al. 2020). The transcriptomes were assembled using Trinity (Haas et al. 2013) with default parameters. To remove contamination (non-sponge contigs/scaffolds), these transcripts together with eukaryotic reference sequences from refseq (nt/nr) and UniProt were mapped against the polished assembly using gmap (Wu et al. 2016). Contigs with more than 20% coverage of either transcripts or refseq reads were retained. Coverage was calculated by mapping short and long reads to the genome with BWA (Li and Durbin 2009) and minimap2 (Li 2018) respectively. The depth of the resulting BAM files was extracted using samtools depth (Li et al. 2009) and the average and median across the coverage at all positions we calculated.'
RUN_REF:        ERR10902930,ERR10857208,ERR10857206,ERR10857204,ERR10857202,ERR10857169
FLATFILE:       geodia_barretti_n_genome_C.embl.gz
```

Where the `ASSEMBLYNAME` was provided by the DS referencing the organism, year, and month the assembly was to be submitted. Additional information for `COVERAGE`, `PROGRAM`, `MINGAPLENGTH`, and `DESCRIPTION` was provided by the researchers, where the information in the latter is a copy-paste from the article to be published. The files listed in `RUN_REF` are the accession numbers for the raw data reads previously submitted (# 5.2-5.4). 

## 6.3 Submitting the Assemblies to ENA

Executing the (now updated to v6.1.0) webin-cli client with the command:

```java -jar webin-cli-6.1.0.jar -ascp -context=genome -manifest=manifest_nDNA_genome.txt -userName=[username] -password=[password] -validate```

Running the above command resulted in multiple errors written to the [filename].report file, limited to the three categories (e.g.):

  1. `ERROR: Invalid date: 15-DEC-2022 [ line: 9]`

  2. `ERROR: Abutting features cannot be adjacent between neighbouring exons.`

  3. `ERROR: "exon" Features locations are duplicated - consider merging qualifiers.`

The first error (1.) was, after extensive troubleshooting, caused by the submitting DS laptop being set to Swedish system locale (sv_SE). Changing it to English (en_UK) by adding the java flags `-Duser.language=en` and `-Duser.country=UK` solved the issue:

```java -jar -Duser.language=en -Duser.country=UK webin-cli-6.1.0.jar -ascp -context=genome -manifest=manifest_nDNA_genome.txt -userName=[username] -password=[password] -validate```

The remaining errors (2. and 3.) also required extensive troubleshooting, but the solution was to modify the `translation_gff_attribute_to_embl_qualifier.json` and `translation_gff_feature_to_embl_feature.json` files located in the respective assembly folders by first running the command:

`EMBLmyGFF3 --expose_translations`

And then modifying `translation_gff_attribute_to_embl_qualifier.json` to the following:

```
"Dbxref": {
   "source description": "A database cross reference.",
   "target": "inference",
   "dev comment": "inference"
 },
 "Ontology_term": {
   "source description": "A cross reference to an ontology term.",
   "target": "inference",
   "dev comment": ""
 },
 ```
 
 And in `translation_gff_feature_to_embl_feature.json` to:
 
```
 '"exon": {
    "remove": true
},
```

After which the webin-cli was again executed with the command:

```java -jar -Duser.language=en -Duser.country=UK webin-cli-6.1.0.jar -ascp -context=genome -manifest=manifest_nDNA_genome.txt -userName=[username] -password=[password] -validate```

And after passed validation again with the `-submit` flag: 

```java -jar -Duser.language=en -Duser.country=UK webin-cli-6.1.0.jar -ascp -context=genome -manifest=manifest_nDNA_genome.txt -userName=[username] -password=[password] -validate```

In case the submission failed with a system error the same file was submitted again but without the `-ascp` flag.

## 6.4 Mitochondrial assembly submisison

The same thing was then repeated for the Mithochondrial genome with one exception. In an ENA submission the Mitochondria must be submitted as an organelle, which is treated as a chromosome in the submission. For webin-cli to submit the mithochondrial assembly an additional file must be referenced in the manifest:

```
STUDY           PRJEB58046
SAMPLE          ERS14471852
ASSEMBLYNAME    Geodia_barretti_mt_2020_01
ASSEMBLY_TYPE   isolate
COVERAGE        19
PROGRAM         HGAP
PLATFORM        HiSeq X Ten, PacBio RS II, Sequel-4
MOLECULETYPE    genomic DNA
DESCRIPTION     'PacBio data was assembled with Flye using the ‘-meta’ flag (Kolmogorov et al. 2020) and polished with the short reads using Pilon (Walker et al. 2014). RNA sequencing data of the same specimen sequenced here and six other G. barretti individuals were used for identification of sponge contigs and gene annotation. These seven poly-A selected transcriptomes (bioproject: PRJNA603347, SRA: SRS6083072) include four individuals from the Norwegian and Barents Sea, sequenced with Scriptseqv2 (ROV6_3, trawl_5, trawl_6, trawl_8) and three individuals from Sweden sequenced with Trueseqv2 (Geodia_01 (UPSZMC 184975), Geodia_02 (UPSZMC 184976), Geodia_03 (UPSZMC 184977)) (Koutsouveli, Cárdenas, Conejero, et al. 2020). The transcriptomes were assembled using Trinity (Haas et al. 2013) with default parameters. To remove contamination (non-sponge contigs/scaffolds), these transcripts together with eukaryotic reference sequences from refseq (nt/nr) and UniProt were mapped against the polished assembly using gmap (Wu et al. 2016). Contigs with more than 20% coverage of either transcripts or refseq reads were retained. Coverage was calculated by mapping short and long reads to the genome with BWA (Li and Durbin 2009) and minimap2 (Li 2018) respectively. The depth of the resulting BAM files was extracted using samtools depth (Li et al. 2009) and the average and median across the coverage at all positions we calculated.'
RUN_REF:        ERR10902930,ERR10857208,ERR10857206,ERR10857204,ERR10857202,ERR10857169
FLATFILE:       geodia_barretti_mt_genome.embl.gz
CHROMOSOME_LIST: chromosome_list.txt.gz
```

The text file `chromosome_list.txt.gz` in this case contains a single line with the following information separated by tabs:

`Gb1_v12	MIT Linear-Chromosome Mitochondrion`

  - The value in the initial row `Gb1_v12` must be the same as referenced in the corresponding .EMBL flat file on the `AC *` line. 
  - The second value `MIT` is a standard abbreviation of the Mitochondria in `CHROMOSOME_NAME` format
  - The third value refers to the CHROMOSOME_TYPE input with an optional `Linear` modifier as the mitochondria is submitted as a linear sequence.
  - The fourth value is optional and refers to the `CHROMOSOME_LOCATION` for which ENA has pre-defined values.

Executing the command line:

```java -jar -Duser.language=en -Duser.country=UK webin-cli-6.1.0.jar -context=genome -manifest=manifest_mtDNA_genome.txt -userName=[username] -password=[password] -validate```

And after successful validation followed by:

```java -jar -Duser.language=en -Duser.country=UK webin-cli-6.1.0.jar -context=genome -manifest=manifest_mtDNA_genome.txt -userName=[username] -password=[password] -submit```

# 7 Post submission follow up

After confirming successful submissions by loggin into ENA and checking that all submissions have been accepted, the raw data accession numbers toghether with the two annotated assembly accession numbers, were mailed to the researchers. Confirmation of received accession numbers effectively closed the issue on 2023-03-02.