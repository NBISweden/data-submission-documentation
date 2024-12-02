# README

## 1. Overview

This dataset contains proteomics data generated from mass spectrometry experiments. The data includes processed information on peptide and protein identifications, as well as normalized intensities for each sample. Brain samples from **alcohol-use disorder (AUD)** patients (N=12 cases) and matched **unaffected comparsion (UC) subjects** (N=12 controls) were submitted to subcellular extractions, which yielded three extracts (i.e., synaptomal-, cytosolic-, and pellet/insoluble extracts). All three extracts (total N=72 samples) were subjected to TMT-based quantitative proteomics.

The files are structured to comply with NIH submission guidelines and include associated metadata for transparency and reusability.

## 2. Dataset Description
- **Sample Type**: Brain tissue samples from 12 alcohol-dependent patients and 12 matched controls.
- **Data Types**: 
  - Peptide-level data
  - Protein group data
  - Normalized intensity values

## 3. File Structure
The dataset is organized into the following categories:

### Raw Data - Is this avaliable? 
- Contains raw mass spectrometry files in [FORMAT] (e.g., `.raw`, `.mzML`, `.mzXML`).
- These files are the direct outputs of the mass spectrometer and can be used for reanalysis and processing.

### Processed Data - Can we decribe the two groups (Group 1 and Group2)?

Data from all three extracts—synaptomal, cytosolic, and pellet extracts—are provided for Peptide-Level Data and Protein Group Data.

1. **Peptide-level Data**:
   - **Files**: 
   - **Synapsomal peptide-level data:**`Data result_SYNAPTOSOMAL extracts (CPJS05122201)_peptides_G1.csv`, `Data result_SYNAPTOSOMAL extracts (CPJS05122201)_peptides_G2.csv`
   -**Cytosolic peptide-level data:** `Data result_CYTOSOLIC extracts (CPJS05122201)_peptides_G1.csv`, `Data result_CYTOSOLIC extracts (CPJS05122201)_peptides_G2.csv`
   -**Pellet peptide-level data**: `Data result_PELLETS (CPJS05122201-02)_peptides_G1.csv`, `Data result_PELLETS (CPJS05122201-02)_peptides_G2` 

   - **Description**: Contains peptide identifications with associated details such as sequence information, cleavage positions, quantification (reporter intensities), and confidence scores (PEP and Score).
   - **Columns**: Includes fields such as `Sequence`, `Mass`, `Proteins`, `Reporter intensity corrected [126-133C]`, and more.

2. **Protein Group Data**: 
   - **Files:**
   - **Synapsomal Protein Group Data:**`Data result_SYNAPTOSOMAL extracts (CPJS05122201)_proteinGroups_G1.csv`, `Data result_SYNAPTOSOMAL extracts (CPJS05122201)_proteinGroups_G2.csv`
   -**Cytosolic Protein Group Data:** `Data result_CYTOSOLIC extracts (CPJS05122201)_proteinGroups_G1.csv`, `Data result_CYTOSOLIC extracts (CPJS05122201)_proteinGroups_G2.csv`,   -**Pellet Protein Group Data:** Data result_PELLETS (CPJS05122201-02)_proteinGroups_G1.csv`, `Data result_PELLETS (CPJS05122201-02)_proteinGroups_G2.csv`

   - **Description**: Provides protein-level information inferred from peptide identifications, including majority protein IDs, peptide counts, sequence coverage, molecular weight, and reporter intensities.
   - **Columns**: Includes fields such as `Protein IDs`, `Gene names`, `Reporter intensity corrected [126-133C]`, and more.

3. **Normalized Intensities**:
   - **Files**: `Synaptosomal_NormalizedIntensity.csv`, `Cytosolic_NormalizedIntensity.csv`, `Pellet_NormalizedIntensity.csv`

   - **Description**: Contains normalized protein intensities for each sample and extract type, suitable for downstream statistical and biological analyses.
   - **Columns**: Includes sample identifiers, protein IDs, and normalized intensity values.

## 4. Data Processing and Quality Control - Have I understood this correctly?
- Data was processed using MaxQuant for peptide and protein identification.
- Normalization was performed using the TMT method to account for sample loading differences.
- QC steps included filtering peptides with less than 50% intensity and ensuring the absence of batch effects. 

## 4. Metadata - Do you want to add more information to the samples? 

# Table of samples and group 

- **SampleID**: 

| Sample ID         | Group       |
|-------------------|-------------|
| NDAR_INVZP533HRY  | AUD         |
| NDAR_INVET382VUA  | AUD         |
| NDAR_INVHF337EVP  | AUD         |
| NDAR_INV7WXA8DKW  | AUD         |
| NDAR_INVVP147RCJ  | AUD         |
| NDAR_INVTX575ZGC  | AUD         |
| NDAR_INVGU478YAJ  | AUD         |
| NDAR_INVN5RLV2EL  | AUD         |
| NDAR_INVHV107HP0  | AUD         |
| NDAR_INVTM428AP8  | AUD         |
| NDAR_INVTZ367WAL  | AUD         |
| NDAR_INVDL334YXC  | AUD         |
| NDAR_INVJH664FE9  | UC          |
| NDAR_INVGT723XVK  | UC          |
| NDAR_INVWP390HYA  | UC          |
| NDAR_INVNV020YP6  | UC          |
| NDAR_INVXE218GX0  | UC          |
| NDAR_INVLX361NYZ  | UC          |
| NDAR_INVJ6D7UTY9  | UC          |
| NDAR_INVZH180FUN  | UC          |
| NDAR_INVWG603WH3  | UC          |
| NDAR_INVZY800BZV  | UC          |
| NDAR_INVCG998BZN  | UC          |
| NDAR_INVYN293LN8  | UC          |


- **Group**: **alcohol-use disorder (AUD)** or **Unaffected comparsion (UC) subjects** 
- **Fraction Type**: Synaptomal, Cytosolic, and Pellet/Insoluble
- **Human Subject Compliance**: Samples were colleced from the NIH NeuroBiobank (NBB). The policies and procedures of the NBB have been reviewed and approved by the respective Institutional Review Board (IRB), and trained individuals request and document consent for brain tissue donation from the deceased's next-of-kin or legally authorized representative. Individual requests for release of medical records, questionnaires, and/or interviews with individuals knowledgeable of the deceased are obtained according to IRB-approved policies and procedures.

- **Processing Details**:
  - Data were processed using [SOFTWARE NAME] (e.g., MaxQuant, Proteome Discoverer).
  - Normalized intensities were calculated using [METHOD].
  - Reporter intensities were extracted and corrected using [METHOD].

## 5. Data Sharing and Usage - Do you agree with this? 
- This dataset is publicly available for research purposes and is provided in accordance with the NIH Data Sharing Policy.
- Data Use Agreement (DUA) applies. Please review and adhere to the terms outlined in the DUA.


## 6. Notes and Considerations - 
- **File Updates**: Any updates or additional documentation (e.g., revised README) will be submitted as supplemental files.
- **Data Reusability**: All files are provided in open formats (.csv, .raw) to ensure compatibility with downstream analysis software and for research purposes.
- **Contact**: For questions or clarifications, please contact [Your Name] at [Your Email].

## 9. Contact Information - Do you want to include this? 
- For questions or further information, please contact Philippe Melas at philippe.melas@ki.se or Yuan Li at yuan.li@immun.lth.se