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
from collections import defaultdict
from _pytest.outcomes import skip


#load in owl ontology
onto = get_ontology("DEB_20191001.owl").load()
file_name = "DEB_20191001."
with open("test",'w') as f: 
    f.write('TERM\tLABEL\tSYNONYMS\n')
#return dictionary of class : all subclasses
#if class is subclassof another class, only include in parent 
    dict = {}
#classes = onto.classes()
#for i in classes:
#    if len(list(i.subclasses())) ==0:
#        pass
#    else:
#        dict[i]=list(i.subclasses())
#print(dict)
    superclass_list = ["Biomaterial","BiomaterialType",
  "BiologicallyActiveSubstance","ManufacturedObject","ManufacturedObjectComponent",
  "MedicalApplication","EffectOnBiologicalSystem","AdverseEffects","AssociatedBiologicalProcess",
  "Structure","Shape","ArchitecturalOrganization","DegradationFeatures",
  "ManufacturedObjectFeatures", "MaterialProcessing","StudyType","CellType"]
    ont_classes = onto.classes()
    for x in ont_classes:
        id = x.name.replace('_',':')
        synonym = str(x.equivalent_to)
        classes = [i for i in x.is_a]
        class_list = list(classes)
        if len(class_list)==1:
            if id in superclass_list:
                dict[id]=id
                f.write(id+'\t'+'LABEL='+id+'\n')
            else:
                superclass_full = str(class_list)
                superclass_edit = superclass_full[14:-1]
                dict[id]=superclass_edit
                f.write(id+'\t'+'LABEL='+superclass_edit+'\n')
        else:
            a = str(class_list[1:]).split("&")
            b = [i.replace("[DEB_20191001.","") for i in a]
            dict[id]=b[0] 
            f.write(id+'\t'+'LABEL='+b[0]+'\n')
            for k,v in dict.items():
            if v in superclass_list:
                pass
            else:
                for x, y in dict.items():
                    if v == x:
                        v == y
    print(dict)
                            
            

