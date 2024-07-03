import sys
import time
import threading
import random
import turtle

sys.path.insert(0, "../lib")

from phidias.Lib import *
from phidias.Agent import *
from phidias.Types import *

import configparser
from owlready2 import *

config = configparser.ConfigParser()
config.read('config_mas.ini')

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
REACTORS = config.get('CLASSES', 'PHI-Reactors').split(",")
DESIRES = config.get('CLASSES', 'PHI-Desires').split(",")
INTENTIONS = config.get('CLASSES', 'PHI-Intentions').split(",")
GROUNDS = config.get('CLASSES', 'PHI-Grounds').split(",")

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

    class REACTOR(Thing):
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

for i in range(len(REACTORS)):
    # creating subclasses BELIEFS
    new_belief = types.new_class(REACTORS[i].strip(), (REACTOR,))

    globals()[REACTORS[i].strip()] = type(REACTORS[i].strip(), (Reactor,), {})
    istanza = globals()[REACTORS[i].strip()]()

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


# ---------------------------------------------------------------------
# System procedures section
# ---------------------------------------------------------------------

# Ontology intialization
class init(Procedure): pass

# Processing beliefs
class load(Procedure): pass

# Import OWL triples
class pre_process(Procedure): pass

# ---------------------------------------------------------------------
# Ontology section
# ---------------------------------------------------------------------


# ID prefix
ID_PREFIX = "worker"
# Agent number
AGENT_NUMBER = 3
# Max work time for a worker (seconds)
MAX_WORKDAY_TIME = 30
# Max work time for a worker (seconds)
MAX_WORK_TIME = 5
# Rest time for a worker (seconds)
REST_TIME = 3


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

        print("BELIEFS: ", BELIEFS)

        for i in range(len(BELIEFS)):
            BDI_INDS = config.get('INDIVIDUALS', BELIEFS[i].strip()).split(" & ")

            for j in range(len(BDI_INDS)):
                triple = BDI_INDS[j].strip()

                print("BELIEFS: ", BELIEFS)
                print("BDI_INDS: ", BDI_INDS)
                print("triple: ", triple)

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



# ---------------------------------------------------------------------
# Non-ontological variables
# ---------------------------------------------------------------------

# Coordinates spamming range
N = 500
# time-range to get the job done
LOWER_BOUND = 0
UPPER_BOUND = 4

# Worker-Turtle dictionary
dict_turtle = {}

# ---------------------------------------------------------------------
# Sensors section
# ---------------------------------------------------------------------

class TaskDetect(Sensor):

    def on_start(self):
        # Starting task detection
       self.running = True

    def on_restart(self):
        # Re-Starting task detection
        self.do_restart = True

    def on_stop(self):
        #Stopping task detection
        self.running = False

    def sense(self):
        while self.running:
           time.sleep(1)

           pos_x = random.randint(-N // 2, N // 2)
           pos_y = random.randint(-N // 2, N // 2)
           self.assert_belief(TASK(pos_x, pos_y))



class Timer(Sensor):

    def on_start(self, uTimeout):
        evt = threading.Event()
        self.event = evt
        self.timeout = uTimeout()
        self.do_restart = False


    def on_restart(self, uTimeout):
        self.do_restart = True
        self.event.set()

    def on_stop(self):
        self.do_restart = False
        self.event.set()

    def sense(self):
        while True:
            time.sleep(self.timeout)
            self.event.clear()
            if self.do_restart:
                self.do_restart = False
                continue
            elif self.stopped:
                self.assert_belief(TIMEOUT("ON"))
                return
            else:
                return


# ---------------------------------------------------------------------
# Turtle section
# ---------------------------------------------------------------------


class move_turtle(Action):
    """moving turtle to coordinates (x,y)"""
    def execute(self, arg0, arg1, arg2):
      # print(arg0, arg1, arg2)
      id_turtle = str(arg0).split("'")[2]
      pos_x = str(arg1).split("'")[2]
      pos_y = str(arg2).split("'")[2]

      id_turtle = id_turtle[1:-1]
      pos_x = int(pos_x[1:-1])
      pos_y = int(pos_y[1:-1])

      dict_turtle["t"+id_turtle].goto(pos_x, pos_y)

      # time to get the job done
      rnd = random.uniform(LOWER_BOUND, UPPER_BOUND)
      time.sleep(rnd)



class rest(Action):
    """resting for few seconds"""
    def execute(self, arg):
      rest_time = int(str(arg))
      print(f"\nresting for {rest_time} seconds...")

      for t in dict_turtle:
          dict_turtle[t].color("red")

      time.sleep(rest_time)

      for t in dict_turtle:
          dict_turtle[t].color("black")



class UpdateLedger(Action):
    """Update completed jobs"""
    def execute(self, arg1, arg2):

      agent = str(arg1)[1:-1]
      jobs = int(str(arg2).split("'")[3])
      jobs = jobs + 1
      print(f"Updating {agent} ledger: {jobs}")
      self.assert_belief(LEDGER(agent, str(jobs)))


class UpdateWorkTime(Action):
    """Update completed jobs"""
    def execute(self, arg1, arg2):

        arg1_num = str(arg1).split("'")[2][1:-1]
        arg2_num = str(arg2).split("'")[2][1:-1]
        arg_num_tot = int(arg1_num)+int(arg2_num)
        self.assert_belief(WORKTIME(arg_num_tot))



# ---------------------------------------------------------------------
# Variable declaration
# ---------------------------------------------------------------------

def_vars("X","Y", "D", "H", "Z", "L", "M")


# ---------------------------------------------------------------------
# Agents section
# ---------------------------------------------------------------------


def create_class_with_main(class_name):
    def main(self):
        # MoveAndCompleteJob intention
        +TASK(X, Y, Z)[{'from': M}] >> [show_line("\nWorker moving to (", X, ",", Y, "), received task from ", M), move_turtle(Z, X, Y), +COMM("DONE")[{'to': 'main'}]]

    # Creiamo una nuova classe con il metodo 'main' definito sopra
    return type(class_name, (Agent,), {"main": main})

for i in range(AGENT_NUMBER):
    class_name = f"{ID_PREFIX}{i+1}"
    globals()[class_name] = create_class_with_main(class_name)

# Ora puoi creare istanze delle nuove classi e chiamare il loro metodo main
for i in range(AGENT_NUMBER):
    class_name = f"{ID_PREFIX}{i+1}"
    instance = globals()[class_name]()
    instance.main()



# ---------------------------------------------------------------------
# Agent 'main'
# ---------------------------------------------------------------------

class main(Agent):
    def main(self):

        # World initialization
        init() >> [show_line("\nInitialiting Ontology...\n"), initWorld(), declareRules(), saveOnto()]

        # Importing related triples
        load() >> [show_line("\nAsserting all OWL 2 beliefs triples...\n"), assert_beliefs_triples(), pre_process()]

        # desires
        setup() >> [show_line("Setup jobs ledger...\n"), +LEDGER("worker1", "0"), +LEDGER("worker2", "0"), +LEDGER("worker3", "0"), +WORKTIME(0), +DUTY_TIME(MAX_WORK_TIME)]
        work() >> [show_line("Starting task detection...\n"), +DUTY(1), +DUTY(2), +DUTY(3), Timer(MAX_WORK_TIME).start(), TaskDetect().start(), show_line("Workers on duty...")]

        # AssignJob intentions
        +TASK(X, Y) / DUTY(1) >> [show_line("assigning job to worker1"), -DUTY(1), +TASK(X, Y, 1)[{'to': "worker1"}]]
        +TASK(X, Y) / DUTY(2) >> [show_line("assigning job to worker2"), -DUTY(2), +TASK(X, Y, 2)[{'to': "worker2"}]]
        +TASK(X, Y) / DUTY(3) >> [show_line("assigning job to worker3"), -DUTY(3), +TASK(X, Y, 3)[{'to': "worker3"}]]

        # ReceiveCommunication intentions
        +COMM(X)[{'from': "worker1"}] / LEDGER("worker1", H) >> [show_line("received job done comm from worker1"), -LEDGER("worker1", H), UpdateLedger("worker1", H), +DUTY(1)]
        +COMM(X)[{'from': "worker2"}] / LEDGER("worker2", H) >> [show_line("received job done comm from worker2"), -LEDGER("worker2", H), UpdateLedger("worker2", H), +DUTY(2)]
        +COMM(X)[{'from': "worker3"}] / LEDGER("worker3", H) >> [show_line("received job done comm from worker3"), -LEDGER("worker3", H), UpdateLedger("worker3", H), +DUTY(3)]

        # Pause work intentions - WORKTIME value is (DUTY_TIME * 6)
        +TIMEOUT("ON") / WORKTIME(MAX_WORKDAY_TIME) >> [show_line("\nWorkers are very tired Finishing working day.\n"), +STOPWORK("YES")]
        +TIMEOUT("ON") / (WORKTIME(X) & DUTY_TIME(Y)) >> [show_line("\nWorkers are tired, they need some rest.\n"), TaskDetect().stop(), -DUTY(1), -DUTY(2), -DUTY(3), -WORKTIME(X), UpdateWorkTime(X, Y), rest(REST_TIME), work()]

        # Stop work intention
        +STOPWORK("YES") >> [show_line("\nWorking day completed."), -DUTY(1), -DUTY(2), -DUTY(3), TaskDetect().stop(), -WORKTIME(MAX_WORKDAY_TIME), pay()]

        # pay desires
        pay() / LEDGER(Z, H) >> [show_line("\nSending payment to ",Z, " for ",H," tasks..."), -LEDGER(Z, H), pay()]
        pay() >> [show_line("\nPayments completed.")]



def turtle_thread_func():
    wn = turtle.Screen()
    wn.title("Workers jobs assignment")

    for i in range(AGENT_NUMBER):
        dict_turtle["t"+str(i+1)] = turtle.Turtle()

    wn.mainloop()


# Avviare il thread della tartaruga
turtle_thread = threading.Thread(target=turtle_thread_func)
turtle_thread.daemon = True
turtle_thread.start()


for i in range(AGENT_NUMBER):
    class_name = f"{ID_PREFIX}{i+1}"
    instance = globals()[class_name]()
    instance.start()

main().start()


# run the engine shell
PHIDIAS.shell(globals())
