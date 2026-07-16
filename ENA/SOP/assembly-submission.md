# Submit assembly data

This SOP describes how to submit an (annotated) assembly to ENA.

An assembly can either be submitted to the same study/project as the raw data, or in a separate study. We have chosen the first approach.

**Note:** Submission of assembly needs to be the last step, since it will refer not only to study and sample accessions but also the run accessions of the raw data that has been used either for assembly itself or the annotation.

## Steps
1. Collect assembly metadata
    1. Create manifest file
    1. Create EMBL flat file (if annotated assembly)
1. Submit using Webin-CLI
    1. Post-submission check
1. Update assembly
1. Post-release check

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
* See [GFF3 to EMBL](./GFF3-to-EMBL.md) for details on the conversion to EMBL flat file

* Ensure that the annotation (in the .gff file) is also on CDS level, not only on mRNA level
* **Note:** tRNAScan-SE (used in some annotation pipelines) produces anticodons in a format not accepted by ENA. Only solution at the moment is to not include tRNA in gff file.

* Also check the [assembly annotation tools](./assembly-annotation-tools.md) page for tips and tricks on annotated assemblies.

## Submit using Webin-CLI
* Validate then submit the assembly manifest using the ([latest](https://github.com/enasequence/webin-cli/releases/latest)) Webin-CLI:
    ```
    java -jar /path/to/webin-cli-9.0.3.jar -ascp -context genome -userName Webin-XXX -password 'YYY' -manifest ./assembly-manifest.txt -validate 

    java -jar /path/to/webin-cli-9.0.3.jar -ascp -context genome -userName Webin-XXX -password 'YYY' -manifest ./assembly-manifest.txt -submit   
    ```
* Note down the analysis accession number given (ERZ...).

### Post-submission check
* When ENA has processed the assembly, an email will be sent to the Webin account (or rather to those listed with emails in the account), that the assembly has been accessioned. The timeline varies with ENA workload, but most often within a week. 
    * The assembly will have an accession starting with `GCA_` and the level will have a span 
    * Ensure that the level (contig, scaffold or chromosome) is as expected
    * Ensure that the span encompasses the expected number of contigs/scaffolds/chromosomes
    * Note the identifiers in an appropriate place
* If you don't get an email within reasonable time, login to the account and check the status in `Data Analyses > Analysis Processing Report`. This shows the processing status of archived analysis files, and you can see if it is *active*, *completed*, or *failed*. Nothe though that even if a processing has failed, the system will retry failed analyses so errors may resolve themselves. If it doesn't within a couple of weeks, you might need to contact ENA support and ask them to try to identify why processing keeps failing.

## Update assembly
* Some of the metadata, i.e. the information found in the manifest, can be updated in the ENA portal by editing the XML file
* If the assembly itself needs another version to be submitted, here's the steps:
    * Copy the manifest to a new file indicating that it is an updated version
    * Add a `.2` to the `NAME`
    * Change the file name in `FLATFILE` and update any other field values that has changed
    * Submit using Webin-CLI

## Post-release check
It is important to verify that everything displays as it should when public.
For annotated assemblies, even if validation was without errors, and accession numbers were assigned, the only way to verify that an assembly is displaying correctly is when it's become public.

1. Enter the project accession number in [ENA browser](https://www.ebi.ac.uk/ena/browser/home)
1. Verify that the description displays correctly
1. To the right is the **General** and **Data** links
    1. *General > Related ENA Records*: Gives hyperlinks to the Assembly, Coding & Non-coding (if annotated), and Sequence. If you follow the *Assembly* link, you will find all metadata that was included in the manifest, some quality statistics calculated by ENA, and have the possibility to download `All Seq EMBL` and `All Seq FASTA`, and dito for the WGS set (i.e. `WGS Set EMBL` and `WGS Set FASTA`). If you follow the *Sequence* link, you will see (some) sample metadata as well as have the possibility to view or download FASTA/EMBL/GFF per level (contig/scaffold/chromosome). Both ways of downloading the EMBL format gives the same information, irrespective of if annotated or not. The GFF format is of no interest if not annotated assembly, since this file describes the features.
    1. *Data > Sequence files*: Gives the same as *General > Related ENA Records > Sequence* described above.
    1. *Data > Wgs files*: Gives the same as *General > Related ENA Records > Assembly* decribed above.
1. Verify that the EMBL (annotated assembly) / FASTA (not annotated assembly) formatted file has the same features and annotation as the EMBL file you uploaded.

**Note:** A short-cut is to paste the assembly or sequence accession after the last '/' in the following hyperlink: <https://www.ebi.ac.uk/ena/browser/view/>