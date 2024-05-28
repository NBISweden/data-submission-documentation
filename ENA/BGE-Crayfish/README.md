---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: 
---

# BGE - *Austropotamobius torrentium* (Crayfish)
## Submission task description
Submission of raw reads for *Austropotamobius torrentium* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Austropotamobius-torrentium-metadata.xlsx)

## Lessons learned
* There's been some struggle regarding HiFi sequencing on this species, has been done in several rounds, resulting in 3 separate deliveries from NGI. There was some uncertanties on which datasets to submit.


## Detailed step by step description

### Collect metadata
* Looking at BioSamples, 20 samples in total are candidates, 10 are same as one of the other 10.
* Looking at the HiFi deliveries, in the README files (there are 3 of them), all refer to 2(!) samples, ERGA_DS_328X_04_(01+02) as UGC_user_id (UGC_id is pr_047_001). Which sample do we submit the datasets to? Need to ask NGI/UGC
    * Answer from NGI is to use [SAMEA112878228](https://www.ebi.ac.uk/biosamples/samples/SAMEA112878228)
* Looking at the HiC delivery, they only have 8 'internal' samples, no indication on which BioSample might have been used. Need to ask NGI/SNP&SEQ.
