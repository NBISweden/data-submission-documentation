---
Redmine_issue: https://projects.nbis.se/issues/4750
Repository: ENA
Submission_type: assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB69221
---

# 4750 - Spruce assembly

## Submission task description
Submission of spruce (*Picea abies*) genome assembly, using not only flat file but chromosome list, unlocalised list as well as AGP file. It was important that the gene order was maintained, and that the locus tag had a certain format (“PABIES_000001", “PABIES_000002” ....).

A project had already been created at ENA (`ERP154169`, `PRJEB69221`), but locus tag `PABIES` needed to be added to the project, and also click in that functional annotation will be provided.

## Procedure overview and links to examples

* All files necessary for submission using Webin-CLI was prepared by project member (except flat file)

1. [Ensure GFF file correct](#ensure-gff-file-correct)
1. [Create EMBL flat file](#create-embl-flat-file)
1. [Validate AGP file](#validate-agp-file)
1. [Update manifest file](#update-manifest-file)
1. [Validate and submit assembly](#validate-and-submit-assembly)

## Lessons learned
* AGP files are still a mystery how the identifiers should be namned, in the end we had to exclude the AGP file
* Automatic sorting of identifiers seems to be the default on many scripts, which in this case was very unwanted since the gene order needed to be maintained
* Learned how to manipulate the locus tags numbering

## Detailed step by step description

### Ensure GFF file correct
* A few genes had an additional feature, `geneID` in the 9th column. This caused an error when validating the embl file.
* I removed all `geneID=...` resulting in file `Picab02_230926_at01_longest_no_TE_sorted_CDSonly-nogeneID.gff`
* When trying to validate again, I received error messages about introns being too short and some stating that `A partial codon appears after the stop codon`
* There is a script, [agat_sp_flag_short_introns](https://agat.readthedocs.io/en/latest/tools/agat_sp_flag_short_introns.html), but the gene order is not maintained, so in the end I flagged all genes listed in [validation-error-genes.txt](./data/validation-error-genes.txt) with `;pseudo`, resulting in file `Picab02_230926_at01_longest_no_TE_sorted_CDSonly-nogeneID-pseudoFix.gff`.
```
source /projects/martin/prog/bin/conda_init.sh
agat_sp_flag_short_introns.pl --gff Picab02_230926_at01_longest_no_TE_sorted_CDSonly-nogeneID.gff3 --out Picab02_230926_at01_longest_no_TE_sorted_CDSonly-nogeneID-pseudo.gff3
flag the gene pa_chr07_g004647
flag the gene pa_chr01_g005891
flag the gene pa_chr10_g001046
flag the gene pa_chr04_g002783
flag the gene pa_chr11_g001440
flag the gene pa_chr04_g002213
flag the gene pa_chr05_g000114
flag the gene pa_chr08_g004752
flag the gene pa_chr05_g002089
flag the gene pa_chr07_g002782
flag the gene pa_chr01_g002390
We found 11 cases where introns were < 10, we flagged them with the attribute pseudo. The value of this tag is size of the shortest intron found in this gene.
```

### Create EMBL flat file
* I decided to set `--locus_numbering_start 1000001`. This way we can manually edit and remove 'LOCUS1' from all entries and get the numbering we want (example locus row is then `/locus_tag="PABIES_LOCUS1000001"`)
    ```
    sed 's/LOCUS1//' ERP154169-PABIES.embl > ERP154169-PABIES-noLOCUS.embl
    ```
* Annotation team found a way to avoid sortering but instead keep the order of the input fasta file. It requires to comment out `all_ids.sort` in file `/home/asoares/.conda/envs/EMBLmyGFF3/lib/python3.10/site-packages/BCBio/GFF/GFFParser.py`
* Script [run_emblmygff3_spruce_locus.sh](./scripts/run_emblmygff3_spruce_locus.sh) was used to create `ERP154169-PABIES-fixlocustag-nosort-v4.embl.gz`.

### Validate AGP file
* I ran NCBIs AGP validator online: The agp file needed an update, where term `contig` was replaced by `scaffold`, resulting in file `Picab02_chromosomes_and_unplaced-scaffold.agp.gz`.
* In the end, the AGP file didn't pass validation at ENA, hence was excluded from submission. Error messages complained (for every line) that:
```
ERROR: The component does not exist: "PA_chr01_c0001". [ line: 1]
ERROR: Invalid linkage evidence for object: "PA_chr01". [ line: 2]
``` 

### Update manifest file
* The manifest file needed update on the file fields, both name of field as well as filename
* Found an [example online](https://bioinformaticsworkbook.org/dataWrangling/ena-genome-submission.html#gsc.tab=0) regarding genome submission and manifests (was first time for me to provide more than one file in a manifest)
* [UPSC-0208.Manifest-ykUpdate.txt](./data/UPSC-0208.Manifest-ykUpdate.txt)

### Validate and submit assembly
* I was unable to validate using Ubuntu app, had Java Heap size issues, so I did it via Power shell instead.
* Validation failed complaining about intron features locations being duplicated ,so I added the following to `translation_gff_feature_to_embl_feature.json`:
    ```
     "intron": {
        "remove": true
    },
    ```

```
java -jar ../../../../Downloads/webin-cli-7.1.1.jar -ascp -context genome -userName Webin-XXX -password 'YYYY' -manifest UPSC-0208.Manifest-ykUpdate.txt -validate
java -jar ../../../../Downloads/webin-cli-7.1.1.jar -ascp -context genome -userName Webin-XXX -password 'YYYY' -manifest UPSC-0208.Manifest-ykUpdate.txt -submit
```
* Accession number: `ERZ23880246`
* Genome accession: ``
