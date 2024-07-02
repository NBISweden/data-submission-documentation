# BGE SOP

This SOP collects all experience and various issues with submitting data to ENA in the BGE project. It is a working document and will be continually extended as we learn new things and gather new knowledge. All information in this document is written from an NBIS perspective and may not be applicable in full by other involved BGE-node active data stewards.

## Submitting Experiment and Runs in a pre-registered Study.

The developed script for submitting BGE data to ENA (get_ENA_xml_files.py) automatically generates a Study.xml file together with an Experiment.xml and Runs.xml. It assumes no study has been registered in the ENA portal beforehand and is streamlined for generating all necessary files for both study registration as well as data submission. Whenever the study needs to be registered before the actual data submission, the generated study.xml becomes superflous while the experiment.xml and runs.xml can still be used, but with modification.

1. Register a study at ENA including the [BGE specific and required information](https://github.com/ERGA-consortium/ERGA-submission/blob/main/BGE/ERGA-BGE_ReadData_Submission_Guide.md).

1. For the data, use [the BGE script](https://github.com/ERGA-consortium/ERGA-submission/blob/main/get_submission_xmls/get_ENA_xml_files.py) to generate the standardized experiment.xml and runs.xml files.

1. Make sure to calculate md5 checksums for each file as these are required in the runs.xml files. 

1. Upload the raw data files to ENA. In this example the Aspera upload from command prompt was used:

    `ascp -QT -l300M -L- <file(s)> <Webin-NNNNN>@webin.ebi.ac.uk:.`

    The above uploads the file(s) without the ability to resume if transfer is interrupted. It also creates a log file `-L-` that might not be required.

    `ascp -QT -l300M -k 1 <file(s)> <Webin-NNNNN>@webin.ebi.ac.uk:.`

    This starts an upload that, if interrupted, checks the resumed upload against file attributes and if possible resumes it.
    More alternatives are available in the [Aspera Command-Line Interface Guide](https://download.asperasoft.com/download/docs/cli/3.9.6/user_win/webhelp/index.html)

1. In the generated experiment.xml file, the line(s) containing STUDY_REF needs to be modified. The default line contains a `<STUDY_REF refname="XYZ"/>` element, where the refname points to an alias defined in the study.xml file.

    If unmodified any attempt to submit the xml will generate a null error since the alias does not exist in the ENA database.

    Change the above to `<STUDY_REF accession="PRJEBXXXX"/>` for the pre-registered study.

    Also enter the calculated md5 checksums after `filename=XYZ"` as `checksum_method="MD5" checksum="enter_here" filetype="XYZ"/>`

1. In the generated runs.xml, modify the `filename` to only the filename. The submission will automatically assume the file is present in the ENA upload root folder for the Webin user, as we specified by `<Webin-NNNNN>@webin.ebi.ac.uk:.` above.

1. Also create a submisson.xml as described in the [ENA submission documents](https://ena-docs.readthedocs.io/en/latest/submit/reads/programmatic.html)

1. Now when the files are upoaded to ENA and we have the correctly modified xml's for experiment and runs, and a submission.xml, submit using e.g. curl, first to the ENA test server to check for errors:

```
curl -u Webin-NNNNN:PASSWORD -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@experiment.xml" -F "RUN=@runs.xml" "https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit/"
```

If no errors are encountered, proceed by submitting the same files to the sharp ENA server using a nearly identical command:

```
curl -u Webin-NNNNN:PASSWORD -F "SUBMISSION=@submission.xml" -F "EXPERIMENT=@experiment.xml" -F "RUN=@runs.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
```