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
    * Note down the received accession number from the receipt, as well make a copy of the receipt itself.

* **Note:** according to [ENA documentation on umbrella](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#releasing-umbrella-studies): "*Umbrella studies do not appear in the list of studies shown in your Webin account.*". This means that the only way to check what is submitted for a private umbrella project is to query programatically. See how to use [Swagger-UI](#swagger-ui) further down.

## How to update an umbrella project

* ENA doc on [Adding Children To An Umbrella](https://ena-docs.readthedocs.io/en/latest/faq/umbrella.html#adding-children-to-an-umbrella)


* First, create an [update.xml](./data/update.xml) (or copy the linked one).
* Then, copy the umbrella.xml file used to create the umbrella project, and rename it appropriately in order to identify the action, e.g. `umbrella-add-mito.xml`.
* It is important that the `TITLE`, `DESCRIPTION` and `alias` remains the same.
* Replace the `RELATED_PROJECTS` block with the block below ( i.e. there should be only a single `RELATED_PROJECT` block):

    ```
    <RELATED_PROJECTS>
        <RELATED_PROJECT>
            <CHILD_PROJECT accession="TODO:child_accession"/>
        </RELATED_PROJECT>
    </RELATED_PROJECTS>
    ```
* Replace `TODO:child_accession` with the new child project accession number (PRJEB...).
* **Note:** Unlike other updates using xml, where everything already existing needs to be kept in order not to be removed, already exisiting child projects in the umbrella project will not be affected by not being listed. In fact, the only way that projects can be removed from an umbrella is by contacting [ENA helpdesk](https://www.ebi.ac.uk/ena/browser/support).


* Submit using curl:
    ```
    curl -u Username:Password -F SUBMISSION=@update.xml" -F "PROJECT=@umbrella-add-mito.xml" "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    ```
* Check that the receipt contains `submissionFile="update.xml" success="true"` (i.e. no error messages or success="false"), and copy the whole receipt to the documentation (for future reference).

## Swagger-UI

ENA has service endpoints documented using Swagger, that can be used to query ENA programatically.

* Go to <https://www.ebi.ac.uk/ena/submit/report/swagger-ui.html>
* Click on the green `Authorize` button to the right, and enter the broker account credentials.
* In order to see the metadata for an umbrella project, scroll down to `GET /projects/xml/{ids}`, under **project controller** header, and click on the down arrow next to the lock image.
* When expanded, click on the `Try it out` button, enter the project accession number in the 'ids' field, and then click on the blue `Execute` bar.
* Scroll down to the response body, therein one will see what metadata has been registered with the umbrella project. It is also possible to download the xml.

**Note:** The child projects that have been added will not be shown.