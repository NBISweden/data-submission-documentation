# data-submission-documentation
Documentation for data submissions from life science research in public repositories.

## How to add documentation for a new submission project

1. Create a new branch, e.g. based on the Redmine project issue number
   * Note, this can be done either remotely or locally, whereupon you either open it locally or publish remotely, respectively
3. Copy the [projectID-title-template](./projectID-title-template) under the repository which the submission concerns, rename it as follows:
   * If **ENA** submission: Redmine project issue number followed by the submission type, and last the Redmine title (title can be shortened if it is long), separate with dash (projectID-submissionType-title)  
      * Regarding the submission type, this is in order to highlight what is special with the submission, like a tag, so that it is easy just by looking at the folder names to find the type of submission you are looking for. Select from the following list, or add to this list if the type is not in list yet:
         * metagenome
         * metatranscriptome
         * assembly
         * RNAseq
   * If **not** ENA: skip the submissionType, i.e. Redmine project issue number followed by the Redmine title (title can be shortened if it is long), separate with dash (projectID-title)
5. Use the README file as the main documentation file, and add images, scripts or data in their respective folders
6. Make a pull request and ask for review by one of your colleagues
7. The reviewer checks that the documentation makes sense and that there is no sensitive data included (e.g. passwords in scripts, see further below on what *not* to include), approves and merge. 

## What to exclude in documentation   <!-- could be phrased better -->

* Big data files
* Names of people involved, use roles such as PI / Researcher / Data Steward / Bioinformatician
* Folder paths to where the data resides, use placeholders or variables
