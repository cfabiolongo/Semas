import time
from actions_mas import *

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
        setup() >> [show_line("Setup jobs ledger...\n"), +LEDGER("worker1", "0"), +LEDGER("worker2", "0"), +LEDGER("worker3", "0"), +LEDGER("worker4", "0"), +WORKTIME(0), +DUTY_TIME(MAX_WORK_TIME)]
        work() >> [show_line("Starting task detection...\n"), +DUTY(1), +DUTY(2), +DUTY(3), +DUTY(4), Timer(MAX_WORK_TIME).start(), TaskDetect().start(), show_line("Workers on duty...")]

        # AssignJob intentions
        +TASK(X, Y) / DUTY(1) >> [show_line("assigning job to worker1"), -DUTY(1), +TASK(X, Y, 1)[{'to': "worker1"}]]
        +TASK(X, Y) / DUTY(2) >> [show_line("assigning job to worker2"), -DUTY(2), +TASK(X, Y, 2)[{'to': "worker2"}]]
        +TASK(X, Y) / DUTY(3) >> [show_line("assigning job to worker3"), -DUTY(3), +TASK(X, Y, 3)[{'to': "worker3"}]]
        +TASK(X, Y) / DUTY(4) >> [show_line("assigning job to worker4"), -DUTY(4), +TASK(X, Y, 4)[{'to': "worker4"}]]

        # ReceiveCommunication intentions
        +COMM(X)[{'from': "worker1"}] / LEDGER("worker1", H) >> [show_line("received job done comm from worker1"), -LEDGER("worker1", H), UpdateLedger("worker1", H), +DUTY(1)]
        +COMM(X)[{'from': "worker2"}] / LEDGER("worker2", H) >> [show_line("received job done comm from worker2"), -LEDGER("worker2", H), UpdateLedger("worker2", H), +DUTY(2)]
        +COMM(X)[{'from': "worker3"}] / LEDGER("worker3", H) >> [show_line("received job done comm from worker3"), -LEDGER("worker3", H), UpdateLedger("worker3", H), +DUTY(3)]
        +COMM(X)[{'from': "worker4"}] / LEDGER("worker4", H) >> [show_line("received job done comm from worker4"), -LEDGER("worker4", H), UpdateLedger("worker4", H), +DUTY(4)]


        # Pause work intentions - WORKTIME value is (DUTY_TIME * 6)
        +TIMEOUT("ON") / WORKTIME(MAX_WORKDAY_TIME) >> [show_line("\nWorkers are very tired Finishing working day.\n"), +STOPWORK("YES")]
        +TIMEOUT("ON") / (WORKTIME(X) & DUTY_TIME(Y)) >> [show_line("\nWorkers are tired, they need some rest.\n"), TaskDetect().stop(), -DUTY(1), -DUTY(2), -DUTY(3), -DUTY(4), -WORKTIME(X), UpdateWorkTime(X, Y), rest(REST_TIME), work()]

        # Stop work intention
        +STOPWORK("YES") >> [show_line("\nWorking day completed."), -DUTY(1), -DUTY(2), -DUTY(3), -DUTY(4), TaskDetect().stop(), -WORKTIME(MAX_WORKDAY_TIME), pay()]

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