#!/usr/bin/env python3
import argparse
import configparser
import logging
import os
import sys
import owlready2
from owlready2 import get_ontology
import re
import pprint

pp = pprint.PrettyPrinter(indent=4)

# get filename
# path, file = os.path.split("DEB_20200220.owl")
path, file = os.path.split("DEB_ontology_13082020.owl")
# remove "owl" from file name, keep "."
file_name = file[:-3]
# load ontology
onto = get_ontology(file).load()
# owlready doesn't automatically remove these special characters or the file name
removal = ["[", file_name, "]", " ", '.value(True)', '.some(True)', '.some(None)', "_"]
with open("DEB_ONTOLOGY.lst", 'w') as f:
    # create dictionaries for synonyms, all classes of individual terms, alternative lables (altLab) and properties
    synonyms = {}
    ids = {}
    altLabs = {}
    ontology_path = {}
    properties = {}
    merged = {}
    # two dictionaries will be identical, third will be the final one with changes
    dict_all_terms = {}
    dict_superclasses = {}
    # list of superclasses
    superclass_list = ["Biomaterial", "BiomaterialType",
                       "BiologicallyActiveSubstance", "ManufacturedObject", "ManufacturedObjectComponent",
                       "MedicalApplication", "EffectOnBiologicalSystem", "AdverseEffects",
                       "AssociatedBiologicalProcess",
                       "Structure", "Shape", "ArchitecturalOrganization", "DegradationFeatures",
                       "ManufacturedObjectFeatures", "MaterialProcessing", "StudyType", "CellType"]
    ont_classes = onto.classes()
    for x in ont_classes:
        id = x
        terms = x.name
        altLab = re.sub(r'|'.join(map(re.escape, removal)), '', str(x.altLabel))
        altLab = altLab.split(',')
        altLab = list(filter(None, altLab))
        altLab = [i.replace("'", "") for i in altLab]
        # print(altLab)
        synonym = re.sub(r'|'.join(map(re.escape, removal)), '', str(x.equivalent_to))
        # print(synonym)
        ids[terms] = id
        altLabs[terms] = altLab
        synonyms[terms] = synonym
        classes = [i for i in x.is_a]
        # print(classes)
        class_list = list(classes)
        properties[terms] = ''
        # if term is in superclass_list, term is superlclass (i.e. Biomaterial = Biomaterial)
        if len(class_list) == 1:
            if terms in superclass_list:
                dict_all_terms[terms] = terms
            else:
                for term in removal:
                    c = str(class_list)
                    d = re.sub(r'|'.join(map(re.escape, removal)), '', c)
                    dict_all_terms[terms] = d
        # if term is not in super class list
        # # #if length is more than 1, owl.Thing is [0]
        else:
            a = str(class_list[1:2]).split("&")
            b = [re.sub(r'|'.join(map(re.escape, removal)), '', a[0])]
            onProperty = [re.sub(r'|'.join(map(re.escape, removal)), '', a[1])]
            dict_all_terms[terms] = b[0]
            properties[terms] = onProperty[0]
        # f.write(str(terms) + '\t' + 'LABEL=' + '\t' + 'ID=' + str(id) + '\t' +  '\n')
        # if len(altLab) == 0:
        #     pass
        # else:
        #     for i in altLab:
        #         f.write(str(i) + '\t' + 'LABEL=' + '\t' + 'ID=' + str(id) + '\t' + 'PREFSYNONYM=' + str(terms) +  '\n')

    # we have all terms and their direct parent class
    # now we retrieve their superparent class
    for k, v in dict_all_terms.items():
        ontology_path[k] = [v]
        term = k
        parent = v
        variable = None
        if parent in superclass_list:
            dict_superclasses[k] = parent
        else:
            variable = dict_all_terms.get(parent)
            ontology_path[k].append(variable)
            if variable not in superclass_list:
                variable = dict_all_terms.get(variable)
                ontology_path[k].append(variable)
            else:
                dict_superclasses[term] = variable
    # pp.pprint(dict_superclasses)
    # pp.pprint(altLabs)
    # # print(altLabs)

    # merge synonym, ontology_path, and dict3 dictionaries into NEW dictionary
    # pp.pprint(dict_superclasses)
    # pp.pprint(altLabs)
    # pp.pprint(ids)
    keys = dict_superclasses.keys()
    ids_sorted = {i:ids[i] for i in dict_superclasses.keys()}
    synonyms_sorted = {i:synonyms[i] for i in dict_superclasses.keys()}
    properties_sorted = {i:properties[i] for i in dict_superclasses.keys()}
    altLabs_sorted = {i:altLabs[i] for i in dict_superclasses.keys()}
    ontology_path_sorted = {i:ontology_path[i] for i in dict_superclasses.keys()}
    values = zip(dict_superclasses.values(), ids_sorted.values(), ontology_path_sorted.values(), synonyms_sorted.values(), properties_sorted.values(), altLabs_sorted.values())
    merged = dict(zip(keys, values))
    # pp.pprint(merged)
    # merged.update({key: [value1, value2, value3, value4, value5] for key, value1, value2, value3, value4, value5 in
    #                zip(dict_superclasses.keys(), dict_superclasses.values(), ids.values(), synonyms.values(),
    #                    properties.values(), altLabs.values())})
    # print(merged)

    # # if key has a property or altLabel associated, a new line with property as key is created
    # for k, v in list(merged.items()):
    #     if len(v[3]) is not 0:
    #         merged.update({v[3]: [v[0], v[1], v[2], v[4], k]})
    #     elif len(v[4]) is not 0:
    #         merged.update({v[4]: [v[0], v[1], v[2], v[3], k]})
    
    # clean all terms
    for k, v in merged.items():
        path = v[2]
        path = [x for x in path if x is not None]
        path = [ x for x in path if "owl.Thing" not in x ]
        synonym = v[3]
        property = v[4]
        altLab = v[5]
        if k.isupper() == True:
            k = k
        elif synonym.isupper() == True:
            synonym = synonym
        elif property.isupper() == True:
            property = property
        # elif altLab.isupper() == True:
        #     altLab = altLab
        #     print(altLab)
        else:
            clean_k = re.sub(r"([A-Z])", r" \1", k).split()
            clean_synonym = re.sub(r"([A-Z])", r" \1", synonym).split()
            clean_property = re.sub(r"([A-Z])", r" \1", property).split()
            # clean_altLab = altLab.split(",")
            k = ' '.join(clean_k)
            k = k.replace("3 D", "3D")
            k = k.replace("- ", "-")
            k = k.lower()
            synonym = ' '.join(clean_synonym)
            synonym = synonym.replace("3 D", "3D")
            synonym = synonym.replace("- ", "-")
            synonym = synonym.lower()
            property = ' '.join(clean_property)
            property = property.replace("3 D", "3D")
            property = property.replace("- ", "-")
            property = property.lower()
        f.write(str(k) + '\t' + 'LABEL=' + str(v[0]) + '\t' + 'PATH=' + str(path) + '\t' + 'SYNONYM=' + str(
            synonym) + '\t' + 'PROPERTY=' + str(property) + '\t' + '\n')
        for i in altLab:
            if i.isupper() == True:
                f.write(str(i) + '\t' + 'LABEL=' + str(v[0]) + '\t' + 'PATH=' + str(path) + '\t' + 'SYNONYM=' + str(synonym) + '\t' + 'PROPERTY=' + str(property) + '\t' + 'PREFSYN=' + str(k) +  '\n')
            elif i == 'rhBMP':
                f.write(str(i) + '\t' + 'LABEL=' + str(v[0]) + '\t' + 'PATH=' + str(path) + '\t' + 'SYNONYM=' + str(synonym) + '\t' + 'PROPERTY=' + str(property) + '\t' + 'PREFSYN=' + str(k) +  '\n')
            elif '-' in i:
                f.write(str(i) + '\t' + 'LABEL=' + str(v[0]) + '\t' + 'PATH=' + str(path) + '\t' + 'SYNONYM=' + str(synonym) + '\t' + 'PROPERTY=' + str(property) + '\t' + 'PREFSYN=' + str(k) +  '\n')
            elif '(' in i:
                f.write(str(i) + '\t' + 'LABEL=' + str(v[0]) + '\t' + 'PATH=' + str(path) + '\t' + 'SYNONYM=' + str(synonym) + '\t' + 'PROPERTY=' + str(property) + '\t' + 'PREFSYN=' + str(k) +  '\n')
            else:
                a = re.sub(r"([A-Z])", r" \1", i).split()
                a = ' '.join(a)
                a = a.lower()
                f.write(str(a) + '\t' + 'LABEL=' + str(v[0]) + '\t' + 'PATH=' + str(path) + '\t' + 'SYNONYM=' + str(synonym) + '\t' + 'PROPERTY=' + str(property) + '\t' + 'PREFSYN=' + str(k) +  '\n')


