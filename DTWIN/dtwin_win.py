import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk
import os
import base64
import requests
import threading
import json


# Endpoint locale di Ollama
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# CONTEXTO GLOBALE
system = """Extract only beliefs (without other text), and single-word (possible other words as additional belief arguments), related to an agent
             from the text of a scene beliefs related to verb can have two arguments. For example: The car runs on the highway —→ AGENT(CAR),  RUN(CAR, HIGHWAY).
"""

image_prompt = "Describe briefly the picture, with no further text."
image_temp = "0.8"

beliefs_prompt = "extract only beliefs (without other text), and single-word (possible other words as additional belief arguments), related to an agent from the text of a scene, for example: The car runs on the highway—→ AGENT(CAR), RUNNING(CAR), PLACE(CAR, HIGHWAY):"
beliefs_temp = "0.8"


# Manteniamo il contesto globale delle interazioni
conversation_history = []

# Funzione per inviare richieste in streaming
def ask_ollama_stream(user_prompt, system, temp, model="qwen2.5:14b-instruct-q8_0"):
    # Costruiamo il prompt cumulativo
    context_prompt = ""
    for turn in conversation_history:
        context_prompt += f"Tu: {turn['user']}\nModello: {turn['model']}\n"
    context_prompt += f"Tu: {user_prompt}\nModello:"

    payload = {
        "model": model,
        "system": system,
        "prompt": context_prompt,
        "stream": True,  # Abilita lo streaming token per token
        "temperature": 0.8,
    }
    risposta = ""
    try:
        with requests.post(OLLAMA_API_URL, json=payload, stream=True) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    try:
                        token_json = json.loads(line.decode('utf-8'))
                        token = token_json.get("response", "")
                        print(token, end="", flush=True)
                        risposta += token
                    except json.JSONDecodeError as e:
                        print(f"\n[Errore parsing token JSON]: {e}")
            print()  # newline finale

        # Aggiungiamo la nuova interazione alla cronologia
        conversation_history.append({"user": user_prompt, "model": risposta.strip()})


    except requests.exceptions.RequestException as e:
        print(f"Errore nella richiesta: {e}")
    return risposta




# === Funzioni per la gestione dell'immagine e inferenza ===

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')


def describe_image(image_path, prompt, temp, model="llava:13b-v1.6-vicuna-q8_0"):
    image_base64 = image_to_base64(image_path)

    # Messaggio da inviare al modello
    data = {
        "model": model,
        "prompt": prompt,
        "images": [image_base64],
        "temperature": temp,
        "stream": False
    }

    try:
        response = requests.post("http://localhost:11434/api/generate", json=data)

        if response.status_code == 200:
            result = response.json()
            return result.get("response", "Nessuna risposta dal modello.")
        else:
            return f"Errore: {response.status_code} - {response.text}"
    except requests.exceptions.ConnectionError:
        return "Errore: impossibile connettersi a Ollama. Verifica che sia in esecuzione su http://localhost:11434."


# === Funzioni per Achieve ===

def on_achieve():
    achieve_button.config(state="disabled")
    text_field.config(state="normal", fg="gray")
    text_field.delete("1.0", tk.END)
    text_field.insert(tk.END, "thinking...")
    text_field.config(state="disabled")

    # Esegui inferenza in un thread separato per non bloccare la GUI
    threading.Thread(target=run_inference, daemon=True).start()


def run_inference():
    prompt = prompt_entry.get()
    try:
        temp = float(temp_entry.get())
    except ValueError:
        temp = 0.7  # valore di default se la temperatura non è valida
    # Esegue la chiamata LLM
    descrizione = describe_image(image_path, prompt, temp)

    # Dopo l’inferenza, aggiorna la GUI nel thread principale
    root.after(0, lambda: update_result(descrizione))


def update_result(descrizione):
    text_field.config(state="normal", fg="black")
    text_field.delete("1.0", tk.END)
    text_field.insert(tk.END, descrizione)
    text_field.config(state="normal")
    achieve_button.config(state="normal")


# === Funzioni per Beliefs ===

def achieve_beliefs():
    achieve_beliefs_button.config(state="disabled")
    beliefs_text_field.config(state="normal", fg="gray")
    beliefs_text_field.delete("1.0", tk.END)
    beliefs_text_field.insert(tk.END, "thinking...")
    beliefs_text_field.config(state="disabled")

    # Recupera i valori di prompt e temperatura per i beliefs
    beliefs_prompt = beliefs_prompt_entry.get()
    try:
        beliefs_temperature = float(beliefs_temp_entry.get())
    except ValueError:
        beliefs_temperature = 0.7  # valore di default

    # Esegui inferenza per i beliefs in background
    threading.Thread(target=run_beliefs_inference, args=(beliefs_prompt, beliefs_temperature), daemon=True).start()


def run_beliefs_inference(prompt, temperature):

    prompt = beliefs_prompt_entry.get()
    outcome = ask_ollama_stream(prompt, system, beliefs_temp)
    root.after(0, lambda: update_beliefs_result(outcome))


def update_beliefs_result(descrizione):
    beliefs_text_field.config(state="normal", fg="black")
    beliefs_text_field.delete("1.0", tk.END)
    beliefs_text_field.insert(tk.END, descrizione)
    beliefs_text_field.config(state="disabled")
    achieve_beliefs_button.config(state="normal")


# === Funzioni per l'interfaccia grafica ===

# Caricamento dell'immagine
def load_image(image_path):
    if os.path.exists(image_path):
        img = Image.open(image_path)
        img = img.resize((400, 300), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)

        image_label = tk.Label(root, image=photo)
        image_label.image = photo  # Previene garbage collection
        image_label.pack(pady=10)
    else:
        image_label = tk.Label(root, text="Immagine non trovata")
        image_label.pack(pady=10)


# Funzione per aprire la finestra di dialogo per modificare beliefs_prompt
def edit_beliefs_prompt():
    # Crea una finestra di dialogo personalizzata
    dialog = Toplevel(root)
    dialog.title("Modifica Prompt")

    # Ottieni le dimensioni della finestra principale
    window_width = root.winfo_width()
    window_height = root.winfo_height()

    # Ottieni le dimensioni della finestra di dialogo
    dialog_width = 700  # Aumento della larghezza
    dialog_height = 450  # Aumento dell'altezza

    # Calcola la posizione per centrare la finestra di dialogo
    position_top = int(window_height / 2 - dialog_height / 2)
    position_left = int(window_width / 2 - dialog_width / 2)

    # Imposta la geometria della finestra di dialogo
    dialog.geometry(f"{dialog_width}x{dialog_height}+{position_left}+{position_top}")

    # Crea il campo di testo ancora più grande
    text_widget = tk.Text(dialog, height=20, width=70)  # Aumento le dimensioni del campo di testo
    text_widget.insert(tk.END, beliefs_prompt)  # Inserisci il valore corrente
    text_widget.pack(padx=10, pady=10)

    # Funzione per salvare il testo modificato
    def save_changes():
        new_beliefs_prompt = text_widget.get("1.0", tk.END).strip()
        if new_beliefs_prompt:  # Se il nuovo testo non è vuoto
            beliefs_prompt_entry.delete(0, tk.END)
            beliefs_prompt_entry.insert(0, new_beliefs_prompt)
        dialog.destroy()

    # Bottone "Salva"
    save_button = tk.Button(dialog, text="Salva", command=save_changes)
    save_button.pack(side="left", padx=20, pady=10)

    # Bottone "Annulla"
    cancel_button = tk.Button(dialog, text="Annulla", command=dialog.destroy)
    cancel_button.pack(side="right", padx=20, pady=10)


# Creazione della finestra principale
root = tk.Tk()
root.title("DTwin Assessment")
root.geometry("1200x800")

# Percorso dell'immagine .jpg
image_path = "images/immagine_webcam.jpg"  # <-- Cambia con il percorso della tua immagine
load_image(image_path)

# Frame principale per i controlli
control_frame = tk.Frame(root)
control_frame.pack(pady=10, fill=tk.X)

# Bottone "Achieve description"
achieve_button = tk.Button(control_frame, text="Achieve description", command=on_achieve)
achieve_button.pack(anchor="w", padx=10, pady=(0, 5))

# Campo prompt
tk.Label(control_frame, text="Prompt:").pack(side="left", padx=(10, 2))
prompt_entry = tk.Entry(control_frame, width=100)
prompt_entry.insert(0, image_prompt)
prompt_entry.pack(side="left")

# Campo temperatura
tk.Label(control_frame, text="Temperatura:").pack(side="left", padx=(10, 2))
temp_entry = tk.Entry(control_frame, width=5)
temp_entry.insert(0, image_temp)
temp_entry.pack(side="left")

# Campo di testo per il risultato dell'inferenza
text_field = tk.Text(root, height=4, width=140, wrap=tk.WORD)
text_field.pack(pady=10)

# Sezione controlli per Achieve Beliefs
beliefs_control_frame = tk.Frame(root)
beliefs_control_frame.pack(pady=10, fill=tk.X, padx=10)

# Bottone "Achieve Beliefs"
achieve_beliefs_button = tk.Button(beliefs_control_frame, text="Achieve Beliefs", command=achieve_beliefs)
achieve_beliefs_button.pack(anchor="w", padx=10, pady=(0, 5))

# Campo prompt per beliefs
tk.Label(beliefs_control_frame, text="System:").pack(side="left", padx=(10, 2))
beliefs_prompt_entry = tk.Entry(beliefs_control_frame, width=100)
beliefs_prompt_entry.insert(0, beliefs_prompt)
beliefs_prompt_entry.pack(side="left")

# Bottone per modificare il beliefs_prompt
edit_button = tk.Button(beliefs_control_frame, text="Modifica", command=edit_beliefs_prompt)
edit_button.pack(side="left", padx=5)

# Campo temperatura per beliefs
tk.Label(beliefs_control_frame, text="Temperatura:").pack(side="left", padx=(10, 2))
beliefs_temp_entry = tk.Entry(beliefs_control_frame, width=5)
beliefs_temp_entry.insert(0, beliefs_temp)
beliefs_temp_entry.pack(side="left")

# Campo di testo per il risultato dei beliefs
beliefs_text_field = tk.Text(root, height=4, width=140, wrap=tk.WORD)
beliefs_text_field.pack(padx=10)
beliefs_text_field.config(state="disabled", fg="black")

# Avvio del loop dell'interfaccia
root.mainloop()
