---
Redmine_issue: https://projects.nbis.se/issues/6717
Repository: ENA
Submission_type: ERGA, HiFi, HiC, Iso-Seq, assembly, annotation
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB71764
---

# ERGA *Bufotes viridis* (European green toad)

## Submission task description
Submit genomic and assembly data for the European green toad, *Bufotes viridis*, as part of the ERGA pilot project. Sample metadata has already been submitted via COPO and is linked through BioSamples.

## Steps

1. Create metadata manifest templates in textfiles (for webin-CLI submission)
2. Query BioSamples for sample candidates, then ask PI and NGI staff which sample(s) has been sequenced
3. Identify and locate relevant raw data files used in the project
4. Register study in ENA, including locus tag
5. Submit experiments (raw data files) using filled in manifest templates
6. Submit assembly using manifest

## Lessons learned
* In this project there was extensive issues with connecting samples in BioSamples to data type, with contradicting information from the PI and NGI, without any possibility to sort out the details. When this happens, the Data Steward will need to make educated guesses and document the choices (e.g. here) for future reference.  

## Detailed step by step description
### Sample metadata

* [Biosamples query](https://www.ebi.ac.uk/biosamples/samples?text=Bufotes+viridis&filter=attr:project+name:ERGA) returned 11 ids (range SAMEA13166615-SAMEA13166625)

* In communication with NGI and the PI, some raw data file types (PacBio HiFi and Hi-C) samples were impossible to trace back to specific BioSample ID's. Also, the two liver samples have potentially been mixed up. It is not crucial for the integrity of the data, but should be noted for the future. NGI claims HiFi data was done on a provided blood sample, while there is no such sample among the registered BioSamples. The HiFi data was likely generated from one of the two muscle samples, but which one cannot be determined with certainty. Again, for sake of metadata integrity the choice of used sample is here registered for future reference. See below:

  - SAMEA13166615 WHOLE ORGANISM (not used? Perhaps remaining voucher specimen after sampling, but no info in BioSample record) 
  - SAMEA13166616 MUSCLE (labeled pt 097 001 - probably used for HiFi) 
  - SAMEA13166617 LIVER (Used for RNA-seq) 
  - SAMEA13166618 SKIN (Used for RNA-seq)
  - SAMEA13166619 SPLEEN (Used for RNA-seq)
  - SAMEA13166620 MUSCLE (Used for RNA-seq)
  - SAMEA13166621 LUNG (Used for RNA-seq)
  - SAMEA13166622 HEART (Used for RNA-seq)
  - SAMEA13166623 PANCREAS (For RNA-seq, but not used) 
  - SAMEA13166624 LIVER (labeled P21406 - Probably used for Hi-C) 
  - SAMEA13166625 KIDNEY (Used for RNA-seq)

### Register study including locus tag

The study was registered following the agreed convention for ERGA pilot projects at NBIS, with the locus tag set to BUFVIR.

### Submitting Hi-C data

The data consisted of four fastq files (paired reads), for a total of ~500G. A menifest file was made:

```
STUDY PRJEB71764
SAMPLE SAMEA13166624
NAME ILLUMINA-HIC-aBufVir1-[1/2]
INSTRUMENT Illumina NovaSeq 6000
INSERT_SIZE 480
LIBRARY_SOURCE GENOMIC
LIBRARY_SELECTION RANDOM
LIBRARY_STRATEGY Hi-C
LIBRARY_CONSTRUCTION_PROTOCOL 'From a muscle tissue sample that was snap-frozen then ground into a powder, Hi-C libraries were preprared using Dovetail OmniC'
FASTQ [File 1.1/2.1]
FASTQ [File 1.2/2.2]
```
The data was submitted in two sets, files 1.1+1.2, and then files 2.1+2.2. Manifest was uploaded to the data direcotory at UPPMAX, and the files were valiated before being submitted using the commands:

```interactive -t 08:00:00 -A naiss2023-5-307```

```module load ascp```

```java -jar webin-cli-6.7.2.jar -ascp -context=reads -manifest=BUFVIR_manifest_Hi-C.txt -userName=[USER] -password=[PASSWORD] -[submit/-validate]```

Due to the file sizes and random drops in upload speed the files required three attemts over three dayes before being fully submitted, in spite of the 8h interactive session window.

### Submitting HiFi data

 * 7 .bam files
   * 6 files from run pt_097
   * 1 file from run pt_099
 * Manifest file for HiFi data, with names modified for each submission round:

```
STUDY PRJEB71764
SAMPLE SAMEA13166616
NAME PACBIO-HIFI-aBufVir1-[1-7]
INSTRUMENT Sequel IIe
INSERT_SIZE 18000
LIBRARY_SOURCE GENOMIC
LIBRARY_SELECTION SIZE FRACTIONATION
LIBRARY_STRATEGY WGS
LIBRARY_LAYOUT SINGLE
LIBRARY_CONSTRUCTION_PROTOCOL 'HiFi SMRTbell® Libraries using the SMRTbell Express Template Prep Kit 2.0'
BAM [Files 1.1-1.7]
```
The manifest was uploaded to the data directory at UPPMAX and data was first validated then submitted for each file, after modification of the manifest file.

Files were submitted using webin-cli 6.7.2 running the command with `-validate` before switching to `-submit`.

`java -jar webin-cli-6.7.2.jar -ascp -context=reads -manifest=BUFVIR_manifest_HiFi.txt -userName=[user] -password=[pwd] -[validate/submit]`

NOTE! The HiFi data files were very large (4x125G) and proved a challenge to submit in one go. Was divided into four separate submissions with one file each, and even then the uploads to ENA timed out for the intreactive sessions on Uppmax due to sudden drops in upload speed. Had to be retried several times over three days.

### Submitting Iso-Seq data

 * Consisted of a single .bam file
 * Manifest file for IsoSeq data:

 ```
 STUDY PRJEB71764
SAMPLE SAMEA13166616
NAME PACBIO-Isoseq-aBufVir1-1
INSTRUMENT Sequel IIe
INSERT_SIZE 18000
LIBRARY_SOURCE TRANSCRIPTOMIC
LIBRARY_SELECTION cDNA
LIBRARY_STRATEGY RNA-Seq
LIBRARY_CONSTRUCTION_PROTOCOL 'Library construction was done using SMRTbell prep kit'
BAM flnc.bam
 ```

Submission was done using webin-cli 6.7.2 using the command:

 `java -jar webin-cli-6.7.2.jar -ascp -context=reads -manifest=BUFVIR_manifest_Isoseq.txt -userName=[user] -password=[pwd] -[validate/submit]`

### Submitting RNA-Seq data

 * 8 BioSamples, of which 7 can be connected to tissue for RNA-seq.
   * Pancreas sample was not sequenced
 * Manifest template for RNA-seq data:

 ```
STUDY PRJEB71764
SAMPLE SAMEA131666[XX]
NAME ILLUMINA-RNA-[tissue type]-aBufVir1-1
INSTRUMENT Illumina NovaSeq 6000
INSERT_SIZE 160
LIBRARY_SOURCE 	TRANSCRIPTOMIC
LIBRARY_SELECTION RANDOM
LIBRARY_STRATEGY RNA-Seq
LIBRARY_CONSTRUCTION_PROTOCOL 'polyA capture protocol using Illumina Stranded mRNA Prep kit (manufacturers protocol). MagBio HighPrep PCR magnetic beads for library cleanup. RNA library denatured into two separate pools for paired-end sequencing using NovaSeq 6000 S1'
FASTQ BV_[index]_R1_001.fastq.gz
FASTQ BV_[index]_R2_001.fastq.gz 
 ``` 

Manifest and webin client was uplpoaded to Uppmax. Each pair of fastq files were checked against leballed tissue type and its corresponding BioSample accession number. Manifest file was adapted and webin-cli was run:

`java -jar webin-cli-6.7.2.jar -ascp -context=reads -manifest=BUFVIR_manifest_RNAseq.txt -userName=[UserID] -password=[pwd] -[validate/submit]`

### Submitting genome assembly

 * 1 .gff file
 * 1 genome.fa file

Contact with bioinformaticians and project coordinator to locate the correct files. Due to file size (.gff was 13G) the EMBLmyGFF was run on the nac-cluster instead of a laptop. Files were transferred from Uppmax to nac.

1. The file run_emblmygff3.sh was modified to:

```#!/bin/bash
#SBATCH -n 2
#SBATCH -t 5-00:00:00
#SBATCH -J EMBLmygff3

source /projects/martin/prog/bin/conda_init.sh
conda activate /home/asoares/.conda/envs/EMBLmyGFF3

EMBLmyGFF3 /home/steny/rc3_functional_ENAcompliant_27_11_23.gff /home/steny/genome.fa  --topology linear --molecule_type 'genomic DNA' --transl_table 1 --species 'Bufotes viridis' --locus_tag BUFVIR --project_id PRJEB71764 -o PRJEB71764_BUFVIR.embl
```
2. module load conda
3. conda activate /home/asoares/.conda/envs/EMBLmyGFF3
4. EMBLmyGFF --expose_translations
    * .json files were modified as in [here](https://github.com/NBISweden/data-submission-documentation/tree/main/ENA/5894-Geodia-assembly) or [here](https://github.com/NBISweden/data-submission-documentation/tree/main/ENA/ERGA-arctic-fox)
5. script was run with `sbatch run_emblmygff3.sh`

### Summary

A large submission with somewhat confused connection between data and samples. Time consuming.