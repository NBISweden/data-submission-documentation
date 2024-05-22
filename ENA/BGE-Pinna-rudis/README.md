---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: HiFi, Hi-C, RNAseq, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB75035
---

# BGE - *Pinna rudis*

## Submission task description
Submission of raw reads for *Pinna rudis* to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). HiFi, Hi-C and RNAseq datasets will be produced and submitted. There will also be an assembly to be submitted. For BGE projects there will be no annotation done, instead this will be handled by Ensembl. The sample used for sequencing has already been submitted via COPO.

## Procedure overview and links to examples

* [Metadata template](./data/BGE-Pinna-rudis-metadata.xlsx)
* [BGE metadata template](https://docs.google.com/spreadsheets/d/1zd7DLNkX5F-z_4KIQ4u4LvSu6UaRXbYG/)
* [ERGA-BGE_ReadData_Submission_Guide](https://github.com/ERGA-consortium/ERGA-submission/blob/main/BGE/ERGA-BGE_ReadData_Submission_Guide.md)
* [CNAG ERGA repo](https://github.com/cnag-aat/ERGA-Status/) - with scripts among other things
* [BGE mRupRup umbrella project](https://www.ncbi.nlm.nih.gov/bioproject/1084634)
* [Meeting CNAG notes](https://docs.google.com/document/d/1YjD7BoSPbPnI3lTSGztj0CXcHZJRVAQ4F2Nuwd5x9iE/)

## Lessons learned
* There was some struggle to identify which COPO registered biosample number to use, there had been a mistake when uploading to NGI so the sample was labelled with a specimen id for another species.

## Detailed step by step description

### Collect metadata
* After some struggle biosample [SAMEA112748815](https://www.ebi.ac.uk/biosamples/samples/SAMEA112748815) was identified as origin.

### Register sequencing study
* BGE projects should follow a certain standard when it comes to naming, which was followed in this study:
    * Title: Pinna rudis, genomic and transcriptomic data.
    * Name: xbPinRudi
    * Description: This project collects the genomic and transcriptomic data generated for Pinna rudis to facilitate genome assembly and annotation as part of the Biodiversity Genomics Europe project (BGE, https://biodiversitygenomics.eu/) and organised by the European Reference Genome Atlas (ERGA, https://www.erga-biodiversity.eu/) initiative.
    * Attribute: TAG="Keyword" VALUE="ERGA-BGE"
* Release date was set 2 years in the future, 2026-03-07 (same as for all our BGE projects). This should be updated when all datasets have been submitted, so that the annotation group can access them.
* The study was registered via the browser, using NBIS DM broker account, received accession number: `PRJEB75035`.

### Submit HiFi
* NGI filled and checked the experiment metadata
* I created a [manifest](./data/PRJEB75035-HiFi-manifest.txt) file manually, based on the xml output from the script, and compared with the metadata template. The only question that remains is the tube_or_well_id, that is used to create the LIBRARY_NAME (a field where we normally would put platform-data type-species abreviation).
    * I decided to use the UGC_id, and also to include the platform (PacBio) since Illumina is mentioned if RNA-Seq. Hence, the library name will be `pr_036_001 PacBio Hifi WGS`
* We have decided to set `SCILIFELAB` as center name (by default this will be the same as broker name, i.e. `NBIS`). I don't know how to set this using manifests, don't think it is possible. Hence, we need to edit this afterwards in the Webin Portal. Might be easier to submit programmatically in the future...
* I copied the manifest file to Uppmax, and validated and submitted using Webin-CLI:
    ```
    interactive -t 03:00:00 -A naiss2023-5-307
    module load ascp
    java -jar ../webin-cli-7.0.1.jar -ascp -context reads -userName $1 -password $2 -manifest PRJEB75035-HiFi-manifest.txt -outputDir Webin_output/ -submit
    ```
* Accession number received: ``
* Added the accession number to [BGE Species list for SciLifeLab](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/)

### About ERGA scripts
There are some issues when it comes to using the scripts (described below). We have decided to continue doing submission the same way as done previously for VR-EBP and ERGA-pilot, but will make sure that we follow the rules when it comes to naming.

* In the [ERGA submission](https://github.com/ERGA-consortium/ERGA-submission/) repo, there are python scripts to produce xml files for submitting sequencing data. I decided to give it a try.
    * I created a new tab in the metadata template (named BGE_experiment), filled as well as I could, and saved as [PRJEB75035-experiment.tsv](./data/PRJEB75035-experiment.tsv)
    * I then downloaded the ERGA-submission repo and edited the python file, changing first line from `python` to `python3` (making sure to have 'LF' not 'CRLF' in Visual Studio)
    * I had a lot of issues and since I in the end don't know what worked or not I provide a set of possible actions:
        ```
        conda deactivate - making sure that I don't use any conda environment
        sudo pip3 install Jinja2 - the readme file in repo state that module JINJA2 is needed
        sudo pip3 install pandas - an error message said ModuleNotFoundError: No module named 'pandas'
        ```
    * I tried script on example tsv first, then my own using commands:
        ```
        ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f fValHis.BGE.runs.tsv -p ERGA-BGE -o fValHis1
        ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f PRJEB75035-experiment.tsv -p ERGA-BGE -o PRJEB75035
        ```
    * The study xml produces 2 projects, one for sequencing and one for assembly, so that is all fine. However, since I've already created a project at ENA for the raw data, the experiment xml submission will not work (no project alias, it is not even possible to add an alias, if not afterwards?)
    * The example tsv only accept paired reads or Nanopore native file. I put the bam file name in 'native_file_name'. The run xml looks okay.
    * The experiment ignored the library_construction_protocol, and assumed paired layout and Illumina platform. I don't know how to get it to accept PacBio, I'm guessing that the script needs to be updated... There are some fields in the input tsv file that I could experiment with, but I doubt it will help.
    * I added a code snippet in order to obtain the correct platform and layout, but am not sure if this will break anything in future types:
    ```
        elif read_type =="Hifi":
            layout = 'SINGLE'
            model = 'PACBIO_SMRT'
    ```

    * I tried adding the protocol in column `exp_attr` (as well as in `lib_attr`), but to no avail. I'm beginning to suspect that they don't want this type of information (or at least that the script isn't written to do anything with it).
    * I added some code in order to obtain value in `exp_attr` to be written as `LIBRARY_CONSTRUCTION_PROTOCOL`, which seems to work (comparing to what xml looks like for already submitted experiments), but is it correct, can it be broken? No idea, but works for now...
    * I need to figure out `sample_tube_or_well_id`, should it be e.g. UGC id or UGC user id? Is this something that should/could be read from the portal? Is it the specimen id (which is almost the UGC user id, but with space changed into '_').
    * I have no idea what `yield` is, but the values in example tsv is not output anywhere in the xml files, so I guess it can be ignored/omitted without effect.
    * `recipe` - not sure what it is, the script doesn't use it...
* I think it would be good to have a look at the [ERGA portal](https://genomes.cnag.cat/erga-stream/) and see which of the column names in the example tsv can be found there (if any). This way we could get more examples in order to better understand the column names.
    * Recipe can be found at [sequencing](https://genomes.cnag.cat/erga-stream/sequencing/) (but there is no menu for this?), seems as if values could be either [HiFi25](https://genomes.cnag.cat/erga-stream/recipe/3/) or [ONT60](https://genomes.cnag.cat/erga-stream/recipe/4/) (for now).
    * Yield can be found in HiFi/Hi-C/Illumina/ONT (Gb) column in [reads](https://genomes.cnag.cat/erga-stream/reads/), while the coverage is in the dito (x) column.
    * In the [CNAG meeting](https://docs.google.com/document/d/1YjD7BoSPbPnI3lTSGztj0CXcHZJRVAQ4F2Nuwd5x9iE/) they said that the center should be the broker account holder (which is NBIS for us), but I'm guessing we could still use SCILIFELAB?
    * Tube_or_well_id can be found in view [samples](https://genomes.cnag.cat/erga-stream/samples/) but that doesn't make me any wiser since it is the derived samples and have id's such as R-1, R-2, R-3 etc... I have no idea how to solve this since NGI has told me to use the origin BioSample, not the derived ones.
* CNAG has created perl scripts that seems to be able to query the portal, in [CNAG ERGA repo](https://github.com/cnag-aat/ERGA-Status/), but I have no idea how to set them up...
