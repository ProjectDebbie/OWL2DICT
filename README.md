# OWL2DICT

Web Ontology Language (OWL) files are a popular format for ontologies. Tools, such as OWLREADY and OWLREADY2 can be used for OWL ontology exploration and modification. 

For annotation tasks, and especially when using GATE, it is often necessary to convert ontologies to dictionaries. By default, when converting OWL files to dictionaries (for example: using Protege), the term's immediate parent class or the top superclass are automatically used as labels. However, in reality, and espeicially in complex ontologies with many levels, the user may want to use other higher level superclasses as labels.

The aim of OWL2DICT is to enable users to create a dictionary from owl files. The user can choose classes he would like as labels, and the tool will collect all children of this class as terms.    

The input of this tool is a list containing the desired labels (classes) in a designated file. OWL2DICT maps out the entire OWL file to retrieve all the child terms for the provided classes. OWL2DICT also retrieves any associated synonyms and/or properties for retrieved child terms.

In case a class of interest (ie a label) is within a different class of interest, OWL2DICT will label a term with its nearest parent. 


The output of OWL2DICT is a dictionary object in .txt file format.

## OWL2DICT Light

Thw OWL2DICT light is a simpler implementation of owlready2. It retrieves all classes (but no properties) for given ancestors  from an .owl ontology provided locally. It labels each class with provided 'new labels', creating a .txt dictionary in the same format shown below. 


### Prerequisites

Python 3+, argparse, configparser, logging, os, sys, owlready2, re

### Example

Food ontology:

Food
  Italian
    Pizza
      Margarita
      Capressa
    Pasta
  Japanese
    Sushi
    Udon
    
Requested labels: Italian, Japanese, Pizza 

Resulting Dictionary:

Pizza      Label: Italian
Margarita    Label: Pizza
Capressa    Label: Pizza
Pasta    Label: Italian
Sushi    Label: Japanese
Udon    Label: Japanese

## Authors

**Austin McKitrick, Javi Corvi and Osnat Hakimi** 



## License

This project is licensed under the GNU License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* This tool is related to Javi Corvi's send\_terminology\_retrieval tool (https://github.com/javicorvi/send\_terminology\_retrieval)
