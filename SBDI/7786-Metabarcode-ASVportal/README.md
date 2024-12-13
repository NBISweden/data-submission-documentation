---
Redmine_issue: https://projects.nbis.se/issues/7786<id>
Repository: <Swedish Biodiversity Data Infrastructure(SBDI)>
Submission_type: <Metabarcode; Amplicon Seuquence Variants> # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- <pf>
Top_level_acccession: <AC>
---

# 7786 - Submission to Swedish Biodiversity Data Infrastrucutre - ASVs av fruktkroppar från Uppsala Svampklubb

## Submission task description
Evolutionsmuseet wants to upload a number of sequences they possess to the SBDI/ASV portal, using the metadata that already exists in Artportalen for the corresponding samples. They need help extracting metadata from Artportalen, reformatting it for the ASV portal, adding sequences and sequence information (possibly uploading raw data to ENA and/or uploading sequences to GenBank or equivalent), and then submitting everything to the ASV portal.

### Main steps of the submission process 
1. Submit your raw data to ENA.
2. Denoise your data to Amplicon Sequence Variants (ASVs) (you can use the ampliseq pipeline).
3. Download, fill in and upload the data input template provided by SBDI.
4. SBDI will contact you to write a data-sharing contract.
5. Your data will be published in the ASV database and bioatlas.


## Procedure overview and links to examples

### Extracting metadata from Artportalen

* [Artportalen](https://www.artportalen.se/ViewSighting/SearchSighting)

Pre-requisits:
-Account at Artportalen. You can export the data you want metadata from in Artportalen and extract metadata from there. 

### Denoise raw data to ASVs
* [Tool for denoise raw data to ASVs, nf-core/ampliseq, with instructions for the pipeline](https://nf-co.re/ampliseq/1.2.0) 

* Pre-requsits for using the tool:
- Nextflow installed 
- Singularity/apptainer or docker or conda
- [Sample sheet](https://github.com/nf-core/ampliseq/blob/master/assets/samplesheet.tsv)

* Input for denoising data: 
1. Raw data 
2. Primer sequences 
3. Metadata file (optinal) - Recommends adding a metadata file as the nf-core/ampliseq tool can generate metadata in a fileformat that is compatible with SBDI. Should include:
- Sample collection informatin: date, location
- Sequencing information 
- Any other data 


### Submission of data to SBDI 

*[SBDI Submission Guide](https://asv-portal.biodiversitydata.se/submit)
 [Video with insturctions for publishing metabarcoding data to SBDI](https://www.youtube.com/watch?v=a9ABLK0OzjU)


## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

* one
* two


## Meeting minutes 

### First consultation 
Attendees: Karin

Questions: 
1. How much data is there? 
2. Do you have amplicon swequence varians (ASVs)? 
3. If not, do you have: Raw data, Primer sequences and meta data file? (optional but recommend beacuse it can produce a metadata file in format to submit to sbdi)
4. Do you have an account at Artportalen? 
5. Can you send me a link to the data in Artportalen? 

 

## Meeting minutes 

* Krävs att man har referenser med objekt som är lagrade i ENA. Skapa en study, lägga upp sampels and lägga upp raw-reads. Raw-reads har taggar på sig som de behöver ta bort. 
* Deras data är fruktkroppar - bara en sekvens som kommer ut per prov. När de sekvenserar så har samma prov kunnats köra med flera barcodes. 

* Kan vi lägga upp i ASV-portalen utan att lägga upp i ENA? Dubbelkolla. 

* Taggarna. Olika taggar på olika prover. Brendon är den enda som kan fixa det. Jeanette kanske kan hjälpa till. Brendon har skickat förslag på hur man ska göra. 
* ENA dom har kvar sina tags. Får vi lägga upp data med taggar i ENA? 

* Karin få tillgång till test-portalen i ENA. 
* Skicka länk till repositoriet med koden i Github. 

* Hur många prover är det? 2000 i Artportalen som de finns sekvenser för. Har 2800 sekvenser totalt. De ska solla ut en viss mängd 

* Kan man omvandla rådata med taggar till ASV? 