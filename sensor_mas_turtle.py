import sys
import time
import threading
import random
import turtle

sys.path.insert(0, "../lib")

from phidias.Lib import *
from phidias.Agent import *
from phidias.Types import *



class setup(Procedure): pass
class work(Procedure): pass
class TIMEOUT(Reactor): pass
class STOPWORK(Reactor): pass
class TASK(Reactor): pass
class DUTY1(Belief): pass
class DUTY2(Belief): pass
class LEDGER(Belief): pass

class WORKTIME(Belief): pass
class DUTY_TIME(Belief): pass

dict_turtle = {}

# Max work time for a worker
MAX_WORK_TIME = 10
# Rest time for a worker
REST_TIME = 5

# Coordinates spamming range
N = 500

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
                print("CAZZZZZZZZZZZZZZZZZZZZOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
                self.assert_belief(TIMEOUT("ON"))
                return
            else:
                return


# ---------------------------------------------------------------------
# Turtle section
# ---------------------------------------------------------------------


class move_turtle(Action):
    """render unicorn to coordinates (x,y) and heading h"""
    def execute(self, arg0, arg1, arg2):
      id_turtle = str(arg0)[1:-1]
      pos_x = str(arg1).split("'")[2]
      pos_y = str(arg2).split("'")[2]
      pos_x = int(pos_x[1:-1])
      pos_y = int(pos_y[1:-1])
      print(f"POS({pos_x}, {pos_y})")

      dict_turtle["t"+id_turtle].goto(pos_x, pos_y)

      # time to get the job done
      time.sleep(1)



class rest(Action):
    """resting for few seconds"""
    def execute(self, arg):
      print("rest: ", arg)
      rest_time = int(str(arg))
      print(f"\nresting for {rest_time} seconds...")

      t1.color("red")
      t2.color("red")

      time.sleep(rest_time)

      t1.color("black")
      t2.color("black")


class UpdateLedger(Action):
    """Update completed jobs"""
    def execute(self, arg1, arg2):

      agent = str(arg1)[1:-1]
      jobs = int(str(arg2).split("'")[3])
      jobs = jobs + 1
      self.assert_belief(LEDGER(agent, str(jobs)))


class UpdateWorkTime(Action):
    """Update completed jobs"""
    def execute(self, arg1, arg2):
        print(" UpdateWorkTime arg1: ", arg1)
        print(" UpdateWorkTime arg2: ", arg2)

        arg1_num = str(arg1).split("'")[2][1:-1]
        arg2_num = str(arg2).split("'")[2][1:-1]
        arg_num_tot = int(arg1_num)+int(arg2_num)
        self.assert_belief(WORKTIME(arg_num_tot))


class check_worktime(ActiveBelief):
    """check if R is a Well Formed Rule"""
    def evaluate(self, arg1, arg2):

        print("arg1: ", arg1)
        print("arg2: ", arg2)

        if 0 == 0:
            return True
        else:
            return False




# ---------------------------------------------------------------------
# Variable declaration
# ---------------------------------------------------------------------
def_vars("X","Y", "D", "H", "Z")


# ---------------------------------------------------------------------
# Agents 'worker', 'worker2'
# ---------------------------------------------------------------------
class worker1(Agent):
    def main(self):
        +TASK(X, Y)[{'from': Z}] >> [show_line("Worker1 moving to (", X,",", Y, "), received task from ", Z), move_turtle("1",X,Y), +DUTY1("YES")[{'to':'main'}]]

class worker2(Agent):
    def main(self):
        +TASK(X, Y)[{'from': Z}] >> [show_line("Worker2 moving to (", X,",", Y, "), received task from ", Z), move_turtle("2",X, Y), +DUTY2("YES")[{'to':'main'}]]


# ---------------------------------------------------------------------
# Agent 'main'
# ---------------------------------------------------------------------
class main(Agent):
    def main(self):

        setup() >> [show_line("Setup jobs ledger...\n"), +LEDGER("worker1", "0"), +LEDGER("worker2", "0"), +WORKTIME(0), +DUTY_TIME(MAX_WORK_TIME)]
        work() >> [show_line("Starting task detection...\n"), TaskDetect().start(), show_line("Workers on duty..."), +DUTY1("YES"), +DUTY2("YES"), Timer(MAX_WORK_TIME).start()]

        +DUTY1("YES")[{'from': "worker1"}] / LEDGER("worker1", X) >> [show_line("received comm DUTY from worker1"), -LEDGER("worker1", X), UpdateLedger("worker1", X)]
        +DUTY2("YES")[{'from': "worker2"}] / LEDGER("worker2", X) >> [show_line("received comm DUTY2 from worker2"), -LEDGER("worker2", X), UpdateLedger("worker2", X)]

        +TASK(X, Y) / DUTY1("YES") >> [-DUTY1("YES"), +TASK(X, Y)[{'to':'worker1'}]]
        +TASK(X, Y) / DUTY2("YES") >> [-DUTY2("YES"), +TASK(X, Y)[{'to':'worker2'}]]

        +TIMEOUT("ON") / WORKTIME(100) >> [show_line("\nWorkers are very tired Finishing working day.\n"), +STOPWORK("YES")]
        +TIMEOUT("ON") / (WORKTIME(X) & DUTY_TIME(Y)) >> [show_line("\nWorkers are tired, they need some rest.\n"), TaskDetect().stop(), -DUTY1("YES"), -DUTY2("YES"), -WORKTIME(X), UpdateWorkTime(X, Y), rest(REST_TIME), work()]
        +STOPWORK("YES") >> [show_line("\nWorking day completed.\n"), TaskDetect().stop(), -DUTY1("YES"), -DUTY2("YES")]


def turtle_thread_func():
    wn = turtle.Screen()
    wn.title("Workers jobs assignment")

    global t1, t2
    t1 = turtle.Turtle()
    t2 = turtle.Turtle()

    dict_turtle["t1"] = t1
    dict_turtle["t2"] = t2

    # Questo mantiene la finestra aperta finché non viene chiusa dall'utente
    wn.mainloop()


# Avviare il thread della tartaruga
turtle_thread = threading.Thread(target=turtle_thread_func)
turtle_thread.daemon = True
turtle_thread.start()


# start the actors
worker1().start()
worker2().start()

main().start()


# run the engine shell
PHIDIAS.shell(globals())
