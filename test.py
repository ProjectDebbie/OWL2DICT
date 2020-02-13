#!/usr/bin/env python3
import argparse
import configparser
import logging
import os
import sys
import urllib.request
import owlready2
import networkx
import xml.etree.ElementTree as ET
from owlready2 import get_ontology


#load in owl ontology
onto = get_ontology("DEB_20191001.owl").load()
file_name = "DEB_20191001."
removal = ["[", file_name, "]"]
with open("test",'w') as f: 
    f.write('TERM\tLABEL\n')
#return dictionary of class : all subclasses
#if class is subclassof another class, only include in parent 
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
        synonym = str(x.equivalent_to)
        classes = [i for i in x.is_a]
        class_list = list(classes)
#if term is in superclass_list, term is superlclass (i.e. Biomaterial = Biomaterial)
        if len(class_list)==1:
            if id in superclass_list:
                dict1[id]=id
                dict2[id]=id
                #f.write(id+'\t'+id+'\n')
            else:
                c = str(class_list)
                d = c.replace("["+file_name,"")
                e = d.replace("]","")
                g = e.replace(" ","")
                dict1[id]=g
                dict2[id]=g
                #f.write(id+'\t'+g+'\n')
#if term is not in super class list
#if length is more than 1, owl.Thing is [0]
        else:
            a = str(class_list[1:2]).split("&")
            b = [i.replace("["+file_name,"") for i in a]
            h = [i.replace(" ","") for i in b]
            dict1[id]=h[0]
            dict2[id]=h[0] 
            #f.write(id+'\t'+h[0]+'\n')
    for k, v in dict2.items():
        if v in superclass_list:
            dict3[k] = v
        else: 
            dict3[k]=dict1.get(v)
            for x,y in dict3.items():
                if y not in superclass_list:
                    dict3[k]=dict1.get(y)
    for k,v in dict3.items():
        f.write(k+'\t'+'LABEL='+v+'\n')
    


            