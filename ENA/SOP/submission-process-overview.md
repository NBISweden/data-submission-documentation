# Process overview for raw data and assemblies/annotations submissions to ENA in the VR-EBP/ERGA/BGE biodiversity initiative

The SOP describes an overview of the entire process for publishing data at ENA in the VR-EBP/ERGA/BGE biodiversity projects where NBIS acts as broker for data submissions.

## Species assignment and data arrival at NBIS

Data arrives at NBIS via assignment of species. Physical biologic material is prepared by Principal Investigators (PI's) both nationally and internationally, and sent to the Swedish NGI facilities for sequencing. The NGI facility makes suitable library preparations followed by: 

- Short read genomic sequencing </br>
(e.g. Illumina Hi-C)
- Long read genomic sequencing <br/> (e.g. PacBio HiFi)
- Transcriptomic sequencing </br>
(e.g. PacBio Iso-seq, Illumina RNA-seq, Oxford Nanopore)

After sequencing the raw data is downloaded to a project folder at Uppmax, while the assembly and annotation work is done separately on the Annotation cluster. Raw data files are usually available to all involved on Uppmax, while anything related to annotation is available on the annotation cluster.

```
Note! For species in the "sharp" BGE initiative, all annotation will be made by the Ensembl annotation team. NBS will only be involved up to assembly.
```
There is no particular set time when data submission to ENA can begin. From the start of "sharp" BGE we could aim for data submissions as early as possible (<90 days, if desired).

## Submission process

### Assembling the necessary information

The information required by the Data Steward (DS) to initiate a data submission to ENA can be divided into four groups:

- Sample metadata
- Technical metadata
- Raw data file paths
- Assembly data file paths

But before data can be submitted at all there needs to be a study registered at ENA. The registration is done by the DS at NBIS and is described differently depending if it is VR-EBP, ERGA, or BGE.

- [Example for VR-EBP](https://github.com/NBISweden/data-submission-documentation/blob/SOP-Submission-process-overview/ENA/VR-EBP-Porodaedalea-granticka/README.md#L64)
- [Example for ERGA](https://github.com/NBISweden/data-submission-documentation/blob/4c738f7681d95cd301d0957506ee712303627f7f/ENA/ERGA-arctic-fox/README.md#L48)
- Example for BGE

#### Sample metadata

Data submissions to ENA requires sample metadata to be registered before raw data can be submitted.