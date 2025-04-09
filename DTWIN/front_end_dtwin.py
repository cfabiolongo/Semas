import time
from actions_dtwin import *

# ---------------------------------------------------------------------
# PHIDIAS rules variable declaration
# ---------------------------------------------------------------------

def_vars("X", "Y", "D", "H", "Z", "L", "M", "A", "D", "W")

# ---------------------------------------------------------------------
# Agents section
# ---------------------------------------------------------------------

agents = get_agents_names()[1:]

if len(agents) == 0:
   print("\nWARNING: Agents list is empty. Please initialize the ontology with init() from the eShell, then restart Semas.")
else:
   print("Agents list: ", agents)


def create_agents(class_name):
    def main(self):
        # MoveAndCompleteJob intention
        +TASK(X, Y, A)[{'from': M}] >> [show_line("\n",A," is moving to (", X, ",", Y, "), received task from ", M), move_turtle(A, X, Y), +COMM("DONE")[{'to': 'main'}]]

    return type(class_name, (Agent,), {"main": main})


def create_custom_agent(class_name):
    def main(self):
        # MoveAndCompleteJob intention
        with open("main_script.txt", 'r') as f:
            script_code = f.read()
        exec(script_code, globals(), locals())

    return type(class_name, (Agent,), {"main": main})

# General agents from OWL
for i in range(len(agents)):
    globals()[agents[i]] = create_agents(agents[i])

for i in range(len(agents)):
    instance = globals()[agents[i]]()

# custom agent rocco
globals()["rocco"] = create_custom_agent("rocco")
instance = globals()["rocco"]()


# ---------------------------------------------------------------------
# Agent 'main'
# ---------------------------------------------------------------------

class main(Agent):
    def main(self):

        # World initialization
        init() >> [show_line("\nInitialiting Ontology...\n"), initWorld(), declareRules(), saveOnto()]

        # Importing related triples
        load() >> [show_line("\nAsserting all OWL 2 triples beliefs...\n"), assert_beliefs_triples(), show_line("\nTurning triples beliefs into Semas beliefs...\n"), turn()]
        turn() / TRIPLE(X, "hasLedger",Z) >> [-TRIPLE(X,"hasLedger",Z), +LEDGER(X,"0"), AssignId(X), turn()]

        # desires
        setup() / WORKTIME(W) >> [show_line("Setup worktime again...\n"), load(), -WORKTIME(W), +WORKTIME(0)]
        setup() >> [show_line("Setup worktime...\n"), +WORKTIME(0), +MAX_WORK_TIME(Max_Work_Time), +MAX_WORKDAY_TIME(Max_WorkDay_Time), +REST_TIME(Rest_Time)]
        work() >> [show_line("Starting task detection...\n"), Timer(Max_Work_Time).start(), TaskDetect().start(), show_line("Workers on duty...")]

        # AssignJob intentions
        +TASK(X, Y) / (AGT(A, D) & DUTY(D)) >> [show_line("assigning job to ",A), -DUTY(D), +TASK(X, Y, A)[{'to': A}]]

        # ReceiveCommunication intentions
        +COMM(X)[{'from': W}] / LEDGER(W, H) >> [show_line("received job done comm from ", W), -LEDGER(W, H), UpdateLedger(W, H)]

        # Pause work intentions - check if the whole working time belief WORKTIME is greater-equal than MAX_WORKDAY_TIME
        +TIMEOUT("ON") / (WORKTIME(X) & MAX_WORKDAY_TIME(Y) & geq(X,Y)) >> [show_line("\nWorkers are very tired. Finishing working day.\n"), TaskDetect().stop(), stopwork()]

        # End work intentions - Add the MAX_WORK_TIME quantity (during the pause) to the whole working time belief WORKTIME
        +TIMEOUT("ON") / (WORKTIME(X) & MAX_WORK_TIME(Y)) >> [show_line("\nWorkers are tired, they need some rest.\n"), TaskDetect().stop(), -WORKTIME(X), UpdateWorkTime(X, Y), noduty()]
        noduty() / (AGT(A, D) & DUTY(D)) >> [show_line("Putting agent" , A, " to rest..."), -DUTY(D), noduty()]
        noduty() / REST_TIME(X) >> [rest(X), work()]

        # Stop work intention
        stopwork() / (AGT(A, D) & DUTY(D)) >> [show_line("\n-------------------------> Stopping ", A), -DUTY(D), stopwork()]
        stopwork() >> [show_line("\nAll workers were stopped. Starting payment process."), pay()]

        # pay desires
        pay() / LEDGER(Z, H) >> [show_line("\nSending payment to ",Z, " for ",H," tasks..."), -LEDGER(Z, H), pay()]
        pay() >> [show_line("\nPayments completed.")]

        # Sending belief to agent
        send(A, X) >> [show_line("Sending belief TASK(",X,") to agent ", A), +AGT(A), +TASK(X)]
        +TASK(X) / AGT(A) >> [-AGT(A), +TASK(X)[{'to': A}]]


# General agents
for i in range(len(agents)):
    instance = globals()[agents[i]]()
    instance.start()

# Custom agent
instance = globals()["rocco"]()
instance.start()

main().start()

# PHIDIAS.achieve(load(), "main")
# PHIDIAS.achieve(setup(), "main")
# PHIDIAS.achieve(work(), "main")