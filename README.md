# OWL2DICT

Web Ontology Language (OWL) files have become a popular format for biomedical ontologies. OWL format provides many benefits for annotation purposes such as reasoning and quantified relationships. Tools, such as OWLREADY and OWLREADY2, have allowed for OWL ontology exploration and modification via Python.

However, no tool has been available to extract these meaningful relationships in order to annotate files. By default, OWL files provide information on a term's immediate parent class, but not on higher levels. These higher levels, or superclasses, are often used for annotation categories. Therefore, it is necessary to extract terms and their superclasses. 

After the user inputs a list containing the superclasses in their designated file, OWL2DICT maps out the entire OWL file to retrieve each term's superclass. OWL2DICT also retrieves each individual class that a term belongs to, and any associated synonyms and/or properties.

The output of OWL2DICT is a txt file that is ready to be uploaded to GATE, or a similar annotation program.    

### Prerequisites

Python 3+, argparse, configparser, logging, os, sys, owlready2, re

## Authors

* **Austin McKitrick** 


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Work inspired by Javi Corvi's send\_terminology\_retrieval tool (https://github.com/javicorvi/send\_terminology\_retrieval)
