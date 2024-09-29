import time
from actions_mas import *

# ---------------------------------------------------------------------
# PHIDIAS rules variable declaration
# ---------------------------------------------------------------------

def_vars("X", "Y", "D", "H", "Z", "L", "M", "A", "D", "W")

# ---------------------------------------------------------------------
# Agents section
# ---------------------------------------------------------------------

def create_agents(class_name):
    def main(self):
        # MoveAndCompleteJob intention
        +TASK(X, Y, Z)[{'from': M}] >> [show_line("\nWorker moving to (", X, ",", Y, "), received task from ", M), move_turtle(Z, X, Y), +COMM("DONE")[{'to': 'main'}]]

    # Creiamo una nuova classe con il metodo 'main' definito sopra
    return type(class_name, (Agent,), {"main": main})

for i in range(AGENT_NUMBER):
    class_name = f"{ID_PREFIX}{i+1}"
    globals()[class_name] = create_agents(class_name)

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
        load() >> [show_line("\nAsserting all OWL 2 triples beliefs...\n"), assert_beliefs_triples(), pre_process()]
        turn() / TRIPLE(X, "hasLedger",Z) >> [show_line("\nTurning triples beliefs into Semas beliefs...\n"), -TRIPLE(X,"hasLedger",Z), +LEDGER(X,"0"), AssignId(X), turn()]

        # desires
        setup() >> [show_line("Setup worktime...\n"), +WORKTIME(0), +DUTY_TIME(MAX_WORK_TIME)]
        work() >> [show_line("Starting task detection...\n"), Timer(MAX_WORK_TIME).start(), TaskDetect().start(), show_line("Workers on duty...")]

        # AssignJob intentions
        +TASK(X, Y) / (AGT(A, D) & DUTY(D)) >> [show_line("assigning job to ",A), -DUTY(D), +TASK(X, Y, D)[{'to': A}]]

        # ReceiveCommunication intentions
        +COMM(X)[{'from': W}] / LEDGER(W, H) >> [show_line("received job done comm from ", W), -LEDGER(W, H), UpdateLedger(W, H)]

        # Pause work intentions - MAX_WORKDAY_TIME must be multiple of MAX_WORK_TIME  (----> inserire ActiveBeliefs)
        +TIMEOUT("ON") / WORKTIME(MAX_WORKDAY_TIME) >> [show_line("\nWorkers are very tired. Finishing working day.\n"), TaskDetect().stop(), -WORKTIME(MAX_WORKDAY_TIME), stopwork()]

        +TIMEOUT("ON") / (WORKTIME(X) & DUTY_TIME(Y)) >> [show_line("\nWorkers are tired, they need some rest.\n"), TaskDetect().stop(), -WORKTIME(X), UpdateWorkTime(X, Y), noduty()]
        noduty() / (AGT(A, D) & DUTY(D)) >> [show_line("Putting agent", A, "to rest..."), -DUTY(D), noduty()]
        noduty() >> [rest(REST_TIME), work()]

        # Stop work intention
        stopwork() / ((AGT(A, D) & DUTY(D))) >> [show_line("\n-------------------------> Stopping ", A), -DUTY(D), stopwork()]
        stopwork() >> [show_line("\nAll workers were stopped. Starting payment process."), pay()]

        # pay desires
        pay() / LEDGER(Z, H) >> [show_line("\nSending payment to ",Z, " for ",H," tasks..."), -LEDGER(Z, H), pay()]
        pay() >> [show_line("\nPayments completed.")]



for i in range(AGENT_NUMBER):
    class_name = f"{ID_PREFIX}{i+1}"
    instance = globals()[class_name]()
    instance.start()

main().start()