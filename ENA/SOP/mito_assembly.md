# Submit mitochondrial assembly data

This SOP describes how to handle a situation where mitochondrial data has been assembled within a biodiversity project.

It is advised to submit the mito assembly using a separate project from the genome assembly project, as both of them will be associated with the same sample accession number. Adding an assembly to an existing study + sample pair, will be interpreted as an update of existing assembly rather than an additional assembly.

## Steps
1. Register study
1. Prepare assembly submission
    1. Create chromosome_list.txt
    1. Create manifest file
    1. Create EMBL flat file (if annotated assembly)
1. Submit assembly
1. Add study to umbrella project

## Register study
* Register a study via ENA portal, remember to add a locus tag if the assembly is annotated

## Prepare assembly submission
### Create chromosome_list.txt
* ENA guidelines says the following about [contig assembly](https://ena-docs.readthedocs.io/en/latest/submit/assembly/genome.html#contig-assembly): `"If you do not have a minimum of 2 contigs, then you will need to submit at a higher assembly level."`
* Hence, in order to submit a mito assembly, a [chromosome assembly](https://ena-docs.readthedocs.io/en/latest/submit/assembly/genome.html#chromosome-assembly) submission is the way to go:

    * Create a file [mito-chromosome_list.txt](./data/mito-chromosome_list.txt), containing a single row with four columns.
    * The [naming convention](https://ena-docs.readthedocs.io/en/latest/submit/fileprep/assembly.html#chromosome-list-file) for the columns is:
        * The first column, `OBJECT_NAME` must be identical to the identifier in the FASTA sequence file. E.g. if the sequence file has a header `>ptg000007l_rotated` then `ptg000007l_rotated` is put in the first column.
        * The second column, `CHROMOSOME_NAME` is set to `MIT` (a standard abbreviation of the Mitochondria in CHROMOSOME_NAME format).
        * The third column, `TOPOLOGY-CHROMOSOME_TYPE` is set to `Linear-Chromosome`. **Note:** Ask the assembly bioinformatician if the topology is `Circular` instead.
        * The fourth column, `CHROMOSOME_LOCATION` is set to the pre-defined value `Mitochondrion`.

### Create manifest file
* Create a manifest file, use e.g. [mito-assembly-manifest.txt](./data/mito-assembly-manifest.txt) as template:
    * Add the collected the metadata from the bioinformatician who did the assembly, as well as the accession numbers of the study (created above) and the sample (created earlier, either at ENA or via COPO).
    * For the `ASSEMBLY_NAME`, set a species abbreviation in combination with the type of assembly, e.g. `StyAte-mito-assembly`.
    * Add the name of the assembly file (gzipped fasta format). **Note:** If this is an annotated assembly, change `FASTA` to `FLATFILE` and add the name of the EMBL flat file instead (gzipped)
    * Add the name of the chromosome list (gzipped)

### Create EMBL flat file (if annotated assembly)
* If the assembly is annotated, see [GFF3 to EMBL](./GFF3-to-EMBL.md) on how to transform the FASTA and GFF file into EMBL flat file format (remember especially to add `--organelle mitochondrion`).
* The .gff file *must* have gene + CDS while mRNA is optional for mitochondrial genomes.
* If it is not a CDS, but rather tRNA or rRNA, ensure that there is a gene + tRNA, or gene + rRNA, respectively, and that their relation is correctly specified with *ID* and *Parent*, e.g.:
    ```
    ptg000351l_1_rc_rotated mitofinder      gene    1       69      .       +       .       ID=gene_tRNA-Met;Name=tRNA-Met gene
    ptg000351l_1_rc_rotated mitofinder      tRNA    1       69      .       +       .       ID=tRNA-Met;Parent=gene_tRNA-Met;Name=tRNA-Met
    ```
* Column 8 of the GFF file, “phase”: The phase of the CDS feature, which is related to /codon_start in the flatfile specification. The phase is computed based on the known phase at the start of the CDS and computed for subsequent CDS rows. It may not be accurate if the CDS contains internal frameshifts, which can occur in pseudogenes and in genomes with indels, assembly gaps, and other errors. The phase is one of the integers 0, 1, or 2, indicating the number of bases that should be removed from the beginning of this CDS feature to reach the first base of the next codon. **If the feature is not a CDS, this field should be set to “.”.**
* Ensure afterwards that there is a 'OG   mitochondrion' organelle feature
* Double check that the locus tags indeces are (increased) as expected (should be if the Parent was defined correctly in the .gff)

* Also check the [assembly annotation tools](./assembly-annotation-tools.md) page for tips and tricks on annotated assemblies.

## Submit assembly
* Validate then submit the assembly manifest using Webin-CLI:
    ```
    java -jar /path/to/webin-cli-9.0.3.jar -ascp -context genome -userName Webin-XXX -password 'YYY' -manifest ./mito-assembly-manifest.txt -validate 
    java -jar /path/to/webin-cli-9.0.3.jar -ascp -context genome -userName Webin-XXX -password 'YYY' -manifest ./mito-assembly-manifest.txt -submit   
    ```

## Add study to umbrella project

* If not already done, an umbrella project should be created, see further the SOP [register_umbrella_project](./register_umbrella_project.md). 

* In that SOP, please also find information on [how to update an existing umbrella project](register_umbrella_project.md#how-to-update-an-umbrella-project).

