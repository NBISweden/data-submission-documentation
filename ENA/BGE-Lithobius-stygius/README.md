---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: 
---

# BGE - *Lithobius stygius*

## Submission task description
Submission of raw reads for *Lithobius stygius* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.
Submission will be (attempted) done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Lithobius-stygius-metadata.xlsx)
* [BGE HiFi metadata](./data/bge-hifi.tsv)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Collecting metadata
* I went to [BioSamples](https://www.ebi.ac.uk/biosamples/samples?text=Lithobius+stygius) and extracted all samples for this species, where SCILIFELAB was the GAL. I then looked at the delivery README for the HiFi dataset (on Uppmax) and extracted the Name (`FS42595405`). This I then pasted as filter in `Tube or well id` field, in the [ERGA tracking portal](https://genomes.cnag.cat/erga-stream/samples/) which returned biosample [SAMEA115117740](https://www.ebi.ac.uk/biosamples/samples/SAMEA115117740).

