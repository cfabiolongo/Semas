import turtle
import random

# Definire le dimensioni del canvas
N = 500

# Numero di tartarughe
num_turtles = 10

# Inizializzare lo schermo
screen = turtle.Screen()
screen.setup(N, N)
screen.title("Tartarughe che si muovono in maniera randomica")

# Creare una lista per memorizzare le tartarughe
turtles = []

# Funzione per inizializzare le tartarughe
def create_turtles(num):
    for _ in range(num):
        t = turtle.Turtle()
        t.shape("turtle")
        t.penup()
        t.speed(1)
        t.setpos(random.randint(-N//2, N//2), random.randint(-N//2, N//2))
        turtles.append(t)

# Funzione per far muovere le tartarughe in maniera randomica
def move_turtles():
    for t in turtles:
        angle = random.randint(0, 360)
        t.setheading(angle)
        t.forward(20)
        
        # Controllare se la tartaruga è fuori dai bordi e reindirizzarla
        x, y = t.position()
        if abs(x) > N//2 or abs(y) > N//2:
            t.right(180)
            t.forward(20)

    # Chiamare la funzione di nuovo dopo 100 millisecondi
    screen.ontimer(move_turtles, 100)

# Creare le tartarughe
create_turtles(num_turtles)

# Iniziare il movimento delle tartarughe
move_turtles()

# Avviare il main loop di turtle
turtle.done()
