#!/usr/bin/env python3
import argparse
import configparser
import logging
import os
import sys
import owlready2
from owlready2 import get_ontology
import re

#load in owl ontology
file = "DEB_20191001.owl"
onto = get_ontology(file).load()
#remove "owl" from file name, keep "."
file_name = file[:-3]
removal = ["[", file_name, "]", " "]
with open("test",'w') as f: 
    f.write('TERM\tLABEL\tPATH\tSYNONYMS\n')
#create dictionaries for synonyms and all classes of individual terms
    synonyms = {}
    ontology_path = {}
#two dictionaries will be identical, third will be the final one with changes
    dict1 = {}
    dict2 = {}
    dict3 = {}
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
                dict1[id]=id
                dict2[id]=id
            else:
                for term in removal:
                    c = str(class_list)
                    d = re.sub(r'|'.join(map(re.escape, removal)), '', c)
                    dict1[id]=d
                    dict2[id]=d
#if term is not in super class list
# # #if length is more than 1, owl.Thing is [0]
        else:
            a = str(class_list[1:2]).split("&")
            b = [re.sub(r'|'.join(map(re.escape, removal)), '', a[0])]
            dict1[id]=b[0]
            dict2[id]=b[0]
#we have all terms and their direct parent class
#now we retrieve their superparent class
    for k, v in dict2.items():
        ontology_path[k]=[v]
        if v in superclass_list:
            dict3[k] = v
        else: 
            dict3[k]=dict1.get(v)
            ontology_path[k].append(dict1.get(v))
            for x,y in dict3.items():
                if y not in superclass_list:
                    dict3[k]=dict1.get(y)
                    ontology_path[k].append(dict1.get(y))
#merge synoynm, ontology_path, and dict3 dictionaries into NEW dictionary
    merged = {key: (value1, value2, value3) for key, value1, value2, value3 in zip(dict3.keys(), dict3.values(), ontology_path.values(), synonyms.values())}
#print new dictionary
    for k, v in merged.items():
        f.write(k+'\t'+'LABEL='+str(v[0])+'\t'+'PATH='+str(v[1])+'\t'+str(v[2])+'\n')



            