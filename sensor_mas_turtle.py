import sys
import time
import threading
import random
import turtle

sys.path.insert(0, "../lib")

from phidias.Lib import *
from phidias.Agent import *
from phidias.Types import *

class go(Procedure): pass
class work(Procedure): pass
class TIMEOUT(Reactor): pass
class TASK(Reactor): pass
class DUTY1(Belief): pass
class DUTY2(Belief): pass

# Canvas size
N = 500

# ---------------------------------------------------------------------
# Sensors section
# ---------------------------------------------------------------------


class TaskDetect(Sensor):

    def on_start(self):
        # Starting task detection
       self.running = True

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
            self.event.wait(self.timeout)
            self.event.clear()
            if self.do_restart:
                self.do_restart = False
                continue
            if self.stopped:
                return
            else:
                self.assert_belief(TIMEOUT("ON"))
                return


# ---------------------------------------------------------------------
# Turtle section
# ---------------------------------------------------------------------


class move_turtle1(Action):
    """render unicorn to coordinates (x,y) and heading h"""
    def execute(self, arg1, arg2):
      pos_x = str(arg1).split("'")[2]
      pos_y = str(arg2).split("'")[2]
      pos_x = int(pos_x[1:-1])
      pos_y = int(pos_y[1:-1])
      t1.goto(pos_x, pos_y)

      # time to get the job done
      time.sleep(1)


class move_turtle2(Action):
    """render unicorn to coordinates (x,y) and heading h"""
    def execute(self, arg1, arg2):
      pos_x = str(arg1).split("'")[2]
      pos_y = str(arg2).split("'")[2]
      pos_x = int(pos_x[1:-1])
      pos_y = int(pos_y[1:-1])
      t2.goto(pos_x, pos_y)

      # time to get the job done
      time.sleep(1)



# ---------------------------------------------------------------------
# Variable declaration
# ---------------------------------------------------------------------
def_vars("X","Y", "D", "H", "Z")


# ---------------------------------------------------------------------
# Agents 'worker', 'worker2'
# ---------------------------------------------------------------------
class worker(Agent):
    def main(self):
        +TASK(X, Y)[{'from': Z}] >> [show_line("Worker moving to (", X,",", Y, "), received task from ", Z), move_turtle1(X,Y), +DUTY1("YES")[{'to':'main'}]]

class worker2(Agent):
    def main(self):
        +TASK(X, Y)[{'from': Z}] >> [show_line("Worker2 moving to (", X,",", Y, "), received task from ", Z), move_turtle2(X, Y), +DUTY2("YES")[{'to':'main'}]]


# ---------------------------------------------------------------------
# Agent 'main'
# ---------------------------------------------------------------------
class main(Agent):
    def main(self):

        go() >> [show_line("Starting task detection...\n"), TaskDetect().start()]
        work() >> [show_line("Workers on duty..."), +DUTY1("YES"), +DUTY2("YES"), Timer(0.1).start()]

        +DUTY1(X)[{'from': "worker"}] >> [show_line("received comm DUTY ",X," from worker"), +DUTY1(X)]
        +DUTY2(X)[{'from': "worker2"}] >> [show_line("received comm DUTY2 ",X," from worker2"), +DUTY2(X)]

        +TASK(X, Y) / DUTY1("YES") >> [-DUTY1("YES"), +TASK(X, Y)[{'to':'worker'}]]
        +TASK(X, Y) / DUTY2("YES") >> [-DUTY2("YES"), +TASK(X, Y)[{'to': 'worker2'}]]

        +TIMEOUT("ON") >> [show_line("\nWorkers are tired...\n"), -DUTY1("YES"), -DUTY2("YES")]


def turtle_thread_func():
    wn = turtle.Screen()
    wn.title("Movimento della tartaruga")

    global t1, t2
    t1 = turtle.Turtle()
    t2 = turtle.Turtle()

    # Questo mantiene la finestra aperta finché non viene chiusa dall'utente
    wn.mainloop()


# Avviare il thread della tartaruga
turtle_thread = threading.Thread(target=turtle_thread_func)
turtle_thread.daemon = True
turtle_thread.start()


# start the actors
worker().start()
worker2().start()

main().start()


# run the engine shell
PHIDIAS.shell(globals())
