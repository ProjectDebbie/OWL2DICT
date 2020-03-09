#!/usr/bin/env python3
import argparse
import configparser
import logging
import os
import sys
import owlready2
from owlready2 import get_ontology
import re

#get filename
path, file = os.path.split("DEB_20200220.owl")
#remove "owl" from file name, keep "."
file_name = file[:-3]
#load ontology 
onto = get_ontology(file).load()
#owlready doesn't automatically remove these special characters or the file name
removal = ["[", file_name, "]", " ", '.value(True)', '.some(True)', '.some(None)', "_"]
with open("DEB_ONTOLOGY.txt",'w') as f: 
#create dictionaries for synonyms, all classes of individual terms, and properties
    synonyms = {}
    ontology_path = {}
    properties = {}
    merged ={}
#two dictionaries will be identical, third will be the final one with changes
    dict_all_terms = {}
    dict_superclasses = {}
#list of superclasses
    superclass_list = ["Biomaterial","BiomaterialType",
  "BiologicallyActiveSubstance","ManufacturedObject","ManufacturedObjectComponent",
  "MedicalApplication","EffectOnBiologicalSystem","AdverseEffects","AssociatedBiologicalProcess",
  "Structure","Shape","ArchitecturalOrganization","DegradationFeatures",
  "ManufacturedObjectFeatures","MaterialProcessing","StudyType","CellType"]
    ont_classes = onto.classes()
    for x in ont_classes:
        id = x.name
        synonym = re.sub(r'|'.join(map(re.escape, removal)), '', str(x.equivalent_to))
        synonyms[id] = synonym
        classes = [i for i in x.is_a]
        class_list = list(classes)
        properties[id]=''
#if term is in superclass_list, term is superlclass (i.e. Biomaterial = Biomaterial)
        if len(class_list)==1:
            if id in superclass_list:
                dict_all_terms[id]=id
            else:
                for term in removal:
                    c = str(class_list)
                    d = re.sub(r'|'.join(map(re.escape, removal)), '', c)
                    dict_all_terms[id]=d
#if term is not in super class list
# # #if length is more than 1, owl.Thing is [0]
        else:
            a = str(class_list[1:2]).split("&")
            b = [re.sub(r'|'.join(map(re.escape, removal)), '', a[0])]
            onProperty = [re.sub(r'|'.join(map(re.escape, removal)), '', a[1])]
            dict_all_terms[id]=b[0]
            properties[id]=onProperty[0]
#we have all terms and their direct parent class
#now we retrieve their superparent class
    for k, v in dict_all_terms.items():
        ontology_path[k]=[v]
        term = k
        parent = v
        variable = None
        if parent in superclass_list:
            dict_superclasses[k]=parent
        else:
            variable = dict_all_terms.get(parent)
            ontology_path[k].append(variable)
            while variable not in superclass_list:
                variable = dict_all_terms.get(variable)
                ontology_path[k].append(variable)
            else:
                dict_superclasses[term] = variable
#merge synoynm, ontology_path, and dict3 dictionaries into NEW dictionary
    merged.update({key: [value1, value2, value3, value4] for key, value1, value2, value3, value4 in zip(dict_superclasses.keys(), dict_superclasses.values(), ontology_path.values(), synonyms.values(), properties.values())})
#if key has a propery associated, I want to create new line with property as key
    for k,v in list(merged.items()):
        if len(v[3]) is not 0:
            merged.update({v[3]:[v[0],v[1],v[2],k]})
#clean terms
    for k,v in merged.items():
        synonym = v[2]
        property = v[3]
        if k.isupper() == True:
            k = k + '\t'
        elif synonym.isupper() == True:
            synonym = synonym + '\t'
        elif property.isupper() == True:
            property= property + '\t'
        else:    
            clean_k = re.sub(r"([A-Z])",r" \1", k).split()
            clean_synonym = re.sub(r"([A-Z])",r" \1", synonym).split()
            clean_property = re.sub(r"([A-Z])",r" \1", property).split()
            k = ' '.join(clean_k)
            k = k + '\t'
            k = k.replace("3 D", "3D")
            k = k.replace("- ", "-")
            synonym = ' '.join(clean_synonym)
            synonym = synonym + '\t'
            synonym = synonym.replace("3 D", "3D")
            synonym = synonym.replace("- ", "-")
            property = ' '.join(clean_property)
            property = property + '\t'
            property = property.replace("3 D", "3D")
            property = property.replace("- ", "-")
        f.write(k+'\t'+'LABEL='+str(v[0])+'\t'+'PATH='+str(v[1])+'\t'+'SYNONYM='+str(synonym)+'\t'+'PROPERTY='+str(property)+'\n')
    print(merged)


            