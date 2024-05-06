# Submit experiment (raw reads) data

This SOP describes how to submit an experiment (raw reads) to ENA.

**Note**: There are several [ways to submit raw reads](https://ena-docs.readthedocs.io/en/latest/submit/reads.html#submission-options), this SOP describes how to do it using Webin-CLI.

## Steps
1. Collect experiment metadata
1. Submit

### Collect experiment metadata
* Most of the metadata information resides with the data producer, e.g. NGI, ask them to fill in missing values.

* Create a manifest file, use e.g. [experiment-manifest.txt](./data/experiment-manifest.txt):
    * For the `NAME`, set a combination of platform, data type and species/TolID, e.g. PacBio-HiFi-StyAte1 (ERGA-pilot), `Pinna rudis Hifi WGS data` (BGE).
    * Though optional field, it is recommended to use `LIBRARY_CONSTRUCTION_PROTOCOL` to describe as much as possible regarding on what has happened with the sample from when it was taken until it was sequenced. At a minimum, library preparation protocols should be added.
    * On the last line `BAM:`, add the full path to where the sequence file resides, make sure that it is gzipp:ed.
    * **Note**: If paired reads are to be submitted, add a row (after row INSTRUMENT) with `INSERT_SIZE:` and the value of the insert size. Also, change the last row from `BAM:` to two rows with `FASTQ:`
* For additional fields, please see ENA's documentation on [Manifest file](https://ena-docs.readthedocs.io/en/latest/submit/reads/webin-cli.html#manifest-file).

### Submit
* Download the [latest Webin-CLI version](https://github.com/enasequence/webin-cli/releases/latest), and validate & submit:
    ```
    java -jar /path/to/webin-cli-7.1.1.jar -ascp -context reads -userName Webin-XXX -password 'YYY' -manifest ./experiment-manifest.txt -validate 
    java -jar /path/to/webin-cli-7.1.1.jar -ascp -context reads -userName Webin-XXX -password 'YYY' -manifest ./experiment-manifest.txt -submit
    ```
* **Note** the option `-context reads` in the commands.
* Note down the accession number given.
