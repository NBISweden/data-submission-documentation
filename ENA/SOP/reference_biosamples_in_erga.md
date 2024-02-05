# Reference BioSamples in ERGA projects

For ERGA associated projects all samples will already be registered in the [COPO](https://copo-project.org/) (**C**ollaborative **OP**en **O**mics) portal. The registered metadata will follow the [sample manifest](https://github.com/ERGA-consortium/ERGA-sample-manifest) established and updated by the ERGA consortium.

The person responsible for metadata registration, and updates of the records, is the PI of each project (species). In case the Data Stewards spots errors or inconsistencies in the metadata, the PI should be alerted. No changes or updates are to be made by the Data Steward! Also note that submitted metadata may be registered in an earlier version of the metadata template. 

Metadata records submitted to COPO will pass a validation check, and if ok, publish them and make them available for ENA.

`There is no easy way to search or extract metadata records directly from the COPO portal!`

Instead, all records can be searched and located in the [BioSamples portal](https://www.ebi.ac.uk/biosamples/docs) using e.g. the species name. It will list all samples matching the search string, and a manual sorting of the records have to be made (References in the records to Earlham institute will indicate ERGA associated species). Relevant records can be downloaded in .json format. The set of records will carry information on samples related to the entire or parts of the organism (e.g. Whole organism, liver, kidney, blood, etc.). The latter is of importance to RNA sequencing of separate organs)

All BioSamples accession numbers will begin with the prefix `SAMEA`, which is what is used in sequence submissions.

At ENA, when referencing BioSamples accession numbers in a submission, instead of registering samples online using a downloadable spreadsheet and getting accession numbers, the reference is made directly to the SAMEA samples at BioSamples.

```
Note! It is very important to reference the correct BioSample in the ENA manifest. Make sure to double check before submitting! There is no easy way to correct an incorrect reference.
```
At submission ENA will reference the provided BioSample, but it will not be visible under the Samples tab in the ENA portal.