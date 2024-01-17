---
Redmine_issue: https://projects.nbis.se/issues/6717
Repository: ENA
Submission_type: ERGA, HiFi, HiC, assembly, annotation # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB71153
---

# ERGA Vulpes lagopus (arctic fox)

## Submission task description
Submit genomic and assembly data for the arctic fox, Vulpes lagopus, as part of the ERGA pilot project. The sample metadata has already been submitted via COPO.

## Procedure overview and links to examples

### Links
* [Metadata template](/data/ERGA-Vulpes-lagopus-metadata.xlsx)
* [Biosamples query](https://www.ebi.ac.uk/biosamples/samples?text=Vulpes+lagopus&filter=attr:project+name:ERGA) gave 2 ids: [SAMEA12927189](https://www.ebi.ac.uk/biosamples/samples/SAMEA12927189) and [SAMEA12927190](https://www.ebi.ac.uk/biosamples/samples/SAMEA12927190)
* Notes on how to [Create EMBL file](https://github.com/NBISweden/annotation-cluster/wiki/ENA-submission#create-embl-file)
* [ENA WebFeat](https://www.ebi.ac.uk/ena/WebFeat/) - lookup for embl format features

### Steps
1. Collect metadata
    * Create a metadata template and fill in pre-knowledge based on previous projects such as [Stylops ater](https://github.com/YvonneKallberg/5440-ERGA-stylops) and [Parnassius mnemosynes](https://github.com/NBISweden/data-submission-documentation/tree/main/ENA/ERGA-Parnassius)
    * Query BioSamples for sample candidates, then ask PI which sample(s) has been sequenced
    * Ask NBIS bioinformatician where raw data and assembly files are, and to fill the assembly metadata
    * Ask NGI to fill the experiment metadata for HiC and HiFi
1. Register study including locus tag
1. Submit experiments using manifests
1. Create EMBL file for assembly
1. Submit assembly using manifest

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->
* Finding which samples have been sequenced is difficult, BioSamples is not the easiest interface to search in
* Note on RUN_REFS in assembly manifest file: It is not accepted to write a span of accession numbers (i.e. ERRXXX1-ERRXXX9), all numbers needs to be explicitly written
* tRNAScan-SE (used in some annotation pipelines) produces anticodons in a format not accepted by ENA. Only solution at the moment is to not include tRNA in gff file (see more further down on [validation errors](./README.md/#validation-errors))

## Detailed step by step description
### Collect metadata

* [Metadata template](https://docs.google.com/spreadsheets/d/1RPtxpa62pWYfimf6JAPuKZVCjet2ixlR/)
* [Biosamples query](https://www.ebi.ac.uk/biosamples/samples?text=Vulpes+lagopus&filter=attr:project+name:ERGA) gave 2 ids: [SAMEA12927189](https://www.ebi.ac.uk/biosamples/samples/SAMEA12927189) and [SAMEA12927190](https://www.ebi.ac.uk/biosamples/samples/SAMEA12927190)

* PI has taken over this project from someone else, and had not been the person who registered the sample to BioSample, but could confirm that it was the muscle sample (SAMEA12927190) that had been used for sequencing.

### Register study including locus tag

* The decided naming convention for locus tags (three first characters in each of the binominal name) results in `VULLAG`

* Title and abstract is based on previous submissions for ERGA pilot projects:
    * Name: `VulLag1`
    * Title: `Vulpes lagopus (arctic fox) genomic and assembly data, ERGA pilot`
    * Abstract: `This project collects genomic data generated for Vulpes lagopus, the arctic fox, to facilitate assembly and annotation as part of the ERGA pilot (https://www.erga-biodiversity.eu/pilot-project).`
    * Release date: `2025-12-14`

* Received accession number: `PRJEB71153`

### Submit experiments using manifests

* [HiC manifest](/data/PRJEB71153-HiC-manifest.txt)
* [HiFi manifest 1](/data/PRJEB71153-HiFi-mVulLag1-1-manifest.txt)
* [HiFi manifest 2](/data/PRJEB71153-HiFi-mVulLag1-2-manifest.txt)
* [HiFi manifest 3](/data/PRJEB71153-HiFi-mVulLag1-3-manifest.txt)

* When completed, the manifests were copied to Uppmax, where the actual submission took place, calling the script [webin-cli](/scripts/webin-cli-args.sh):

```
  interactive -t 08:00:00 -A naiss2023-5-307
  module load ascp
  java -jar ../webin-cli-6.5.0.jar -ascp -context reads -userName $1 -password $2 -manifest $3 -outputDir Webin_output/ -submit
```

* Received accession numbers:
    * HiC - `ERX11800015`, `ERR12423593`
    * HiFi 1 - `ERX11757893`, `ERR12381328`
    * HiFi 2 - `ERX11757895`, `ERR12381330`
    * HiFi 3 - `ERX11757896`, `ERR12381331`

### Create EMBL file for assembly

* I didn't see any annotation on the CDS level in the gff (final_annotation.gff), only on mRNA level. I contacted the responsible bioinformatician who realized that they had given me the wrong gff file. A new file, with annotation on CDS level was created ENA_compatible_final_annotation.gff

* I copied the gff3 and fasta file to my local computer, and updated [attribute](/data/translation_gff_attribute_to_embl_qualifier.json) and [feature](/data/translation_gff_feature_to_embl_feature.json) json files as recommended in [Create EMBL file](https://github.com/NBISweden/annotation-cluster/wiki/ENA-submission#create-embl-file):
    ```
    conda activate py38
    EMBLmyGFF3 --expose_translations
    ```
    Add to file `translation_gff_attribute_to_embl_qualifier.json` the following modification:
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
    Add to file `translation_gff_feature_to_embl_feature.json` the following modification:
    ```
    "exon": {
    "remove": true
    }   
    ```

* Then I tried running EMBLmyGFF3: 

    ```
    conda activate py38
    EMBLmyGFF3 ENA_compatible_final_annotation.gff mVulLag1.prim.ipa.hic.20231213.fasta --topology linear --molecule_type 'genomic DNA' --transl_table 1 --species "Vulpes lagopus" --locus_tag VULLAG --project_id PRJEB71153 -o PRJEB71153-VulLag.embl
    gzip PRJEB71153-VulLag.embl
    ```

* Ran into memory issues, the process was killed. I tried to increase the amount of memory for WSL to use to 32GB in C:/<user>/.wslconfig 
* Ran the command "wsl --shutdown" then "restart-service LxssManager" in PowerShell running as administrator
* Still the EMBLmyGFF3 is killed. I even tried doing a restart and not opening anything else but the Ubuntu app, to no avail. Asked a bioinformatician who suggested to run on the annotation cluster, since conda enviroment is already installed.
* Turned out that the environment didn't work, so in the end a bioinformatician created a new one, and they also created the embl flat file, but below are the steps needed:

    ```
    ssh -A yvonnek@nac-login.nbis.se
    source /projects/martin/prog/bin/conda_init.sh
    conda activate /home/asoares/.conda/envs/EMBLmyGFF3
    EMBLmyGFF3 --expose_translations
    ```
  * Update the attribute and feature json files as described above, and then run the EMBLmyGFF3 command as is or, (run via a shell script [run_emblmygff3.sh](/scripts/run_emblmygff3.sh) by typing `sbatch run_emblmygff3.sh`):

    ```
    EMBLmyGFF3 /projects/annotation/arctic_fox/Delivery/gff/ENA_compatible_final_annotation.gff /projects/annotation/arctic_fox/Delivery/fasta/genome.fa --topology linear --molecule_type 'genomic DNA' --transl_table 1 --species "Vulpes lagopus" --locus_tag VULLAG --project_id PRJEB71153 -o PRJEB71153-VulLag.embl
    ```

* **Note:** It has been confirmed by a data steward colleague that updated json files are included also when using sbatch/script, whish was a bit uncertain to begin with.

### Validate assembly using manifest

* External RNA sequencing data was used for annotation, and reference to these were added to the run_ref section of the manifest.
* The [manifest](/data/PRJEB71153-assembly-manifest.txt) used

* Note on RUN_REFS: It was not accepted to write a span of accession numbers (i.e. ERRXXX1-ERRXXX9), all numbers needs to be explicitly written

```
java -jar ../../../Downloads/webin-cli-6.5.0.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./PRJEB71153-assembly-manifest.txt -validate
```

#### Validation errors

I got a lot if errors concerning `anticodon`

Example from validation report file:
```
ERROR: Invalid anticodon qualifier value: NNN.
...
ERROR: Feature qualifier "anticodon" value "NNN" is invalid. Refer to the feature documentation or ask a curator for guidance." [ line: 24240 of PRJEB71153-VulLag.embl.gz]
```

In gff file:
```
HiC_scaffold_1  tRNAscan-SE     gene    970247  970304  16.6    -       .       ID=nbisL1-trna-1;Name=HiC_scaffold_1.tRNA12-SerNNN;anticodon=NNN;gene_biotype=tRNA;isotype=Ser
HiC_scaffold_1  tRNAscan-SE     tRNA    970247  970304  16.6    -       .       ID=HiC_scaffold_1.trna12;Parent=nbisL1-trna-1;Name=HiC_scaffold_1.tRNA12-SerNNN;anticodon=NNN;gene_biotype=tRNA;isotype=Ser
HiC_scaffold_1  tRNAscan-SE     exon    970247  970304  .       -       .       ID=HiC_scaffold_1.trna12.exon1;Parent=HiC_scaffold_1.trna12
```
In embl file:
```
FT   tRNA            complement(970247..970304)
FT                   /anticodon="NNN"
FT                   /locus_tag="VULLAG_LOCUS18"
FT                   /note="ID:HiC_scaffold_1.trna12"
FT                   /note="source:tRNAscan-SE"
FT                   /standard_name="HiC_scaffold_1.tRNA12-SerNNN"
```

[WebFeat on anticodon](https://www.ebi.ac.uk/ena/WebFeat/qualifiers/anticodon.html) at ENA says:

```
Definition	
location of the anticodon of tRNA and the amino acid for which it codes

Value Format	
(pos:<location>,aa:<amino_acid>,seq:<text>) 
where location is the position of the anticodon and amino_acid is the abbreviation for the amino acid encoded and seq is the sequence of the anticodon

Example	
/anticodon=(pos:34..36,aa:Phe,seq:aaa)
/anticodon=(pos:join(5,495..496),aa:Leu,seq:taa)
/anticodon=(pos:complement(4156..4158),aa:Gln,seq:ttg)
```

A possible fix would be to not include tRNA, only mRNA. Bioinformatician removed this from gff file and re-run the EMBLmyGFF3 script.

### Submit assembly using manifest

* The new embl file, without the tRNA parts, was copied to my local computer, successfully validated without any errors. Hence, the assembly was submitted:

    ```
    java -jar ../../../Downloads/webin-cli-6.5.0.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./PRJEB71153-assembly-manifest.txt -submit
    ```

* Recieved accession number: `ERZ22276713`