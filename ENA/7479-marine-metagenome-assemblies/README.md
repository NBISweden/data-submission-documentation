---
Redmine_issue: https://projects.nbis.se/issues/7479
Repository: ENA
Submission_type: metagenome, assembly # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB59221
---

# 7490 - Marine metagenome assemblies submission

## Submission task description
Marine metagenome samples were taken from the Roskilde fjord ouside of Denmark. Data includes metagenomic and metatranscriptomic sequences, as well as assemblies produced from those sequences.

This subission was initiated by one data steward, who registered the study, submitted the raw data, and prepared the assembly submissions. It was then continued by another data steward, who did the assembly submissions. The documentation will cover the assembly submission part.

The paper is already published, <https://doi.org/10.1093/ismeco/ycad016>.

## Procedure overview and links to examples

* Example submissions to look at

  * Metagenomic study: https://www.ebi.ac.uk/ena/browser/view/PRJEB34883?show=xrefs
  * Metatranscriptomic study: https://www.ebi.ac.uk/ena/browser/view/PRJEB36728?show=xrefs

## Lessons learned
* How to create virtual samples in order to be able to submit multiple assemblies to one project, and using a special checklist for binned samples ([ERC000050 ENA binned metagenome](https://www.ebi.ac.uk/ena/browser/view/ERC000050)).
* How to write scripts and use sbatch instead of interactive session at Uppmax
* Use nobackup folder of the project rather than my own home folder when submitting large number of assemblies, since ENA wants to write a lot of reports (my disk quota exceeded...)
* When having issues with disk quota, I also tried using the latest version of Webin-CLI (7.3.0) but that gave me taxonomy errors so I reverted to using version 7.0.1 instead.

## Detailed step by step description

**Table of contents**
* [Study registration](#study-registration)
* [Sample registration](#sample-registration)
    * [Submission steps - co-assembly samples](#submission-steps---co-assembly-samples)
    * [Submission steps - binned samples](#submission-steps---binned-samples)
* [Experiment registration](#experiment-registration)
* [Assemblies](#assemblies)
    * [Submit primary and co-assemblies](#submit-primary-and-co-assemblies)
    * [GZip script](#gzip-script)
    * [Submit binned assemblies](#submit-binned-assemblies)

### Study registration
All data, raw reads as well as all the assemblies, will be collected under one project/study at ENA, since the paper is already published and only one project is referred to from there.

* Accession number received: `PRJEB59221`
* Temporary release date, to be updated when all submission is done: `2025-04-24`

### Sample registration

There are 3 types of sample metadata, gathered in separate tabs in [samples-metadata.xlsx](./data/samples-metadata.xlsx), a well as the tsv files submitted to ENA:
* [samples-water.tsv](./data/samples-water.tsv) - 41 samples for the raw reads (already submitted)
  * The raw reads consist of 17 samples of `metagenome Roskilde fjord, Denmark`, 12 samples of `metatranscriptome Roskilde fjord, Denmark`, and 12 samples of `16S amplicon Roskilde fjord, Denmark`.
  * Checklist [ERC000024 GSC MIxS water](https://www.ebi.ac.uk/ena/browser/view/ERC000024) was used
  * Accession numbers at ENA is in a separate tab of the samples-metadata file
* [samples-coassembly.tsv](./data/samples-coassembly.tsv) - 3 samples for the co-primary assemblies
    * To be submitted
* [samples-binned.tsv](./data/samples-binned.tsv) - 2180 samples for the binned assemblies
    * To be submitted

#### Submission steps - co-assembly samples

* Since these samples are not really binned, even if virtual, I decided to use the same checklist as for the water samples, i.e. `ERC000024 GSC MIxS water` (it seems to have been prepared for this, as well).
* I formatted the [samples-coassembly.tsv](./data/samples-coassembly.tsv) file header according to checklist (added a units line as well as the initial line telling which checklist is used)
* I removed the units from columns `Size Fraction Lower Threshold` and `Size Fraction Upper Threshold`
* These co-assembly samples needs to be submitted previous to the binned ones, since the binned ones are derived from these and thus the accession numbers are needed.
* I received an error when uploading the tsv file, will try again later
    * After logout and then login, submission was successful
    * Received accession numbers are added to a separate tab of the samples-metadata file

#### Submission steps - binned samples

* Decide which checklist to use for the binned, derived, samples. There is a checklist [ERC000050 ENA binned metagenome](https://www.ebi.ac.uk/ena/browser/view/ERC000050)
* Match the headers from the original `samples-binned.tsv` with the downloaded [checklist](./data/Checklist_ENA-binned%20metagenome_1719325121537.tsv)
    * I formatted the tsv file header according to checklist (added a units line as well as the initial line telling which checklist is used)
    * Some headers were updated to ENA naming convention
    * I had concerns about `Denmark` as `geographic location (country and/or sea)` value, but the `Roskilde fjord` is not available in the controlled vocabulary
    * `sample derived from` needs to be accession numbers not aliases, hence I had to update them
        * **NOTE: the co-samples needs to be submitted first in order to complete the task**
    * Check with researcher if recommended fields missing can be filled: `completeness score`, `contamination score`, and `assembly quality`
    * 2 of 3 was filled by researcher.
* I updated the sample descriptions according to [ENA docs registering-binned-samples](https://ena-docs.readthedocs.io/en/latest/submit/assembly/metagenome/binned.html#registering-binned-samples), so that it says `This sample represents a metagenomic bin from the metagenomic sample ERSXXXXX` rather than `binned sample` only.
* `binning software` is recommended to have a persistent ID (description text in the checklist), so I updated the values to `MetaBAT2 v2.14 (biotools:MetaBAT_2)`. 
* Researcher declined to fill `assembly quality`, but wanted to include user-defined columns `Genome size (bp)`, `# contigs`, `N50 (contigs)`, and `Longest contig (bp)`, so that reusers can judge for themselves.
* Binned samples were submitted by uploading file [samples-binned.tsv](./data/samples-binned.tsv), created by copy&paste from [samples-metadata.xlsx](./data/samples-metadata.xlsx)
    * Received accession numbers are added to a separate tab of the samples-metadata file

### Experiment registration

Experiments were already submitted, the metadata and received accession numbers are collected in [experiment-metadata.xlsx](./data/experiment-metadata.xlsx)

### Assemblies

There are 3 types of assemblies: primary (17), co-primary (3) (consisting of different combinations of primary assemblies), and binned (2180). The assembly metadata and received accession numbers are collected in [assemblies-metadata.xlsx](./data/assemblies-metadata.xlsx)

* For all assemblies the accession numbers of the raw data, `RUN_REF` column, was added

#### Submit primary and co-assemblies
* Program [create-assembly-manifest.c](./scripts/create-assembly-manifest.c) was used to create the primary assembly manifest files:

    ```
    ../../scripts/create-assembly-manifest primary-metagenomes.tsv 1 > submit-primary-assemblies.sh
    ```
    * **Note:** primary-metagenomes.tsv was created by doing a copy and paste from the assemblies-metadata file. ***Important that there are no blank rows in the end of the tsv file, as this will cause a duplication of the last webin-cli command.*** The second argument of the script is the column to be used for creating the output/manifest file name, i.e. `SAMPLE` in this case. The program prints Webin-CLI commands to stdout, captured in submit-primary-assemblies.sh. 
    * Example of manifest output: [example-manifest.txt](./data/example-manifest.txt)

* The script file needs to be updated with an initial line `#!/bin/sh`, and replace $1 with username, $2 with password, and $3 with validate or submit.
* All manifest files and the script file were put in a folder and copied to Uppmax, and the script was run first with validate, and then with submit:
    ```
    scp primary-assemblies-manifests/* yvonnek@rackham.uppmax.uu.se:/home/yvonnek/7479-marine-metagenome/primary-assemblies-manifests/
    interactive -t 08:00:00 -A naiss2024-22-345
    ./submit-primary-assemblies.sh username password validate
    ./submit-primary-assemblies.sh username password submit
    ```
* It turns out that the fasta assembly files needs to be gzipped, hence I needed to update the tsv file, create new manifests, and create a script that gzipped all files (see [section below](#gzip-script)).

* The submission then (mostly) went without any hickups, the accession numbers have been added in a separate tab [assemblies-metadata.xlsx](./data/assemblies-metadata.xlsx)
    * Broke on the co-assemblies. As it turned out I had exceeded my disk quota in hone directory on Uppmax, so I moved to `/proj/naiss2024-22-345/nobackup/yvonnek/7479-marine-metagenome/primary-assemblies-manifests`
    * Also, I shifted into using slurm instead, i.e. creating scripts such as:
        ```
        #!/bin/bash
        #SBATCH -A naiss2024-22-345
        #SBATCH -p core
        #SBATCH -n 1
        #SBATCH -t 5:00:00
        #SBATCH -J ENA-co-R8

        java -jar ../../webin-cli-7.0.1.jar -context genome -ascp -userName Webin-XXX -password 'YYY' -manifest R8_metagenome-manifest.txt -submit
        ```

#### Gzip script

* I created a gzip script for both binned and primary assemblies, that I ran on Uppmax in an interactive session.
* Checking the results (had broken pipe so not sure how far the script went), I realised that not all binned assemblies are in the metadata sheet. Need to confirm with researcher that there are bins that should not be included, otherwise I need to redo a lot...

    * 1802 bins are not in my list/on my radar
    * I've emailed researcher about it. Initial respons is *"the idea was to only submit the minimum medium quality bins and not all bins"*, but will look in detail. Final response is that the bins are correct.

#### Submit binned assemblies

* The original assemblies metadata file had sample aliases such as `binned-R12-A.60`, while the aliases registered were e.g. `sam_R12-A.metabat.60`. I changed the aliases accordingly.
* `RUN_REF` column was updated with the appropriate ERRxxxx accession numbers.

* Program [create-assembly-manifest.c](./scripts/create-assembly-manifest.c) was used to create the binned assembly manifest files:

    ```
    ../../scripts/create-assembly-manifest binned-metagenomes.tsv 1 > submit-binned-assemblies.sh
    ```
    * binned-metagenomes.tsv was created by doing a copy and paste from the assemblies-metadata file. 
    * The Webin-CLI commands was collected in submit-binned-assemblies.sh, and updated the same way as for the primary assemblies. 

* I divided the rows of submit-binned-assemblies.sh into sub-scripts, based on the name of the manifests, e.g.:
    ```
    grep 'sam_R6-E.' submit-binned-assemblies.sh > sam_R6-E.submit-binned-assemblies.sh
    ```
    * This to divide it so that not everything is submitted all at once
    * Also, added the following at the beginning, in each of the sub-scripts
        ```
        #!/bin/bash
        #SBATCH -A naiss2024-22-345
        #SBATCH -p core
        #SBATCH -n 1
        #SBATCH -t 20:00:00
        #SBATCH -J ENA-metagenome-R6-A
        ```
    * I have no idea how long time the scripts need, is 20 hours enough? I calculated roughly 5 minutes per row and then added some. 
* A folder with all the manifests and submit scripts was copied to Uppmax, and the submission scripts were run:
    ```
    scp binned-assemblies-manifests/* yvonnek@rackham.uppmax.uu.se:/proj/naiss2024-22-345/nobackup/yvonnek/7479-marine-metagenome/binned-assemblies-manifests/
    ```
    * I submitted one by one, waiting for each to finish before starting next one, thinking that it might help in order to get the accession numbers in consecutive order per 'bin'
    * I did a `grep -c 'The submission has been completed successfully' slurm-*.out` and compared to number of java rows in each submission script, in order to make sure that everything went ok
    * Submission of the bins went much faster than I thought, around 30 minutes for most of them

    * Submission checks:
        ```
        sbatch ./sam_R3-A.submit-binned-assemblies.sh - batch job 48348613 - 62 assemblies, ERZ24796548--ERZ24796609 received
        sbatch ./sam_R1-A.submit-binned-assemblies.sh - batch job 48348864 - 81 assemblies, ERZ24796610--ERZ24796691 received
        sbatch ./sam_R10-A.submit-binned-assemblies.sh - batch job 48349095 - 95 assemblies, ERZ24796692--ERZ24796786 received
        sbatch ./sam_R11-A.submit-binned-assemblies.sh - batch job 48349340 - 108 assemblies, ERZ24796789--ERZ24796896 recieved
        sbatch ./sam_R12-A.submit-binned-assemblies.sh - batch job 48349862 - 118 assemblies, ERZ24796897--ERZ24797017 received 
        sbatch ./sam_R2-A.submit-binned-assemblies.sh - batch job 48350513 - 89 assemblies, ERZ24797018--ERZ24797106 received
        sbatch ./sam_R4-A.submit-binned-assemblies.sh - batch job 48351471 - 95 assemblies, ERZ24797107--ERZ24797201 received
        sbatch ./sam_R5-A.submit-binned-assemblies.sh - batch job 48351855 - 68 assemblies, ERZ24797202--ERZ24797269 received
        sbatch ./sam_R7-A.submit-binned-assemblies.sh - batch job 48352146 - 105 assemblies, ERZ24797270--ERZ24797374 received
        sbatch ./sam_R9-A.submit-binned-assemblies.sh - batch job 48352454 - 90 assemblies, ERZ24797375--ERZ24797464 received
        sbatch ./sam_R6-A.submit-binned-assemblies.sh - batch job 48354260 - 100 assemblies, ERZ24797465--ERZ24797564 received
        sbatch ./sam_R6-D.submit-binned-assemblies.sh - batch job 48355348 - 91 assemblies, ERZ24797565--ERZ24797655 received
        sbatch ./sam_R6-E.submit-binned-assemblies.sh - batch job 48355762 - 93 assemblies, ERZ24797656--ERZ24797748 received
        sbatch ./sam_R6.submit-binned-assemblies.sh - batch job 48356101 - 131 assemblies, ERZ24797749--ERZ24797879 received
        sbatch ./sam_R8-A.submit-binned-assemblies.sh - batch job 48356560 - 98 assemblies, ERZ24797880--ERZ24797977 - sam_R8-A.metabat.48 initially failed and was resubmitted receiving the last accession number
        sbatch ./sam_R8-II-B1.submit-binned-assemblies.sh - batch job 48357173 - 118 assemblies, ERZ24797978--ERZ24798095 received
        sbatch ./sam_R8-II-Pre.submit-binned-assemblies.sh - batch job 48358282 - 109 assemblies, ERZ24798096--ERZ24798204 received
        sbatch ./sam_R8-II-con.submit-binned-assemblies.sh - batch job 48358680 - 108 assemblies, ERZ24798205--ERZ24798312 received
        sbatch ./sam_R8.submit-binned-assemblies.sh - batch job 48358879 - 155 assemblies, ERZ24798313--ERZ24798467 received
        sbatch ./sam_R.submit-binned-assemblies.sh - batch job 48359481 -  266 assemblies, ERZ24798468--ERZ24798733 received
        ```
* Accession numbers recieved were added to the [assemblies-metadata.xlsx](./data/assemblies-metadata.xlsx) in a separate tab
