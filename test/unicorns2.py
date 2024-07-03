import turtle
import random
from tkinter import Tk, Scale, HORIZONTAL, Label

# Definire le dimensioni iniziali del canvas
N = 500

# Numero iniziale di automobili
num_cars = 10

# Dimensione iniziale di ogni step
step_size = 5

# Velocità iniziale (in millisecondi)
speed = 50

# Inizializzare lo schermo
screen = turtle.Screen()
screen.setup(N, N)
screen.title("Agents collisions canvas")
screen.tracer(0)  # Disabilita l'aggiornamento automatico dello schermo

# Registrare l'immagine dell'automobile
screen.register_shape("turtles/icons8-unicorn_color.gif")

# Creare una lista per memorizzare le automobili
cars = []


# Funzione per inizializzare le automobili
def create_cars(num):
    for _ in range(num):
        car = turtle.Turtle()
        car.shape("turtles/icons8-unicorn_color.gif")
        car.penup()
        car.speed(0)
        car.setpos(random.randint(-N // 2, N // 2), random.randint(-N // 2, N // 2))
        car.setheading(random.randint(0, 360))
        cars.append(car)


# Funzione per rimuovere tutte le automobili
def clear_cars():
    for car in cars:
        car.hideturtle()
    cars.clear()


# Funzione per aggiornare il numero di automobili
def update_cars(num):
    clear_cars()
    create_cars(num)


# Funzione per controllare le collisioni con le pareti
def check_wall_collision(car):
    x, y = car.position()
    if abs(x) > N // 2 or abs(y) > N // 2:
        return True
    return False


# Funzione per controllare le collisioni tra automobili
def check_car_collision(car1, car2):
    return car1.distance(car2) < 20  # Considera una collisione se la distanza è inferiore a 20 pixel


# Funzione per far muovere le automobili
def move_cars():
    for car in cars:
        car.forward(step_size)  # Usa la dimensione di ogni step

        # Controllare collisioni con le pareti
        if check_wall_collision(car):
            car.right(180)

        # Controllare collisioni con altre automobili
        for other in cars:
            if car != other and check_car_collision(car, other):
                car.right(180)
                break  # Cambiare direzione una sola volta per ciclo

    screen.update()  # Aggiornare lo schermo
    root.after(speed, move_cars)  # Richiama questa funzione dopo "speed" millisecondi


# Funzione per aggiornare le dimensioni del canvas
def update_canvas_size(size):
    global N
    N = size
    screen.setup(N, N)
    clear_cars()
    create_cars(num_cars)


# Configurare l'interfaccia di controllo con tkinter
root = Tk()
root.title("Agents parameters control")
root.geometry("400x300")

# Slider per il numero di automobili
Label(root, text="Agents number").pack()
car_slider = Scale(root, from_=1, to=50, orient=HORIZONTAL, length=300)
car_slider.set(num_cars)
car_slider.pack()


def on_car_slider_change(value):
    global num_cars
    num_cars = int(value)
    update_cars(num_cars)


car_slider.config(command=on_car_slider_change)

# Slider per la dimensione del canvas
Label(root, text="Canvas size").pack()
canvas_slider = Scale(root, from_=200, to=800, orient=HORIZONTAL, length=300)
canvas_slider.set(N)
canvas_slider.pack()


def on_canvas_slider_change(value):
    update_canvas_size(int(value))


canvas_slider.config(command=on_canvas_slider_change)

# Slider per la dimensione di ogni step
Label(root, text="Step sizing").pack()
step_slider = Scale(root, from_=1, to=100, orient=HORIZONTAL, length=300)
step_slider.set(step_size)
step_slider.pack()


def on_step_slider_change(value):
    global step_size
    step_size = int(value)


step_slider.config(command=on_step_slider_change)

# Slider per la velocità
Label(root, text="Speed (ms)").pack()
speed_slider = Scale(root, from_=0, to=500, orient=HORIZONTAL, length=300)
speed_slider.set(speed)
speed_slider.pack()


def on_speed_slider_change(value):
    global speed
    speed = 500 - int(value)  # Invertire la logica dello slider


speed_slider.config(command=on_speed_slider_change)

# Creare le automobili iniziali
create_cars(num_cars)

# Iniziare il movimento delle automobili
root.after(speed, move_cars)

# Avviare il main loop di tkinter
root.mainloop()

# Avviare il main loop di turtle (necessario per evitare che la finestra si chiuda)
turtle.done()
