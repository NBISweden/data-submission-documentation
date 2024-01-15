# Register Tree of Life ID (ToLID) for biodiversity projects

[Tree of Life ID webpage](https://id.tol.sanger.ac.uk/)

A ToLID is an standardised identifier for a single specimen of a species for genome sequence purposes. The identifier uniquely points to a particular specimen with a name that provides species recognition, differentiates between specimen of the same species, and adds taxonomic context.

Any specied sampled for the Earth Biogenome Project (EBP) is recommended to have registered a ToLID as it facilitates communication, and helps EBP to track past and present sequencing projects. Further, a ToLID hold no metadata about the samples specimen (as e.g. a BioSAmples record do). It should therefore not be considered a competitor to other metadata manifests.

## Example of ToLID construction
A ToLID consists of the following:

1. A single lower case letter prefix representing the higher taxonomic rank (e.g. "u" representing Algae).
2. A second single lower case letter prefix representing a subgroup of the first rank (e.g. "c" representing Chlorophyta).
3. Three letters (one upper case, two lower cases) for genus (e.g. "Ulv" representing the genus *Ulva*).
4. Three letters (one upper case, three lower cases) for species (e.g. "Lact" representing the species *U. lactuca*).
5. An index number representing the number of the sampled specimen, which is not a rank but serves to separate individuals if multiple specimen of the same species are, or have been, sampled (e.g. "1").

For the above example, the first sampled specimen of the algea species *Ulva lactuca* would be ucUlvLact1
  
There are exceptions if the samples are vertebrates, as per the Vertebrate Genome Project (VBP) legacy. The exceptions are:

1. The prefix is limited to a single lower case letter (e.g. "m" for mammals, or "r" for reptiles). No second prefix letter is used.
2. The species name is shortened to one upper, two lower case letters.

For example, the second sampled and registered specimen of the snake species *Lampropeltis getula* would get the ToLID rLamGet2

All species registering for a ToLID must have an official taxonomy ID. In case of a new species not previously described, [a new taxonomic ID must be requested e.g. from ENA](https://ena-docs.readthedocs.io/en/latest/faq/taxonomy_requests.html). 

## How to register a ToLID
In the [Tree of Life ID webpage](https://id.tol.sanger.ac.uk/), begin by checking if the species is already registered with a ToLID by using the search function and providing either ToLID prefix (e.g. mHomSap), taxonomy ID (e.g. 9606), species name (e.g. Homo sapiens) or ToLID (e.g. mHomSap1). If it is, a list of registered specimen will be shown, and you can get an idea of what your ToLID will be.

Continue by loggin in to the platform. The login is federated, so check if your university is available (e.g. Uppsala University is). Once logged in you can select "CREATE" from the top bar.

Provide the following:
1. NCBI taxonomy ID (if there is no ID for your species, make sure to register it first!).
2. Specimen ID (Can be any identifier you use to distinguish the specimen in your lab. Whatever you provide here will only be used by ToLID for tracking purposes, but make sure it is a valid string traceable to your specimen).
3. Scientific name (genus + species).

When submitted the ToLID will be automatically generated based on your provided information. If there is already registered ToLIDs for your species, you will notice the assigned index number is higher than 1. The process should only take a couple of seconds, and once it is finished you can continue with using the newly generated identifier.
