import turtle
import random
from tkinter import Tk, Scale, HORIZONTAL, Label, IntVar, Checkbutton

# Definire le dimensioni iniziali del canvas
N = 500

# Numero iniziale di automobili
num_cars = 10

# Dimensione iniziale di ogni step
step_size = 5

# Velocità iniziale (in millisecondi)
speed = 50

# Energia iniziale di ogni automobile
initial_energy = 100

# Variabile per il trigger di visibilità dell'energia
show_energy = True


# Funzione per inizializzare lo schermo di turtle
def setup_screen():
    global screen
    screen = turtle.Screen()
    screen.setup(N, N)
    screen.title("Automobili che si muovono in maniera randomica")
    screen.tracer(0)  # Disabilita l'aggiornamento automatico dello schermo
    screen.register_shape("turtles/icons8-crab.gif")


# Creare una lista per memorizzare le automobili
cars = []


# Funzione per inizializzare le automobili
def create_cars(num):
    for _ in range(num):
        car = turtle.Turtle()
        car.shape("turtles/icons8-crab.gif")
        car.penup()
        car.speed(0)
        car.setpos(random.randint(-N // 2, N // 2), random.randint(-N // 2, N // 2))
        car.setheading(random.randint(0, 360))
        car.energy = initial_energy  # Inizializza l'energia dell'automobile
        car.energy_display = turtle.Turtle(visible=False)
        cars.append(car)


# Funzione per aggiornare il numero di automobili
def update_cars(num):
    remove_inactive_cars()
    while len(cars) < num:
        create_cars(1)  # Aggiungi automobili finché non raggiungi il numero desiderato


# Funzione per rimuovere un'automobile specifica
def remove_car(car):
    car.hideturtle()
    car.energy_display.clear()
    car.energy_display.hideturtle()
    cars.remove(car)


# Funzione per rimuovere tutte le automobili con energia zero
def remove_inactive_cars():
    for car in cars[:]:  # Itera sulla copia della lista per evitare problemi di modifica durante l'iterazione
        if car.energy <= 0:
            remove_car(car)


# Funzione per controllare le collisioni con le pareti e diminuire l'energia
def check_wall_collision(car):
    x, y = car.position()
    if abs(x) > N // 2 or abs(y) > N // 2:
        car.right(180)
        car.energy -= 10  # Diminuisci energia dopo una collisione con la parete
        if car.energy <= 0:
            remove_car(car)
        update_energy_display(car)
        return True
    return False


# Funzione per controllare le collisioni tra automobili e diminuire l'energia
def check_car_collision(car1, car2):
    if car1.distance(car2) < 20:  # Considera una collisione se la distanza è inferiore a 20 pixel
        car1.right(180)
        car2.right(180)
        car1.energy -= 10  # Diminuisci energia dopo una collisione con un'altra automobile
        car2.energy -= 10
        if car1.energy <= 0:
            remove_car(car1)
        if car2.energy <= 0:
            remove_car(car2)
        update_energy_display(car1)
        update_energy_display(car2)
        return True
    return False


# Funzione per aggiornare il display dell'energia sotto ogni automobile
def update_energy_display(car):
    if show_energy:
        car.energy_display.clear()
        car.energy_display.hideturtle()
        if car.energy > 0:
            car.energy_display.penup()
            car.energy_display.setpos(car.xcor(), car.ycor() - 20)
            car.energy_display.write(car.energy, align="center", font=("Arial", 12, "normal"))
            car.energy_display.showturtle()
    else:
        car.energy_display.clear()
        car.energy_display.hideturtle()


# Funzione per far muovere le automobili
def move_cars():
    for car in cars[:]:  # Iteriamo sulla copia della lista per evitare problemi di modifica durante l'iterazione
        car.forward(step_size)  # Usa la dimensione di ogni step

        # Controllare collisioni con le pareti
        if check_wall_collision(car):
            continue

        # Controllare collisioni con altre automobili
        for other in cars:
            if car != other and check_car_collision(car, other):
                break  # Cambiare direzione una sola volta per ciclo

        update_energy_display(car)  # Aggiorna la posizione del display dell'energia

    screen.update()  # Aggiornare lo schermo
    root.after(speed, move_cars)  # Richiama questa funzione dopo "speed" millisecondi


# Funzione per aggiornare le dimensioni del canvas
def update_canvas_size(size):
    global N
    N = size
    screen.setup(N, N)
    remove_inactive_cars()  # Rimuovi automobili fuori dai limiti del nuovo canvas


# Funzione per gestire il trigger per la visibilità dell'energia
def toggle_energy_visibility():
    global show_energy
    show_energy = not show_energy
    for car in cars:
        update_energy_display(car)


# Configurare l'interfaccia di controllo con tkinter
root = Tk()
root.title("Parametri Agenti")

# Impostare le dimensioni della finestra di tkinter
root.geometry("450x350")  # Larghezza x Altezza

# Slider per il numero di automobili
Label(root, text="Numero di automobili").pack()
car_slider = Scale(root, from_=1, to=50, orient=HORIZONTAL, length=400)
car_slider.set(num_cars)
car_slider.pack()


def on_car_slider_change(value):
    global num_cars
    num_cars = int(value)
    update_cars(num_cars)


car_slider.config(command=on_car_slider_change)

# Slider per la dimensione del canvas
Label(root, text="Dimensione del canvas").pack()
canvas_slider = Scale(root, from_=200, to=800, orient=HORIZONTAL, length=400)
canvas_slider.set(N)
canvas_slider.pack()


def on_canvas_slider_change(value):
    update_canvas_size(int(value))


canvas_slider.config(command=on_canvas_slider_change)

# Slider per la dimensione di ogni step
Label(root, text="Dimensione di ogni step").pack()
step_slider = Scale(root, from_=1, to=20, orient=HORIZONTAL, length=400)
step_slider.set(step_size)
step_slider.pack()


def on_step_slider_change(value):
    global step_size
    step_size = int(value)


step_slider.config(command=on_step_slider_change)

# Slider per la velocità
Label(root, text="Velocità (ms)").pack()
speed_slider = Scale(root, from_=10, to=200, orient=HORIZONTAL, length=400)
speed_slider.set(speed)
speed_slider.pack()


def on_speed_slider_change(value):
    global speed
    speed = 210 - int(value)  # Invertire la logica dello slider


speed_slider.config(command=on_speed_slider_change)

# Checkbox per la visibilità dell'energia
show_energy_var = IntVar()
show_energy_checkbox = Checkbutton(root, text="Mostra energia", variable=show_energy_var,
                                   command=toggle_energy_visibility)
show_energy_checkbox.pack()

# Inizializzare lo schermo di turtle
setup_screen()

# Creare le automobili iniziali
create_cars(num_cars)

# Iniziare il movimento delle automobili
root.after(speed, move_cars)

# Avviare il main loop di tkinter
root.mainloop()

# Avviare il main loop di turtle (necessario per evitare che la finestra si chiuda)
turtle.done()
