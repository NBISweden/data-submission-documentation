---
Redmine_issue: https://projects.nbis.se/issues/6716
Repository: ENA
Submission_type: RNAseq # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: Not applicable
---

# BGE - multiple species

## Submission task description
Submission of RNAseq raw reads for a mixture of species (45 in total) delivered 2026-02-27 to facilitate assembly and annotation as part of ERGA (https://www.erga-biodiversity.eu/) - BGE (https://biodiversitygenomics.eu/). 

Submission will be done via CNAG script and programmatic submission route using xml files produced by the script.

## Procedure overview and links to examples

* [BGE RNAseq metadata](./data/RNAseq-delivery_202026-02-27.xlsx)

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->

## Detailed step by step description

### Submit RNAseq 
#### Preparations
* Data producer provided me with a list of sample identifiers, via slack
* Data was delivered in two rounds, where the first round contained 90 paired reads from 44 species, and the second round only contained 2 paired reads (labelled with CNAG) from one species.
* With the data delivery we received checksum.md5 files containing a list of all files and the md5 sums
    * I asked Gemini to create a script to put paired read md5 sum information on one row, tab separated, which resulted in [reformat_md5.sh](./scripts/reformat_md5.sh)
* All cleaned and transformed metadata was collected in `BGE_sheet` tab of the  .xlsx file, while semi-formatted metadata from different sources was put in the other tabs.
* For some species, we have not created the project (done by CNAG  or Oslo), but I looked them up and verified the project accession number at ENA. For 2 of them, i was unable to access the project, **Eumannia arenbergeri (PRJEB105540)** and **Troglophilus ovuliformis (PRJEB96082)**.

* Sample ID gave BioSample ID via ERGA tracker portal. 
    * In most cases there was a 1-1 relationship between the samples
    * In some cases there were a pool of samples, but taken from same individual. In those cases I used the BioSample accession number for the origin sample, that the pool samples were derived from
    * In one case, ***O. puerlilis***, it was not possible to identify an origin, instead I had to crate a virtual sample, and also a new ToLID (**TODO**):
        * Requested a ToLID at https://id.tol.sanger.ac.uk/, referring to the original specimen IDs's. I expect to obtain `wjOphPuer20`.
        * I created [wjOphPuer-RNAseq-virtual-sample.tsv](./data/wjOphPuer-RNAseq-virtual-sample.tsv) and submitted via browser. Accession number received: `ERS29404660`

* All data files received in this batch were transferred using `lftp webin2.ebi.ac.uk -u Webin-39907` and `mput Sample*/*.fastq.gz`. Given the time limitations before project ends, and that there were 45 species delivered, I did not follow previous procedures of adding ToLID to the files using rename function in FileZilla. Instead I double and triple checked that the correct files was connected to the correct sample, before creating any .xml files.

#### XML
* I created [RNAseq-main.tsv](./data/RNAseq-main.tsv), excluding libraries YF-4364-RE032-2A (O. puerilis), YF-4364-RE069-1A (Eumannia arenbergeri), and YK-4511-CNAG-BGE-214-4447AK (Troglophilus ovuliformis)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f RNAseq-main.tsv -p ERGA-BGE -o RNAseq-main
    ```
* Remove row `<PAIRED/>` (error in script)
* I ensured that 'Illumina' is added to the library name and title, since the other data types have the platform named
* There are 2 lanes per species, i.e. 2 paired reads per experiment, which caused the script to create duplicate experiments. I removed these.
* Update RNAseq.exp.xml to reference accession number of previously registered studies (from `Species` tab in the .xlsx metadata file):
    ```
    <STUDY_REF accession=""/>
    ```
* All studies are already public, so submission.xml without hold date is used.
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@RNAseq-main.exp.xml" -F "RUN=@RNAseq-main.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2026-03-04T08:28:50.838Z" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX16161540" alias="exp_heTriNodu_Illumina_RNA-Seq_TnoduSample004_YF-4364-RE026-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161541" alias="exp_gfCryBron_Illumina_RNA-Seq_DSM_104551_18__DSM_104551_19__DSM_104551_20__DSM_104551_21_YF-4364-RE027-1A1-2-pool" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161542" alias="exp_qmNipGamm_Illumina_RNA-Seq_DE105_012_YF-4364-RE028-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161543" alias="exp_kaClaLepa_Illumina_RNA-Seq_FS42549324_YF-4364-RE029-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161544" alias="exp_kaMicSqua_Illumina_RNA-Seq_FS42549335_YF-4364-RE030-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161545" alias="exp_icLapAnag_Illumina_RNA-Seq_FS38819785_YF-4364-RE031-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161546" alias="exp_qqTroLibu_Illumina_RNA-Seq_FF03939993_FF03939999_YF-4364-RE033-2A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161547" alias="exp_qqRhoMagi_Illumina_RNA-Seq_H000528066_H000535907_YF-4364-RE034-2A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161548" alias="exp_qqStaHerc_Illumina_RNA-Seq_H000528904_YF-4364-RE035-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161549" alias="exp_inOsmFulv_Illumina_RNA-Seq_FS55571897_YF-4364-RE036-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161550" alias="exp_rTriTgu_Illumina_RNA-Seq_TT1_TT3_TT4_TT5_YF-4364-RE037-1A1-2-pool" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161551" alias="exp_icProCypr_Illumina_RNA-Seq_LV6000912292_YF-4364-RE038-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161552" alias="exp_qqAegCypr_Illumina_RNA-Seq_LV6000912370_YF-4364-RE039-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161553" alias="exp_qqAgeOrie_Illumina_RNA-Seq_LV6000912408_YF-4364-RE040-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161554" alias="exp_qqArtNeph_Illumina_RNA-Seq_LV6000659173_YF-4364-RE041-2A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161555" alias="exp_qqButKunt_Illumina_RNA-Seq_LV6000912364_LV6000912379_LV6000912355_YF-4364-RE042-1A2-4-pool" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161556" alias="exp_qqLycPrae_Illumina_RNA-Seq_LV6000912302_YF-4364-RE043-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161557" alias="exp_iqAioThal_Illumina_RNA-Seq_LV6000904914_YF-4364-RE044-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161558" alias="exp_iqDecAlbi_Illumina_RNA-Seq_LV6000905102_YF-4364-RE045-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161559" alias="exp_iqPlaFalx_Illumina_RNA-Seq_LV6000903691_YF-4364-RE046-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161560" alias="exp_iqSphRube_Illumina_RNA-Seq_LV6000908963_YF-4364-RE047-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161561" alias="exp_iyAntRoge_Illumina_RNA-Seq_LV6000659260_YF-4364-RE048-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161562" alias="exp_iyCatAphr_Illumina_RNA-Seq_LV6000912123_YF-4364-RE049-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161563" alias="exp_iyCerCypr_Illumina_RNA-Seq_LV6000912598_YF-4364-RE050-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161564" alias="exp_iyColCypr_Illumina_RNA-Seq_LV6000911862_YF-4364-RE051-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161565" alias="exp_ihConPter_Illumina_RNA-Seq_LV6000912627_YF-4364-RE052-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161566" alias="exp_iyEucMavr_Illumina_RNA-Seq_LV6000911915_YF-4364-RE053-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161567" alias="exp_icEutAnna_Illumina_RNA-Seq_LV6000912026_YF-4364-RE054-2A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161568" alias="exp_iyHalNico_Illumina_RNA-Seq_LV6000911861_YF-4364-RE055-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161569" alias="exp_iyMegPost_Illumina_RNA-Seq_LV6000912700_LV6000912692_YF-4364-RE056-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161570" alias="exp_iyMesBuce_Illumina_RNA-Seq_LV6000912124_YF-4364-RE057-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161571" alias="exp_iyMesOrie_Illumina_RNA-Seq_LV6000912109_YF-4364-RE058-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161572" alias="exp_icSteAust_Illumina_RNA-Seq_LV6000912687_YF-4364-RE059-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161573" alias="exp_ihAphHill_Illumina_RNA-Seq_LV6000904602_YF-4364-RE060-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161574" alias="exp_iyBomRudr_Illumina_RNA-Seq_LV6000905150_YF-4364-RE061-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161575" alias="exp_ihDacCocc_Illumina_RNA-Seq_LV6000903709_YF-4364-RE062-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161576" alias="exp_icScaAbbr_Illumina_RNA-Seq_LV6000905033_YF-4364-RE064-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161577" alias="exp_mMonMoa_Illumina_RNA-Seq_FS42549316_YF-4364-RE065-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161578" alias="exp_uoHydFoet_Illumina_RNA-Seq_TM2301_HydFoe_25-4-23_YF-4364-RE066-1A1-2-pool" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161579" alias="exp_icAgrGian_Illumina_RNA-Seq_LV6000912612_YF-4364-RE067-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161580" alias="exp_qdBraStyg_Illumina_RNA-Seq_LV6000914151_LV6000914150_YF-4364-RE068-2A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16161581" alias="exp_ilManCypr_Illumina_RNA-Seq_LV6000912707_YF-4364-RE070-1A" status="PRIVATE"/>
        <RUN accession="ERR16768420" alias="run_heTriNodu_Illumina_RNA-Seq_TnoduSample004_YF-4364-RE026-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768421" alias="run_heTriNodu_Illumina_RNA-Seq_TnoduSample004_YF-4364-RE026-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768422" alias="run_gfCryBron_Illumina_RNA-Seq_DSM_104551_18__DSM_104551_19__DSM_104551_20__DSM_104551_21_YF-4364-RE027-1A1-2-pool_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768423" alias="run_gfCryBron_Illumina_RNA-Seq_DSM_104551_18__DSM_104551_19__DSM_104551_20__DSM_104551_21_YF-4364-RE027-1A1-2-pool_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768424" alias="run_qmNipGamm_Illumina_RNA-Seq_DE105_012_YF-4364-RE028-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768425" alias="run_qmNipGamm_Illumina_RNA-Seq_DE105_012_YF-4364-RE028-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768426" alias="run_kaClaLepa_Illumina_RNA-Seq_FS42549324_YF-4364-RE029-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768427" alias="run_kaClaLepa_Illumina_RNA-Seq_FS42549324_YF-4364-RE029-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768428" alias="run_kaMicSqua_Illumina_RNA-Seq_FS42549335_YF-4364-RE030-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768429" alias="run_kaMicSqua_Illumina_RNA-Seq_FS42549335_YF-4364-RE030-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768430" alias="run_icLapAnag_Illumina_RNA-Seq_FS38819785_YF-4364-RE031-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768431" alias="run_icLapAnag_Illumina_RNA-Seq_FS38819785_YF-4364-RE031-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768432" alias="run_qqTroLibu_Illumina_RNA-Seq_FF03939993_FF03939999_YF-4364-RE033-2A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768433" alias="run_qqTroLibu_Illumina_RNA-Seq_FF03939993_FF03939999_YF-4364-RE033-2A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768434" alias="run_qqRhoMagi_Illumina_RNA-Seq_H000528066_H000535907_YF-4364-RE034-2A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768435" alias="run_qqRhoMagi_Illumina_RNA-Seq_H000528066_H000535907_YF-4364-RE034-2A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768436" alias="run_qqStaHerc_Illumina_RNA-Seq_H000528904_YF-4364-RE035-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768437" alias="run_qqStaHerc_Illumina_RNA-Seq_H000528904_YF-4364-RE035-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768438" alias="run_inOsmFulv_Illumina_RNA-Seq_FS55571897_YF-4364-RE036-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768439" alias="run_inOsmFulv_Illumina_RNA-Seq_FS55571897_YF-4364-RE036-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768440" alias="run_rTriTgu_Illumina_RNA-Seq_TT1_TT3_TT4_TT5_YF-4364-RE037-1A1-2-pool_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768441" alias="run_rTriTgu_Illumina_RNA-Seq_TT1_TT3_TT4_TT5_YF-4364-RE037-1A1-2-pool_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768442" alias="run_icProCypr_Illumina_RNA-Seq_LV6000912292_YF-4364-RE038-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768443" alias="run_icProCypr_Illumina_RNA-Seq_LV6000912292_YF-4364-RE038-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768444" alias="run_qqAegCypr_Illumina_RNA-Seq_LV6000912370_YF-4364-RE039-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768445" alias="run_qqAegCypr_Illumina_RNA-Seq_LV6000912370_YF-4364-RE039-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768446" alias="run_qqAgeOrie_Illumina_RNA-Seq_LV6000912408_YF-4364-RE040-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768447" alias="run_qqAgeOrie_Illumina_RNA-Seq_LV6000912408_YF-4364-RE040-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768448" alias="run_qqArtNeph_Illumina_RNA-Seq_LV6000659173_YF-4364-RE041-2A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768449" alias="run_qqArtNeph_Illumina_RNA-Seq_LV6000659173_YF-4364-RE041-2A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768450" alias="run_qqButKunt_Illumina_RNA-Seq_LV6000912364_LV6000912379_LV6000912355_YF-4364-RE042-1A2-4-pool_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768451" alias="run_qqButKunt_Illumina_RNA-Seq_LV6000912364_LV6000912379_LV6000912355_YF-4364-RE042-1A2-4-pool_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768452" alias="run_qqLycPrae_Illumina_RNA-Seq_LV6000912302_YF-4364-RE043-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768453" alias="run_qqLycPrae_Illumina_RNA-Seq_LV6000912302_YF-4364-RE043-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768454" alias="run_iqAioThal_Illumina_RNA-Seq_LV6000904914_YF-4364-RE044-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768455" alias="run_iqAioThal_Illumina_RNA-Seq_LV6000904914_YF-4364-RE044-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768456" alias="run_iqDecAlbi_Illumina_RNA-Seq_LV6000905102_YF-4364-RE045-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768457" alias="run_iqDecAlbi_Illumina_RNA-Seq_LV6000905102_YF-4364-RE045-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768458" alias="run_iqPlaFalx_Illumina_RNA-Seq_LV6000903691_YF-4364-RE046-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768459" alias="run_iqPlaFalx_Illumina_RNA-Seq_LV6000903691_YF-4364-RE046-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768460" alias="run_iqSphRube_Illumina_RNA-Seq_LV6000908963_YF-4364-RE047-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768461" alias="run_iqSphRube_Illumina_RNA-Seq_LV6000908963_YF-4364-RE047-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768462" alias="run_iyAntRoge_Illumina_RNA-Seq_LV6000659260_YF-4364-RE048-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768463" alias="run_iyAntRoge_Illumina_RNA-Seq_LV6000659260_YF-4364-RE048-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768464" alias="run_iyCatAphr_Illumina_RNA-Seq_LV6000912123_YF-4364-RE049-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768465" alias="run_iyCatAphr_Illumina_RNA-Seq_LV6000912123_YF-4364-RE049-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768466" alias="run_iyCerCypr_Illumina_RNA-Seq_LV6000912598_YF-4364-RE050-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768467" alias="run_iyCerCypr_Illumina_RNA-Seq_LV6000912598_YF-4364-RE050-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768468" alias="run_iyColCypr_Illumina_RNA-Seq_LV6000911862_YF-4364-RE051-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768469" alias="run_iyColCypr_Illumina_RNA-Seq_LV6000911862_YF-4364-RE051-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768470" alias="run_ihConPter_Illumina_RNA-Seq_LV6000912627_YF-4364-RE052-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768471" alias="run_ihConPter_Illumina_RNA-Seq_LV6000912627_YF-4364-RE052-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768472" alias="run_iyEucMavr_Illumina_RNA-Seq_LV6000911915_YF-4364-RE053-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768473" alias="run_iyEucMavr_Illumina_RNA-Seq_LV6000911915_YF-4364-RE053-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768474" alias="run_icEutAnna_Illumina_RNA-Seq_LV6000912026_YF-4364-RE054-2A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768475" alias="run_icEutAnna_Illumina_RNA-Seq_LV6000912026_YF-4364-RE054-2A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768476" alias="run_iyHalNico_Illumina_RNA-Seq_LV6000911861_YF-4364-RE055-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768477" alias="run_iyHalNico_Illumina_RNA-Seq_LV6000911861_YF-4364-RE055-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768478" alias="run_iyMegPost_Illumina_RNA-Seq_LV6000912700_LV6000912692_YF-4364-RE056-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768479" alias="run_iyMegPost_Illumina_RNA-Seq_LV6000912700_LV6000912692_YF-4364-RE056-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768480" alias="run_iyMesBuce_Illumina_RNA-Seq_LV6000912124_YF-4364-RE057-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768481" alias="run_iyMesBuce_Illumina_RNA-Seq_LV6000912124_YF-4364-RE057-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768482" alias="run_iyMesOrie_Illumina_RNA-Seq_LV6000912109_YF-4364-RE058-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768483" alias="run_iyMesOrie_Illumina_RNA-Seq_LV6000912109_YF-4364-RE058-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768484" alias="run_icSteAust_Illumina_RNA-Seq_LV6000912687_YF-4364-RE059-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768485" alias="run_icSteAust_Illumina_RNA-Seq_LV6000912687_YF-4364-RE059-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768486" alias="run_ihAphHill_Illumina_RNA-Seq_LV6000904602_YF-4364-RE060-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768487" alias="run_ihAphHill_Illumina_RNA-Seq_LV6000904602_YF-4364-RE060-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768488" alias="run_iyBomRudr_Illumina_RNA-Seq_LV6000905150_YF-4364-RE061-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768489" alias="run_iyBomRudr_Illumina_RNA-Seq_LV6000905150_YF-4364-RE061-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768490" alias="run_ihDacCocc_Illumina_RNA-Seq_LV6000903709_YF-4364-RE062-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768491" alias="run_ihDacCocc_Illumina_RNA-Seq_LV6000903709_YF-4364-RE062-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768492" alias="run_icScaAbbr_Illumina_RNA-Seq_LV6000905033_YF-4364-RE064-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768493" alias="run_icScaAbbr_Illumina_RNA-Seq_LV6000905033_YF-4364-RE064-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768494" alias="run_mMonMoa_Illumina_RNA-Seq_FS42549316_YF-4364-RE065-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768495" alias="run_mMonMoa_Illumina_RNA-Seq_FS42549316_YF-4364-RE065-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768496" alias="run_uoHydFoet_Illumina_RNA-Seq_TM2301_HydFoe_25-4-23_YF-4364-RE066-1A1-2-pool_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768497" alias="run_uoHydFoet_Illumina_RNA-Seq_TM2301_HydFoe_25-4-23_YF-4364-RE066-1A1-2-pool_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768498" alias="run_icAgrGian_Illumina_RNA-Seq_LV6000912612_YF-4364-RE067-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768499" alias="run_icAgrGian_Illumina_RNA-Seq_LV6000912612_YF-4364-RE067-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768500" alias="run_qdBraStyg_Illumina_RNA-Seq_LV6000914151_LV6000914150_YF-4364-RE068-2A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768501" alias="run_qdBraStyg_Illumina_RNA-Seq_LV6000914151_LV6000914150_YF-4364-RE068-2A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16768502" alias="run_ilManCypr_Illumina_RNA-Seq_LV6000912707_YF-4364-RE070-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16768503" alias="run_ilManCypr_Illumina_RNA-Seq_LV6000912707_YF-4364-RE070-1A_fastq_2" status="PRIVATE"/>
        <SUBMISSION accession="ERA35969685" alias="SUBMISSION-04-03-2026-08:28:44:550"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    ```
* I repeated the steps with [RNAseq-add.tsv](./data/RNAseq-add.tsv)
* Run script:
    ```
    ../../../../ERGA-submission/get_submission_xmls/get_ENA_xml_files.py -f RNAseq-add.tsv -p ERGA-BGE -o RNAseq-add
    ```
* Remove row `<PAIRED/>` (error in script)
* I removed duplicate experiments
* Update RNAseq.exp.xml to reference accession number of previously registered studies (from `Species` tab in the .xlsx metadata file):
    ```
    <STUDY_REF accession=""/>
    ```
* All studies are already public, so submission.xml without hold date is used.
* Submit using curl:
    ```
    curl -u username:password -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@RNAseq-add.exp.xml" -F "RUN=@RNAseq-add.runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```

* Receipt:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2026-03-05T13:21:05.737Z" submissionFile="submission.xml" success="true">
        <EXPERIMENT accession="ERX16167603" alias="exp_wjOphPuer_Illumina_RNA-Seq_FS38820316_FS38820317_YF-4364-RE032-2A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16167604" alias="exp_ilEumAren_Illumina_RNA-Seq_LV6000912183_YF-4364-RE069-1A" status="PRIVATE"/>
        <EXPERIMENT accession="ERX16167605" alias="exp_iqTroOvul_Illumina_RNA-Seq_ERGA_NT_0292_00001_YK-4511-CNAG-BGE-214-4447AK" status="PRIVATE"/>
        <RUN accession="ERR16774630" alias="run_wjOphPuer_Illumina_RNA-Seq_FS38820316_FS38820317_YF-4364-RE032-2A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16774631" alias="run_wjOphPuer_Illumina_RNA-Seq_FS38820316_FS38820317_YF-4364-RE032-2A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16774632" alias="run_ilEumAren_Illumina_RNA-Seq_LV6000912183_YF-4364-RE069-1A_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16774633" alias="run_ilEumAren_Illumina_RNA-Seq_LV6000912183_YF-4364-RE069-1A_fastq_2" status="PRIVATE"/>
        <RUN accession="ERR16774634" alias="run_iqTroOvul_Illumina_RNA-Seq_ERGA_NT_0292_00001_YK-4511-CNAG-BGE-214-4447AK_fastq_1" status="PRIVATE"/>
        <RUN accession="ERR16774635" alias="run_iqTroOvul_Illumina_RNA-Seq_ERGA_NT_0292_00001_YK-4511-CNAG-BGE-214-4447AK_fastq_2" status="PRIVATE"/>
        <SUBMISSION accession="ERA35973441" alias="SUBMISSION-05-03-2026-13:21:05:121"/>
        <MESSAGES/>
        <ACTIONS>ADD</ACTIONS>
    </RECEIPT>
    ```
* Add accession numbers & update status in SciLifeLab [sheet](https://docs.google.com/spreadsheets/d/1mSuL_qGffscer7G1FaiEOdyR68igscJB0CjDNSCNsvg/)

* **Note:** We haven't received (now or earlier delivery) any RNAseq data for Wirenia argentea, Cladocora caespitosa and Omalisus fontisbellaquei. However, the sequencing facility told me that these 3 species already had been sequenced before BGE started.