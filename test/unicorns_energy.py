import turtle
import random
from tkinter import Tk, Scale, HORIZONTAL, Label, IntVar, Checkbutton

# Definire le dimensioni iniziali del canvas
N = 500

# Numero iniziale di unicorni
num_unicorns = 10

# Dimensione iniziale di ogni step
step_size = 5

# Velocità iniziale (in millisecondi)
speed = 50

# Energia iniziale di ogni unicorno
initial_energy = 100

# Variabile per il trigger di visibilità dell'energia
show_energy = True


# Funzione per inizializzare lo schermo di turtle
def setup_screen():
    global screen
    screen = turtle.Screen()
    screen.setup(N, N)
    screen.title("Randomic unicorns")
    screen.tracer(0)  # Disabilita l'aggiornamento automatico dello schermo
    screen.register_shape("turtles/icons8-unicorn_color.gif")


# Creare una lista per memorizzare gli unicorni
unicorns = []


# Funzione per inizializzare gli unicorni
def create_unicorns(num):
    for _ in range(num):
        unicorn = turtle.Turtle()
        unicorn.shape("turtles/icons8-unicorn_color.gif")
        unicorn.penup()
        unicorn.speed(0)
        unicorn.setpos(random.randint(-N // 2, N // 2), random.randint(-N // 2, N // 2))
        unicorn.setheading(random.randint(0, 360))
        unicorn.energy = initial_energy  # Inizializza l'energia dell'unicorno
        unicorn.energy_display = turtle.Turtle(visible=False)
        unicorns.append(unicorn)


# Funzione per aggiornare il numero di unicorni
def update_unicorns(num):
    remove_inactive_unicorns()
    while len(unicorns) < num:
        create_unicorns(1)  # Aggiungi automobili finché non raggiungi il numero desiderato


# Funzione per rimuovere un unicorno specifico
def remove_unicorn(unicorn):
    if unicorn in unicorns:
        unicorn.hideturtle()
        unicorn.energy_display.clear()
        unicorn.energy_display.hideturtle()
        unicorns.remove(unicorn)


# Funzione per rimuovere tutti gli unicorni con energia zero
def remove_inactive_unicorns():
    for unicorn in unicorns[:]:  # Itera sulla copia della lista per evitare problemi di modifica durante l'iterazione
        if unicorn.energy <= 0:
            remove_unicorn(unicorn)


# Funzione per controllare le collisioni con le pareti e diminuire l'energia
def check_wall_collision(unicorn):
    x, y = unicorn.position()
    if abs(x) > N // 2 or abs(y) > N // 2:
        unicorn.right(180)
        unicorn.energy -= 10  # Diminuisci energia dopo una collisione con la parete
        if unicorn.energy <= 0:
            remove_unicorn(unicorn)
        update_energy_display(unicorn)
        return True
    return False


# Funzione per controllare le collisioni tra automobili e diminuire l'energia
def check_unicorn_collision(unicorn1, unicorn2):
    if unicorn1.distance(unicorn2) < 20:  # Considera una collisione se la distanza è inferiore a 20 pixel
        unicorn1.right(180)
        unicorn2.right(180)
        unicorn1.energy -= 10  # Diminuisci energia dopo una collisione con un'altra automobile
        unicorn2.energy -= 10
        if unicorn1.energy <= 0:
            remove_unicorn(unicorn1)
        if unicorn2.energy <= 0:
            remove_unicorn(unicorn2)
        update_energy_display(unicorn1)
        update_energy_display(unicorn2)
        return True
    return False


# Funzione per aggiornare il display dell'energia sotto ogni unicorno
def update_energy_display(unicorn):
    if show_energy:
        unicorn.energy_display.clear()
        unicorn.energy_display.hideturtle()
        if unicorn.energy > 0:
            unicorn.energy_display.penup()
            unicorn.energy_display.setpos(unicorn.xcor(), unicorn.ycor() - 20)
            unicorn.energy_display.write(unicorn.energy, align="center", font=("Arial", 12, "normal"))
            unicorn.energy_display.showturtle()
    else:
        unicorn.energy_display.clear()
        unicorn.energy_display.hideturtle()


# Funzione per far muovere gli unicorni
def move_unicorns():
    unicorns_to_remove = []
    for unicorn in unicorns[:]:  # Iteriamo sulla copia della lista per evitare problemi di modifica durante l'iterazione
        unicorn.forward(step_size)  # Usa la dimensione di ogni step

        # Controllare collisioni con le pareti
        if check_wall_collision(unicorn):
            if unicorn.energy <= 0:
                unicorns_to_remove.append(unicorn)
            continue

        # Controllare collisioni con altre automobili
        for other in unicorns:
            if unicorn != other and check_unicorn_collision(unicorn, other):
                if unicorn.energy <= 0:
                    unicorns_to_remove.append(unicorn)
                if other.energy <= 0:
                    unicorns_to_remove.append(other)
                break  # Cambiare direzione una sola volta per ciclo

        update_energy_display(unicorn)  # Aggiorna la posizione del display dell'energia

    # Rimuovere le automobili con energia zero
    for unicorn in unicorns_to_remove:
        remove_unicorn(unicorn)

    screen.update()  # Aggiornare lo schermo
    root.after(speed, move_unicorns)  # Richiama questa funzione dopo "speed" millisecondi


# Funzione per aggiornare le dimensioni del canvas
def update_canvas_size(size):
    global N
    N = size
    screen.setup(N, N)
    remove_inactive_unicorns()  # Rimuovi automobili fuori dai limiti del nuovo canvas


# Funzione per gestire il trigger per la visibilità dell'energia
def toggle_energy_visibility():
    global show_energy
    show_energy = not show_energy
    for unicorn in unicorns:
        update_energy_display(unicorn)


# Configurare l'interfaccia di controllo con tkinter
root = Tk()
root.title("Agents parameters")

# Impostare le dimensioni della finestra di tkinter
root.geometry("450x400")  # Larghezza x Altezza

# Slider per il numero di unicorni
Label(root, text="Agent number").pack()
unicorn_slider = Scale(root, from_=1, to=50, orient=HORIZONTAL, length=400)
unicorn_slider.set(num_unicorns)
unicorn_slider.pack()


def on_unicorn_slider_change(value):
    global num_unicorns
    num_unicorns = int(value)
    update_unicorns(num_unicorns)


unicorn_slider.config(command=on_unicorn_slider_change)

# Slider per la dimensione del canvas
Label(root, text="Canvas size").pack()
canvas_slider = Scale(root, from_=200, to=800, orient=HORIZONTAL, length=400)
canvas_slider.set(N)
canvas_slider.pack()


def on_canvas_slider_change(value):
    update_canvas_size(int(value))


canvas_slider.config(command=on_canvas_slider_change)

# Slider per la dimensione di ogni step
Label(root, text="Step size").pack()
step_slider = Scale(root, from_=1, to=20, orient=HORIZONTAL, length=400)
step_slider.set(step_size)
step_slider.pack()


def on_step_slider_change(value):
    global step_size
    step_size = int(value)


step_slider.config(command=on_step_slider_change)

# Slider per la velocità
Label(root, text="Speed (ms)").pack()
speed_slider = Scale(root, from_=10, to=200, orient=HORIZONTAL, length=400)
speed_slider.set(speed)
speed_slider.pack()


def on_speed_slider_change(value):
    global speed
    speed = 210 - int(value)  # Invertire la logica dello slider


speed_slider.config(command=on_speed_slider_change)

# Checkbox per la visibilità dell'energia
show_energy_var = IntVar(value=1)
show_energy_checkbox = Checkbutton(root, text="Show energy", variable=show_energy_var,
                                   command=toggle_energy_visibility)
show_energy_checkbox.pack()

# Inizializzare lo schermo di turtle
setup_screen()

# Creazione automobili iniziali
create_unicorns(num_unicorns)

# Iniziare il movimento degli unicorni
root.after(speed, move_unicorns)

# Avviare il main loop di tkinter
root.mainloop()

# Avviare il main loop di turtle (necessario per evitare che la finestra si chiuda)
turtle.done()
