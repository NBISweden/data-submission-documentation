---
Redmine_issue: https://projects.nbis.se/issues/5872
Repository: ENA
Submission_type: HiFi, Isoseq, RNA, mito, assembly, umbrella # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB72359
---

# VR EBP - *Tricholoma matsutake*

## Submission task description
Within the VR-EBP (Earth Biogenome Project) a fungi, *Tricholoma matsutake*, is to be submitted. There are raw reads in form of HiFi, Isoseq and Illumina RNA sequences, an annotated genome assembly and a mito assembly. An umbrella project will be created to collect the two assemblies.

## Procedure overview and links to examples
* [Metadata template](https://docs.google.com/spreadsheets/d/1i0bnT1SdiVmxTRZ_CiTQAAdvRYDHpZdL/edit#gid=268563316)
* [File locations on Uppmax](/proj/snic2022-6-208/VREBP-Tricholoma_matsutake-2023-AsmAnno/data/to_ENA/)
* Notes on how to [Create EMBL file](https://github.com/NBISweden/annotation-cluster/wiki/ENA-submission#create-embl-file)
* Umbrella project at ENA [how to](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#umbrella-studies)
* [SOP Umbrella projects](../SOP/register_umbrella_projects.md)

### Steps
* [Collect metadata](#collect-metadata)
* [Submit 3 studies](#register-study) (umbrella, raw reads + genome assembly, mito assembly)
* [Submit sample](#register-sample)
* Prepare and submit [raw reads](#register-experiment)
* Prepare and submit [genome assembly](#genome-assembly)
* Prepare and submit [mito assembly](#mito-assembly)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->
* I asked the PI to fill the sample metadata a bit late, in spite of knowing that these things take time.

## Detailed step by step description

### Collect metadata

* PI was asked to fill the sample metadata in the template
* I also asked if I should register a ToLID (tree of life ID)
* The NBIS bioinformatician filled the assembly metadata
* The experiments was divided into three tabs, one each of HiFi, Iso and Illumina RNA, and 2 (1 for PacBio and 1 for Illumina) NGI responsible persons were asked to fill in the metadata for these.

### Register study
* All metadata regarding studies is in the ENA_study tab of the metadata template.
* For the raw reads and the genome assembly a project was registered in the Webin Portal, receiving `PRJEB72359` as accession number. 
    * Study alias: `TriMat1` 
    * Locus tag: `TRIMAT` 
    * Release date: `2026-02-05`
* A study for the mitochondrial assembly was registered in the Webin Portal with a release date of `2026-02-05`, study alias `mito-TriMat1`. The accession number obtained was `PRJEB73337`.
* An umbrella study was submitted programmatically, with a release date of `2026-02-05`, using [submission.xml](./data/submission.xml) and [umbrella.xml](./data/umbrella.xml):

    ```
    curl -u Username:Password -F "SUBMISSION=@submission.xml" -F "PROJECT=@umbrella.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"    
    ```

    * Accession number received: `PRJEB73338`
    * Receipt of the sumbission:

    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-02-27T09:15:58.272Z" submissionFile="submission.xml" success="true">
        <PROJECT accession="PRJEB73338" alias="all-TriMat1" status="PRIVATE" holdUntilDate="2026-02-05Z"/>
        <SUBMISSION accession="ERA29182228" alias="SUBMISSION-27-02-2024-09:15:58:087"/>
        <MESSAGES>
            <INFO>All objects in this submission are set to private status (HOLD).</INFO>
        </MESSAGES>
        <ACTIONS>ADD</ACTIONS>
        <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```

### Register sample
* A ToLID was not provided, so I asked for one according to [SOP](../SOP/register_ToLID.md)
    * Taxonomy id: `40145`
    * Specimen ID: `TM_Rim_1`
    * Scientific name: `Tricholoma matsutake`
    * Received id: `gfTriMats1`
    **Note:** I did not get a notification via email, but when searching at [TOLID homepage](https://id.tol.sanger.ac.uk/search) I found the identifier (specimen ID matched)
* The sample was registered using the Webin Portal uploading [PRJEB72359-sample-metadata.tsv](./data/PRJEB72359-sample-metadata.tsv)
* Received accession number: `ERS18360571`

* Logged in to ENA and updated 'project_name' in the sample to 'The Swedish EBP pilot' so that it matches the other VR_EBP projects.

### Register experiment
* Manifests were created and copied (using WinSCP) to Uppmax, for each of the three types of sequences:
    * [PacBio HiFi manifest](./data/PRJEB72359-hifi-manifest.txt)
    * [PacBio Isoseq manifest](./data/PRJEB72359-isoseq-manifest.txt)
    * [Illumina RNA manifest](./data/PRJEB72359-Illumina-RNA-manifest.txt)
* They were each validated and submitted using Webin-CLI:
    ```
    interactive -t 08:00:00 -A naiss2023-5-307
    module load ascp
    mkdir Webin_output
    java -jar ../webin-cli-7.0.1.jar -ascp -context reads -userName $1 -password $2 -manifest $3 -outputDir Webin_output/ -validate
    java -jar ../webin-cli-7.0.1.jar -ascp -context reads -userName $1 -password $2 -manifest $3 -outputDir Webin_output/ -submit
    ```
* HiFi: `ERX12084821`, `ERR12710834`
* Isoseq: `ERX12084825`, `ERR12710838`
* RNA: `ERX12084862`, `ERR12710875`

### Genome assembly
* The bioinformatician needed to fix the gff file, so that the annotation is also on CDS level and not only on mRNA level
* I copied the gff3 and fasta file to nac-login cluster
* I exposed EMBLmyGFF3 variables and changed in 2 of the json files exposed, according to instructions in [Create EMBL file](https://github.com/NBISweden/annotation-cluster/wiki/ENA-submission#create-embl-file):
    ```
    source /projects/martin/prog/bin/conda_init.sh
    conda activate /home/asoares/.conda/envs/EMBLmyGFF3
    EMBLmyGFF3 --expose_translations
    ```
    Add to file [translation_gff_attribute_to_embl_qualifier.json](./data/translation_gff_attribute_to_embl_qualifier.json) the following modification:
    ```
    "Dbxref": {
    "source description": "A database cross reference.",
    "target": "inference",
    "dev comment": "inference"
    },
    "Ontology_term": {
    "source description": "A cross reference to an ontology term.",
    "target": "inference",
    "dev comment": ""
    },
    ```
    Add to file [translation_gff_feature_to_embl_feature.json](./data/translation_gff_feature_to_embl_feature.json) the following modification:
    ```
    "exon": {
        "remove": true
    },
    ```
    There is a third file exposed [translation_gff_other_to_embl_qualifier.json](./data/translation_gff_other_to_embl_qualifier.json), which is unaltered.

    Run script [run_emblmygff3_TRIMAT.sh](./scripts/run_emblmygff3_TRIMAT.sh), using command `sbatch run_emblmygff3_TRIMAT.sh`:
    ```
    EMBLmyGFF3 gfTriMats.pri.20231213.ENAconform.gff gfTriMats.pri.20231213.fa.gz --topology linear --molecule_type 'genomic DNA' --transl_table 1 --species "Tricholoma matsutake" --locus_tag TRIMAT --project_id PRJEB72359 -o PRJEB72359-TRIMAT.embl
    gzip PRJEB72359-TRIMAT.embl
    ```
    Output EMBLmyGFF3:
    ```
    08:28:19 WARNING feature: Unknown qualifier 'uniprot_id' - skipped
    08:28:20 ERROR feature: >>stop_codon<< is not a valid EMBL feature type. You can ignore this message if you don't need the feature. Otherwise tell me which EMBL feature it corresponds to by adding the information within the json mapping file.
    08:28:20 ERROR feature: >>start_codon<< is not a valid EMBL feature type. You can ignore this message if you don't need the feature. Otherwise tell me which EMBL feature it corresponds to by adding the information within the json mapping file.
    08:28:21 ERROR feature: >>five_prime_utr<< is not a valid EMBL feature type. You can ignore this message if you don't need the feature. Otherwise tell me which EMBL feature it corresponds to by adding the information within the json mapping file.
    08:28:21 ERROR feature: >>three_prime_utr<< is not a valid EMBL feature type. You can ignore this message if you don't need the feature. Otherwise tell me which EMBL feature it corresponds to by adding the information within the json mapping file.
    ```
* Validation and submission of [PRJEB72359-genome-manifest.txt](./data/PRJEB72359-genome-manifest.txt) was done using webin-cli
    ```
    java -jar ../../../../../Downloads/webin-cli-7.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest PRJEB72359-genome-manifest.txt -validate
    ```
* Validation of flatfile (embl) showed several (more than 1600) error messages regarding intron duplications.
    * This needs to be handled by bioinformatician, but I was curious on how to connect the error message to embl-file and then to corresponding position in gff
    * First look at the error message and extract the line numbers, e.g. `ERROR: "intron" Features locations are duplicated - consider merging qualifiers. [ line: 128910 of PRJEB72359-TRIMAT.embl.gz,  line: 128883 of PRJEB72359-TRIMAT.embl.gz]

    * Then do a sed command to extract line in embl file , e.g. `sed -n '128883,128915p;128916q' PRJEB72359-TRIMAT.embl > err2` (note that the error message might put the line numbers in wrong order)
    * Then, using `more` on the err2 file see the intron number, then check these in the gff file
    * The bioinformatician fixed the gff file, and also created an embl flatfile. I was told that we can update the `translation_gff_feature_to_embl_feature.json` file, adding the following snippet:
    ```
    "intron": {
        "remove": true
    },
    ```
* I updated the script [run_emblmygff3_TRIMAT.sh](./scripts/run_emblmygff3_TRIMAT.sh)
* A new validation of the resulting embl file produced no errors, thus could be submitted. **Note:** Submission produced an error, suggesting enclosing password in single quotes, which I already had. When removing the quotes, submission was completed successfully...
* Accession number: `ERZ23774140`

### Mito assembly
* Since mito assemblies consists of only one sequence in the sequence file, a [chromosome assembly](https://ena-docs.readthedocs.io/en/latest/submit/assembly/genome.html#chromosome-assembly) submission is the way to go:
    * The manifest needs one additional file, therein referenced as `CHROMOSOME_LIST: chromosome_list.txt.gz`
    * In this [chromosome_list.txt](./data/chromosome_list.txt), a single row is added `ptg000014c_rc_rotated	MIT	Linear-Chromosome	Mitochondrion`
    * The [naming convention](https://ena-docs.readthedocs.io/en/latest/submit/fileprep/assembly.html#chromosome-list-file)
* Validation and submission of [PRJEB73337-mito-manifest.txt](./data/PRJEB73337-mito-manifest.txt) was done using webin-cli
    ```
    java -jar ../../../../../Downloads/webin-cli-7.0.1.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./PRJEB73337-mito-manifest.txt -validate
    ```
* Accession number: `ERZ23581694`
