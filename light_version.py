#This version simply retrieves all classes for a given ancestor from an .owl ontology provided locally, creating a .txt dictionary 

import owlready2

#input to provide
ontology = 'path/to/extracted/ontology.owl'
wanted_superclasses = ['blabla', 'blabla2']
new_dictionary = 'dictionary_name.txt'


# load ontology
from owlready2 import *
onto = get_ontology(ontology).load()
namespace = onto.get_namespace(ontology)

#lists
class_list = list(onto.classes())
label_list = []
ancestor_list = []

#get all classes (if needed)
for c in class_list:
    label_list.append(c.label)

#get all classes from wanted ancestors
for c in class_list:
    ancestors = list(c.ancestors())
    for a in ancestors:
        for superclass in wanted_superclasses:
            x = a.label
            if superclass in str(x):
                with open(new_dictionary, 'a') as n:
                    n.write(c.label[0] + '\t' + 'LABEL=' + x[0] +'\n')
