# Converting a GFF3 to EMBL file format for ENA submission of a genome assembly

This SOP describes the necessary steps in how to convert a genome assembly in GFF3 format, to an EMBL flat file format accepted by ENA for submission.

The conversion requires three things:

- [Download and install the EMBLmyGFF3 tool](https://github.com/NBISweden/EMBLmyGFF3)
- A genome assembly in [GFF3 format](https://www.ncbi.nlm.nih.gov/datasets/docs/v1/reference-docs/file-formats/about-ncbi-gff3/). Additional documentation and explanation [here](https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md).
- The genome sequence in fasta format

After installing EMBLmyGFF3, open a command line terminal and navigate to the folder where the GFF and FASTA files are located. 

## Nuclear genome conversion
You can run the script using the mandatory flags defined below, but several more are listed in the EMBLmyGFF3 [documentation](https://github.com/NBISweden/EMBLmyGFF3):

```
EMBLmyGFF3 -i [XYZ] -p [PRJEB00000] -r [1] -s '[Genus species]' -t [linear] -m '[genomic DNA]' [filename].gff [filename].fasta -o [output_file].embl                        
```
- `EMBLmyGFF3` - activates the script
- `-i` sets the [locus tag](https://github.com/NBISweden/data-submission-documentation/blob/95118f344707b3a1003cd153168cb7c08d8ca55f/ENA/SOP/locus_tag_registration.md) as defined in the associated ENA study
- `-p` sets the accession for the [registered ENA project](https://github.com/NBISweden/data-submission-documentation/blob/95118f344707b3a1003cd153168cb7c08d8ca55f/ENA/SOP/study_registration_and_description.md)
- `-r` defines the [CDS translation table](https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi) for the organism 
- `-s` sets the full Genus+species name separated by a blank space
- `-t` defines the genome topology (e.g. `linear` for nuclear, `circular` for mitochondrial)
- `-m` sets the molecule type of the sample (e.g. `genomic DNA` for nuclear genome assembly)

Executing the script will take some time depending on the size of the GFF and FASTA. A small genome might take under a minute, while large genomes of several Gb is known to have taken hours, or even days.

Common error messages are warnings about duplicate and/or overlapping exons/introns as described e.g. [here](https://github.com/NBISweden/data-submission-documentation/blob/95118f344707b3a1003cd153168cb7c08d8ca55f/ENA/5894-Geodia-assembly/README.md) with solutions.

The finished EMBL file must then be compressed using gzip:

```
gzip -k [File].embl
````
With the `-k` flag active to force gzip to retain the original file. The zipped file can then be uploaded to ENA using the Webin-CLI client as described [here](https://github.com/NBISweden/data-submission-documentation/blob/95118f344707b3a1003cd153168cb7c08d8ca55f/ENA/5894-Geodia-assembly/README.md).