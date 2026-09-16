# Tools and scripts when submitting annotated assemblies
An annotated assembly typically consists of a .gff file and a .fasta file. ENA currently only accepts .embl flat file format (will likely be changed end of 2026 to accept .gff and .fasta files directly).
Annotated assemblies, no matter if a full genome or organelle assembly, most often requires an iterative validation (using Webin-CLI) and correction process before it passes. Also, even if the file passes validation, there could still be errors in the post-submission processing step, and it has happen that this processing step removes feature annotations (i.e. the published record is missing annotation), which is only apparent when the assembly is public.

This SOP provides a collection of the tools, scripts and how-to, in order to help solve the most common issues. Note that other tricks, not related to assemblies, are also in this file (last).

**On this page:**

- [Making ENA compliant .embl flat file](#making-ena-compliant-embl-flat-file)
- [Extracting genes with validation issues](#extracting-genes-with-validation-issues)
- [Other useful tips and tricks](#other-useful-tips-and-tricks)
  - [XML validation](#xml-validation)
  - [Installing lftp locally on Dardel (PDC)](#installing-lftp-locally-on-dardel-pdc)

## Making ENA compliant .embl flat file
<!-- add every tool, scripts, trick we have used or know of in order to make the GFF work as input -->
* AGAT, [annotation team guide](https://github.com/NBISweden/annotation-cluster/wiki/ENA-submission)
* See [GFF3 to EMBL](./GFF3-to-EMBL.md) on how to use EMBLmyGFF3 in order to create EMBL flat file from .gff and .fasta file.
* Information on how to calculate MINGAPLENGTH and COVERAGE for assembly manifests is found in [assembly submission](assembly-submission.md)

## Extracting genes with validation issues
Validation of an assembly (using Webin-CLI) is done on the .embl file, and any error messages refers to line numbers in this file. If an error is due to e.g. duplicated features, it is the .gff file that should be updated. Hence, we need to figure out which gene it concerns, in order to make it possible to map which lines this corresponds to in the .gff file.

### An example
Say that the validation produces the following error message:

```
ERROR: "5'UTR" Features locations are duplicated - consider merging qualifiers. [ line: 108571150 of ERP161594-PSYLV.embl.gz,  line: 108571128 of ERP161594-PSYLV.embl.gz]
``` 
The task is to extract sufficient surrounding lines in order to tell us which gene is concerned. The following 3 alternatives will each extract 80 lines above the first duplicated line (108571128) and 5 lines below the second duplicated line (108571150) in the file named ERP161594-PSYLV.embl.gz:

  1. Unzip and use awk:
  ```
  gunzip -c ERP161594-PSYLV.embl.gz | awk -v from=108571047 -v to=108571155 'NR>=from { print NR,$0; if (NR>=to) exit 1}' 
  ```

  2. Use zgrep and point the output to a .txt-file:
  ```
  zgrep '108571047,108571155!d' ERP161594-PSYLV.embl.gz > out.txt
  ```

  3. Unzip and use sed and point the output to a .txt-file:

  ```
  gunzip -c ERP161594-PSYLV.embl.gz | sed -n '108571047,108571047;108571155' > out.txt
  ```
---

# Other useful tips and tricks

## XML validation
Before submitting an .xml file to ENA, they can be validated at <https://www.xmlvalidation.com>, by either copy-pasting the file content, or uploading an entire file, on the website.

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
