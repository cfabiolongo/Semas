import configparser
from owlready2 import *
import os
import threading
from phidias.Types import *


from flask import Flask, request, jsonify

app = Flask(__name__)

os.environ['FLASK_ENV'] = 'production'

config = configparser.ConfigParser()
config.read('config.ini')

# ONTOLOGY section
FILE_NAME = config.get('ONTOLOGY', 'FILE_NAME')
ONTO_NAME = config.get('ONTOLOGY', 'ONTO_NAME')

# REASONING Section
REASONING_ACTIVE = config.getboolean('REASONING', 'ACTIVE')
REASONER = config.get('REASONING', 'REASONER').split(",")
PREFIXES = config.get('REASONING', 'PREFIXES').split(",")
PREFIX = " ".join(PREFIXES)
PREFIX = PREFIX + f"PREFIX {ONTO_NAME}: <http://test.org/{FILE_NAME}#> "

# BDI-CLASSES Section
ENTITIES = config.get('CLASSES', 'Entities').split(",")

# Properties
BELIEFS = config.get('CLASSES', 'PHI-Beliefs').split(",")
DESIRES = config.get('CLASSES', 'PHI-Desires').split(",")
INTENTIONS = config.get('CLASSES', 'PHI-Intentions').split(",")

PROPERTIES = config.get('CLASSES', 'Properties').split(",")

try:
    my_onto = get_ontology(FILE_NAME).load()
    print("\nLoading worlds "+FILE_NAME+"...")
except IOError:
    my_onto = get_ontology("http://test.org/"+FILE_NAME)
    print("\nCreating new "+FILE_NAME+" file...")
    print("\nPlease Re-Run Semas.")
    my_onto.save(file=FILE_NAME, format="rdfxml")
    exit()


# instances name/instances dictionary
dict_ent = {}
# properties name/properites dictionary
dict_prop = {}


# Phidias belief containing OWL triples
class TRIPLE(Belief):
    pass



with my_onto:

    class ENTITY(Thing):
        pass

    class BELIEF(Thing):
        pass

    class DESIRE(Thing):
        pass

    class INTENTION(Thing):
        pass


    # Declaring Owlready properties
    for i in range(len(PROPERTIES)):
        globals()[PROPERTIES[i].strip()] = type(PROPERTIES[i].strip(), (ObjectProperty,), {})
        istanza = globals()[PROPERTIES[i].strip()]()
        dict_prop[PROPERTIES[i].strip()] = istanza





# Declaring Phidias belief from OWL
for i in range(len(BELIEFS)):
    # creating subclasses BELIEFS
    new_belief = types.new_class(BELIEFS[i].strip(), (BELIEF,))

    globals()[BELIEFS[i].strip()] = type(BELIEFS[i].strip(), (Belief,), {})
    istanza = globals()[BELIEFS[i].strip()]()

for i in range(len(DESIRES)):
    # creating subclasses DESIRES
    new_belief = types.new_class(DESIRES[i].strip(), (DESIRE,))

    globals()[DESIRES[i].strip()] = type(DESIRES[i].strip(), (Procedure,), {})
    istanza = globals()[DESIRES[i].strip()]()

for i in range(len(INTENTIONS)):
    # creating subclasses INTENTIONS
    new_belief = types.new_class(INTENTIONS[i].strip(), (INTENTION,))

    globals()[INTENTIONS[i].strip()] = type(INTENTIONS[i].strip(), (Reactor,), {})
    istanza = globals()[INTENTIONS[i].strip()]()


# ---------------------------------------------
# --------- Ontology modelling Section ---------
# ---------------------------------------------


class initWorld(Action):
    """World entities initialization"""
    def execute(self):

        # Entities
        for i in range(len(ENTITIES)):
            # creating subclasses ENTITY
            entity = types.new_class(ENTITIES[i].strip(), (ENTITY,))

            ENT_INDS = config.get('INDIVIDUALS', ENTITIES[i].strip()).split(",")

            # creating ENTITY individuals
            for j in range(len(ENT_INDS)):
                new_entity = entity(ENT_INDS[j].strip())
                dict_ent[ENT_INDS[j].strip()] = new_entity

        for i in range(len(BELIEFS)):
            BDI_INDS = config.get('INDIVIDUALS', BELIEFS[i].strip()).split(" & ")

            for j in range(len(BDI_INDS)):
                triple = BDI_INDS[j].strip()

                subject = triple.split(",")[0][1:].strip()
                prop = triple.split(",")[1].strip()
                object = triple.split(",")[2][:-1].strip()

                getattr(dict_ent[subject], prop).append(dict_ent[object])



class declareRules(Action):
    """assert an SWRL rule"""
    def execute(self):
        number_of_rules = int(config.get('SWRL', 'NUMBER_OF_RULES'))
        with my_onto:
           rule = Imp()

           print(f"\nAdding the following {number_of_rules} rules to ontology: ")
           for i in range(number_of_rules):
               rule_str = config.get('SWRL', 'RULE'+str(i+1))
               print(f"Rule {str(i+1)}: {rule_str}")
               rule.set_as_rule(rule_str)



class saveOnto(Action):
    """Creating a subclass of the class Verb"""
    def execute(self):
        with my_onto:
            #sync_reasoner_pellet()
            my_onto.save(file=FILE_NAME, format="rdfxml")
            print("Ontology saved.")


# ----------------------------------
# --------- SPARQL Section ---------
# ----------------------------------


class assert_beliefs_triples(Action):
    """create sparql query from MST"""
    def execute(self):

        q = PREFIX + f" SELECT ?subj ?prop ?obj" + " WHERE { "
        q = q + f"?subj ?prop ?obj. ?subj rdf:type/rdfs:subClassOf* {ONTO_NAME}:ENTITY. ?obj rdf:type/rdfs:subClassOf* {ONTO_NAME}:ENTITY." + "}"

        my_world = owlready2.World()
        my_world.get_ontology(FILE_NAME).load()  # path to the owl file is given here

        if REASONING_ACTIVE:
            # sync_reasoner_pellet(my_world, infer_property_values = True, infer_data_property_values = True)
            sync_reasoner_hermit(my_world, infer_property_values=True)
            # sync_reasoner_hermit(my_world)

        graph = my_world.as_rdflib_graph()
        result = list(graph.query(q))

        for res in result:

            subj = str(res).split(",")[0]
            subj = subj.split("#")[1][:-2]

            prop = str(res).split(",")[1]
            prop = prop.split("#")[1][:-2]

            obj = str(res).split(",")[2]
            obj = obj.split("#")[1][:-3]

            self.assert_belief(TRIPLE(subj, prop, obj))

# Funzione per avviare il server Flask in background


# ----------------------------------
# --------- RESTful Section ---------
# ----------------------------------

from phidias.Main import *

class load(Procedure): pass
class start_rest(Procedure): pass

def avvia_flask():
    app.run(port=5000)

flask_thread = threading.Thread(target=avvia_flask)

json_response = {"Response": []}


class start_rest_service(Action):
    """create sparql query from MST"""
    def execute(self):
        flask_thread.daemon = True  # Rende il thread daemon, così si chiude quando il programma principale termina
        flask_thread.start()



class build_json_response(Action):
    """build json response"""
    def execute(self, arg1, arg2):
       arg1 = str(arg1).split("'")[3]
       arg2 = str(arg2).split("'")[3]

       global json_response
       print("Setting json_response...")

       new_item = {
           arg1: arg2,
       }
       json_response['Response'].append(new_item)




# curl -X POST http://localhost:5000/build_publicationship -H "Content-Type: application/json" -d '{"testo": "Artificial-Intelligence"}'

@app.route('/build_publicationship', methods=['POST'])
def build_publicationship():
    # Verifica che il corpo della richiesta sia presente
    if not request.data:
        return jsonify({'errore': 'Richiesta vuota'}), 400

    # Tenta di elaborare la richiesta come JSON
    try:
        if request.is_json:
            testo = request.json['testo']
        else:
            # Se non è JSON, interpreta il corpo come stringa
            testo = request.data.decode('utf-8')
    except Exception as e:
        return jsonify({'errore': 'Formato non valido'}), 400

    PHIDIAS.achieve(Publicationship(testo), "main")

    # Crea e ritorna una risposta JSON con il testo elaborato
    return jsonify(json_response), 200



# curl -X POST http://localhost:5000/get_publicationship -H "Content-Type: application/json" -d '{"testo": "Artificial-Intelligence"}'

@app.route('/get_publicationship', methods=['POST'])
def get_publicationship():
    # Verifica che il corpo della richiesta sia presente
    if not request.data:
        return jsonify({'errore': 'Richiesta vuota'}), 400

    # Tenta di elaborare la richiesta come JSON
    try:
        if request.is_json:
            testo = request.json['testo']
        else:
            # Se non è JSON, interpreta il corpo come stringa
            testo = request.data.decode('utf-8')
    except Exception as e:
        return jsonify({'errore': 'Formato non valido'}), 400

    # Crea e ritorna una risposta JSON con il testo elaborato
    return jsonify(json_response), 200




