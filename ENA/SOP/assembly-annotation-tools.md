# Tools and scripts when submitting annotated assemblies
An annotated assembly typically consists of a .gff file and a .fasta file. ENA currently only accepts .embl flat file format (will likely be changed end of 2026 to accept .gff and .fasta files directly).
Annotated assemblies, no matter if a full genome or organelle assembly, most often requires an iterative validation (using Webin-CLI) and correction process before it passes. Also, even if the file passes validation, there could still be errors in the post-submission processing step, and it has happen that this processing step removes feature annotations (i.e. the published record is missing annotation), which is only apparent when the assembly is public.

This SOP provides a collection of the tools, scripts and how-to, in order to help solve the most common issues. Note, for now other, not related to assemblies, tricks are also in this file (last).

## TOC
* [Making ENA compliant EMBL flat file](#making-ena-compliant-embl-flat-file)
* [Extracting genes with validation issues](#extracting-genes-with-validation-issues)
* [Installing lftp locally on Dardel](#installing-lftp-locally-on-dardel-pdc)
* [XML validation](#xml-validation)
* []()

## Making ENA compliant .embl flat file
* EMBLmyGFF3, expose_translation etc [EMBLmyGFF](https://github.com/NBISweden/EMBLmyGFF3)
* AGAT, annotation teams [How-to on github](https://github.com/NBISweden/annotation-cluster/wiki/ENA-submission#create-embl-file)
* Identify which translational table to be used at [NCBI taxonomy lookup](https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi).

## Extracting genes with validation issues
Since validation of the assembly is done on the .embl file, and any error messages refers to line numbers in this file, we need to map which lines this corresponds to in the .gff file.

If validation fails with error message referring to duplicate/overlapping genes

```
gunzip -c [filename].embl.gz | awk -v from=18969820 -v to=18969898 'NR>=from { print NR,$0; if (NR>=to) exit 1}' 
```

An alternative to the above is to use zgrep and point the output to a .txt-file:

```
zgrep '18969820,18969898!d' [filename].embl.gz > out.txt
```

or:

```
gunzip -c [filename].embl.gz | sed -n '18969820,18969820;18969898' > out.txt
```
---
# Other useful tips and tricks

## XML validation
* Before submitting an .xml file to ENA, they can be validated at <https://www.xmlvalidation.com>

## Installing lftp locally on Dardel (PDC)
The *lftp* command is often the only option in order to submit sequences to ENA. Here's how to install and run it locally via conda.
* In the home directory, on Dardel:
    ```
    ml PDC/24.11
    ml miniconda3
    conda create --name lftp-env -c conda-forge lftp
    source activate lftp-env
    ```
* This installs and activates the lftp environment. Then files can be transferred by `cd` into directory with files on Dardel, and from there run:
```
lftp webin2.ebi.ac.uk -u Webin-[XXXXX]
(enter password at prompt)
mput *.gz
```
* When all files in the current directory are transferred, exit lftp with `bye`
