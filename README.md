# data-submission-documentation
Documentation for data submissions from life science research in public repositories.

## How to add documentation for a new submission project

1. Create a new branch, e.g. based on the Redmine project issue number
   * Note, this can be done either remotely or locally, whereupon you either open it locally or publish remotely, respectively
3. Copy the [projectID-title-template](./projectID-title-template) under the repository which the submission concerns, rename it starting with the Redmine project issue number followed by a dash and the Redmine title (title can be shortened if it is long): projectID-title
5. Use the README file as the main documentation file, and add images, scripts or data in their respective folders
6. Make a pull request and ask for review by one of your colleagues
7. The reviewer checks that the documentation makes sense and that there is no sensitive data included (e.g. passwords in scripts), approves and merge. <!-- is it the submitter or the reviewer who should merge? -->

## What to exclude in documentation   <!-- could be phrased better -->

* Big data files
* Names of people involved, use roles such as PI / Researcher / Data Steward / Bioinformatician
* Folder paths to where the data resides, use placeholders or variables
