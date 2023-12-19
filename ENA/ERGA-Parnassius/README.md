---
Redmine_issue: -
Repository: ENA
Submission_type: WGS, assembly,
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB67749
---

# Parnassius_mnemosynes_assembly-submission-23-10-to-23-11

Description of the data submission process of Clouded Apollo (*Parnassius mnemosyne*) data in the NBIS ERGA pilot.

# 1. Project Orientation

Project was initiated in the EvolBio team after bioinformaticians and team coordinator decided that all relevant work had been done on the assembly.

Data types were listed as:

Raw data:
  - PacBio Sequel II HiFi reads
  - PacBio Sequel II IsoSeq reads
  - Novaseq 6000 Hi-C reads
  - Novaseq 6000 RNA-seq reads
     
Assembly:
  - Annotated nuclear genome

# 2. Data overview

Bioinformatician provided a list of files with paths of the data to be submitted to ENA:
  - HiFi
    - m64077_211103_083236.hifi_reads.bam
    - m64204e_211029_093505.hifi_reads.bam
  - IsoSeq
    - m64204e_220724_000530.hifi_reads.bam
  - Hi-C
    - PM_S6_L001_R1_001.fastq.gz
    - PM_S6_L001_R2_001.fastq.gz
  - RNA-seq
    - PM_R1_001.fastq.gz
    - PM_R2_001.fastq.gz
  - Assembly
    - pmne_functional.gff

# 3.  ERGA metadata manifest

# 3.1 The COPO incident
As *Parnassius mnemosyne* was the first representative of the ERGA Pilot species to have its data submitted to ENA, it was important to know if the metadata was present and readily available in COPO. All ERGA species are supposed to have the ERGA manifest validated in COPO. However, it was unclear if the manifest was to be submitted to COPO by the researcher or the DS. Upon request the PI sent the manifest file by email.

Checking the filled in manifest against the requirements and ERGA guidelines revealed a few discrepancies. Minor corrections to the metadata was made to bring it into line with the current guidelines, after which it was submitted in the COPO portal.

All manifest submissions to COPO are validated, and post-submission of the manifest the COPO staff made contact and informed there were now two separate versions of the manifest in their system, the latest one also duplicated. It was revealed the PI had already submitted an earlier version of the manifest, and it had to be decided which version had priority.

After much confusion it was eventually decided that the original version of the manifest was to be kept and the updated version deleted from COPO/ENA, in spite of the original version not complying in full with stated guidelines.

--------

NOTE!

There is no easy way to search COPO for individual manifests. The easiest way to reference the metadata appears to be by searching the species name at BioSamples and manually identify which records are related to the COPO manifest. It will result in a list of BioSample accession numbers each related to a sample, which can later be referenced in the ENA submission process.

This will be a seemingly persistent issue in future ERGA submissions!

--------

When the COPO staff had removed the duplicate manifest versions from ENA, the submission could continue.

## 3.2 Tree of Life ID (ToLID)
For the species *Parnassius mnemosyne* a search at ```https://id.tol.sanger.ac.uk/``` revealed there was already a ToLID registered. Therefore it was decided that all sample names would reference this ToLID (ilParMnem1) to increase findability.

# 4. Registration of ENA project and study

For ERGA species NBIS will act as a submission broker, using the NBIS ENA broker account. In that account a study was registered for *Parnassius mnemosyne* with the title

```Parnassius mnemosyne, genomic and transcriptomic data, ERGA Pilot```

Release date was set to 2025-10-24 (two tyears from project creation date), which will be a standard for all brokered ERGA data.

The short descriptive title was set to the same as the Study Name, and the detailed study abstract was limited to:

```Pilot species in the ERGA (European Reference Genome Archive) initiative.```

The box for "Will you provide a functional genome annotation?" was checked, and the locus tag was set to ```PARMNEM```.

# 5. Sample registration

As the sample metadata is submitted to ENA via COPO there are no visible records at ENA to reference. Instead the submission refers to the BioSample accession numbers. For *Parnassus mnemosyne*, these were copied from BioSamples and kept locally on the laptop.

Three samples were registered for *Parnassius mnemosyne*, one for 'thorax' and two for 'whole body'. The latter two were identical, but one had been included in a shipping to Antwerpen for sequencing. After communication with the PI it was determined the 'thorax' sample was used for RNA-seq, and the 'whole body' for genome (re-)sequencing. 

# 6. Raw data submissions to ENA

## 6.1 File preparations

All files were already in the required ENA format (.gz for fasta files, and .bam) and no prior file preparations were therefore necessary.

## 6.2 First submission round (HiFi+Iso-Seq data)

A manifest file for the PacBio HiFi data was made, named ```Manifest_pacbio_Parnassius.txt``` with the following information:

```
STUDY PRJEB67749
SAMPLE SAMEA13166627 [from BioSamples]
NAME PACBIO-HIFI-ilParMnem1-[1/2]
INSTRUMENT Sequel II
INSERT_SIZE 18000
LIBRARY_SOURCE GENOMIC
LIBRARY_SELECTION RANDOM
LIBRARY_STRATEGY WGS
BAM [Filename(s) as above]
```
Information for the webin-CLI manifest was gathered from the PI and the NGI report.

Using the webin-cli client (version 6.7.1) the submission was first validated using the command line:

```
java -jar webin-cli-6.7.1.jar -ascp -context=reads -manifest=Manifest_pacbio_Parnassius.txt -userName=[username] -password=[password] -validate
```

After validation pass the command line was changed to:

```
java -jar webin-cli-6.7.1.jar -ascp -context=reads -manifest=Manifest_pacbio_Parnassius.txt -userName=[username] -password=[password] -submit
```

A successful submission was verified by command line output.

The submission was done thrice, once for each .bam file in the dataset for HiFi-data, with updated file names and sample name index number, plus once for the Iso-Seq submission where the ```NAME``` in the manifest file was changed to ```PACBIO-Isoseq-ilParMnem1-3```


## 6.3 Second submission round (Hi-C data)

A new manifest file was made for the Hi-C data:

```
STUDY PRJEB67749
SAMPLE SAMEA13166627
NAME HIC-ILLUMINA-ilParMnem1-1
INSTRUMENT Illumina NovaSeq 6000
INSERT_SIZE 600
LIBRARY_SOURCE GENOMIC
LIBRARY_SELECTION RANDOM
LIBRARY_STRATEGY Hi-C
FASTQ PM_S6_L001_R1_001.fastq.gz
FASTQ PM_S6_L001_R2_001.fastq.gz
```

The submission was validated as described above (6.2):

```
java -jar webin-cli-6.7.1.jar -ascp -context=reads -manifest=Manifest_HiC_Parnassius.txt -userName=[username] -password=[password] -validate
```

After validation pass the command line was changed to:

```
java -jar webin-cli-6.7.1.jar -ascp -context=reads -manifest=Manifest_HiC_Parnassius..txt -userName=[username] -password=[password] -submit
```



## 6.5 Fourth submission round (RNA-seq data)

For the final raw data category, the procedure was followed as described above, but with the BioSample changed to the 'thorax' sample.

```
STUDY PRJEB67749
SAMPLE SAMEA13166629
NAME RNA-MISEQ-ilParMnem1
INSTRUMENT Illumina MiSeq
INSERT_SIZE 450
LIBRARY_SOURCE TRANSCRIPTOMIC
LIBRARY_SELECTION cDNA
LIBRARY_STRATEGY RNA-Seq
FASTQ PM_R1_001.fastq.gz
FASTQ PM_R2_001.fastq.gz
```

The submission was validated as described previously:

```
java -jar webin-cli-6.7.1.jar -ascp -context=reads -manifest=manifest_rna_Parnassius.txt -userName=[username] -password=[password] -validate
```

After validation pass the command line was changed to:

```
java -jar webin-cli-6.7.1.jar -ascp -context=reads -manifest=manifest_rna_Parnassius.txt -userName=[username] -password=[password] -submit
```

With the HiFi, Hi-C and RNA-seq data submitted, the raw data was finally registered at ENA, and attention could be switched to the assembly.


# 7. Assembly submission to ENA

The assembly for *Parnassius mnemosyne* was downloaded locally to laptop and converted to EMBL flatfile using the EMBLmyGFF3 script. After conversion a manifest file was made:

```
STUDY           PRJEB67749
SAMPLE          SAMEA13166627
ASSEMBLYNAME    Parnassius_mnemosyne_n_2023_11
ASSEMBLY_TYPE   isolate
COVERAGE        30
PROGRAM         Hifiasm
PLATFORM        PacBio HiFi, Illumina Hi-C
MINGAPLENGTH    1
MOLECULETYPE    genomic DNA
DESCRIPTION     'The PacBio HiFi reads were assembled using Hifiasm v0.16.0. Purge_Dups v1.2.5 was used to remove putative haplotype-induced duplications. Hi-C data was aligned to the purged assembly and processed with pairtools v0.3.0, and contigs were scaffolded with YaHS v1.1a. Hi-C scaffolds were manually edited with JBAT v2.20.00 using the Hi-C contact maps and telomere motif annotation from tidk (https://github.com/tolkit/telomeric-identifier) v0.2.31 to produce the final assembly.'
RUN_REF:        ERR12146337, ERR12148427, ERR12148429
FLATFILE:       PARMNEM_for_ENA.embl.gz
```

The assembly was submitted for validation to ENA using the webin-CLI command:

```
java -jar webin-cli-6.7.1.jar -ascp -context=genome -manifest=PARMNEM_manifest.txt -userName=[username] -password=[password] -validate
```

Validation failed with multiple error messages referring to duplicate/overlapping exon/intron features. Using the flag ```EMBLmyGFF3 --expose_translation``` and making .json modifications as described in the Geodia submisson [https://github.com/NBISweden/data-submission-documentation/blob/main/ENA/5894-Geodia-assembly/README.md] the issues with introns were managed. However, subsequent validatons still produced a warning for two overlapping genes.

There are two solutions to the problem, one being manually removing either of the duplications, or the other, to run the .gff through AGAT to merge duplicates. Prior to contacting the bioinformatician the overlapping genes had to be identified. As ENA assembly validation is made on .gz files and the error message refers to numbered rows in the .gz file, the gene identification had to be extracted from the compressed file. This was done using the below command line, capturing a number of rows before and after the span indicated in the validation process, and give output only in the command window:

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

After contact with the bioinformatician who produced the .gff the overlappping issue was fixed (unknown exactly how), and the assembly passed validation. The assembly was then submitted using the commmand:

```
java -jar webin-cli-6.7.1.jar -ascp -context=genome -manifest=PARMNEM_manifest.txt -userName=[username] -password=[password] -submit
```
# 8. Post-submission mop-up

After submission of the assembly it was considered complete. Accession numbers were gathered and sent to the PI via email, and the assembly team was informed.

# 9. Lessons learned, plus take-aways

The first take-away lesson was that the responsibility for COPO metadata quality and submission is on the PI and no-one else. The DM-staff will only accept the COPO-submitted metadata *as is*. Any updates should be made by the PI, not the DM staff. It seems as if the content of the manifest is updated, but the manifest itself is of a more recent version than the already submitted one, COPO does not produce an update of the present record, but duplicates it. If this happens COPO needs to be contacted to manually remove the auto-generated record at ENA.

It also seems like the curation of COPO submissions are limited to a validation tool Boolean outcome. Anything passing validation will be automatically submitted to ENA with automatic creation of records. It was also possible to make duplicate submission in COPO since the progress bar associated with the submit button was active in the background, leaving the submit button open for re-clicks.

For the assembly a lesson learned was the process of finding out the location and name of duplicate and/or overlapping exons/genes so the Bioinformatician can make adjustments to the .gff. 