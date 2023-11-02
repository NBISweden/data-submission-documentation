---
Redmine_issue: https://projects.nbis.se/issues/6159
Repository: https://www.ebi.ac.uk/biostudies/
Submission_type: <type> # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: https://www.ebi.ac.uk/biostudies/studies/S-BSST1185
---

# 6159 - Sharing SARS-CoV-2 variant analysis from Swedish wastewater samples

## Submission task description
During 2021 and 2022, SLU and KTH have done monitoring of SARS-CoV-2 levels and variants in wastewater from six Swedish cities. The sequences have been published in ENA, but the variant analysis and sequencing run reports need to be submitted to BioStudies.

## Procedure overview and links to examples

### Links
* [Samples sheet](https://docs.google.com/spreadsheets/d/1iwtpGGobkjkSiowS_QKM-5qo_PB_ngcVsIpUaoJ4TY8/) - overview of all sequenced samples and submitted data
* [file with PageTab info](https://www.ebi.ac.uk/biostudies/misc/SubmissionFormatV5a.pdf) - might be outdated
* [BioStudies - GitHub](https://github.com/EBIBioStudies/EBIBioStudies.github.io)
* [BioStudies-PageTab-Example](https://ebibiostudies.github.io/page-tab-specification/examples/AllInOneExample.html)
* [BioStudies-PageTab-Specification](https://ebibiostudies.github.io/page-tab-specification/specification/PageTabSpecification.html)
* [Submit help for BioImage Archive](https://www.ebi.ac.uk/bioimage-archive/submit/) - uses BioStudies
* [File List Guide](https://www.ebi.ac.uk/bioimage-archive/help-file-list/) - BioImage Archive but shows how to organise files for BioStudies in PageTab format
* [BioStudies database: aggregating all outputs of a life sciences study](https://www.ebi.ac.uk/training/events/biostudies-database-aggregating-all-outputs-life-sciences-study) - ENA training material
* [A guide to organising data associated to a publication using BioStudies](https://www.ebi.ac.uk/training/events/guide-organising-data-associated-publication-using-biostudies) - ENA training material

### Procedure
Everything was submitted via the web browser (using PI's account at BioStudies), but the description below will also cover how to do PageTab submission, where everything is written in a tsv file which is then uploaded to BioStudies (hence all the links concerning PageTab above).

## Lessons learned
* The information on how to submit using PageTab is not complete and is spread in different places
* Once you have a pagetab template, it is very easy to use
* Even if PageTab is used, do an initial submission of the study in the browser, then you can obtain a PageTab template to change in
* All information already submitted needs to be in the PageTab file, otherwise it will be removed (i.e. considered as an update, if field is missing it is interpreted as an instruction that it should be removed)
* It is quite easy to add any type of data files, as well as adding links to external sources, since very little metadata is required
* There is no test submission site, but as long as the release date is in the future, it is very easy to delete any test studies made 

## Detailed step by step description

* [Submit wastewater via browser](./instructions-submit-biostudies.md)
* [About submitting using PageTab](instructions-submit-pagetab.md)
