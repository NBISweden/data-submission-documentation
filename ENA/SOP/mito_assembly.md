# Submit mitochondrial assembly data

This SOP describes how to handle a situation where mitochondrial data has been assembled within a biodiversity project.

It is advised to submit the mito assembly using a separate project from the genome assembly project, as both of them will be associated with the same sample accession number. Adding an assembly to an existing study + sample pair, will be interpreted as an update of existing assembly rather than an additional assembly.

## Steps
1. Register study
1. Prepare assembly submission
1. Submit assembly
1. Add study to umbrella project

### Register study


### Prepare assembly submission
* ENA guidelines says the following about [contig assembly](https://ena-docs.readthedocs.io/en/latest/submit/assembly/genome.html#contig-assembly): `"If you do not have a minimum of 2 contigs, then you will need to submit at a higher assembly level."`
* Hence, in order to submit a mito assembly, a [chromosome assembly](https://ena-docs.readthedocs.io/en/latest/submit/assembly/genome.html#chromosome-assembly) submission is the way to go:

    * Create a file [mito-chromosome_list.txt](./data/mito-chromosome_list.txt), containing a single row with four columns.
    * The [naming convention](https://ena-docs.readthedocs.io/en/latest/submit/fileprep/assembly.html#chromosome-list-file) for the columns is:
        * The first column, `OBJECT_NAME` must be identical to the identifier in the FASTA sequence file. E.g. if the sequence file has a header `>ptg000007l_rotated` then `ptg000007l_rotated` is put in the first column.
        * The second column, `CHROMOSOME_NAME` is set to `MIT` (a standard abbreviation of the Mitochondria in CHROMOSOME_NAME format).
        * The third column, `TOPOLOGY-CHROMOSOME_TYPE` is set to `linear-chromosome`.
        * The fourth column, `CHROMOSOME_LOCATION` is set to the pre-defined value `Mitochondrion`.
* Create a manifest file, use e.g. [mito-assembly-manifest.txt](./data/mito-assembly-manifest.txt) as template:
    * Add the collected the metadata from the bioinformatician who did the assembly, as well as the accession numbers of the study (created above) and the sample (created earlier, either at ENA or via COPO).
    * For the `ASSEMBLY_NAME`, set a species abbreviation in combination with the type of assembly, e.g. `StyAte-mito-assembly`.
    * Add the name of the assembly file (gzipped fasta format)
    * Add the name of the chromosome list (gzipped)

### Submit assembly
* Validate then submit the assembly manifest using Webin-CLI:
    ```
    java -jar /path/to/webin-cli-6.5.0.jar -ascp -context genome -userName Webin-XXX -password 'YYY' -manifest ./mito-assembly-manifest.txt -validate 
    java -jar /path/to/webin-cli-6.5.0.jar -ascp -context genome -userName Webin-XXX -password 'YYY' -manifest ./mito-assembly-manifest.txt -submit   
    ```

### Add study to umbrella project

* If not already done, an umbrella project should be created, see further the SOP [register_umbrella_project](./register_umbrella_project.md). 

* In that SOP, please also find information on [how to update an existing umbrella project](register_umbrella_project.md#how-to-update-an-umbrella-project).

