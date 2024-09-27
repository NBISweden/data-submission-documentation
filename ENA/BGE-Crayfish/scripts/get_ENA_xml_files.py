#!/usr/bin/env python3
import os
from os import path
import json
import argparse
import sys
from xml.dom import minidom
from collections import OrderedDict
import jinja2
from datetime import datetime
import re
import pandas as pd 

#Author: Jessica Gomez-Garrido, CNAG.
#Contact email: jessica.gomez@cnag.eu
#Date:20230602

script_loc = os.path.dirname(sys.argv[0])
env = jinja2.Environment(loader=jinja2.FileSystemLoader(script_loc + "/templates/"))
print(script_loc)
def get_attributes (root, parent, child, attr, **element):
    child = root.createElement(attr)
    if element:
        for key in element:
          if element[key] != "":
            child.setAttribute(key, element[key])
          else:
            text = root.createTextNode(key)
            child.appendChild(text)
    parent.appendChild(child)
    return child

def get_studies (project, center, cname, tolid, species, sample_coordinator, study_type, use, locus_tag):
    study_title = species + " "  + study_type
    description = ""
    study_name = tolid
    if study_type == "genome assembly":
        alias = cname.replace(' ', '_') + "_genome_assembly"
        study_title = env.get_template("assembly_title.txt").render(
            species = species,
            cname = cname,
            tolid = tolid
        )
        if project == "ERGA-pilot":
            description_template = "pilot_assembly_description.txt"
        elif project == "CBP":
            description_template = "cbp_assembly_description.txt"
        elif project == "ERGA-BGE":
            alias = "erga-bge-" + tolid + "_primary-" + datetime.now().strftime('%Y-%m-%d')
            study_title = env.get_template("bge_assembly_title.txt").render(
                species = species,
                tolid = tolid
            )
            description_template = "bge_assembly_description.txt"          
        else:
            description_template = "other_assembly_description.txt"
        description = env.get_template(description_template).render(
            species = species,
            cname = cname,
            sample_coordinator = sample_coordinator,
            use = use.lower()
        )
    elif study_type == "alternate assembly":
        alt_use = use
        if alternate_annot == "no":
            alt_use = "assembly"
        alias = cname.replace(' ', '_') + "_alternate_genome_assembly"
        study_name += ", alternate haplotype" 
        study_title = env.get_template("alternate_assembly_title.txt").render(
            species = species,
            cname = cname,
            tolid = tolid
        )
        if project == "ERGA-pilot":
            description_template = "pilot_alternate_assembly_description.txt"
        elif project == "CBP":
            description_template = "cbp_alternate_assembly_description.txt"
        elif project == "ERGA-BGE":
            alias = "erga-bge-" + tolid + "_alternate-" + datetime.now().strftime('%Y-%m-%d')
            study_title = env.get_template("bge_alternate_assembly_title.txt").render(
                species = species,
                tolid = tolid
            )
            description_template = "bge_alternate_assembly_description.txt"          
        else:
            description_template = "other_alternate_assembly_description.txt"
        description = env.get_template(description_template).render(
            species = species,
            cname = cname,
            sample_coordinator = sample_coordinator,
            use = alt_use.lower()
        )        
    elif study_type == "resequencing Data":
        alias = cname.replace(' ', '_') + '_resequencing_data'
        study_register[tolid_pref] = alias
        description = "This project collects the " + study_type + " generated for " + species +\
                         " (common name " + cname + ")" 
    else:
        alias = cname.replace(' ', '_') + '_data'
        study_title = env.get_template("data_title.txt").render(
            species = species,
            cname = cname,
            data = study_type
        )
        study_name = tolid_pref
        if project == "ERGA-pilot":
            description_template = "pilot_data_description.txt"       
        elif project == "CBP":
            description_template = "cbp_data_description.txt"   
        elif project == "ERGA-BGE":
            alias = "erga-bge-" + tolid_pref + "-study-rawdata-" + datetime.now().strftime('%Y-%m-%d')
            study_title =  env.get_template("bge_data_title.txt").render(
                species = species,
                data = study_type
            )
            description_template = "bge_data_description.txt"               
        else:
            description_template = "other_data_description.txt" 
        study_register[tolid_pref] = alias
        description = env.get_template(description_template).render(
            species = species,
            cname = cname,
            sample_coordinator = sample_coordinator,
            data = study_type, 
            use = use.lower()
        )  

    if 'all' in args.xml or "study" in args.xml:    
        get_study_xml(project, center, alias, study_name, study_title, description, study_type, locus_tag)

def get_study_xml(project, center, alias, study_name, study_title, description, study_type, locus_tag):   

    projects = ""
    elements = {}
    elements['center_name'] = center
    elements['alias'] = alias
    projects = get_attributes (root["study"], study_xml, projects, 'PROJECT', **elements)

    attr = OrderedDict()
    attr['NAME'] = study_name
    attr['TITLE'] = study_title
    attr['DESCRIPTION'] = description
    
    for key in attr:
        attributes = root["study"].createElement(key)
        text = root["study"].createTextNode(attr[key])
        attributes.appendChild(text)
        projects.appendChild(attributes)

    attributes = ""
    attributes = get_attributes (root["study"], projects, attributes, 'SUBMISSION_PROJECT')

    seqp = root["study"].createElement('SEQUENCING_PROJECT')
    if study_type == "genome assembly" and locus_tag != "-":
        loc = ""
        loc = get_attributes (root["study"], seqp, loc, 'LOCUS_TAG_PREFIX', **{locus_tag:""})
    
    if study_type == "alternate assembly" and alternate_annot == "yes":
        hlocus_tag = locus_tag + "H2"
        loc = ""
        loc = get_attributes (root["study"], seqp, loc, 'LOCUS_TAG_PREFIX', **{hlocus_tag:""})
    attributes.appendChild(seqp)

    if project == "CBP" or project == "EASI" or project == "ERGA-BGE":
        keyword = {}
        keyword['TAG'] = "Keyword"
        keyword['VALUE'] = project
        attributes = ""
        study_attr = ""
        attributes = get_attributes (root["study"],projects, attributes, 'PROJECT_ATTRIBUTES')
        # Fix code so that project attributes are written with TAG and VALUE as separate rows instead of on one
        #study_attr = get_attributes (root["study"], attributes, study_attr, 'PROJECT_ATTRIBUTE', **keyword)
        study_attr = get_attributes (root["study"], attributes, study_attr, 'PROJECT_ATTRIBUTE')
        kw_attr=""
        kw_attr = get_attributes (root["study"], study_attr, kw_attr, 'TAG', **{'Keyword':""})
        kw_attr = get_attributes (root["study"], study_attr, kw_attr, 'VALUE', **{project:""})


#add exp_attr & insert_size as argument in function
def get_experiments (center, alias, species, read_type, instrument, study_alias, sample_ref, flowcell, library_strategy, library_selection, exp_attr, add_lib, add_exp, library_id, insert_size):
    exp_title = species + " " + read_type + " " + library_strategy +  " data"
    lib_name = library_id + " " + read_type + " " + library_strategy
    if read_type == library_strategy:
        exp_title = species + " " + library_strategy +  " data"
        lib_name = library_id + " " + library_strategy     
    if read_type == "HiFi": # added code for including PacBio in title and library name
        exp_title = species + " " + "PacBio" + " " + read_type + " " + library_strategy +  " data"
        lib_name = library_id + " " + "PacBio" + " " + read_type + " " + library_strategy
    source = "GENOMIC"
    if library_strategy == "RNA-Seq":
        source = 'TRANSCRIPTOMIC'
  
    layout= 'PAIRED'
    model = 'ILLUMINA'
    if read_type == "ONT":
        layout = 'SINGLE'
        model = 'OXFORD_NANOPORE'
    elif read_type == "HiFi":  #add PacBio, might cause issues for others
        layout = 'SINGLE'
        model = 'PACBIO_SMRT'

    if 'all' in args.xml or "experiment" in args.xml:
        get_exp_xml (center, alias, exp_title,study_alias, sample_ref, lib_name, library_strategy, source, layout, library_selection, add_lib, exp_attr, add_exp, model, instrument, insert_size) #add exp_attr, insert_size

def get_exp_xml (center, alias, exp_title, study_alias, sample_ref, lib_name, library_strategy, source,layout, library_selection, add_lib, exp_attr, add_exp, model, instrument, insert_size): #add exp_attr, insert_size
 
    experiments = ""
    elements = {}
    elements['center_name'] = center
    elements['alias'] = alias
    experiments = get_attributes (root["exp"], exp_xml, experiments, 'EXPERIMENT', **elements)

    attributes = ""
    attributes = get_attributes (root["exp"],experiments, attributes, 'TITLE', **{exp_title:""})
    attributes = get_attributes (root["exp"],experiments, attributes,  'STUDY_REF', **{'refname': study_alias})
    attributes = get_attributes (root["exp"],experiments, attributes, 'DESIGN')

    design=""
    design = get_attributes (root["exp"],attributes, design, 'DESIGN_DESCRIPTION')
    design = get_attributes (root["exp"],attributes, design, 'SAMPLE_DESCRIPTOR', **{'accession': sample_ref})
    design = get_attributes (root["exp"],attributes, design, 'LIBRARY_DESCRIPTOR')

    library = ""
    library = get_attributes (root["exp"],design, library, 'LIBRARY_NAME', **{lib_name:""})  
    library = get_attributes (root["exp"],design, library, 'LIBRARY_STRATEGY', **{library_strategy:""})
    library = get_attributes (root["exp"],design, library, 'LIBRARY_SOURCE', **{source:""})
    library = get_attributes (root["exp"],design, library, 'LIBRARY_SELECTION', **{library_selection:""})
    layout_lib = ""
    library  = get_attributes (root["exp"],design, library, 'LIBRARY_LAYOUT' )

    # handle insert_size if paired reads, requires an extra column insert_size in tsv
    #    layout_lib  = get_attributes (root["exp"],library,layout_lib,layout) # original row
    layout_lib  = get_attributes (root["exp"],library,layout_lib,layout,**{"NOMINAL_LENGTH":str(insert_size)})
    if add_lib:
        my_dict = add_lib.split(';')
        for dict in my_dict:
            key = dict.split(':')
            library = get_attributes (root["exp"],design, library, key[0], **{key[1]:""})

    #added code
    #library  = get_attributes (root["exp"],design, library, 'LIBRARY_CONSTRUCTION_PROTOCOL', **{exp_attr:""})

    platform=""
    attributes = get_attributes (root["exp"],experiments, attributes, 'PLATFORM')
    platform = get_attributes (root["exp"],attributes, platform, model)
    machine = ""
    machine = get_attributes (root["exp"],platform, machine, 'INSTRUMENT_MODEL', **{instrument:''})
 
    if add_exp:
        attributes = get_attributes (root["exp"], experiments, attributes, 'EXPERIMENT_ATTRIBUTES')
        experiment=""
        my_dict = add_exp.split(';')
        for dict in my_dict:
            key = dict.split(':')
            experiment = get_attributes (root["exp"],attributes, experiment, 'EXPERIMENT_ATTRIBUTE')
            TAGS=""
            TAGS = get_attributes (root["exp"],experiment, TAGS, "TAG", **{key[0]:""})
            TAGS = get_attributes (root["exp"],experiment, TAGS, "VALUE", **{key[1]:""})

def get_runs_xml(center, alias, exp_alias, element, files_reverse):
    runs = ""
    elements = {}
    elements['center_name'] = center
    elements['alias'] = "run_" + alias
    runs = get_attributes (root["runs"], runs_xml, runs, 'RUN', **elements)

    attributes = ""
    attributes = get_attributes (root["runs"], runs, attributes, 'EXPERIMENT_REF', **{"refname":exp_alias})
    attributes = get_attributes (root["runs"], runs, attributes,  'DATA_BLOCK')
    
    files = ""
    files = get_attributes (root["runs"], attributes, files, 'FILES')

    file= ""

    file = get_attributes (root["runs"], files, file, 'FILE',
    **{"filename": element, "checksum_method":"MD5","checksum":md5sum[element],"filetype":filetype[element]})

    if element in files_reverse:
        type = ""
        type = get_attributes (root["runs"], file, type, 'READ_TYPE', **{'paired': ""})
        type = get_attributes (root["runs"], file, type, 'READ_TYPE', **{'sample_barcode': ""})
        file = get_attributes (root["runs"], files, file, 'FILE',
        **{"filename": files_reverse[element], "checksum_method":"MD5","checksum":md5sum[files_reverse[element]],"filetype":filetype[element]})
        type = get_attributes (root["runs"], file, type, 'READ_TYPE', **{'paired': ""})
        type = get_attributes (root["runs"], file, type, 'READ_TYPE', **{'sample_barcode': ""})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--files",  required=True, help="TABLE file with appropriate headers")
    parser.add_argument("-p", "--project", default = 'ERGA-BGE', choices=['ERGA-BGE', 'CBP', 'ERGA-pilot', 'EASI', 'other'], help="project")
    parser.add_argument("-x", "--xml", default= 'all', nargs = "+", choices=['all', 'study', 'experiment', 'runs'], help="specify which xml files do you want")
    parser.add_argument("-o", "--out_prefix", required=True, help="prefix to add to output files")   
    args = parser.parse_args()

    read_type_choice = ['ONT', 'Illumina', 'Hi-C', 'HiFi']
    library_strategy_choice = ['WGS', 'Hi-C', 'RNA-Seq']
    
    if not args.files:
        exit("Input file not given.")
    elif not path.isfile(args.files):
        exit(args.files +  " does not exist.")

    in_file = pd.read_table(args.files, header = 0, index_col=False , delimiter="\t")
    
    files_run = {}
    md5sum = {}
    filetype = {}
    experiments = {}
    files_reverse = {}

    root = {}
    if "all" in args.xml or "study" in args.xml:
        root["study"] = minidom.Document()
        study_xml = root["study"].createElement('PROJECT_SET') 
        root["study"].appendChild(study_xml)
    study_register = {}

    if 'all' in args.xml or "experiment" in args.xml:
        root["exp"] = minidom.Document()
        exp_xml = root["exp"].createElement('EXPERIMENT_SET') 
        root["exp"].appendChild(exp_xml)
    experiment_register = {}


    if 'all' in args.xml or "runs" in args.xml:
        root["runs"] = minidom.Document()
        runs_xml = root["runs"].createElement('RUN_SET') 
        root["runs"].appendChild(runs_xml)   
    
    for i in in_file.index:
             
        if "center" not in in_file or pd.isna(in_file["center"][i]) or in_file["center"][i] == "-":
            center = "CNAG"
        else:
            center = in_file['center'][i]

        if "scientific_name" not in in_file or pd.isna(in_file["scientific_name"][i]) or in_file["scientific_name"][i] == "-":
            exit ("Missing species scientific name, compulsory argument")
        else:
            species = in_file["scientific_name"][i]

        if "tolid" not in in_file or pd.isna(in_file["tolid"][i]) or in_file["tolid"][i] == "-":
            exit ("Missing tolid or tolid prefix, compulsory argument")
        else:
            tolid = in_file["tolid"][i]
            tolid_pref = re.sub(r'[0-9]', '', tolid)

        cname = ""
        if "common_name" in in_file and not pd.isna(in_file["common_name"][i]) and not in_file["common_name"][i] == "-":
            cname = in_file["common_name"][i]  
        elif "common_names" in in_file and not pd.isna(in_file["common_names"][i]) and not in_file["common_names"][i] == "-":
            cname = in_file["common_names"][i] 


        sample_coordinator = ""
        if "sample_coordinator" not in in_file or pd.isna(in_file["sample_coordinator"][i]) or in_file["sample_coordinator"][i] == "-":
            if args.project == "ERGA-pilot":
                exit ("Missing sample ambassador details, required argument for ERGA-pilot genomes.")
        else:
            sample_coordinator = in_file["sample_coordinator"][i]   

        locus_tag = "-"
        if "locus_tag" in in_file and not pd.isna(in_file["locus_tag"][i]) and not in_file["locus_tag"][i] == "-":
            locus_tag = in_file["locus_tag"][i]        
  
        sample_id = ""
        if 'sample_tube_or_well_id' in in_file and not pd.isna(in_file["sample_tube_or_well_id"][i]) and not in_file["sample_tube_or_well_id"][i] == "-":
            sample_id = in_file["sample_tube_or_well_id"][i]
        else:
            exit ("Missing sample_tube_or_well_id")
          
        if 'all' in args.xml or "experiment" in args.xml:
            instrument = ""
            if "instrument" not in in_file or pd.isna(in_file["instrument"][i]) or in_file["instrument"][i] == "-":
                exit ("Instrument model value is necessary to get the experiment xml")
            instrument = in_file["instrument"][i]  

            sample_ref = ""
            if "biosample_accession" not in in_file or pd.isna(in_file["biosample_accession"][i]) or in_file["biosample_accession"][i] == "-":
                exit ("Sample accession is required to get the experiment xml")
            sample_ref = in_file["biosample_accession"][i]    

            library_selection = ""
            if "library_selection" not in in_file or pd.isna(in_file["library_selection"][i]) or in_file["library_selection"][i] == "-":
                exit ("Library selection value is required to get the experiment xml")
            library_selection = in_file["library_selection"][i]      

            #added code for handling exp_attr & insert_size
            exp_attr = ""
            if "exp_attr" in in_file and not in_file["exp_attr"][i] == "-":
                exp_attr =  in_file["exp_attr"][i]
            insert_size = ""
            if "insert_size" in in_file and not in_file["insert_size"][i] == "-":
                insert_size = in_file["insert_size"][i]
        if 'all' in args.xml or 'experiment' in args.xml or 'runs' in args.xml:
            if "library_strategy" not in in_file or pd.isna(in_file["library_strategy"][i]) or in_file["library_strategy"][i] == "-":
                exit ("Library strategy value is required to get the experiment xml")
            library_strategy = in_file["library_strategy"][i]                
            
            if library_strategy not in library_strategy_choice:
                exit(library_strategy + " is not one of the accepted values. Accepted values:" + str(library_strategy_choice))

            if "read_type" not in in_file or pd.isna(in_file["read_type"][i]) or in_file["read_type"][i] == "-":
                if library_strategy == "Hi-C":
                    read_type = library_strategy
                elif "illumina" in instrument.lower():
                    read_type = "Illumina"
                elif "ION" in instrument:
                    read_type = "ONT"
                else:
                    read_type = "HiFi"
            else:
                read_type = in_file['read_type'][i]
        
            if read_type not in read_type_choice:
                if read_type == "HiC":
                    read_type = "Hi-C"
                else:
                    exit(read_type + " is not one of the accepted values for read_type. Accepted values: " + str(read_type_choice))

        aim = "assembly and annotation"
        if "aim" in in_file and not pd.isna(in_file["aim"][i]) and not in_file["aim"][i] == "-":
            aim = in_file["aim"][i]
            if args.project == "ERGA-BGE":
                aim = "assembly and annotation"    
             
        
        study_type = {}
        #if read_type == "ONT" or read_type == "HiFi":
        study_type[tolid] = []

        if aim.lower() == "assembly":
            study_type[tolid].append("genomic data")
            study_type[tolid].append("genome assembly")
        elif aim.lower() == "annotation":
            study_type[tolid].append("transcriptomic data")
        elif aim.lower() == "assembly and annotation":
            study_type[tolid].append("genomic and transcriptomic data")
            study_type[tolid].append("genome assembly")
        elif aim.lower() == "resequencing":
            study_type[tolid].append("resequencing data")
        else:
            exit(aim + " is not and accepted aim for the project.")
        
        alternate = ""
        alternate_annot = "no"
        if "alternate" in in_file:
            alternate = in_file["alternate"][i] 
            if "assembly" in alternate.lower():
                study_type[tolid].append("alternate assembly")
            if "annotation" in alternate.lower():
                alternate_annot = "yes"

        library_id = in_file["library_name"][i]
        add_lib = {}
        library_attributes = ""
        if "lib_attr" in in_file and not pd.isna(in_file["lib_attr"][i]) and not in_file["lib_attr"][i] == "-":
            library_attributes = in_file["lib_attr"][i] 
            add_lib = library_attributes.replace('{','').replace('}','')
                                                                 
        if read_type == library_strategy:
            rname = tolid_pref + "_" + read_type + "_" + sample_id + "_" + library_id
            experiments[rname] = "exp_" + tolid_pref + "_" + library_strategy + "_" + sample_id  + "_" + library_id
        else:
            rname = tolid_pref + "_" + read_type + "_" + library_strategy + "_" + sample_id + "_" + library_id
            experiments[rname] = "exp_" + tolid_pref + "_" + read_type + "_" + library_strategy + "_" + sample_id + "_" + library_id
       

        forward_file_name = ""
        if "forward_file_name" in in_file and not pd.isna(in_file["forward_file_name"][i]) and not in_file["forward_file_name"][i] == "-":
            forward_file_name = in_file["forward_file_name"][i]         
                
            filetype[forward_file_name] = "fastq"
            fastq_run = rname + "_fastq"
            if not fastq_run in files_run:
                files_run[fastq_run] = []
            files_run[fastq_run].append(forward_file_name)

            if "forward_file_md5" not in in_file or pd.isna(in_file["forward_file_md5"][i]) or in_file["forward_file_md5"][i] == "-":
                exit ("Missing md5 value for " + forward_file_name)
            else:
                md5sum[forward_file_name] = in_file["forward_file_md5"][i]

        reverse_file_name = ""
        if "reverse_file_name" in in_file and not pd.isna(in_file["reverse_file_name"][i]) and not in_file["reverse_file_name"][i] == "-":
            reverse_file_name = in_file["reverse_file_name"][i]       
            if "fastq" in reverse_file_name:
                files_reverse[forward_file_name] = reverse_file_name

                if "reverse_file_md5" not in in_file or pd.isna(in_file["reverse_file_md5"][i]) or in_file["reverse_file_md5"][i] == "-":
                    exit ("Missing md5 value for " + reverse_file_name)
                else:
                    md5sum[reverse_file_name] = in_file["reverse_file_md5"][i]

        native_file_name = ""
        if "native_file_name" in in_file and not pd.isna(in_file["native_file_name"][i]) and not in_file["native_file_name"][i] == "-":
            native_file_name = in_file["native_file_name"][i] 
            if "native_file_md5" not in in_file or pd.isna(in_file["native_file_md5"][i]) or in_file["native_file_md5"][i] == "-":
                exit ("Missing md5 value for " + native_file_name)
            else:
                md5sum[native_file_name] = in_file["native_file_md5"][i]
    
            native_run = ""  
            if "fast5" in native_file_name:
                filetype[native_file_name] = "OxfordNanopore_native"
                native_run = rname + "_fast5s"
            elif "bam" in native_file_name:
                filetype[native_file_name] = "bam"
                native_run = rname + "_bam" 
            if not native_run in files_run:
                files_run[native_run] = []
            files_run[native_run].append(native_file_name)       

        add_lib = {}
        library_attributes = ""
        if "lib_attr" in in_file and not pd.isna(in_file["lib_attr"][i]) and not in_file["lib_attr"][i] == "-":
            library_attributes = in_file["lib_attr"][i] 
            add_lib = library_attributes.replace('{','').replace('}','')

        add_exp = {}
        experiment_attributes = ""
        if "exp_attr" in in_file and not pd.isna(in_file["exp_attr"][i]) and not in_file["exp_attr"][i] == "-":
            experiment_attributes = in_file["exp_attr"][i] 
            add_exp = experiment_attributes.replace('{','').replace('}','')
 
        if 'all' in args.xml or "study" in args.xml:
            # if read_type == "ONT" or read_type == "Hifi":
            if tolid_pref not in study_register:
                study_register[tolid_pref] = ""
                for type in study_type[tolid]:
                    get_studies(
                        args.project,
                        center,
                        cname,
                        tolid,
                        species,
                        sample_coordinator,
                        type,
                        aim,
                        locus_tag
                    )

        if 'all' in args.xml or "experiment" in args.xml:
            if "exp_" + tolid_pref + "_" + read_type + "_" + library_strategy + "_" + sample_id not in experiment_register and "exp_" + tolid + "_" + library_strategy + "_" + sample_id + "_" + library_id not in experiment_register:
                experiment_register["exp_" + tolid_pref + "_" + read_type + "_" + library_strategy + "_" + sample_id + "_" + library_id] = ""
                if read_type == library_strategy:
                    experiment_register["exp_" + tolid_pref + "_" + library_strategy + "_" + sample_id + "_" + library_id] = ""
               
                get_experiments(
                    center,
                    experiments[rname],
                    species,
                    read_type,
                    instrument,
                    study_register[tolid_pref],
                    sample_ref,
                    sample_id,
                    library_strategy, 
                    library_selection,
                    exp_attr, #addition so that library_construction_protocol is written
                    add_lib,
                    add_exp,
                    library_id,
                    insert_size #addition for paired reads
                )

    if 'all' in args.xml or "runs" in args.xml:
        for run in files_run:
            run_name = '_'.join(run.split('_')[:-1])
            r = 1
            for file in files_run[run]:
                get_runs_xml(center, run + "_" + str(r), experiments[run_name], file, files_reverse)
                r += 1
  
    for i in root:
        xml_str = root[i].toprettyxml(indent ="\t")
        save_path_file = args.out_prefix + "." + i + ".xml"
        with open(save_path_file, "w") as f:
            f.write(xml_str) 
