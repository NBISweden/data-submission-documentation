#!/usr/bin/env python
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

#Modified by: Tyler Alioto, CNAG
#Contact email: tyler.alioto@cnag.eu
#Date: 20240704

script_loc = os.path.dirname(sys.argv[0])
env = jinja2.Environment(loader=jinja2.FileSystemLoader(script_loc + "/templates/"))

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

def get_xml (project, center, species, tolid_pref, description, children):
 
  projects = root.createElement('PROJECT')
  projects.setAttribute('center_name', center)

  projects.setAttribute('alias', alias)
  xml.appendChild(projects)

  attr = OrderedDict()
  attr['NAME'] = tolid_pref
  attr['TITLE'] = species
  attr['DESCRIPTION'] = description

  for key in attr:
    attributes = root.createElement(key)
    text = root.createTextNode(attr[key])
    attributes.appendChild(text)
    projects.appendChild(attributes)

  attributes = get_attributes (root, projects, attributes, 'UMBRELLA_PROJECT')
  organism = root.createElement('ORGANISM')
  attributes.appendChild(organism)
  for key in org_attr:
    org = root.createElement(key)
    text = root.createTextNode(org_attr[key])
    org.appendChild(text)
    organism.appendChild(org)

  if children:
    attributes = get_attributes (root, projects, attributes, 'RELATED_PROJECTS')
    for key in children:
      seqp = get_attributes (root,attributes, attributes,'RELATED_PROJECT')
      accessions = get_attributes (root,seqp,seqp, 'CHILD_PROJECT', **{'accession':key})
    if args.project == "ERGA-BGE":
      seqp = get_attributes (root,attributes, attributes,'RELATED_PROJECT')
      accessions = get_attributes (root,seqp,seqp, 'PARENT_PROJECT', **{'accession':'PRJEB61747'})
   
  if args.project == "CBP" or project == "EASI" or project == "ERGA-BGE":
    keyword = {}
    keyword['TAG'] = "Keyword"
    keyword['VALUE'] = project
    attributes = ""
    study_attr = ""
    attributes = get_attributes (root, projects, attributes, 'PROJECT_ATTRIBUTES')
    study_attr = get_attributes (root, attributes, study_attr, 'PROJECT_ATTRIBUTE', **keyword)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--project", default = 'ERGA-BGE', choices=['ERGA-BGE', 'CBP', 'ERGA-pilot', 'EASI', 'other'], help="project")
    parser.add_argument("-c", "--center", default="CNAG", help="center name")
    parser.add_argument("-n", "--name", required=False, help="common name")
    parser.add_argument("--sample-ambassador", required=False, help="Sample ambassador for ERGA-pilot projects")
    parser.add_argument("-t", "--tolid", required=True, help="tolid")
    parser.add_argument("-s", "--species", required=True, help="species scientific name")
    parser.add_argument("-x", "--taxon_id", required=True, help="species taxon_id")
    parser.add_argument("-a", "--children_accessions", required=True, nargs="+", help="species scientific name")
    
    args = parser.parse_args()
    root = minidom.Document()
    xml = root.createElement('PROJECT_SET') 
    root.appendChild(xml)

    tolid_pref = re.sub(r'[0-9]', '', args.tolid)
    if args.project == "ERGA-pilot":
      alias = args.name
      description_template = "pilot_umbrella_description.txt"
      if not args.sample_ambassador:
        exit ("Required sample ambassador details for ERGA-pilot projects")
      else:
        sample_ambassador = args.sample_ambassador
    elif args.project == "CBP":
      description_template = "cbp_umbrella_description.txt"
      alias = "cbp-" + tolid_pref + "-study-umbrella-" + datetime.now().strftime('%Y-%m-%d')
    elif args.project == "ERGA-BGE":
      alias = "erga-bge-" + tolid_pref + "-study-umbrella-" + datetime.now().strftime('%Y-%m-%d')
      description_template = "bge_umbrella_description.txt"          
    else:
      alias = tolid_pref + "-study-umbrella-" + datetime.now().strftime('%Y-%m-%d')
      description_template = "other_umbrella_description.txt"
    
    org_attr = {}
    org_attr['TAXON_ID'] = args.taxon_id
    org_attr['SCIENTIFIC_NAME'] = args.species
    
    description = env.get_template(description_template).render(
      species = args.species,
      alias = alias,
      sample_ambassador = args.sample_ambassador
    )

    get_xml(
      args.project,
      args.center,
      args.species,
      tolid_pref,
      description,
      args.children_accessions
    )
    xml_str = root.toprettyxml(indent ="\t") 
  
    save_path_file = "umbrella.xml"
  
    with open(save_path_file, "w") as f:
      f.write(xml_str) 