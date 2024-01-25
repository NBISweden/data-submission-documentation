---
Redmine_issue: https://projects.nbis.se/issues/6717
Repository: ENA
Submission_type: HiFi, RNAseq, genome assembly, mito assembly, symbiont assembly, umbrella
Data_generating_platforms:
- NGI, University of Antwerp
Top_level_acccession: https://www.ebi.ac.uk/ena/browser/view/PRJEB71963
---

# ERGA - *Stylops ater*

## Submission task description
Submission of HiFi and RNAseq data for *Stylops ater*, as part of the ERGA pilot project. Samples are already submitted to ENA/BioSample via COPO, so it is a matter of submitting raw reads and, when available, the assembly.

As it turned out, there are several assemblies, one annotated genome assembly, one mitochondrial assembly (unannotated), and 2 Wolbachia symbiont assemblies. At least the symbiont assemblies will be submitted in a separate project/study. Hence, an umbrella project, linking all related projects will also be created.

## Procedure overview and links to examples

### Links
* About [ERGA pilot](https://www.erga-biodiversity.eu/pilot-project)
* [Metadata template](./data/ERGA-Stylops-ater-metadata.xlsx)
* Our NBIS ENA brokering account will be used for submission
* Notes on how to [Create EMBL file](https://github.com/NBISweden/annotation-cluster/wiki/ENA-submission#create-embl-file)
* ENA docs on how to [register umbrella projects](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#umbrella-studies)

### Steps
* [Collect metadata](#metadata-collection) for study, experiments and assemblies
* Register [study](#submission-study)
* Prepare and submit [raw reads](#submission-raw-reads)
* Prepare and submit [genome assembly](#submission-genome-assembly)
    * [Update of genome assembly](#update-of-assembly)
* Prepare and submit [mito assembly](#submission-mito-assembly)
    * [Update of mito assembly study association](#update-of-mito-assembly-project-association)
* Prepare and submit [symbiont assemblies](#submission-symbionts)
* Prepare and submit an [umbrella project](#submission-umbrella-project)

**Note:** The list of steps do not fully follow in order (time wise), the update sub-steps came after submitting umbrella project, but I decided to keep things together in the documentation.

## Lessons learned
<!-- What went well? What did not went so well? What would you have done differently? -->
* There is no set convention on how to name experiments and studies, and since this is a re-ocurring type of submission it would have been nice to have a bit of documentation.
* It is more than likely that this submission's metadata will need to be updated later on, would have been nice to not have to remember to do this.
* Use the flag `-ascp` when submitting via Uppmax and Webin-CLI, also include some time when starting the interactive session, to enhance likelyhood of successful submission
* Learned how to submit mitochondrial assembly
* Learned how to handle symbionts, including registering a new taxonomy
* Learned how to create (and update) an umbrella project
* Learned how to update an already submitted assembly

## Detailed step by step description

### Metadata collection
* I created a google template, with study, HiFi-experiment, and RNA-experiment tabs
* The [metadata template](./data/ERGA-Stylops-ater-metadata.xlsx) was filled, looking at previous submissions on how to name things on study as well as experiment level, e.g. [PRJEB62720](https://www.ebi.ac.uk/ena/browser/view/PRJEB62720) (VR-EBP)
    * Experiments are named identifying the instrument, data type, and study, e.g.  ILLUMINA-RNA-StyAte1, PacBio-HiFi-StyAte1
    * Study title should mention `ERGA pilot`
* After conferring with a collegaue, it was decided that **locus tags** should have a naming convention of first three characters of the scientific name, in this case then `STYATE` 
* Sequencing facilites had to be contacted, in this case NGI and University of Antwerp, in order to receive the experiment metadata
-------------
### Submission study
* The study was submitted via the browser using our NBIS broker account, including a locus tag (STYATE), with a release date 2 years from now, receiving accession number `PRJEB70320`
-------------
### Submission raw reads
* **Decision**: Previously, for ERGA and VR-EBP, these types of submissions have been done using Webin-CLI also for the raw reads. Hence, I will create manifest files and submit from Uppmax.

* Three manifest files were created, based on the information in the metadata template: [HiFi](./data/PRJEB70320-bam-StyAte1-manifest.txt), [RNA 1](./data/PRJEB70320-paired-reads-StyAte1-manifest.txt) and [RNA 2](./data/PRJEB70320-paired-reads-StyAte2-manifest.txt)

* The manifest files were copied to Uppmax, to my home directory, using WinSCP
* I created a script for [Webin-CLI](./scripts/webin-cli-args.sh), that I also copied to home directory (ERGA-stylops)
* Run interactively on Uppmax: `interactive -A naiss2023-5-307`
* I did a validation first, then changed `validate` in the script with `submit`
* Broken pipe error, consulted with DS suggested using ascp flag and set time, hence:
  ```
  interactive -t 08:00:00 -A naiss2023-5-307
  module load ascp
  java -jar ../webin-cli-6.5.0.jar -ascp -context reads -userName $1 -password $2 -manifest $3 -outputDir Webin_output/ -submit
  ```
* HiFi: `ERX11689046`; `ERR12312109`
* RNA StyAte1: `ERX11689259`; `ERR12312322` 
* RNA StyAte2: `ERX11689261`; `ERR12312324`
-------------
### Submission genome assembly

#### Create EMBL file

* I copied the gff3 and fasta file to my local computer
* Then I tried using EMBLmyGFF3 script without exposing any variables, and do a validation:

```
conda activate py38
EMBLmyGFF3 ivStyAter.gff3.gz ivStyAter.fa --topology linear --molecule_type 'genomic DNA' --transl_table 1 --species "Stylops ater" --locus_tag STYATE --project_id PRJEB70320 -o PRJEB70320.embl
gzip PRJEB70320.embl
java -jar ../../../Downloads/webin-cli-6.5.0.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./PRJEB70320-assembly-manifest.txt -validate
```

Validation produced some errors, so some settings are needed for the EMBLmyGFF3 script

```
conda activate py38
EMBLmyGFF3 --expose_translations
```
Added the following to [translation_gff_feature_to_embl_qualifier.json](./data/translation_gff_feature_to_embl_feature.json) file:
```
"exon": {
    "remove": true
}
```

A rerun of EMBLmyGFF3 and Webin-CLI validation showed error messages regarding four duplicated introns (I copy/pasted the parts of concern from the embl file):

```
ERROR: "intron" Features locations are duplicated - consider merging qualifiers. [ line: 3069 of PRJEB70320.embl.gz,  line: 3044 of PRJEB70320.embl.gz]

FT   intron          complement(278202..278261)
FT                   /locus_tag="STYATE_LOCUS82"
FT                   /note="ID:STYATI00000000294"
FT                   /note="source:AUGUSTUS"

FT   intron          complement(278202..278261)
FT                   /locus_tag="STYATE_LOCUS83"
FT                   /note="ID:STYATI00000000296"
FT                   /note="source:GeneMark.hmm3"

ERROR: "intron" Features locations are duplicated - consider merging qualifiers. [ line: 89261 of PRJEB70320.embl.gz,  line: 89235 of PRJEB70320.embl.gz]

FT   intron          complement(3723618..3723852)
FT                   /locus_tag="STYATE_LOCUS1091"
FT                   /note="ID:STYATI00000006245"
FT                   /note="source:GeneMark.hmm3"

FT   intron          complement(3723618..3723852)
FT                   /locus_tag="STYATE_LOCUS1092"
FT                   /note="ID:STYATI00000006246"
FT                   /note="source:AUGUSTUS"

ERROR: "intron" Features locations are duplicated - consider merging qualifiers. [ line: 507982 of PRJEB70320.embl.gz,  line: 507960 of PRJEB70320.embl.gz]

FT   intron          complement(23248..23643)
FT                   /locus_tag="STYATE_LOCUS3435"
FT                   /note="ID:STYATI00000020452"
FT                   /note="source:GeneMark.hmm3"

FT   intron          complement(23248..23643)
FT                   /locus_tag="STYATE_LOCUS3436"
FT                   /note="ID:STYATI00000020453"
FT                   /note="source:AUGUSTUS"

ERROR: "intron" Features locations are duplicated - consider merging qualifiers. [ line: 941367 of PRJEB70320.embl.gz,  line: 941347 of PRJEB70320.embl.gz]

FT   intron          626992..628637
FT                   /locus_tag="STYATE_LOCUS5810"
FT                   /note="ID:STYATI00000033917"
FT                   /note="source:AUGUSTUS"

FT   intron          626992..628637
FT                   /locus_tag="STYATE_LOCUS5811"
FT                   /note="ID:STYATI00000033918"
FT                   /note="source:GeneMark.hmm3"
```
I asked the bioinformatician who produced the assembly for assistance, who in turn removed the problematic 4 introns by hand. All of them were produced by GeneMark and all of them were "single-intron" genes.

```
conda activate py38
EMBLmyGFF3 ivStyAter_cur01.gff3.gz ivStyAter.fa --topology linear --molecule_type 'genomic DNA' --transl_table 1 --species "Stylops ater" --locus_tag STYATE --project_id PRJEB70320 -o PRJEB70320.embl
gzip PRJEB70320.embl
java -jar ../../../Downloads/webin-cli-6.5.0.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./PRJEB70320-assembly-manifest.txt -validate
java -jar ../../../Downloads/webin-cli-6.5.0.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./PRJEB70320-assembly-manifest.txt -submit
```

* Accession number `ERZ21966249`
* Confirmation from ENA:
    ```
    ASSEMBLY_NAME | ASSEMBLY_ACC | STUDY_ID | SAMPLE_ID | CONTIG_ACC | SCAFFOLD_ACC | CHROMOSOME_ACC
    StyAte-assembly | GCA_963692825 | PRJEB70320 | ERS10521290 | CAVNYM010000001-CAVNYM010000021 |  |
    ```

#### Update of assembly
* **Note:** I later learned that also the attribute json file should be updated before using EMBLmyGFF3 (see further how to [create EMBL file](https://github.com/NBISweden/annotation-cluster/wiki/ENA-submission#create-embl-file)). After conferring with data steward colleague and bioinformatician, it was concluded that this should be done and result in an update of the assembly.

* I updated the [attribute file](./data/translation_gff_attribute_to_embl_qualifier.json) with the following:
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
* **Note:** There is a third json file in the repo, [translation_gff_other_to_embl_qualifier.json](./data/translation_gff_other_to_embl_qualifier.json), but this one is not necessary to update.

* Then created a new embl flat file:
    ```
    conda activate py38
    EMBLmyGFF3 ivStyAter_cur01.gff3.gz ivStyAter.fa --topology linear --molecule_type 'genomic DNA' --transl_table 1 --species "Stylops ater" --locus_tag STYATE --project_id PRJEB70320 -o PRJEB70320-v2.embl
    gzip PRJEB70320-v2.embl
    ```
* ENA [how to update assembly](https://ena-docs.readthedocs.io/en/latest/update/assembly.html)
    * Especially notice: "*The Webin-CLI manifest format includes an ‘ASSEMBLYNAME’ field. This must be unique in each of your submissions, whether they are updates or new assemblies.*"
    * It does not say if all metadata needs to be in the new (updated) manifest, but I will keep everything and only give a new assembly name (`StyAte-assembly-v2`).
    * New manifest: [PRJEB70320-assembly-update-manifest.txt](./data/PRJEB70320-assembly-update-manifest.txt)
* I did a validation round first, then submit:
    ```
    java -jar ../../../Downloads/webin-cli-6.5.0.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./PRJEB70320-assembly-update-manifest.txt -validate
    java -jar ../../../Downloads/webin-cli-6.5.0.jar -ascp -context genome -userName Webin-XXXXX -password 'YYYYY' -manifest ./PRJEB70320-assembly-update-manifest.txt -submit
    ```
* New accession: `ERZ22382298` (let's wait and see what ENA does with this)
-------------
### Submission mito assembly

* [PRJEB70320-mito-assembly-manifest.txt](./data/PRJEB70320-mito-assembly-manifest.txt)
```
java -jar ../../../Downloads/webin-cli-6.5.0.jar -ascp -context genome -userName Webin-XXX -password 'YYY' -manifest ./PRJEB70320-mito-assembly-manifest.txt -validate
```

* This didn't work, `ERROR: Invalid number of sequences : 1, Minimum number of sequences for CONTIG is: 2`
* ENA guidelines says the following about [contig assembly](https://ena-docs.readthedocs.io/en/latest/submit/assembly/genome.html#contig-assembly): `"If you do not have a minimum of 2 contigs, then you will need to submit at a higher assembly level."`
* I asked a colleague who has done this previously on how to, who said that a [chromosome assembly](https://ena-docs.readthedocs.io/en/latest/submit/assembly/genome.html#chromosome-assembly) submission is the way to go:
    * The manifest needs one additional file, therein referenced as `CHROMOSOME_LIST: chromosome_list.txt.gz`
    * In this [chromosome_list.txt](./data/chromosome_list.txt.gz), a single row is added `ptg000007l_rotated	MIT	Linear-Chromosome	Mitochondrion`
    * The [naming convention](https://ena-docs.readthedocs.io/en/latest/submit/fileprep/assembly.html#chromosome-list-file):
        * The value in the initial row (ptg000007l_rotated) must be the same as referenced in the corresponding fasta file (after the >).
        * The second value MIT is a standard abbreviation of the Mitochondria in CHROMOSOME_NAME format
        * The third value refers to the CHROMOSOME_TYPE input with an optional Linear modifier as the mitochondria is submitted as a linear sequence.
        * The fourth value is optional and refers to the CHROMOSOME_LOCATION for which ENA has pre-defined values.

* I repeated the validation successfully, then ran: 

    ```
    java -jar ../../../Downloads/webin-cli-6.5.0.jar -ascp -context genome -userName Webin-XXX -password 'YYY' -manifest ./PRJEB70320-mito-assembly-manifest.txt -submit
    ```

* Accession number `ERZ21966604`

#### Update of mito assembly study association

* I did not receive a confirmation about the mito assembly, and there are concerns if we really can put the mito assembly in the same project as the genome assembly since they are referring to the same sample.
* When looking into how to update the genome assembly, I found the following text in ENAs [Updating assemblies](https://ena-docs.readthedocs.io/en/latest/update/assembly.html): *"To submit an assembly update, make sure you reference the same study and sample accessions as were used in the original submission. **In fact, this study-sample pair is unique to your assembly and is the means by which you submission is recognised as an update rather than a new assembly**."* I can only conclude that since the mito assemblies uses the same sample, we need to associate this assembly with another study/project.
* Looking at ENAs [Analysis edits](https://ena-docs.readthedocs.io/en/latest/update/metadata/interactive.html#analysis-edits) on how to update the metadata for an assembly, at point 7: *"The most common analysis edit would be to change the <PRIMARY_ID> and <SECONDARY_ID> where the analysis is pointing at the wrong study"*, makes me think that it is doable.

* Hence the following steps are needed:
1. Create a new study
1. Update the mito assembly metadata with new project id
1. Update the umbrella project, adding the new project id

##### Create a new study
* The following information was added:
    * `Title` - `Stylops ater mitochondrial assembly`
    * `Abstract` - `This project provides the mitochondrial assembly data for Stylops ater.`
    * `Study name` - `mito-StyAte1`
    * `Release date` - `2025-11-21`
* Received accession number - `PRJEB71993` 

##### Update mito assembly object
* Logged in to [Webin Portal](https://www.ebi.ac.uk/ena/submit/webin/login) and selected the ‘Analyses Report’ button 
* Clicked ‘Action’ button of analysis `ERZ21966604` and selected ‘Edit analysis XML’
* Changed the STUDY_REF `accession` from `ERP155255` to `ERP156779`
* Changed the STUDY_REF `PRIMARY_ID` from `ERP155255` to `ERP156779`
* Changed the STUDY_REF `SECONDARY_ID` from `PRJEB70320` to `PRJEB71993`
* Clicked on Save

##### Update the umbrella project

* Copied the xml files used for registering the umbrella project (detailed below) and renamed them to [submission-add-mito.xml](./data/submission-add-mito.xml) and [umbrella-add-mito.xml](./data/umbrella-add-mito.xml)
* Changed the `ADD` action to `MODIFY` in the new submission file
* Added another child in the new umbrella file:
    ```
    <RELATED_PROJECT>
        <CHILD_PROJECT accession="PRJEB71993"/>
    </RELATED_PROJECT>

    ```
* **Note:** I kept everything else the same as in original files (hold date and the first two children), fearing that otherwise there will be unintentional updates / removals, but I later learnt that this is not necessary.
* Submit using curl:
    ```
    curl -u Username:Password -F "SUBMISSION=@submission-add-mito.xml" -F "PROJECT=@umbrella-add-mito.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```

    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-01-22T11:31:46.093Z" submissionFile="submission-add-mito.xml" success="true">
     <PROJECT accession="PRJEB71963" alias="all-StyAte1" status="PRIVATE" holdUntilDate="2025-11-21Z"/>
     <SUBMISSION accession="" alias="SUBMISSION-22-01-2024-11:31:45:883"/>
     <MESSAGES>
          <INFO>The XML md5 checksum for the object being updated has not changed. No update required for PRJEB71963.</INFO>
     </MESSAGES>
     <ACTIONS>MODIFY</ACTIONS>
     <ACTIONS>HOLD</ACTIONS>
    </RECEIPT>
    ```
    Does this mean that the child wasn't added? I need to access the umbrella project programatically and see what is in the umbrella project, perhaps the action should have been another one in the submission file...

**Exploring how to see what is submitted in umbrella**
```
curl -u Username:Password -X 'GET' 'https://www.ebi.ac.uk/ena/submit/drop-box/projects/PRJEB71963'
```
Only gives the umbrella metadata, not which children have been added:
```
<PROJECT_SET>
  <PROJECT accession="PRJEB71963" alias="all-StyAte1"
            broker_name="National Bioinformatics Infrastructure Sweden"
            center_name="National Bioinformatics Infrastructure Sweden">
      <IDENTIFIERS>
         <PRIMARY_ID>PRJEB71963</PRIMARY_ID>
         <SUBMITTER_ID namespace="National Bioinformatics Infrastructure Sweden">all-StyAte1</SUBMITTER_ID>
      </IDENTIFIERS>
      <TITLE>Stylops ater umbrella project, ERGA pilot</TITLE>
      <DESCRIPTION>This project connects the sequencing and assembly data of Stylops ater (host), with two Wolbachia sp. symbionts. The project is part of the  ERGA pilot (https://www.erga-biodiversity.eu/pilot-project).</DESCRIPTION>
      <UMBRELLA_PROJECT/>
  </PROJECT>
</PROJECT_SET>
```
* I've asked ENA (on ELIXIR Slack) for guidance. I got a confirmation that all three children are connected to the umbrella project. Also, at the moment it is not possible for people outside of ENA to query ENA directly themselves, but this will be raised as a desired feature to implement in the future.

**Note:**
* I was notified by the responsible bioinformatician that an improved mito assembly will be made, so there will be an update of the submission:
    * Create new manifest, with new assembly name and the new assembly file
    * Submit using Webin-CLI
-------------
### Submission symbionts

2 complete wolbachia symbionts was also found. It was initially unlcear if they should be uploaded as well but Sanger people says yes.

* Example symbiont accession [PRJEB49039](https://www.ebi.ac.uk/ena/browser/view/PRJEB49039)

* [ENA on registering taxonomy](https://ena-docs.readthedocs.io/en/latest/faq/taxonomy_requests.html)

#### Suggested steps

1. Register a new taxonomy
1. Register a project/study
1. Register 2 (?) samples with fields `sample symbiont of` (with the sample accession of host) and `symbiont` (set to 'Y')
1. Submit assemblies
1. Register an umbrella project at ENA using programmatic submission

#### Register a new taxonomy

For the actual registration it seems straightforward, login to ENA and go to [Register taxonomy](https://www.ebi.ac.uk/ena/submit/webin/taxonomy) in the Samples menu. However, what would the Name type be, Novel species?

![taxa form](./images/register-taxonomy-1.png)
![name type](./images/taxonomy-name-type.png)

* Instructions from ENA:
    * `proposed_name`: the organism name (mandatory). We will check if there is a taxa registered with the given name.
    * `name_type`: allowed taxon name types are
        * Environmental Name
        * Synthetic Name
        * Novel Species
        * Unidentified Species
        * Published Name
    * `host`: host associated with the taxon, if applicable
    * `project_id`: project associated with the taxa, if applicable
    * `description`: a short description of the taxon, please provide an authority or publication where available, or any other information describing the organism


    **Applied:**
    ```
    Proposed name: Wolbachia endosymbiont of Stylops ater
    Name type: Unindentified Species
    Host: Stylops ater
    Project Id: PRJEB70320
    Taxonomy description: Hertig, M. "The rickettsia, Wolbachia pipientis (gen. et sp. n.) and associated inclusions of the mosquito, Culex pipiens." Parasitol. (1936) 28:453-486.
    ```

    * Approved (took about 1 month) but the email confirmation (and the auto-reply) was only sent to the main correspondent of the broker account. Taxid: `3109628` Organism/scientific name: `Wolbachia endosymbiont of Stylops ater`

#### Register study

* Release date was set to the same as for the genome project (2025-11-21)
* The details registered is in the ENA_study tab of the [metadata template](./data/ERGA-Stylops-ater-metadata.xlsx)
* Accession number received: `PRJEB71935`

#### Register samples

* Submitted two samples (w1-StyAte and w2-StyAte), one for each assembly by uploading sample sheet [PRJEB71935-symbiont-samples.tsv](./data/PRJEB71935-symbiont-samples.tsv) 
    * w1-StyAte accession number: `ERS17750876` 
    * w2-StyAte accession number: `ERS17750877`

#### Submit assemblies

* I created two manifest files:
    * [PRJEB71935-Wolbachia-assembly-1-manifest.txt](./data/PRJEB71935-Wolbachia-assembly-1-manifest.txt)
    * [PRJEB71935-Wolbachia-assembly-2-manifest.txt](./data/PRJEB71935-Wolbachia-assembly-2-manifest.txt)

* When validating the first assembly, I received an error message that there was only one contig, and a higher level of submission was required. I repeated the steps of the mitochondrial assembly submission and created chromosome_lists ([wolbachia1-chromosome_list](./data/wolbachia1-chromosome_list.txt.gz), [wolbachia2-chromosome_list](./data/wolbachia2-chromosome_list.txt.gz)), with information `wolbachia_strain1	strain1	Linear-Chromosome` and `wolbachia_strain2	strain2	Linear-Chromosome`, respectively.

* Submission command (for the first assembly): 
    ```
    java -jar ../../../Downloads/webin-cli-6.5.0.jar -ascp -context genome -userName Webin-XXX -password 'YYY' -manifest ./PRJEB71935-Wolbachia-assembly-1-manifest.txt -submit
    ```
* Received accession numbers: assembly-1 - `ERZ22353165`, assembly-2 - `ERZ22353209`
-------------
### Submission umbrella project

* Umbrella at ENA [how to](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#umbrella-studies)
* Study metadata is in the [metadata template](./data/ERGA-Stylops-ater-metadata.xlsx), the release date set to same as che child projects.
* Created 2 xml files: [submission.xml](./data/submission.xml) and [umbrella.xml](./data/umbrella.xml)
* Submitted using curl:
```
curl -u Username:Password -F "SUBMISSION=@submission.xml" -F "PROJECT=@umbrella.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
```
* Receipt:
```
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
<RECEIPT receiptDate="2024-01-19T14:29:08.589Z" submissionFile="submission.xml" success="true">
     <PROJECT accession="PRJEB71963" alias="all-StyAte1" status="PRIVATE" holdUntilDate="2025-11-21Z"/>
     <SUBMISSION accession="ERA27991918" alias="SUBMISSION-19-01-2024-14:29:08:427"/>
     <MESSAGES>
          <INFO>All objects in this submission are set to private status (HOLD).</INFO>
     </MESSAGES>
     <ACTIONS>ADD</ACTIONS>
     <ACTIONS>HOLD</ACTIONS>
</RECEIPT>
```
* Received accession number: `PRJEB71963`

* **Note:** according to [ENA documentation on umbrella](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#releasing-umbrella-studies): "*Umbrella studies do not appear in the list of studies shown in your Webin account.*"