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


#load in owl ontology
onto = get_ontology("DEB_20191001.owl").load()

#return dictionary of class : all subclasses
#if class is subclassof another class, only include in parent 
dict = {}
classes = onto.classes()
for i in classes:
    if len(list(i.subclasses())) ==0:
        pass
    else:
        dict[i]=list(i.subclasses())
print(dict)


dict2 = dict.fromkeys(["DEB_20191001.Biomaterial","DEB_20191001.BiomaterialType",
  "BiologicallyActiveSubstance","ManufacturedObject","ManufacturedObjectComponent","MedicalApplication",
  "EffectOnBiologicalSystem","AdverseEffects","AssociatedBiologicalProcess","Structure","Shape","ArchitecturalOrganization",
  "DegradationFeatures","ManufacturedObjectFeatures", "MaterialProcessing","StudyType","CellType", "Other"])
ont_classes = onto.classes()
for x in ont_classes:
    id = x.name.replace('_',':')
    superclasses = [i for i in x.is_a if not isinstance(i,owlready2.entity.Restriction)]
    print (id, superclasses)

