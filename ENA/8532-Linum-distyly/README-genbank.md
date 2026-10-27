# Background
Attempts trying to fix the .gff files so that they would work with EMBLmyGFF3 proved too difficult and error prone. During these attempts, we often looked at a rerun of GeSeq where also the genbank (.gb) was outputted, as a 'facit' how it should look. Hence, this readme covers the steps to skip the EMBLmyGFF3 step and instead use the genbank files in order to create the embl files.

## 1. Rerun of GeSeq
* Currently this does not work, possibly due to PHP security alerts, but when it is online again:
* Use default settings for each of the 17 assemblies (yes, also leonii and bienne, in order to create an embl file which can be sent to ENA helpdesk if needed):
    * BlastX for tRNA and rRNA
    * Chloe for CDS
    * Output both genbank and gff format

## 2. Create embl files from genbank files
* Gemini produced [gbk2embl.py](./scripts/gbk2embl.py) script (iterative process) which at least works with L austriacum.
* *Note: The script was created using the wrong genbank file, where BlatX produced CDS annotation, and Chloe the tRNA and rRNA. Hence, the script might need some rewrites.*
* Apply the [](./scripts/run-gbk2embl.sh) bash script
* Use `gzip -k *.embl` to prepare for submission

## 3. Update manifest files
* Replace the FLATFILE value with the new embl file name
* Add `-v2` to the ASSEMBLY_NAME in order for it to be unique (for the 15 assemblies already submitted)

## 4. Validate using Webin-CLI
```
java -jar webin-cli-9.0.3.jar -username Webin-[XXXXX] -password [PASSWORD] -context genome -manifest Manifest_[species].txt -validate
```
### Translation table errors
* 2026-10-26: All new genbank files failed with the same errors as for leonii and bienne (i.e. translation table 11 versus 1)! When I changed the embl file, so that the AC feature line didn't have the locus tag, but the identifier in the fasta file e.g. `AC * _Laustriacum` it worked for the majority, even bienne. Well, there's still issues but likely of the same type as below for the old wrong Laustriacum.
    * It din't work for leonii, suffruticosum, and tenuifolium. At least the last 2 has some weirdness going on, suffruticosum was mis-spelled and has a '_thrum', and tenuifolium has also been misspelled to teniufolium. Need to check more, and also chromosome list, but they should have been identified.
    * I finally figured it out, the chromosome_list files needs to match the 'AC' line (as well as the fasta file, but when it comes to annotated assemblies it is the embl file's AC line that is important)! *Now **all** 17 assemblies 'only' has 2-3 errors regarding `Expected and conceptual translations`

### Errors concerning expected and conceptual translations
* The error message currently on all assemblies: `ERROR: Expected and conceptual translations are different.`. See [Webin-CLI-report-errors-list.txt](./data/Webin-CLI-report-errors-list.txt), though L austriacum was already fixed, changing 'V's to 'M's so not included.

* Asked Gemini on L austriacum (though on the old, wrong, genbank file):
    ```
    Can you understand what is meant, and how to solve them? For the first 2 errors, `ERROR: Expected and conceptual translations are different.`, I noticed that the 'translation' sequence don't start with an 'M' which for me indicates a partial sequence. The 3rd error, `ERROR: A partial codon appears after the stop codon.` I don't understand. I've attached both the input and the output files (to the gbk2embl.py script), though I suspect that this cannot be solved by the script but rather needs some manual editing whenever I get errors like these. 
    ```
* Gemini output:

    **Errors 1 & 2:**
    * When ENA’s validator (webin-cli) inspects a CDS feature, it extracts the DNA sequence between the specified coordinates, conceptually translates it using the designated translation table (/transl_table=11), and compares its result against the explicit /translation="..." string stored in your file.
    
    * In your file at Line 82 (the atpI gene at complement(295..981)), the DNA sequence starts with the codon `GTG`. Under Genetic Code Table 11 (Bacterial / Plant Plastid code), GTG is a recognized alternative initiation (start) codon. According to INSDC translation rules, any valid start codon at position 1 (/codon_start=1) of a complete CDS is conceptually translated as `M` (Methionine). However, GeSeq (or the conversion script) translated GTG literally as V (Valine) (/translation="VEVGQHFYW..."). Because the validator expects M at position 1 (MEVGQHFYW...), it flags a mismatch.

    * If the gene is *full-length*: Change the first amino acid in the /translation="..." qualifier from `V` (or L) to `M` (e.g., change VEVGQHFYW... to MEVGQHFYW...). 
    * If the gene is *partial / truncated* at the 5' end: Mark the coordinates as partial by adding `<` or `>` to the boundary in the feature location (e.g., CDS complement(<295..981)). This signals to Webin-CLI that the CDS is incomplete and does not begin with an initiation codon.
    
    **Error 3:**
    * When Webin-CLI parses a CDS from start to end, it translates codons in triplets until it hits an in-frame stop codon (`TAA`, `TAG`, or `TGA`). This error triggers when:
        * Trailing bases: The feature boundary extends 1 or 2 bases past the stop codon (e.g., CDS length is not divisible by 3).
        * Premature stop codon: There is an internal in-frame stop codon, and Webin-CLI stops translating before reaching the annotated end of the CDS feature, leaving leftover partial codon bases.
    * Open Laustriacum.embl and locate the CDS feature around line 1850. Check the total length of the CDS: $\text{Length} = (\text{End} - \text{Start} + 1)$. Ensure that $\text{Length} \pmod 3 == 0$.
    * Trim 1 or 2 extra trailing bases so the feature coordinate ends precisely on the 3rd base of the stop codon (on both gene and CDS feature).
    * If there is an internal premature stop codon (common in pseudogenes or misannotated genes), adjust the 3' boundary to end at the stop codon, or mark the CDS as a pseudogene / partial feature.

* For all 17 assemblies, this was changed: 
    * Predicted psbC, seems to be full sequence, but when I check in uniprot it lacks ~12 amino acids in the beginning. Hence I added '<' to CDS start position, and changed codon_start to 2 (adding '<' only did not help, but I noticed that the original submissions also had start codon equal to 2)
    * Predicted rps19 gene, seems to be fragment, but when I check in uniprot it seems valid length and sequence. Hence, I changed from 'V' to 'M' in first poition of /translation feature 

## 5. Submit the updated assemblies
```
java -jar webin-cli-9.0.3.jar -username Webin-[XXXXX] -password [PASSWORD] -context genome -manifest Manifest_[species].txt -submit
```
* Receipts:
    ´´´
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/Laustriacum.embl.gz
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/chromosome_list_austriacum.txt.gz
    INFO : Files have been successfully uploaded.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ30603604
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/Lbienne.embl.gz
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/chromosome_list_bienne.txt.gz
    INFO : Files have been successfully uploaded.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ30603615
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/Lcampanulatum.embl.gz
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/chromosome_list_campanulatum.txt.gz
    INFO : Files have been successfully uploaded.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ30603631
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/Lcapitatum.embl.gz
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/chromosome_list_capitatum.txt.gz
    INFO : Files have been successfully uploaded.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ30603676
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/Lflavum.embl.gz
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/chromosome_list_flavum.txt.gz
    INFO : Files have been successfully uploaded.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ30603686
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/Lgrandiflorum_thrum.embl.gz
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/chromosome_list_grandiflorum.txt.gz
    INFO : Files have been successfully uploaded.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ30603711
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/Lhirsutum.embl.gz
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/chromosome_list_hirsutum.txt.gz
    INFO : Files have been successfully uploaded.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ30603735
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/Lleonii.embl.gz
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/chromosome_list_leonii.txt.gz
    INFO : Files have been successfully uploaded.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ30603752
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/Lmaritimum_thrum.embl.gz
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/chromosome_list_maritimum.txt.gz
    INFO : Files have been successfully uploaded.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ30603774
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/Lnarbonense.embl.gz
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/chromosome_list_narbonense.txt.gz
    INFO : Files have been successfully uploaded.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ30603794
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/Lperenne.embl.gz
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/chromosome_list_perenne.txt.gz
    INFO : Files have been successfully uploaded.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ30603808
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/Lsuffruticosum_thrum.embl.gz
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/chromosome_list_suffricatosum.txt.gz
    INFO : Files have been successfully uploaded.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ30603819
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/Ltauricum.embl.gz
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/chromosome_list_tauricum.txt.gz
    INFO : Files have been successfully uploaded.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ30603826
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/Ltenue.embl.gz
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/chromosome_list_tenue.txt.gz
    INFO : Files have been successfully uploaded.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ30603833
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/Ltenuifolium.embl.gz
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/chromosome_list_tenuifolium.txt.gz
    INFO : Files have been successfully uploaded.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ30603839
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/Lthracicum.embl.gz
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/chromosome_list_thracicum.txt.gz
    INFO : Files have been successfully uploaded.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ30603846
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/Ltrigynum.embl.gz
    INFO : Uploading file: /mnt/c/Users/yvonne.kallberg/Desktop/GeSeq-leonii/Submission/chromosome_list_trigynum.txt.gz
    INFO : Files have been successfully uploaded.
    INFO : The submission has been completed successfully. The following analysis accession was assigned to the submission: ERZ30603855
    ```
    