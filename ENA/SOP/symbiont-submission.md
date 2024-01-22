# How to handle symbiont data

This SOP describes how to handle situations when a symbiont has been identified during assembly of a host species.

## Steps

1. Register a new taxonomy
1. Register a project/study
1. Register a sample
1. Submit assembly
1. Register an umbrella project

## Details
### New taxonomy
Follow the steps detailed in SOP [new_taxonomy](./new_taxonomy.md)

### Register a study
* Use the [Webin portal](https://www.ebi.ac.uk/ena/submit/webin/login) for registering the study, login with the broker account.
    * `Title` - Include both the symbiont species and the host species, e.g. `Wolbachia endosymbiont of Stylops ater genome assembly` <!-- agree on naming -->
    * `Release date` - set to same as the host release date
    * `Study name` - combine the symbiont species with the study alias of host, e.g. `wolbachia-StyAte1` <!-- agree on naming -->
    * `Study abstract` - e.g. `This project provides the assembly of Wolbachia endosymbiont of Stylops ater.`

### Register sample
* Register a sample using the same template and metadata as for the host, and add two columns:  
    * `sample symbiont of` - with the sample accession number of the host 
    * `symbiont` - set to 'Y'

### Submit assembly

The assembly is typically in a fasta file with one big contig. In order to submit it, a higher level of submission is required and thus a chromosome list is needed to be included in the submission.

* ENA on [Chromosome Assembly](https://ena-docs.readthedocs.io/en/latest/submit/assembly/genome.html#chromosome-assembly)
* ENA on [Chromosome List File](https://ena-docs.readthedocs.io/en/latest/submit/fileprep/assembly.html#chromosome-list-file)

Create a [symbiont chromosome list](./data/symbiont-chromosome_list.txt) file containing three columns:
    * The first column, `OBJECT_NAME` must be identical to the identifier in the FASTA sequence file. E.g. if the sequence file has a header `>wolbachia_strain1` then `wolbachia_strain1` is put in the first column.
    * The second column, `CHROMOSOME_NAME` in this case can be set to `strain1`.
    * The third column, `TOPOLOGY-CHROMOSOME_TYPE` in this case can be set to `linear-chromosome`.

* Create a [symbiont manifest](./data/symbiont-manifest.txt) file

* Validate and submit by using Webin-CLI
    ```
    java -jar /path/to/webin-cli-6.5.0.jar -ascp -context genome -userName Webin-XXX -password 'YYY' -manifest ./symbiont-manifest.txt -validate
    ```
### Register an umbrella project

Follow the steps in SOP [register_umbrella_project](./register_umbrella_project.md) and include the symbiont and host project accession numbers. 

* **Note:** If the umbrella project already exists, create a copy of the (used) existing submission.xml and umbrella.xml, and change the action to  `<MODIFY/>` in the former, and add another child with the symbiont project accession number in the latter file.
