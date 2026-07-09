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

The assembly for *Parnassius mnemosyne* was downloaded locally to laptop and converted to EMBL flatfile using the EMBLmyGFF3 script.

The flatfile was constructed using the provided GFF (pmne_functional_edit1.gff) together with a scaffolded fasta (pmnemosyne_scaffolds.fa) running the following command line: 

```
EMBLmyGFF3 -i PARMNEM -p PRJEB67749 -r 1 -s 'Parnassius mnemosyne' -t linear -m 'genomic DNA' pmne_functional_edit1.gff pmnemosyne_scaffolds.fa -o PARMNEM_for_ENA.embl
```

After successful conversion a manifest file was made:

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

After contact with the bioinformatician who produced the .gff the overlappping issue was fixed (unknown exactly how), a new EMBL flatfile was constructed as described above, and the assembly passed validation. The assembly was then finally submitted using the commmand:

```
java -jar webin-cli-6.7.1.jar -ascp -context=genome -manifest=PARMNEM_manifest.txt -userName=[username] -password=[password] -submit
```

# 8. Mitochondrial assembly submission to ENA

The mito assembly was finished later than the nuclear assembly, and had to be submitted separately.

- The correct mito assembly was identified by the Bioinformatician with path to Rackham.

- A zipped .embl file was prepared using the correct .gff and the mito fasta file. 

- As required, a mito chromosome list was prepared as a .txt file containing tab separated values:

  ```ptg000351l_1_rc_rotated	MIT	linear-chromosome	Mitochondrion```

- A new project was registered at ENA (PRJEB76267) for the mito assembly described as:

  - Name: mito-ParMnem1
  - Title: Parnassius mnemosyne mitochondrial assembly
  - Description: This project provides the mitochondrial assembly data for Parnassius mnemosyne. 

- A manifest file was prepared:

  ```
  STUDY           PRJEB76267
  SAMPLE          SAMEA13166629
  ASSEMBLYNAME    Parnassius_mnemosyne_mito_2024_06
  ASSEMBLY_TYPE   isolate
  COVERAGE        30
  PROGRAM         MitoHiFi, MitoFinder
  PLATFORM        PacBio HiFi, Illumina Hi-C
  MOLECULETYPE    genomic DNA
  DESCRIPTION     The mitochondrial genome was recovered from the primary assembly after haplotig removal using MitoHiFi [10] v2.2. MtDNA was annotated using MitoFinder [11] v1.4.1 and reoriented to start at tRNA-Met to match Parnassius apollo (Acession: NC_024727.1)
  RUN_REF        	ERR12146337, ERR12148427, ERR12148429
  FASTA	      	pmnemosyne_mtdna.fasta.gz
  CHROMOSOME_LIST mito-chromosome_list.txt.gz

- Assembly was submitted to ENA using Webin-CLI with command line:

```
java -jar webin-cli-7.1.1.jar -ascp -context=genome -manifest=Parmnem_mito_manifest.txt -userName=Webin-XXXXX -password=[password] -validate
```
## Note 2026-06: Annotated mito assembly
* It was noticed that although there exists an annotated mito assembly, only the .fasta file with the assembly was submitted.
* The earlier attempt at creating an .embl flat file was not quite successful, no locus tag had been registered (instead the one registered for the whole genome had been used), and indexing (<TAG>_LOCUS1, <TAG>_LOCUS2, etc) didn't increase correctly, as there were several indexes within the same gene feature. This likely is due to the .gff file having more features than the EMBLmyGFF3 knows how to handle.

### Solution
1. Register a locus tag with the mito project: `PARMNEMMT`
1. Compare preparation steps taken from a similar project (Palm tree submission), and update what is needed accordingly
1. Select correct translational table, see <https://www.ncbi.nlm.nih.gov/Taxonomy/taxonomyhome.html/index.cgi?chapter=cgencodes>
1. Add `--organelle mitochondrion`
1. Create a chromosome_list.txt with the following line: `ptg000351l_1_rc_rotated	MIT Circular-Chromosome Mitochondrion`
1. Validate and submit a new version

Initial attempt at creating an embl flatfile:
  ```
  EMBLmyGFF3 pmnemosyne_mtdna.gff pmnemosyne_mtdna.fasta --topology circular --molecule_type 'genomic DNA' --organelle mitochondrion --transl_table 5 --species "Parnassius mnemosyne" --locus_tag PARMNEMMT --project_id PRJEB76267 -o pmnemosyne_mtdna_2026-06.embl
  ```
Output:
  ```
  09:31:02 WARNING feature: The qualifier >mol_type< is mandatory for the feature >source<. We will not report the feature.
  09:31:02 WARNING feature: The qualifier >organism< is mandatory for the feature >source<. We will not report the feature.
  09:31:02 WARNING EMBLmyGFF3: Sequence id <ptg000351l_1_rc_rotated mitofinder> from the gff file not found within the fasta file. Are you sure to provide the correct fasta file? The tool will create a string of ???? as sequence (its length will be the end position of the last feature). For you information, if you use the --translate option the tool will raise an error due to ??? codons that do not exist.
  09:31:02 WARNING EMBLmyGFF3: Sequence <unknown name> too short (1 bp)! Minimum accpeted by ENA is 100, we skip it !
  ```
* pmnemosyne_mtdna_edit.gff:
  * removed the first source line
  * last row didn't have a tab but space btw identifier and `mitofinder`
  * added `##gff-version 3` on first line
* pmnemosyne_mtdna_edit.fasta:
  * divided the sequence into 70 character long lines (was all on one line)
* Column 8: “phase” The phase of the CDS feature, which is related to /codon_start in the flatfile specification. The phase is computed based on the known phase at the start of the CDS and computed for subsequent CDS rows. It may not be accurate if the CDS contains internal frameshifts, which can occur in pseudogenes and in genomes with indels, assembly gaps, and other errors. The phase is one of the integers 0, 1, or 2, indicating the number of bases that should be removed from the beginning of this CDS feature to reach the first base of the next codon. If the feature is not a CDS, this field should be set to “.”.
  * Hence, for all rows not being a CDS I will change from `0` to `.`

* Still an issue that locus tag indexes is increased within genes...
  * I have no idea why, I can understand if it is in gene + tRNA pairs, but it is also on gene + CDS pairs, and these should (have earlier) work
  * I really don't want to manually edit the embl file, even if doable since not so many genes
  * I asked Gemini, who explained 
    ```
    The 9th column (attributes) only contains Name=.... Because there are no ID and Parent attributes linking them together, EMBLmyGFF3 has no way of knowing that the tRNA belongs to that specific gene. It treats them as two completely independent entities and increments the locus tag for each.

    Example:
    ptg000351l_1_rc_rotated mitofinder gene 1 69 . + . ID=gene_tRNA_Met;Name=tRNA-Met gene
    ptg000351l_1_rc_rotated mitofinder tRNA 1 69 . + . ID=tRNA_Met;Parent=gene_tRNA_Met;Name=tRNA-Met
    ```
  * I asked Gemini to fix the file (pmnemosyne_mtdna_edit_gemini.gff)
    ```
    What changed?
    * Formatting Fixes: Your raw file had line-break anomalies (e.g., splitting strands like + or - to the start of a new line), which I have safely stitched back into proper 9-column formatting.  
    * Added IDs to Genes: ID=gene_<Name>;.  Linked Child Features: ID=<Feature>_<Name>;Parent=gene_<Name>;.  
    * D-loop preserved: Kept D-loop at the end as its own independent component since it doesn't fall under a functional gene class. 
    ``` 

* D-loop ended up as first locus tag (index 1) which I don't want, so I asked Gemini for solution. The answer is that I can either wrap it up as a pseudogene or add the desired locus tag explicitly (change last row to `ptg000351l_1_rc_rotated	mitofinder	D-loop	14964	15425	.	+	0	Name=D-loop;locus_tag=PARMNEMMT_LOCUS38`). I decided to go with the first alternative:
  ```
  ptg000351l_1_rc_rotated	mitofinder	gene	14964	15425	.	+	0	ID=gene_D-loop;Name=D-loop region
  ptg000351l_1_rc_rotated	mitofinder	D-loop	14964	15425	.	+	0	ID=D-loop;Parent=gene_D-loop;Name=D-loop
  ```
* I realised that I hadn't given Gemini the correct input file, with the phase set to '.' if not a CDS row. I asked Gemini to fix this, including also the removal of source line, and the pseudogene wrapping of the D-loop, output file: pmnemosyne_mtdna_toENA.gff
* Flatfile:
  ```
  EMBLmyGFF3 pmnemosyne_mtdna_toENA.gff pmnemosyne_mtdna.fasta --topology circular --molecule_type 'genomic DNA' --organelle mitochondrion --transl_table 5 --species "Parnassius mnemosyne" --locus_tag PARMNEMMT --project_id PRJEB76267 -o pmnemosyne_mtdna_2026-06.embl
  ```
  * Note that I did not use the .fasta file where I had shortened the lines, it worked anyway without any warnings.

#### Validation & submission

```
conda deactivate
java -jar ../../../../../Downloads/webin-cli-9.0.3.jar -context=genome -manifest=pmnemosyne_mtdna-manifest.txt -userName=[username] -password=[password] -validate
```
* Receipt:
  ```
  INFO : Your application version is 9.0.3
  INFO : Connecting to FTP server : webin2.ebi.ac.uk
  INFO : Creating report file: /mnt/c/Users/yvonne.kallberg/GitHub/data-submission-documentation/ENA/ERGA-Parnassius/data/./webin-cli.report
  INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/GitHub/data-submission-documentation/ENA/ERGA-Parnassius/data/pmnemosyne_mtdna_2026-06.embl.gz
  INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/GitHub/data-submission-documentation/ENA/ERGA-Parnassius/data/chromosome_list.txt.gz
  INFO : Files have been uploaded to webin2.ebi.ac.uk.
  INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ29716571
  ```
* Accession:
  ```
  ASSEMBLY_NAME                       | ASSEMBLY_ACC | STUDY_ID   | SAMPLE_ID   | CONTIG_ACC | SCAFFOLD_ACC | CHROMOSOME_ACC
  Parnassius_mnemosyne_mito_2024_06.2 | ERZ29716571  | PRJEB76267 | ERS10770208 |            |              | OZ075093-OZ075093
  ```

# Umbrella
- An umbrella was submitted via xml...

```
<PROJECT_SET xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <PROJECT center_name="" alias="all-PARMNEM">
        <TITLE>Parnassius mnemosyne umbrella project</TITLE>
        <DESCRIPTION>This project connects the sequenced raw data and genome assembly of Parnassius mnemosyne, with its corresponding mitochondrial assembly</DESCRIPTION>
        <UMBRELLA_PROJECT/>
        <RELATED_PROJECTS>
          <RELATED_PROJECT>
            <CHILD_PROJECT accession="PRJEB67749"/>
          </RELATED_PROJECT>
          <RELATED_PROJECT>
            <CHILD_PROJECT accession="PRJEB76267"/>
          </RELATED_PROJECT>
        </RELATED_PROJECTS>
    </PROJECT>
</PROJECT_SET>
```
- ... togehter with a submission xml with a defined release date: 

```
<SUBMISSION>
   <ACTIONS>
      <ACTION>
         <ADD/>
      </ACTION>
      <ACTION>
         <HOLD HoldUntilDate="2024-06-13"/>
      </ACTION>
   </ACTIONS>
</SUBMISSION>
```

- A receipt for the submission was printed:

```
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
<RECEIPT receiptDate="2024-06-03T15:16:23.420+01:00" submissionFile="submission.xml" success="true">
     <PROJECT accession="PRJEB76269" alias="all-PARMNEM" status="PRIVATE" holdUntilDate="2024-06-13+01:00"/>
     <SUBMISSION accession="ERA30577384" alias="SUBMISSION-03-06-2024-15:16:23:180"/>
     <MESSAGES>
          <INFO>All objects in this submission are set to private status (HOLD).</INFO>
     </MESSAGES>
     <ACTIONS>ADD</ACTIONS>
     <ACTIONS>HOLD</ACTIONS>
</RECEIPT>
```                           

# 9. Post-submission mop-up

After submission of the assemblies the project was considered complete. Accession numbers were gathered and sent to the PI via email, and the assembly team was informed.

# 10. Lessons learned, plus take-aways

The first take-away lesson was that the responsibility for COPO metadata quality and submission is on the PI and no-one else. The DM-staff will only accept the COPO-submitted metadata *as is*. Any updates should be made by the PI, not the DM staff. It seems as if the content of the manifest is updated, but the manifest itself is of a more recent version than the already submitted one, COPO does not produce an update of the present record, but duplicates it. If this happens COPO needs to be contacted to manually remove the auto-generated record at ENA.

It also seems like the curation of COPO submissions are limited to a validation tool Boolean outcome. Anything passing validation will be automatically submitted to ENA with automatic creation of records. It was also possible to make duplicate submission in COPO since the progress bar associated with the submit button was active in the background, leaving the submit button open for re-clicks.

For the assembly a lesson learned was the process of finding out the location and name of duplicate and/or overlapping exons/genes so the Bioinformatician can make adjustments to the .gff. 