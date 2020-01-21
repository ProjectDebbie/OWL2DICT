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

