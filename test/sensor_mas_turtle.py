import sys
import time
import threading
import random
import turtle

sys.path.insert(0, "../lib")

from phidias.Lib import *
from phidias.Agent import *
from phidias.Types import *


class pay(Procedure): pass
class setup(Procedure): pass
class work(Procedure): pass
class TIMEOUT(Reactor): pass
class STOPWORK(Reactor): pass
class COMM(Reactor): pass
class TASK(Reactor): pass
class LEDGER(Belief): pass

class DUTY(Belief): pass

class WORKTIME(Belief): pass
class DUTY_TIME(Belief): pass

dict_turtle = {}

# Max work time for a worker
MAX_WORK_TIME = 10
# Rest time for a worker
REST_TIME = 5
# Timer tick
TICK = 0.5

# Coordinates spamming range
N = 500

# Agent number
AGENT_NUMBER = 2

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
           time.sleep(TICK)

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
      id_turtle = str(arg0)[1:-1]
      pos_x = str(arg1).split("'")[2]
      pos_y = str(arg2).split("'")[2]
      pos_x = int(pos_x[1:-1])
      pos_y = int(pos_y[1:-1])

      dict_turtle["t"+id_turtle].goto(pos_x, pos_y)

      # time to get the job done
      rnd = random.uniform(0, 1)
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

      agent = str(arg1).split("'")[3]
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
# Agents 'worker', 'worker2'
# ---------------------------------------------------------------------
class worker1(Agent):
    def main(self):
        +TASK(X, Y)[{'from': M}] >> [show_line("\nWorker1 moving to (", X,",", Y, "), received task from ", M), move_turtle("1", X, Y), +COMM("DONE")[{'to':'main'}]]

class worker2(Agent):
    def main(self):
        +TASK(X, Y)[{'from': M}] >> [show_line("\nWorker2 moving to (", X,",", Y, "), received task from ", M), move_turtle("2", X, Y), +COMM("DONE")[{'to':'main'}]]


# ---------------------------------------------------------------------
# Agent 'main'
# ---------------------------------------------------------------------
class main(Agent):
    def main(self):

        setup() >> [show_line("Setup jobs ledger...\n"), +LEDGER("worker1", "0"), +LEDGER("worker2", "0"), +WORKTIME(0), +DUTY_TIME(MAX_WORK_TIME)]
        work() >> [show_line("Starting task detection...\n"), +DUTY("worker1"), +DUTY("worker2"), Timer(MAX_WORK_TIME).start(), TaskDetect().start(), show_line("Workers on duty...")]

        +TASK(X, Y) / DUTY(Z) >> [show_line("assigning job to ", Z), -DUTY(Z), +TASK(X, Y)[{'to': Z}]]

        +COMM(X)[{'from': Z}] / LEDGER(Z, H) >> [show_line("received job done comm from ", Z), -LEDGER(Z, H), UpdateLedger(Z, H), +DUTY(Z)]

        +TIMEOUT("ON") / WORKTIME(30) >> [show_line("\nWorkers are very tired Finishing working day.\n"), +STOPWORK("YES")]
        +TIMEOUT("ON") / (WORKTIME(X) & DUTY_TIME(Y)) >> [show_line("\nWorkers are tired, they need some rest.\n"), TaskDetect().stop(), -DUTY("worker1"), -DUTY("worker2"), -WORKTIME(X), UpdateWorkTime(X, Y), rest(REST_TIME), work()]
        +STOPWORK("YES") >> [show_line("\nWorking day completed."), -DUTY("worker1"), -DUTY("worker2"), TaskDetect().stop(), pay()]

        pay() / LEDGER(Z, H) >> [show_line("\nSending payment to ",Z, " for ",H," task..."), -LEDGER(Z, H), pay()]
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


# start the actors
worker1().start()
worker2().start()

main().start()


# run the engine shell
PHIDIAS.shell(globals())
