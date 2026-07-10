# Converting a GFF3 to EMBL file format for ENA submission of a genome assembly

This SOP describes the necessary steps in how to convert a genome assembly in GFF3 format, to an EMBL flat file format accepted by ENA for submission.

The conversion requires three things:

- [Download and install the EMBLmyGFF3 tool](https://github.com/NBISweden/EMBLmyGFF3)
- A genome assembly in [GFF3 format](https://www.ncbi.nlm.nih.gov/datasets/docs/v1/reference-docs/file-formats/about-ncbi-gff3/). Additional documentation and explanation at [Sequence Ontology GitHub](https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md).
- The genome sequence in fasta format

After installing EMBLmyGFF3, open a command line terminal and navigate to the folder where the GFF and FASTA files are located. 

## Nuclear genome conversion
* You can run the script using the mandatory flags defined below, but several more are listed in the EMBLmyGFF3 [documentation](https://github.com/NBISweden/EMBLmyGFF3).
* See also Annotation teams [How-to on github](https://github.com/NBISweden/annotation-cluster/wiki/ENA-submission#create-embl-file) for info regarding how to expose translations and update the .json files:

    ```
    EMBLmyGFF3 --expose_translations
    ```
    Add the following to `translation_gff_feature_to_embl_qualifier.json`:
    ```
    "exon": {
        "remove": true
    }
    ```
    **Note:** On some occasions there could be an issue with introns as well. Always double check with the assembly bioinformatician, but a possible solution could be to add the following snippet to the file above:
    ```
     "intron": {
        "remove": true
    },
    ```

    Update `translation_gff_attribute_to_embl_qualifier.json` with the following:
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
    * Common error messages are warnings about duplicate and/or overlapping exons/introns as described e.g. in [5894-Geodia-assembly](../5894-Geodia-assembly/README.md) with solutions.

* Run the script:
    ```
    EMBLmyGFF3 [filename].gff [filename].fasta --locus_tag [XYZ] --project_id [PRJEB00000] --transl_table [N] --species '[Genus species]' --topology [linear] --molecule_type '[genomic DNA]' -o [output_file].embl                        
    ```
    - `EMBLmyGFF3` - activates the script
    - `--locus_tag` sets the [locus tag](./locus_tag_registration.md) as defined in the associated ENA study
    - `--project_id` sets the accession for the [registered ENA project](./study_registration_and_description.md)
    - `--transl_table` defines the [CDS translation table](https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi) for the organism 
    - `--species` sets the full Genus+species name separated by a blank space
    - `--topology` defines the genome topology (e.g. `linear` for nuclear, `circular` for mitochondrial)
    - `--molecule_type` sets the molecule type of the sample (e.g. `genomic DNA` for nuclear genome assembly, otherwise any of: "genomic RNA", "mRNA", "tRNA", "rRNA", "other RNA", "other DNA", "transcribed RNA", "viral cRNA", "unassigned DNA", "unassigned RNA")

    Executing the script will take some time depending on the size of the GFF and FASTA. A small genome might take under a minute, while large genomes of several Gb is known to have taken hours, or even days.

* The finished EMBL file must then be compressed using gzip:

    ```
    gzip -k [File].embl
    ````
    With the `-k` flag active to force gzip to retain the original file. 
* The zipped file can then be uploaded to ENA using the Webin-CLI client as described in [5894-Geodia-assembly](../5894-Geodia-assembly/README.md).

## Organelle genome conversion
We have so far come across mitochondrion and chloroplast annotated assemblies, and for these there is one more parameter to set in the EMBLmyGFF3 script:
- `--organelle` defines the `OG` feature in the EMBL flatfile. Set it to `mitochondrion` or `plastid:chloroplast` (other possible values: chromatophore, hydrogenosome, nucleomorph, plastid, mitochondrion:kinetoplast, plastid:apicoplast, plastid:chromoplast, plastid:cyanelle, plastid:leucoplast, plastid:proplastid)

**Note:** The translational table might differ from the nuclear genome's, and the topology is typically circular but ask the assembly bioinformatician.
