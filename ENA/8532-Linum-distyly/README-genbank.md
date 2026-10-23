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

* Tested on L asutriacum (though on the old, wrong, genbank file), and the Webin-cli validation threw 3 errors:
    ```
    ERROR: Expected and conceptual translations are different. [ line: 82 of Laustriacum.embl.gz]
    ERROR: Expected and conceptual translations are different. [ line: 305 of Laustriacum.embl.gz]
    ERROR: A partial codon appears after the stop codon. [ line: 1850 of Laustriacum.embl.gz]
    ```
* Asked Gemini:
    ```
    Can you understand what is meant, and how to solve them? For the first 2 errors, I noticed that the 'translation' sequence don't start with an 'M' which for me indicates a partial sequence. The 3rd error I don't understand. I've attached both the input and the output files (to the gbk2embl.py script), though I suspect that this cannot be solved by the script but rather needs some manual editing whenever I get errors like these. 
    ```
* Gemini output (fix for markdown):

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

* **Conclusion/actions:** I changed the Vs to Ms in translation, fixing the first 2 errors, and then I changed the stop position from 118491 to 118490

## 5. Submit the updated assemblies
```
java -jar webin-cli-9.0.3.jar -username Webin-[XXXXX] -password [PASSWORD] -context genome -manifest Manifest_[species].txt -submit
```
