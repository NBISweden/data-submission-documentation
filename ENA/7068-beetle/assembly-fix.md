# The process of getting a valid EMBL flatfile

## Links
The links below was collected when I myself tried to fix the assembly file, but in the end the researcher had to do this, with help from NBIS bioinformatician.
* Issues with [CDS phase loss](https://github.com/agshumate/Liftoff/issues/67) when using LiftOff
* <https://github.com/NBISweden/AGAT/blob/master/README.md#using-docker>
* <https://agat.readthedocs.io/en/latest/tools/agat_convert_sp_gxf2gxf.html>

## First trial

* I did a test submission of all levels, interactively for study, sample and experiment, Webin-CLI for the assembly. This meant that I had to create a new embl-file, with the test study accession id, but since unsure if the embl file would be accepted, it is worth it.
* The annotation file was not in .gff format but in .gtf, but I tried using EMBLmyGFF3 script anyway.

    ```
    conda activate py38
    EMBLmyGFF3 A.obtectus_v2.0.fasta_liftoff_clean.gtf.gz A.obtectus_v2.0.fasta --topology linear --molecule_type 'genomic DNA' --transl_table 1 --species "Acanthoscelides obtectus" --locus_tag ACAOB --project_id PRJEB67631 -o ACAOB_PRJEB67631_test.embl
    gzip ACAOB_PRJEB67631_test.embl
    ```
* I ran into memory issues on my laptop, turns out I had to increase the amount Ubuntu/WSL could use, but after that the embl.file was created

* Webin-CLI:
    ```
    java -jar ../../Downloads/webin-cli-6.3.0.jar -context genome -userName Webin-XXXXX -password YYYYY -manifest ./manifest_template_assembly_test.txt -validate -test
    ```
    Produced a lot of errors (only the last one was expected):
    ```
    ERROR: "exon" Features locations are duplicated - consider merging qualifiers. [ line: 1688 of ACAOB_PRJEB67631_test.embl.gz,  line: 1605 of ACAOB_PRJEB67631_test.embl.gz]
    ```
    ```
    ERROR: Abutting features cannot be adjacent between neighbouring exons. [ line: 253930 of ACAOB_PRJEB67631_test.embl.gz]
    ```
    ```
    ERROR: Illegal /locus_tag value "ACAOB_LOCUS1 ". locus_tag prefix "ACAOB" is not registered with the project. [ line: 35 of ACAOB_PRJEB67631_test.embl.gz]
    ```

* The researcher created a gff-formatted file, but the errors remained when it came to validation.

* A bioinformatician was consulted, who noticed that the annotation was on mRNA level only and not on CDS level, which would have the effect of ENA ignoring the annotation. The researcher and bioinformatician had a meeting to resolve this issue, resulting in file A.obtectus_v2.0_gt_tidy_v1.3.gff.gz.

* The bioinformatician also told me to expose the json file of the EMBLmyGFF3 script.

### Expose translations EMBLmyGFF3

```
conda activate py38
EMBLmyGFF3 --expose_translations
```
Add the following to translation_gff_attribute_to_embl_qualifier.json file:
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
Which, as it turns out, only is an update of the target (to 'inference').

Since earlier test validation gave error messages concerning 
```
ERROR: "exon" Features locations are duplicated
ERROR: Abutting features cannot be adjacent between neighbouring exons
```
and according to [NBIS ENA submission](https://github.com/NBISweden/annotation-cluster/wiki/ENA-submission#create-embl-file) one should remove exons from the submission, as *"they are already described within the transcripts location in the Embl format"*, by updating the file translation_gff_feature_to_embl_feature.json:

```
"exon": {
    "remove": true
}
```

## Second trial

I did an interactive submission of study (PRJEB69214), sample (sample.tsv), and experiment (experiment-test-PRJEB69214.tsv).

```
  EMBLmyGFF3 A.obtectus_v2.0_gt_tidy_v1.3.gff.gz A.obtectus_v2.0.fasta --topology linear --molecule_type 'genomic DNA' --transl_table 1 --species "Acanthoscelides obtectus" --locus_tag ACAOB --project_id PRJEB69214 -o ACAOB_PRJEB69214_test.embl
  gzip ACAOB_PRJEB69214_test.embl
```

Produced the following warnings (asked bioinformatician who said that it should be fine to ignore):
```
08:24:12 WARNING feature: Unknown qualifier 'makerName' - skipped              ]
08:24:12 WARNING feature: Unknown qualifier 'coverage' - skipped
08:24:12 WARNING feature: Unknown qualifier 'sequence_ID' - skipped
08:24:12 WARNING feature: Unknown qualifier 'valid_ORFs' - skipped
08:24:12 WARNING feature: Unknown qualifier 'extra_copy_number' - skipped
08:24:12 WARNING feature: Unknown qualifier 'copy_num_ID' - skipped
08:24:12 WARNING feature: Unknown qualifier '_AED' - skipped
08:24:12 WARNING feature: Unknown qualifier '_QI' - skipped
08:24:12 WARNING feature: Unknown qualifier '_eAED' - skipped
08:24:12 WARNING feature: Unknown qualifier 'matches_ref_protein' - skipped
08:24:12 WARNING feature: Unknown qualifier 'valid_ORF' - skipped
08:24:12 WARNING feature: Unknown qualifier 'cov' - skipped                    ]
08:24:12 WARNING feature: Unknown qualifier 'fPKM' - skipped
08:24:12 WARNING feature: Unknown qualifier 'gene_id' - skipped
08:24:12 WARNING feature: Unknown qualifier 'tPM' - skipped
08:24:12 WARNING feature: Unknown qualifier 'transcript_id' - skipped
08:24:12 WARNING feature: Unknown qualifier 'uniprot_id' - skipped
08:24:12 WARNING feature: Unknown qualifier '_merge_warning' - skipped         ]
08:28:46 WARNING EMBLmyGFF3: Sequence scaffold_3797 too short (85 bp)! Minimum accpeted by ENA is 100, we skip it !
08:28:46 WARNING EMBLmyGFF3: Sequence scaffold_3798 too short (31 bp)! Minimum accpeted by ENA is 100, we skip it !
08:28:46 WARNING EMBLmyGFF3: Sequence scaffold_3799 too short (19 bp)! Minimum accpeted by ENA is 100, we skip it !
08:28:46 WARNING EMBLmyGFF3: Sequence scaffold_3800 too short (13 bp)! Minimum accpeted by ENA is 100, we skip it !
08:28:46 WARNING EMBLmyGFF3: Sequence scaffold_3801 too short (10 bp)! Minimum accpeted by ENA is 100, we skip it !
08:28:46 WARNING EMBLmyGFF3: Sequence scaffold_3802 too short (8 bp)! Minimum accpeted by ENA is 100, we skip it !
Conversion done
```

Then validating the EMBL file:

```
java -jar ../../Downloads/webin-cli-6.3.0.jar -context genome -userName Webin-XXXXX -password YYYYY -manifest ./test-PRJEB69214-assembly-manifest.txt -validate -test
```

This worked as expected.