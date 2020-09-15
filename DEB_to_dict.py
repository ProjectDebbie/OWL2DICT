
#input to provide
ontology = 'DEB_location'
new_labels = {'Biomaterial':'Biomaterial', 'AdverseEffects':'AdverseEffects',
              'Structure': 'Structure',
              'MaterialProcessing': 'MaterialProcessing',
              'BiomaterialType':'BiomaterialType',
              'BiologicallyActiveSubstance':'BiologicallyActiveSubstance',
              'ManufacturedObject':'ManufacturedObject',
              'ManufacturedObjectComponent':'ManufacturedObjectComponent',
              'MedicalApplication':'MedicalApplication',
              'ManufacturedObjectFeatures':'ManufacturedObjectFeatures',
              'ArchitecturalOrganization':'ArchitecturalOrganization',
              'Shape':'Shape', 'DegradationFeatures':'DegradationFeatures',
              'AssociatedBiologicalProcess':'AssociatedBiologicalProcess',
              'ResearchTechnique':'ResearchTechnique',
              'EffectOnBiologicalSystem': 'EffectOnBiologicalSystem',
              'StudyType': 'StudyType'}
new_dictionary = 'DEB_ONTOLOGY.lst'


# load ontology
from owlready2 import *
onto = get_ontology(ontology).load()
namespace = onto.get_namespace(ontology)

#lists
class_list = list(onto.classes())
ancestor_list = []
relevant_terms = []
property_list = list(onto.properties())
equivalent_properties = []
other_list = []

for p in property_list:
    e = str(p).lower()
    equivalent_properties.append(e)


#get all classes from wanted ancestors

for c in class_list:
    word = str(c)
    ancestors = list(c.ancestors())
    for term, label in new_labels.items():
        for a in ancestors:
            x = str(a)
            if term == x[8:] and c not in relevant_terms:
                relevant_terms.append(c)
                w = word[8:]
                a = w
                if w.isupper() == False:
                    a = re.sub(r"([A-Z])", r" \1", w).split()
                    a = ' '.join(a)
                    a = a.lower()
                with open(new_dictionary, 'a') as n:
                    n.write(a + '\t' + 'LABEL=' + label + '\t' + 'ID=' + str(c) + '\n')

#extract synonyms
                concept = list(c.altLabel)
                for synonym in concept:
                    s = synonym.lower()
                    with open(new_dictionary, 'a') as n:
                        n.write(s + '\t' + 'LABEL=' + label + '\t' + 'ID=' + str(c) + '\t' + 'PrefSynonym=' + a + '\t' + '\n')

#extract properties
                r = list(c.get_class_properties())
                for prop in r:
                    x = str(prop).lower()
                    if x in equivalent_properties and x not in other_list and x.startswith('deb_ont'):
                        other_list.append(x)
                        with open(new_dictionary, 'a') as n:
                            n.write(x[8:] + '\t' + 'LABEL=' + label + '\t' + 'ID=' + x + '\t' + 'PrefSynonym=' + a + '\t' + '\n')




