import turtle
import threading


def turtle_thread_func():
    wn = turtle.Screen()
    wn.title("Movimento della tartaruga")

    global t
    t = turtle.Turtle()

    # Questo mantiene la finestra aperta finché non viene chiusa dall'utente
    wn.mainloop()


def move_turtle(x, y):
    t.goto(x, y)


def main():
    # Avviare il thread della tartaruga
    turtle_thread = threading.Thread(target=turtle_thread_func)
    turtle_thread.daemon = True
    turtle_thread.start()

    while True:
        try:
            # Prendere input dell'utente
            coordinates = input("Inserisci le coordinate (x y) o premi Enter per uscire: ")
            if coordinates.strip() == "":
                break

            # Split the input into x and y coordinates
            x, y = map(float, coordinates.split())

            # Muovere la tartaruga
            move_turtle(x, y)

        except ValueError:
            print("Errore: inserisci coordinate valide nel formato 'x y'.")
        except Exception as e:
            print(f"Errore inaspettato: {e}")


if __name__ == "__main__":
    main()
