# Register an umbrella project at ENA

In situations where there are several assemblies connected to the same sample, the assemblies needs to be submitted under separate studies/projects, in order not to be interpreted as updates of the same assembly. See further at ENA on [Updating assemblies](https://ena-docs.readthedocs.io/en/latest/update/assembly.html): *"To submit an assembly update, make sure you reference the same study and sample accessions as were used in the original submission. **In fact, this study-sample pair is unique to your assembly and is the means by which you submission is recognised as an update rather than a new assembly**.*

In order to link the individual studies, and have a main entry point, an umbrella study/project can be submitted.

* ENA documentation on [umbrella studies](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#umbrella-studies)

* Umbrella projects can only be registered programatically, using xml files and curl command.

* The [submission.xml](./data/submission.xml) file contains the action to be made, in this case `ADD` and the release date. 
    * Set the release date to the same date as che children projects.

* The [umbrella.xml](./data/umbrella.xml) contains a project alias, title, description, and the accession numbers of the children projects.
    * Set `alias` to `all-<LOCUSTAG>`, e.g. `all-StyAte`
    * Set `title` to `<species name> umbrella project, <biodiversity project name>`, e.g. `Stylops ater umbrella project, ERGA pilot`
    * Set `description` to e.g.:
    ```
    This project connects the sequencing and assembly data of Stylops ater (host), with two Wolbachia sp. symbionts. The project is part of the ERGA pilot (https://www.erga-biodiversity.eu/pilot-project).
    ```

* Submit using curl:
    ```
    curl -u Username:Password -F "SUBMISSION=@submission.xml" -F "PROJECT=@umbrella.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
    * Note down the received accession number from the receipt

* **Note:** according to [ENA documentation on umbrella](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#releasing-umbrella-studies): "*Umbrella studies do not appear in the list of studies shown in your Webin account.*"

## How to update an umbrella project
