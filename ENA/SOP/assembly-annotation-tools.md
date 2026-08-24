# Tools and scripts when submitting annotated assemblies
An annotated assembly typically consists of a .gff file and a .fasta file. ENA currently only accepts .embl flat file format (will likely be changed end of 2026 to accept .gff and .fasta files directly).
Annotated assemblies, no matter if a full genome or organelle assembly, most often requires an iterative validation (using Webin-CLI) and correction process before it passes. Also, even if the file passes validation, there could still be errors in the post-submission processing step, and it has happen that this processing step removes feature annotations (i.e. the published record is missing annotation), which is only apparent when the assembly is public.

This SOP provides a collection of the tools, scripts and how-to, in order to help solve the most common issues. Note that other tricks, not related to assemblies, are also in this file (last).

## TOC
- [Tools and scripts when submitting annotated assemblies](#tools-and-scripts-when-submitting-annotated-assemblies)
  - [TOC](#toc)
  - [Making ENA compliant .embl flat file](#making-ena-compliant-embl-flat-file)
  - [Extracting genes with validation issues](#extracting-genes-with-validation-issues)
- [Other useful tips and tricks](#other-useful-tips-and-tricks)
  - [XML validation](#xml-validation)
  - [Installing lftp locally on Dardel (PDC)](#installing-lftp-locally-on-dardel-pdc)

## Making ENA compliant .embl flat file
<!-- add every tool, scripts, trick we have used or know of in order to make the GFF work as input -->
* AGAT, [annotation team guide](https://github.com/NBISweden/annotation-cluster/wiki/ENA-submission)
* See [GFF3 to EMBL](./GFF3-to-EMBL.md) on how to use EMBLmyGFF3 in order to create EMBL flat file from .gff and .fasta file.

## Extracting genes with validation issues
Since validation of the assembly is done on the .embl file, and any error messages refers to line numbers in this file, we need to map which lines this corresponds to in the .gff file.

If validation fails with error message referring to duplicate/overlapping genes
<!---
Is the below an example? If so it should be defined in what way it can be modified to fit other scenarios.
--->

```
gunzip -c [filename].embl.gz | awk -v from=18969820 -v to=18969898 'NR>=from { print NR,$0; if (NR>=to) exit 1}' 
```

An alternative to the above is to use zgrep and point the output to a .txt-file:

<!---
Same question as above
--->
```
zgrep '18969820,18969898!d' [filename].embl.gz > out.txt
```

or:
<!--
And here
-->
```
gunzip -c [filename].embl.gz | sed -n '18969820,18969820;18969898' > out.txt
```
---
# Other useful tips and tricks

## XML validation
* Before submitting an .xml file to ENA, they can be validated at <https://www.xmlvalidation.com>, by either copy-pasting the file content, or uploading an entire file, on the website.

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
