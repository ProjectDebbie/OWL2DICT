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


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

parser=argparse.ArgumentParser()
parser.add_argument('-owl_file', help='OWL File')
parser.add_argument('-dict_output_file', help='Dict Output')
args=parser.parse_args()
parameters={}
if __name__ == '__main__':
    import owl_to_dict
    parameters = owl_to_dict.ReadParameters(args)     
    owl_to_dict.Main(parameters)

codelist_id_dictionary ={};

#tengo que codificar la busqueda del primer padre que se encuenre en este diccionario para mapear con SEND
owl_to_dict_label_mapping = {
  "Biomaterial":"Biomaterial",
  "BiomaterialType":"Biomaterial_Type",
  "BiologicallyActiveSubstance":"Bioactive_Substance",
  "ManufacturedObject":"Manufactured_Object",
  "ManufacturedObjectComponent":"Manufactured_Object_Component",
  "MedicalApplication":"Medical_Application",
  "EffectOnBiologicalSystem":"Effect_On_Biological_System",
  "AdverseEffects":"Adverse_Effect",
  "AssociatedBiologicalProcess":"Associated_Biological_Process",
  "Structure":"Structure",
  "Shape":"Shape",
  "ArchitecturalOrganization":"Architecture",
  "DegradationFeatures":"Degradation",
  "ManufacturedObjectFeatures":"Other_Features", 
  "MaterialProcessing":"Material_Processing",
  "StudyType":"Study_Type",
  "CellType":"Cell_Type",
}



def ReadParameters(args):
    if(args.owl_file!=None and args.dict_output_file!=None):
        parameters['owl_file']=args.owl_file
        parameters['dict_output_file']=args.dict_output_file
    else:
        logging.error("Please send the correct parameters --help ")
        sys.exit(1)
    return parameters   

def Main(parameters):
    
    
    owl_file = parameters['owl_file']
    dict_output_file=parameters['dict_output_file']
    
    #convertion to basic dictionary tab separated with column names
    owl_to_dict(owl_file, dict_output_file)
    
    #convert to specifi gate format from tab separated dictionary
    #dict_to_gate_gazetter(dict_output_file, dict_output_file.replace(".txt",".lst"))
      
def owl_to_dict(owl_file, output_dict_file_path):
    logging.info("owl_to_dict")
    terms_list = []
    with open(output_dict_file_path,'w') as dict: 
        dict.write('INTERNAL_CODE\tTERM\tLABEL\n')
        #obonet is used for Obo format.
        #In this case we have to convert form owl and for that you have to use Owlready2 to iterate over the ontology and generate a txt dictionary.
        #https://pypi.org/project/Owlready2/ 
        graph = owlready2.get_ontology(owl_file)
        graph.save()
    #     internal_code = 1
    #     id_to_name = {id_: data for id_, data in graph.nodes(data=True)}
    #     for node in graph.nodes(data=True):
    #         id = node[0]
    #         data = node[1]
    #         term = data['name'].lower()
            
    #         #print node in dictionary
    #         parents = networkx.descendants(graph, id)
    #         label_map = owl_to_dict_label_mapping.get(id)
    #         if(label_map is None): #look for nearest parent in the owl_to_dict_label_mapping 
    #             for id_parent in parents:
    #                 label_map = owl_to_dict_label_mapping.get(id_parent)    
    #                 if(label_map is not None):
    #                     break
    #         if(label_map is None):
    #             label_map = ' '
    #         terms_list.append(name)
    #         dict.write(str(internal_code) +'\t'+name+'\t'+label_map+'\n')    
    #         internal_code = internal_code + 1
            
    #         dict.flush()   
    # logging.info(" Process end" )
        
def dict_to_gate_gazetter(file, file_new):
    with open(file,'r') as dictionary:
        with open(file_new,'w') as gate_gazetter:
            firstline = dictionary.readline()
            column_names = [i.replace("\n","") for i in firstline.split('\t')]
            next(dictionary)
            for line in dictionary:
                data = line.split('\t')
                newline = data[1] + '\t' + column_names[0].replace("\n","") + '=' + data[0].replace("\n","")
                for a,b in zip(column_names[2:],data[2:]):
                    if b.strip()!='':
                        newline = newline + '\t' + a.replace("\n","") + '=' + b.replace("\n","")
                gate_gazetter.write(newline+'\n')
                gate_gazetter.flush()
