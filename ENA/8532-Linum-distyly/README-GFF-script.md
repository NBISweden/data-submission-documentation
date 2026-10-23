# Background
* Failed attempts using AGAT to fix the .gff files, made us attempt to solve observed issues one by one using python script (with assistance of Gemini).
* *Note 1: In the end this didn't work either, but the scripts are kept just in case.*
    * *Various script version were created, trying to fix the observed issues, all of them found in `scripts/` folder with names starting with `fix_geseq_gff`*
* *Note 2: We initially used L leonii, but later attempts were done using L austriacum, since this assembly at least didn't have any translation table issues in Webin-CLI validation.*

* The 15 assemblies now public contains errors, with **orphan CDS** not having a parent gene feature, and if there are 2 CDS in a gene they are not joined. As a result, there are at least 2 separate locus tag indeces per gene, one for the gene feature and one for the CDS (or 2 if there are 2 CDS) instead of all having the same locus tag index.
* There is also a misinterpretation made by EMBLmyGFF3, causing the locus tag indexing to **start at 2** instead of 1
* Looking at the embl files, there is no source feature at all, which could be one of the reasons why 2 of the assemblies don't go through the validation (though not the whole reason, since the other 15 embl files, which passed validation, don't have these lines either). It would be expected that the features start with e.g.
```
FT   source          1..173198
FT                   /organism="Linum leooni"
FT                   /organelle="plastid:chloroplast"
FT                   /mol_type="genomic DNA"
FT                   /db_xref="taxon:794874"
```
* The conclusion is that the gff3 files produced by GeSeq cannot be directly fed into EMBLmyGFF3.
* The strategy is to work with *L. leonii*, if this embl file can go through validation, and have correct locus tag indices, then the solution can be applied to the other 16 chloroplast assemblies as well.

## Strategy - index start
* In the .gff3 files there are 2 rows with `region` and `source`, e.g.:
    ```
    Lleonii GeSeq   region  1       173198  .       +       0       Is_circular=true
    Lleonii GeSeq   source  1       173198  .       +       1       ID=source-null;gbkey=source
    ```
* These need to be removed (or add a `##` in the beginning), manually or automatically.

## Strategy - orphan DCS
* The .gff3 file should have a `Parent=` on the CDS, just as exons and introns have. I asked Gemini to add this Parent feature.
* Looking at [SOP for mito assembly](../SOP/mito-assembly.md), it is embolded that if not a CDS row, the phase (column 8) should be a `.`. The gff3 files have `1` on all levels, not only.

## Solution
* I asked Gemini to correct the *L leonii* gff file according to the above strategies.
* I then ran EMBLmyGFF3 on this corrected file:
```
(base) yvonne@yvonneklenovo:~/Linum/Leonii$ EMBLmyGFF3 gemini-leonii-updated.gff Pt_asm_repeat_pattern1_UC-2912-LEO-18-2-leonii_S35_L002.fasta --project_id PRJEB108312 --locus_tag LLEOCHL --species "Linum leonii" --taxonomy PLN --organelle "plastid:chloroplast" --topology circular --molecule_type "genomic DNA" --transl_table 11 --data_class STD -o gemini-leonii-updated.embl

    #############################################################################
    # EMBLmyGFF3 v2.4                                                           #
    # NBIS - National Bioinformatics Infrastructure Sweden                      #
    # Authors: Martin Norling, Niclas Jareborg, Jacques Dainat                  #
    # Please visit https://github.com/NBISweden/EMBLmyGFF3 for more information #
    #############################################################################

11:53:45 WARNING feature: Unknown qualifier 'gbkey' - skipped                  
11:53:45 ERROR feature: >>inverted_repeat<< is not a valid EMBL feature type. You can ignore this message if you don't need the feature.
                        Otherwise tell me which EMBL feature it corresponds to by adding the information within the json mapping file.
11:53:45 ERROR feature: >>sequence_feature<< is not a valid EMBL feature type. You can ignore this message if you don't need the feature.
                        Otherwise tell me which EMBL feature it corresponds to by adding the information within the json mapping file.
11:53:45 ERROR feature: >>inferred_parent<< is not a valid EMBL feature type. You can ignore this message if you don't need the feature.
                        Otherwise tell me which EMBL feature it corresponds to by adding the information within the json mapping file.
Conversion done
```
* I will ignore the warnings for now, and focus on inspecting the resulting embl file:
    1. Feature lines starts with a source description - check
    1. Locus tags indexing starts at 1 - check
    1. CDS locus tag has the same index as its gene - check
    1. `/codon_start` is now `1` and not `2` as earlier, could be a good thing
* There are possible issues remaining:
    1. CDS:s are not joined if several within a gene. Not sure it is an issue but could be
    1. There is no `/organelle="plastid:chloroplast" in source feature (has been suggested to cause an issue if missing for the webin-cli validation, and I have seen it in other (mito) embl files)
    1. There is no `/db_xref="taxon:794874" (might not bee needed but have seen it in other (mito) embl files)

### Gemini output: Fix EMBL Flatfile Validation Errors
A review of your EMBL flatfile highlights several structural syntax issues that will cause Webin-CLI sequence validation failures:

**A. Split tRNA and rRNA Features**
Spliced tRNAs (e.g., trnI-GAU at LLEOCHL_LOCUS138/139, trnV-UAC, trnA-UGC, trnG-UCC, trnL-UAA, trnK-UUU) are currently formatted as two separate tRNA feature entries sharing the same locus_tag.

INSDC/ENA standards require spliced tRNAs to be represented as a single tRNA feature using join():
```
Code snippet
FT   gene            complement(143384..144412)
FT                   /gene="trnI-GAU"
FT                   /locus_tag="LLEOCHL_LOCUS138"
FT   tRNA            complement(join(143384..143418,144376..144412))
FT                   /gene="trnI-GAU"
FT                   /locus_tag="LLEOCHL_LOCUS138"
```
**B. Duplicate rps12 Features & Trans-Splicing**
LLEOCHL_LOCUS134 and LLEOCHL_LOCUS137 define the exact same coordinate (complement(56837..56950)) twice for rps12.

Chloroplast rps12 is trans-spliced (Exon 1 is in the LSC region, while Exons 2 and 3 reside in the IR regions). In ENA flatfiles, trans-spliced CDS features must include the /trans_splicing qualifier and join all exons under one feature:
```
Code snippet
FT   CDS             join(56837..56950,148390..148620,149164..149190)
FT                   /gene="rps12"
FT                   /locus_tag="LLEOCHL_LOCUS_RPS12"
FT                   /trans_splicing
FT                   /transl_table=11
```
**C. Non-Standard Gene Names**
Gene names like ndhA-fragment (LLEOCHL_LOCUS87) violate standard INSDC gene nomenclature rules. Use standard gene identifiers (/gene="ndhA") combined with either /pseudo or /note="fragmentary match" to represent partial or pseudogenized genes.
---
**Note:** There *are* definitely issues, also the locus tags have been indexed weirdly, so I am assuming that the tRNAs sometimes are orphaned as well, the gene and its tRNA would otherwise get the same locus tag index. Should probably be fixed on gff level, but for now manually updating the indeces (tRNA comes last so not too many to update)

* I needed to understand trans-splicing better, since I don't know what it means, this is the Gemini output:

    **What Trans-Spliced Means for rps12**

    In standard (cis) splicing, introns are removed from a single continuous pre-mRNA molecule transcribed from a single locus. Trans-splicing occurs when precursor RNA molecules transcribed from two or more separate genomic loci are spliced together into one functional mRNA.

    In land plant chloroplasts, rps12 (encoding ribosomal protein S12) is a classic trans-spliced gene split into two physical locations:

    Exon 1 (5' exon): Located in the Large Single Copy (LSC) region (~56.8 kb in your genome).

    Exons 2 and 3 (3' exons): Located inside the Inverted Repeat (IR) regions (~96.5–97.2 kb and ~148.3–149.1 kb).

    Because the IR region is duplicated (IRa and IRb), there are **two copy instances of Exons 2 and 3** in the genome, resulting in two distinct trans-spliced mRNA transcripts that **join Exon 1** to each respective IR copy.
* In this case there will be three genes, with separate locus tags, and 2 CDS which also needs separate locus tags (i.e. 5 locus tag indeces) and all of them needs to be identified as '/trans_splicing':
    ```
    FT   gene            complement(56837..56950)
    FT                   /gene="rps12"
    FT                   /locus_tag="LLEOCHL_LOCUS_RPS12_5P"
    FT                   /trans_splicing
    FT   gene            complement(96477..97277)
    FT                   /gene="rps12"
    FT                   /locus_tag="LLEOCHL_LOCUS_RPS12_3P1"
    FT                   /trans_splicing
    FT   gene            148390..149190
    FT                   /gene="rps12"
    FT                   /locus_tag="LLEOCHL_LOCUS_RPS12_3P2"
    FT                   /trans_splicing
    FT   CDS             join(complement(56837..56950),complement(97047..97277),complement(96477..96503))
    FT                   /gene="rps12"
    FT                   /locus_tag="LLEOCHL_LOCUS_RPS12_1"
    FT                   /trans_splicing
    FT                   /transl_table=11
    FT                   /product="ribosomal protein S12"
    FT   CDS             join(complement(56837..56950),148390..148620,149164..149190)
    FT                   /gene="rps12"
    FT                   /locus_tag="LLEOCHL_LOCUS_RPS12_2"
    FT                   /trans_splicing
    FT                   /transl_table=11
    FT                   /product="ribosomal protein S12"
    ```
    * Gemini changed its mind, there needs to be a 'join' on 2 genes (and checking the genbank output from GeSeq, this seems valid).

* Note to self, when running EMBLmyGFF3, I really should remove the introns and exons so that they are not included in the embl file (i.e. gene and CDS is enough, and if manual update of the indexing is needed there will be less places to update)

## Other ideas
* Is there any annotated chloroplasts, within similar taxonomy branch, at ENA? Thinking if I can download another species embl file and get a feel for it... check <https://www.ncbi.nlm.nih.gov/nuccore/NC_036356.1/> Linum usitatissimum
