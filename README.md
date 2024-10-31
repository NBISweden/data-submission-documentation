# data-submission-documentation
Documentation for data submissions from life science research in public repositories.

* [How to](#how-to-add-documentation-for-a-new-submission-project)
* [Repository examples](#data-publication--a-quick-guide-and-good-examples-and-experiences-for-the-most-common-repositories) 

## How to add documentation for a new submission project

1. Create a new branch, e.g. based on the Redmine project issue number
   * Note, this can be done either remotely or locally, whereupon you either open it locally or publish remotely, respectively
3. Copy the [projectID-title-template](./projectID-title-template) under the repository which the submission concerns, rename it as follows:
   * If **ENA** submission: Redmine project issue number followed by the submission type, and last the Redmine title (title can be shortened if it is long), separate with dash (projectID-submissionType-title)  
      * Regarding the submission type, this is in order to highlight what is special with the submission, like a tag, so that it is easy just by looking at the folder names to find the type of submission you are looking for. Select from the following list, or add to this list if the type is not in list yet:
         * metagenome
         * metatranscriptome
         * assembly
         * RNAseq
   * If **not** ENA: skip the submissionType, i.e. Redmine project issue number followed by the Redmine title (title can be shortened if it is long), separate with dash (projectID-title)
5. Use the README file as the main documentation file, and add images, scripts or data in their respective folders
6. Make a pull request and ask for review by one of your colleagues
7. The reviewer checks that the documentation makes sense and that there is no sensitive data included (e.g. passwords in scripts, see further below on what *not* to include), approves and merge. 

## What to exclude in documentation   <!-- could be phrased better -->

* Big data files
* Names of people involved, use roles such as PI / Researcher / Data Steward / Bioinformatician
* Folder paths to where the data resides, use placeholders or variables

</br>
</br>


# Data publication – A quick guide, and good examples and experiences for the most common repositories

Below are listed some good example data submissions to the seven most commonly encountered repositories. Additionally, for each repository, a general description is provided which serves as a quick guide, with  eventual experiences from depositing data in the repository.


* [ArrayExpress](#arrayexpress)
* [BioSamples](#biosamples)
* [BioStudies](#biostudies)
* [EGA / FEGA Sweden](#ega--fega-sweden)
* [ENA](#ena)
* [EVA](#eva)
* [SciLifeLab FigShare](#scilifelab-figshare)


## ArrayExpress
### General information

Accepts functional genomics data generated from microarray or next-generation sequencing (NGS) platforms.
Common experiment types: Transcription profiling, SNP genotyping, chromatin immunoprecipitation, comparative genomic hybridization.
Metadata: Experiment description (free text), protocols for experiments and data analyses, sample annotations, author information, sequencing library specification (NGS submissions only).
Data: Raw data (unprocessed data files), processed data.

### Examples

https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-10202 </br>
(good example of an RNA-seq cell line study, rich metadata) RNA-seq of total RNA; *Mus musculus* hippocampus; 12 samples; 2 MAGE-TAB files attached

https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-12545 </br>
(good RNA-seq example) RNA-seq of total RNA; *Mus musculus*; 42 samples;  2 MAGE-TAB files attached

https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-12492 </br>
(good RNA-seq example) RNA-seq of coding RNA; *Homo sapiens* fetal adrenal gland; 46 samples; 2 MAGE-TAB files attached

https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-11745 </br>
(NBIS Support) RNA-seq of coding RNA; *Pacifastacus leniusculus* hematopoietic tissue and hemocytes; 2 samples; 2 MAGE-TAB files attached

### Experiences

[None listed]

</br>

## BioSamples
### General information

Accepts descriptions and metadata about biological samples (either reference samples or samples used in an assay database) used in research and development.
Sample metadata is uploaded in ISA-Tab format.

### Examples

https://www.ebi.ac.uk/biosamples/samples/SAMEA6507890 </br>
(good covid example, rich metadata) Covid complete genome; link to ENA record

https://www.ebi.ac.uk/biosamples/samples/SAMEA2031950 </br>
(good metagenome example) Human gut metagenome; link to ENA record

https://www.ebi.ac.uk/biosamples/samples/SAMEA112672613 </br>
(NBIS Support, wastewater metagenome, Wolmar via ENA) Wastewater metagenome; Covid

### Experiences

[None listed]

</br>

## BioStudies
### General information

Accepts descriptions of biological studies and links to data from these studies in other databases.
Supplementary information of a manuscript can be added and be linked to it from the publication.
Metadata: Submitter contact details, information about the study.
Data: Raw and/or processed data in a free format.

### Examples

https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-10539?accession=E-MTAB-10539 </br>
(extensive example of an RNA-seq stem cell study) RNA seq of coding RNA; *Homo sapiens* embryonic stem cells; 36 samples; 36 BAM-files and 2 MAGE-TAB files attached

https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-10477?accession=E-MTAB-10477 </br>
(extensive example of an RNA-seq human breast cancer cell line study) RNA-seq of total RNA; *Homo sapiens* breast cancer cell line; 12 samples; 24 BAM files and 2 MAGE-TAB files attached

### Experiences

[None listed]

</br>

## EGA / FEGA Sweden

### General information

Accepts personally identifiable genetic, phenotypic and clinical data that is sensitive, i.e. subject to restricted access.
Data types: Sequence, Array, Phenotype, Metagenomics.
A Data Access Committee (DAC) makes a decision on every data access request. 
A Data Access Agreement (Policy) states the terms and conditions for accessing a dataset.
Important to check if the ethical permit allows data sharing, i.e. if the research subjects have consented to it.
Metadata for a Sequence submission: Study, Samples, Experiments, Runs, Dataset, Analysis, Policy, DAC.
Data for a Sequence submission: Raw reads, Analyses.
Metadata for an Array submission: Study, Samples, Array packets, Dataset, Policy, DAC.
Data for an Array submission: Array data files.
Metadata for a Phenotype submission: Study, Samples, Analysis, Dataset, Policy, DAC.
Data for a Phenotype submission: Aligned/Mapped Sequence Reads.

### Examples

[None listed]

### Experiences

[None listed]

</br>

## ENA
### General information

Accepts records of nucleotide sequencing information covering raw sequencing data, sequence assembly information and functional annotation.
Not for sensitive data that is subject to restricted access (consider EGA/FEGA instead).
Metadata: Study (groups together submitted files, controls release date), Sample (information about sequenced source material), Experiment (information about sequencing experiment), Run (refers to data files containing sequence reads), Analysis (secondary analysis results), Submission (submission actions).
Data: Raw Reads (linked to Run and Experiment), Data Analyses (linked to Analyses).

### Examples

https://www.ebi.ac.uk/ena/browser/view/PRJNA926984 </br>
(good example of an RNA-seq project, rich metadata) Project containing 9 Studies; *Aspergillus fumigatus* grown in liquid culture; RNA-seq; 9 FASTQ-files attached

https://www.ebi.ac.uk/ena/browser/view/GCA_000004845.1 </br>
(good human genome assembly example) WGS; Blood sample from *Homo sapiens*; EMBL and FASTA-format

https://www.ebi.ac.uk/ena/browser/view/PRJEB60156 </br>
(NBIS Support, wastewater metagenome) Project; Monitoring Covid in wastewater

### Experiences

https://github.com/NBISweden/data-submission-documentation/blob/main/ENA/5894-Geodia-assembly/README.md </br>
(NBIS Support, marine sponge data)

Genome assembly: https://scilifelab.atlassian.net/wiki/spaces/NBISDM/pages/1571520528/ENA+genome+assembly+submission and https://github.com/YvonneKallberg/ENA-genome-assembly-submission </br>
(the same project and the github version is most likely the better, ask for access since private) 

</br>


## EVA
### General information

Accepts all types of genetic variation data from all species.
Metadata: samples, analyses.
Data: sample genotypes and/or allele frequencies in VCF. The reference sequence, for example an assembly, a transcriptome/transcript or a gene sequence, is either INSDC registered or can be specified at the point of submission.

### Examples

https://www.ebi.ac.uk/ena/browser/view/PRJEB59363 </br>
(good plant biology example) Project containing 10 Studies; *Nicotiana tabacum* L.; Genetic basis of agronomic traits; Sequence variation; 10 VCF-files attached

https://www.ebi.ac.uk/ena/browser/view/PRJEB14018 </br>
(good human cancer cell line study) Project containing 9 Studies; 8 Esophageal adenocarcinoma cell lines; Paired end WGS; single-nucleotide variants; Indels; Copy number variations; 18 FASTQ and 9 BAM-files attached

### Experiences

[None listed]

</br>

## SciLifeLab FigShare
### General information

Accepts any kind of research-related data, for example documents, figures and presentations.
Possibility to deposit data that is under restricted access and to publish Collections (items brought together under a common theme).
Prepare a Readme file (with the same information as the Metadata file plus DOI) and a Manifest file (contains a list of files included in the submission).
Prepare metadata using a special template.

### Examples

https://figshare.scilifelab.se/articles/dataset/Data_from_Breast_cancer_patient-derived_whole-tumor_cell_culture_model_for_efficient_drug_profiling_and_treatment_response_prediction/21516993 </br>
(detailed description of a cancer dataset, restricted access) Breast cancer patient samples; Whole-genome sequencing; RNA-seq; NanoString nCounter BC360 panel; Cell viability assay; Restricted access

https://figshare.scilifelab.se/articles/dataset/DNA_methylation_signatures_predict_cytogenetic_subtype_and_outcome_in_pediatric_acute_myeloid_leukemia_AML_/14666127 </br>(cancer study) Pediatric acute myeloid leukemia samples; DNA methylation signatures

### Experiences

[None listed]