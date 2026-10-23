# Background
The gff format outputted from GeSeq annotation tool, does not harmonize well with the EMBLmyGFF3 used for creating embl files. Hence, I decided to use AGAT on all 17 gff3 files.
*Note: This will likely NOT fix what is wrong with L Leonii and L bienne, but the other 15 assemblies (with wrong locus tag indexes) might work*
AGAT can e.g. sort the features according to strand position, add 'Parent=' on CDS when missing (resolving orphan CDS), etc.

# Steps
* Work on nac-login, where AGAT can be accessed
* Run `agat_convert_sp_gxf2gxf.pl` on all gff files:
    ```
    source ~/conda_init.sh
    conda activate /home/lucso605/.conda/envs/agat
    agat_convert_sp_gxf2gxf.pl -g GeSeqJob-20260401-113716_Laustriacum_GFF3.gff3 -o Laustriacum-agat.gff
    agat_convert_sp_gxf2gxf.pl -g GeSeqJob-20260401-135929-bienne-GeSeq-20260401_Lbiene_GFF3.gff3 -o Lbienne-agat.gff
    agat_convert_sp_gxf2gxf.pl -g GeSeqJob-20260401-135929_Lnarbonense_GFF3.gff3 -o Lnarbonense-agat.gff
    agat_convert_sp_gxf2gxf.pl -g GeSeqJob-20260401-135929_Lperenne_GFF3.gff3 -o Lperenne-agat.gff
    agat_convert_sp_gxf2gxf.pl -g GeSeqJob-20260401-140352_Lcampanulatum_GFF3.gff3 -o Lcampanulatum-agat.gff
    agat_convert_sp_gxf2gxf.pl -g GeSeqJob-20260401-140352_Lcapitatum_GFF3.gff3 -o Lcapitatum-agat.gff
    agat_convert_sp_gxf2gxf.pl -g GeSeqJob-20260401-140352_Lflavum_GFF3.gff3 -o Lflavum-agat.gff
    agat_convert_sp_gxf2gxf.pl -g GeSeqJob-20260401-140352_Lgrandiflorum_thrum_GFF3.gff3 -o Lgrandiflorum_thrum-agat.gff
    agat_convert_sp_gxf2gxf.pl -g GeSeqJob-20260401-140352_Lhirsutum_GFF3.gff3 -o Lhirsutum-agat.gff
    agat_convert_sp_gxf2gxf.pl -g GeSeqJob-20260401-140352_Lmaritimum_thrum_GFF3.gff3 -o Lmaritimum_thrum-agat.gff
    agat_convert_sp_gxf2gxf.pl -g GeSeqJob-20260401-140352_Lsuffruticosum_thrum_GFF3.gff3 -o Lsuffruticosum_thrum-agat.gff
    agat_convert_sp_gxf2gxf.pl -g GeSeqJob-20260401-140352_Ltauricum_GFF3.gff3 -o Ltauricum-agat.gff
    agat_convert_sp_gxf2gxf.pl -g GeSeqJob-20260401-140352_Lteniufolium_GFF3.gff3 -o Lteniufolium-agat.gff
    agat_convert_sp_gxf2gxf.pl -g GeSeqJob-20260401-140352_Ltenue_GFF3.gff3 -o Ltenue-agat.gff
    agat_convert_sp_gxf2gxf.pl -g GeSeqJob-20260401-140352_Lthracicum_GFF3.gff3 -o Lthracicum-agat.gff
    agat_convert_sp_gxf2gxf.pl -g GeSeqJob-20260401-140352_Ltrigynum_GFF3.gff3 -o Ltrigynum-agat.gff
    agat_convert_sp_gxf2gxf.pl -g GeSeqJob-20260401-151120_Lleonii_GFF3.gff3 -o Lleonii-agat.gff
    ```
* Copy the *agat.gff files to laptop, run EMBLmyGFF3 from there, see script [runEMBLmyGFF.sh](./scripts/runEMBLmyGFF.sh)
* Typical warnings and errors which might be needen to fix before running the script:
    ```
    15:06:44 ERROR feature: >>region<< is not a valid EMBL feature type. You can ignore this message if you don't need the feature.
                        Otherwise tell me which EMBL feature it corresponds to by adding the information within the json mapping file.
    15:06:44 WARNING feature: Unknown qualifier 'gbkey' - skipped                  ]
    15:06:44 WARNING feature: The qualifier >mol_type< is mandatory for the feature >source<. We will not report the feature.
    15:06:44 WARNING feature: The qualifier >organism< is mandatory for the feature >source<. We will not report the feature.
    15:06:44 ERROR feature: >>sequence_feature<< is not a valid EMBL feature type. You can ignore this message if you don't need the feature.
                            Otherwise tell me which EMBL feature it corresponds to by adding the information within the json mapping file.
    15:06:44 ERROR feature: >>RNA<< is not a valid EMBL feature type. You can ignore this message if you don't need the feature.
                            Otherwise tell me which EMBL feature it corresponds to by adding the information within the json mapping file.
    15:06:44 ERROR feature: >>inverted_repeat<< is not a valid EMBL feature type. You can ignore this message if you don't need the feature.
                            Otherwise tell me which EMBL feature it corresponds to by adding the information within the json mapping file.
    ```
* I updated the `translation_gff_feature_to_embl_feature.json` file:
    ```
    "exon": {
        "remove": true
    },
    "intron": {
        "remove": true
    },
    "transcript": {
        "target": "mRNA"
    },
    "sequence_feature": {
        "remove": true
    },
    "inverted_repeat": {
        "target": "repeat_region"
    },
    "region": {
        "target": "source"
    }
    ```
* I updated the `translation_gff_attribute_to_embl_qualifier.json` file:
    ```
    "gbkey": {
        "target": "note",
        "prefix": "gbkey:"
    }
    ```
* I also added organism and mol_type information in the region line of the gff files, by using `sed`, see [addOrganismMoltype.sh](./scripts/addOrganismMoltype.sh)
* AGAT has added some 'RNA' i.e. not mRNA, not sure why but these should be updated to mRNA it seems (I *hink* it is because these did not have a CDS, only introns and exons, not sure if it is correct to change to mRNA, Gemini suggested me to map RNA to ncRNA instead, but is this valid? when doing so I ended up with other issues about the need to have ncRNA class). 

* In the end this venue was abandoned, AGAT will not help with our issues. Will try some other way but will keep this documentation.
