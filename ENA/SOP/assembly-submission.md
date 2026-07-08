# Submit assembly data

This SOP describes how to submit an (annotated) assembly to ENA.

An assembly can either be submitted to the same study/project as the raw data, or in a separate study. We have chosen the first approach.

**Note:** Submission of assembly needs to be the last step, since it will refer not only to study and sample accessions but also the run accessions of the raw data that has been used either for assembly itself or the annotation.

## Steps
1. Collect assembly metadata
    1. Create manifest file
    1. Create EMBL flat file (if annotated assembly)
1. Submit using Webin-CLI

## Collect assembly metadata
* Ask assembly bioinformatician for the assembly metadata, and to confirm which raw dataset(s) to reference.
### Create manifest file for non-annotated assembly
* Create a manifest file, use e.g. [assembly-manifest.txt](./data/assembly-manifest.txt) as template:
    * For the `ASSEMBLYNAME`, set a species abbreviation in combination with assembly, ideally add also a version number, in case there are updates e.g. `StyAte-assembly.1`.
    * `ASSEMBLY_TYPE` is likely `isolate`.
    * Ensure that also the annotation details are mentioned in the `DESCRIPTION`.
    * For `RUN_REF`, add the run accession numbers (not experiment accession numbers) separated with comma (a span will not work, they need to be explicitly stated).
    * `MINGAPLENGTH` is a non-zero integer, indicating how many `N` indicates a gap between **scaffolds**. The line can be removed if the assembly is on contig level only.
    * The fasta file needs to be gzipped / compressed.
    * If the assembly is not only on scaffold level, but **chromosome** level (i.e. the most complete level), a `chromosome_list.txt` (gzipped) needs to be created, containing three columns:
        1. identifier as is in the .fasta file
        1. which chromosome it is
        1. if Linear or Circular, and the chromosome type
        * EX: `SUPER_1	1	Linear-Chromosome`
        * See ENA docs on [Chromosome list file](https://ena-docs.readthedocs.io/en/latest/submit/fileprep/assembly.html#chromosome-list-file) for more information
    * Also for chromosome level, any unlocalised scaffolds/contigs needs to be collected in an `unlocalised_list.txt` (gzipped). This file contains the same first two columns as the chromosome list, i.e. identifier and which chromosome it belongs to.

### Create manifest file for annotated assembly
* Create a manifest file, use e.g. [assembly-annotated-manifest.txt](./data/assembly-annotated-manifest.txt) as template:
    * For the `ASSEMBLYNAME`, set a species abbreviation in combination with assembly, ideally add also a version number, in case there are updates e.g. `StyAte-assembly.1`.
    * `ASSEMBLY_TYPE` is likely `isolate`.
    * Ensure that also the annotation details are mentioned in the `DESCRIPTION`.
    * For `RUN_REF`, add the run accession numbers (not experiment accession numbers) separated with comma (a span will not work, they need to be explicitly stated).
    * The flat file needs to be gzipped / compressed.

#### Create EMBL flat file
* Ask assembly bioinformatician where assembly files (.fa and .gff) are located.
* Ensure that a [locus tag](./locus_tag_registration.md) has been registered in the project.
* Identify which translational table to be used at [NCBI taxonomy lookup](https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi).
* Ensure that the annotation (in the .gff file) is also on CDS level, not only on mRNA level
* Use [EMBLmyGFF](https://github.com/NBISweden/EMBLmyGFF3) to create an EBML flat file according to instructions given in [Create EMBL file](https://github.com/NBISweden/annotation-cluster/wiki/ENA-submission#create-embl-file):
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
    Then, run the script, e.g.:
    ```
    EMBLmyGFF3 annotation-file.gff assembly-file.fa --topology linear --molecule_type 'genomic DNA' --transl_table 1 --species "Stylops ater" --locus_tag STYATE --project_id PRJEB70320 -o PRJEB70320.embl
    gzip PRJEB70320.embl
    ```
* **Note:** tRNAScan-SE (used in some annotation pipelines) produces anticodons in a format not accepted by ENA. Only solution at the moment is to not include tRNA in gff file.
* Also check the [assembly annotation tools](./assembly-annotation-tools.md) page for tips and tricks on annotated assemblies.

## Submit using Webin-CLI
* Validate then submit the assembly manifest using the ([latest](https://github.com/enasequence/webin-cli/releases/latest)) Webin-CLI:
    ```
    java -jar /path/to/webin-cli-9.0.3.jar -ascp -context genome -userName Webin-XXX -password 'YYY' -manifest ./assembly-manifest.txt -validate 

    java -jar /path/to/webin-cli-9.0.3.jar -ascp -context genome -userName Webin-XXX -password 'YYY' -manifest ./assembly-manifest.txt -submit   
    ```
* Note down the accession number given.
* When ENA has processed the assembly, an email will be sent to the Webin account (or rather to those listed with emails in the account), that the assembly has been accessioned. The timeline varies with ENA workload, but most often within a week.
