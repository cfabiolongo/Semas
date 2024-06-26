import turtle
import random
import time
import uuid

# Definire le dimensioni del canvas
N = 500

# Numero di tartarughe
num_turtles = 20

# Inizializzare lo schermo
screen = turtle.Screen()
screen.setup(N, N)
screen.title("MAS rendering")
screen.tracer(0)  # Disabilita l'aggiornamento automatico dello schermo

# Creare una lista per memorizzare le tartarughe
turtles = []

# Additional icons (.gif) are available here: https://icons8.com/icons

# Registrare l'immagine dell'automobile
screen.register_shape("turtles/icons8-unicorn_color.gif")


class TurtleWithID(turtle.Turtle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = uuid.uuid4()


# Funzione per inizializzare le tartarughe
def create_turtles(num):
    for _ in range(num):
        t = TurtleWithID()
        t.shape("turtles/icons8-unicorn_color.gif")
        t.penup()
        t.speed(0)
        t.setpos(random.randint(-N // 2, N // 2), random.randint(-N // 2, N // 2))
        t.setheading(random.randint(0, 360))
        turtles.append(t)
        print("id: ",t.id)


# Creare le tartarughe
create_turtles(num_turtles)


# Funzione per controllare le collisioni con le pareti
def check_wall_collision(t):
    x, y = t.position()
    if abs(x) > N // 2 or abs(y) > N // 2:
        return True
    return False


# Funzione per controllare le collisioni tra tartarughe
def check_turtle_collision(t1, t2):
    return t1.distance(t2) < 20  # Considera una collisione se la distanza è inferiore a 15 pixel


# Funzione per far muovere le tartarughe
def move_turtles():
    while True:
        for t in turtles:
            t.forward(1)  # Passi piccoli

            # Controllare collisioni con le pareti
            if check_wall_collision(t):
                t.right(180)

            # Controllare collisioni con altre tartarughe
            for other in turtles:
                if t != other and check_turtle_collision(t, other):
                    t.right(180)
                    break  # Cambiare direzione una sola volta per ciclo

        screen.update()  # Aggiornare lo schermo
        time.sleep(0.01)  # Ritardo minore


# Iniziare il movimento delle tartarughe
move_turtles()

# Avviare il main loop di turtle
turtle.done()
