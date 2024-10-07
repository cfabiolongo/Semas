from owlready2 import *

# Carica l'ontologia da file
def load_ontology(file_path):
    onto = get_ontology(file_path).load()
    return onto

# Estrai individui di una classe specifica
def extract_individuals(onto, class_name):
    individuals = []
    owl_class = onto.search_one(iri="*" + class_name)
    if owl_class:
        individuals = list(owl_class.instances())
    return individuals

# Scrivi su file le liste degli individui
def write_individuals_to_file(oggetti, metodi, output_file):
    with open(output_file, "w") as f:
        oggetti_str = ", ".join([ind.name for ind in oggetti])
        metodi_str = ", ".join([ind.name for ind in metodi])
        f.write(f"[{oggetti_str}] >> [{metodi_str}]\n")

# Funzione principale
def main(ontology_file, output_file):
    onto = load_ontology(ontology_file)

    # Estrai individui delle classi OGGETTO e METODO
    oggetti = extract_individuals(onto, "OGGETTO")
    metodi = extract_individuals(onto, "METODO")

    # Scrivi i risultati su file
    write_individuals_to_file(oggetti, metodi, output_file)

# Esempio di utilizzo
ontology_file = "percorso/alla/tua/ontologia.owl"  # Modifica con il percorso corretto
output_file = "output.py"  # Nome del file di output
main(ontology_file, output_file)
