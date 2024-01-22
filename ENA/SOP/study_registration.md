# Study registration for biodiversity projects

At ENA, a study is the highest level of order and is used to group objects together, e.g. experiments and data (raw reads). By accessing the Study (Project accession number) anyone can find and access the data associated with it. 

For data where there is no pre-registered study, you first need to register a study under which experiments and runs can later be submitted.

1. Login to your individual or broker ENA account and under `Studies (Projects)` select `Register Study`.

2. `Release date [This is when your study will be made public]`
    
    The default release date at ENA is two months from the project registratin date. Instead, set the release date to the maximum date from present day (2 years). The data will be released automatically when referenced in a published journal paper. At the end of an embargo period the release date can be consecutively extended in multiple two year intervals if desired.

3. `Study name`
    
    Use a short abbreviation as Study name following a modified version of the ToLID (Tree of Life ID) format, restricted to the thee first letters of the genus name plus the first three letters of the species name, followed by an index number.

    Example: For *Vulpes lagopus* -  VulLag1

4. `Short descriptive study title`

    - EBP - "[Genus species] (vernacular name), genomic and transcriptomic data"

    Example: "Lemmus lemmus, genomic and transcriptomic data" 

    - ERGA - "[Genus species] (vernacular name), genomic and transcriptomic data, ERGA pilot"

    Example: "Vulpes lagopus (arctic fox) genomic and assembly data, ERGA pilot"

5. `Detailed study abstract` 

    For EBP:

    "This project collects genomic and transcriptomic data generated for [Genus species] (vernacular name), to facilitate assembly and annotation as part of the project "A Swedish Earth Biogenome Project platform: building a pipeline and proof of principle studies” at NBIS (National Bioinformatics Infrastructure Sweden, https://nbis.se/) and NGI (National Genomics Infrastructure, https://www.scilifelab.se/units/ngi/) and funded by Vetenskapsrådet in Sweden, project nr. 2020-06174_VR."

    For ERGA:

    "This project collects genomic data generated for [Genus species], (vernacular name), to facilitate assembly and annotation as part of the ERGA pilot (https://www.erga-biodiversity.eu/pilot-project)."

6. `Will you provide functionable genome annotation?`

    Check this box for all EBP/ERGA studies as they aim at de novo assemblies and annotations.

    Checking this box will activate the option to Add Locus Tag Prefixes at the lower end of the screen.

7. `Add Locus Tag Prefixes`

   Click the black plus sign next to the text, type in the selected locus tag pefix and click `Add`.
   A locus tag for EBP/ERGA is made from the three first letters of the genus name plus the first three letters of the species name, all in capital letters.

   Example: *Bofotes viridis* - BUFVIR

8. Submit the study using the green `Submit` button at the bottom of the screen. The study is made on-the-fly and can be referenced using its accession number immediately. All studies are assigned two different acecssion numbers, one BioProject accession with the prefix `PRJEB`, and another called the study accession with the prefix `ERP`. The former is usually the one used in publications. 
