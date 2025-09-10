---
Redmine_issue: https://projects.nbis.se/issues/8267
Repository: ENA
Submission_type: WGS # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI and Sistemas Genómicos S.L. (Valencia, Spain)
Top_level_acccession: PRJEB96741 
---

# 8267 - Submission of Lens culinaris sequence data 

## Submission task description
Raw reads from multiple samples of a single species (*Lens culinaris*) mainly in bam format to be submitted to ENA. Samples are ancient (~1000 years) taken from an archeological dig site on the Canary Islands.

## Procedure overview and links to examples

Collected information from researcher in a google spreadsheet and converted to tsv fles:

- [Study file](ENA/8267-Lens-culinaris/data/lens_study.tsv)
- [Samples](ENA/8267-Lens-culinaris/data/lens_samples.tsv)
- [Experiment](ENA/8267-Lens-culinaris/data/lens_exp.tsv)

## Detailed step by step description

1. Study submitted via ENA portal. Project accession number PRJEB96741.

2. Samples information filled by PI. Complementary information was addded to enrich sample metadata, exported from the Excel sheet to a tsv file, and uploaded in the ENA portal.

3. Experiment tab was filled in by PI and with additional information provided by Spanish lab staff. **Note!** Insert sizes were provided as numbers with a decimal, but ENA only accepts input as integers. The solution was to round the provided number to closest integer.

4. Relevant files identified on Dardel, renamed to match sample names, and transferred to ENA upload area using FileZilla (via local download) to avoid problems due to issues with Aspera. A set of md5 sums were calculated and added to the experiment tab before submission in the ENA portal. 

## Lessons learned
Considering the sequence data stems from archeological excavations, it would have been optimal with more information relating the samples to e.g. museum collections (if present). The entire submission was done in the ENA portal due to the limited number of files and samples. 