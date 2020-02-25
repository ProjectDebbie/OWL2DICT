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
path, file = os.path.split("austin_test.owl")
#remove "owl" from file name, keep "."
file_name = file[:-3]
#load ontology 
onto = get_ontology(file).load()
#owlready doesn't automatically remove these special characters or the file name from class name
removal = ["[", file_name, "]", " ", '.value(True)', '.some(True)']
with open("test",'w') as f: 
    f.write('TERM\tLABEL\tPATH\tSYNONYMS\tPROPERTIES\n')
#create dictionaries for synonyms and all classes of individual terms
    synonyms = {}
    ontology_path = {}
    properties = {}
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
#     for k, v in dict2.items():
#         ontology_path[k]=[v]
#         if v in superclass_list:
#             dict3[k] = v      
#         else: 
#             dict3[k]=dict2.get(v)
#             ontology_path[k].append(dict2.get(v))
#             for x,y in dict3.items():
#                 while y in superclass_list:
#                     break
#                 else:
#                     dict3[k]=dict2.get(y)
#                     ontology_path[k].append(dict2.get(y))
#merge synoynm, ontology_path, and dict3 dictionaries into NEW dictionary
    merged = {key: [value1, value2, value3] for key, value1, value2, value3 in zip(dict_superclasses.keys(), dict_superclasses.values(), ontology_path.values(), synonyms.values())}
    for id, value in properties.items():
        merged[id].append(value)
#print new dictionary
    for k, v in merged.items():
        if len(v)==4:
            f.write(k+'\t'+'LABEL='+str(v[0])+'\t'+'PATH='+str(v[1])+'\t'+str(v[2])+'\t'+str(v[3])+'\n')
        if len(v)==3:
            f.write(k+'\t'+'LABEL='+str(v[0])+'\t'+'PATH='+str(v[1])+'\t'+str(v[2])+'\n')



            