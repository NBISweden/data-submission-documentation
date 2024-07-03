# Need for additions
* `PACBIO_SMRT` as platform for HiFi, not only `ILLUMINA` - when tried with the PacBio Revio input, which is the means of SciLifeLab HiFi sequencing, the xml put out an ILLUMINA capture
* `library_construction_protocol` (or possibly `design_description`) - currently no text explanation of how the samples were prepared for sequencing is included, which is something we as data stewards stress is important for future reuse
* documentation - not that easy to find out how to contribute without the code additions being ugly hacks instead of real, valuable solutions. At least comments in the code explaining functions, would be helpful.

## Additions made
I've made additions that works for our purpose (BGE *Pinna rudis* HiFi sequencing initiated the need for additions in code), all rows affected/updated has a comment, but I don't know Python or this program so it is likely not good enough for production (I would check all resulting xml files and check that nothing looks weird).

### PacBio
Add an `elif` in `get_experiments` function (ugly hack, which might destroy things for others):
```
    if read_type == "ONT":
        layout = 'SINGLE'
        model = 'OXFORD_NANOPORE'
    elif read_type == "Hifi":
        layout = 'SINGLE'
        model = 'PACBIO_SMRT'
```

### library_construction_protocol
Using `exp_attr` variable to be put as library construction protocol, all places where updates have been made has a comment (#add...).

### PROJECT_ATTRIBUTES

* The Keyword-ERGA-BGE attributes does not take (i.e. there are no attributes registered) when using the script. Hence, the code needs to be updated to write:
    ```
    <PROJECT_ATTRIBUTES>
        <PROJECT_ATTRIBUTE>
        <TAG>Keyword</TAG>
        <VALUE>ERGA-BGE</VALUE>
        </PROJECT_ATTRIBUTE>
    </PROJECT_ATTRIBUTES>
    ```
    instead of:
    ```
    <PROJECT_ATTRIBUTES>
        <PROJECT_ATTRIBUTE TAG="Keyword" VALUE="ERGA-BGE"/>
    </PROJECT_ATTRIBUTES>
* I entered the following code on line 171:
    ```
    # Fix code so that project attributes are written with TAG and VALUE as separate rows instead of on one
    # original row: 
    # study_attr = get_attributes (root["study"], attributes, study_attr, 'PROJECT_ATTRIBUTE', **keyword)
    # replaced by:
    study_attr = get_attributes (root["study"], attributes, study_attr, 'PROJECT_ATTRIBUTE')
    kw_attr=""
    kw_attr = get_attributes (root["study"], study_attr, kw_attr, 'TAG', **{'Keyword':""})
    kw_attr = get_attributes (root["study"], study_attr, kw_attr, 'VALUE', **{project:""})
    ```

### To do
* The xml script is not fully funtioning, insert size for paired reads is missing, and read_type 'sample_barcode' should likely be added to HiFi data, hence these needs to be added manually in the output run xmls for now.
