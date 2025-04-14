import tkinter as tk
from tkinter import Toplevel, filedialog

# pip install pillow
from PIL import Image, ImageTk
import os
import base64
import requests
import threading
import json
# pip install opencv-python
import cv2
from datetime import datetime



# Endpoint locale di Ollama
OLLAMA_API_URL = "http://localhost:11434/api/generate"

image_label = None  # dichiarazione globale

# Goal system
# Formulate an optimal-single goal from the scene (without other text) in the shape of predicate, with single-words label related to an agent from the text of the scene. Verbs can have two arguments. For example: "The car runs on the highway —→ AGENT(CAR),  RUN(CAR, HIGHWAY)"

multimodal_model = "llava:13b-v1.6-vicuna-q8_0"
text_model = "qwen2.5:14b-instruct-q8_0"

# home: llava:13b-v1.5-q6_K, llama3:8b-instruct-q8_0
# work: llava:13b-v1.6-vicuna-q8_0, qwen2.5:14b-instruct-q8_0

image_prompt = "Describe briefly the picture, with no further text."
image_temp = "0.8"
beliefs_temp = "0.8"

# Prompt predefiniti per ogni tipo
prediction_prompts = {
    "beliefs": """Extract only beliefs separated by commas (without other text), and single-word (possible other words as additional belief arguments), related to an actor from the text of a scene beliefs related to verb can have two arguments. The belief ACTOR(X) must be present, where X is the main subject of the scene. For example: The car runs on the highway —→ ACTOR(CAR),  RUN(CAR, HIGHWAY).""",
    "goal": """Formulate briefly a single goal for an external agent observing the described scene. No additional text.""",
    "action": """Formulate very briefly the most appropriate action to achieve the goal for an agent before the scene, without additional text or explanation. Each action must be in the a predicate ACTION(X), where ACTION=verb, ACTOR(X), where X is the man subject object of the action (in capital). Non other text is admitted."""
}

# Manteniamo il contesto globale delle interazioni
conversation_history = []

# Funzione per inviare richieste in streaming
def ask_ollama_stream(user_prompt, system, temp, model=text_model):
    # Costruiamo il prompt cumulativo

    payload = {
        "model": model,
        "system": system,
        "prompt": user_prompt,
        "stream": True,  # Abilita lo streaming token per token
        "temperature": temp,
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

    except requests.exceptions.RequestException as e:
        print(f"Errore nella richiesta: {e}")
    return risposta




# === Funzioni per la gestione dell'immagine e inferenza ===

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')


def describe_image(image_path, prompt, temp, model=multimodal_model):
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
    print(f"\nAchieving image prediction with temperature {temp}...")
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
    beliefs_prompt = text_field.get("1.0", tk.END).strip()
    beliefs_system_prompt = beliefs_prompt_entry.get().strip()
    try:
        beliefs_temperature = float(beliefs_temp_entry.get())
    except ValueError:
        beliefs_temperature = 0.7  # valore di default

    # Esegui inferenza per i beliefs in background
    threading.Thread(target=run_beliefs_inference, args=(beliefs_prompt, beliefs_system_prompt, beliefs_temperature), daemon=True).start()


def run_beliefs_inference(prompt, system, temp):

    print(f"\nAchieving beliefs prediction with temperature {temp}...")
    print(f"system: {system}")
    print(f"prompt: {prompt}")
    outcome = ask_ollama_stream(prompt, system, temp)
    root.after(0, lambda: update_beliefs_result(outcome))


def update_beliefs_result(descrizione):
    beliefs_text_field.config(state="normal", fg="black")
    beliefs_text_field.delete("1.0", tk.END)
    beliefs_text_field.insert(tk.END, descrizione)
    beliefs_text_field.config(state="disabled")
    achieve_beliefs_button.config(state="normal")


# === Funzioni per l'interfaccia grafica ===

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
    text_widget = tk.Text(dialog, height=20, width=70, wrap=tk.WORD)  # Aumento le dimensioni del campo di testo
    text_widget.insert(tk.END, beliefs_prompt_entry.get()) # Inserisci il valore corrente
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
root.resizable(False, False)

# Layout a due colonne: immagine a sinistra, box etichette a destra
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

# Frame sinistro: immagine
left_frame = tk.Frame(top_frame)
left_frame.pack(side=tk.LEFT, padx=20)

# Frame destro: etichette Belief, Goal, Action, Plan
# Frame destro con bordo, titolo e stile migliorato
right_frame = tk.LabelFrame(top_frame, text="🧠 Agent Mental State", padx=20, pady=20,
                            font=("Arial", 14, "bold"), labelanchor="n")
right_frame.pack(side="left", fill=tk.BOTH, expand=True, padx=20, pady=20)


button_frame = tk.Frame(left_frame)
# Aggiungi i bottoni al button_frame...
button_frame.pack(side=tk.TOP)

# Caricamento e posizionamento immagine nel frame sinistro
def load_image(image_path):
    global image_label

    # Se esiste già un'immagine, la rimuoviamo
    if image_label is not None:
        image_label.destroy()

    if os.path.exists(image_path):
        img = Image.open(image_path)
        img = img.resize((300, 225), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)

        image_label = tk.Label(left_frame, image=photo)
        image_label.image = photo  # Previene garbage collection
        image_label.pack(before=button_frame)
    else:
        image_label = tk.Label(left_frame, text="Immagine non trovata")
        image_label.pack(before=button_frame)

# Aggiunta delle label nel frame destro
# Label e TextField dinamici nel frame destro
# Funzione per aggiungere un campo con label e text box espanso
def add_labeled_field(parent, label_text_with_emoji):
    frame = tk.Frame(parent)
    frame.pack(anchor="w", pady=10, fill=tk.X, expand=True)

    # Riduzione della dimensione del font della label
    tk.Label(frame, text=label_text_with_emoji, width=12, anchor="w", font=("Arial", 10, "bold")).pack(side="left", padx=(0, 10))

    # Riduzione della dimensione del font del campo di testo
    text = tk.Text(frame, height=2, width=80, wrap=tk.WORD, font=("Arial", 9))
    text.pack(side="left", fill=tk.X, expand=True)

    return text


def on_acquire_image():
    print("Acquire image clicked")

    cap = cv2.VideoCapture(0)  # Usa la webcam di default

    if not cap.isOpened():
        print("Errore: impossibile accedere alla webcam")
        return

    ret, frame = cap.read()
    if ret:
        # Salva l'immagine acquisita

        # Ottieni data e ora correnti in formato breve
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Definisci il nome del file con timestamp
        acquired_image_path = f"images/webcam_{timestamp}.jpg"

        cv2.imwrite(acquired_image_path, frame)

        # Rilascia la webcam
        cap.release()
        cv2.destroyAllWindows()

        # Aggiorna il path globale e carica l'immagine acquisita
        global image_path
        image_path = acquired_image_path
        load_image(image_path)
    else:
        print("Errore nell'acquisizione dell'immagine")
        cap.release()
        cv2.destroyAllWindows()


# Funzione di esempio per aggiungere beliefs
def add_belief_action():
    print("Add Beliefs action triggered")
    beliefs_content = beliefs_text_field.get("1.0", tk.END).strip()

    # Imposta il contenuto nel campo belief_field
    belief_field.delete("1.0", tk.END)  # Pulisce il campo precedente
    belief_field.insert(tk.END, beliefs_content)  # Inserisce il contenuto nel campo belief_field

# Funzione di esempio per cambiare il goal
def change_goal_action():
    print("Change Goal action triggered")
    goal_content = beliefs_text_field.get("1.0", tk.END).strip()

    # Imposta il contenuto nel campo belief_field
    goal_field.delete("1.0", tk.END)  # Pulisce il campo precedente
    goal_field.insert(tk.END, goal_content)  # Inserisce il contenuto nel campo belief_field

# Funzione di esempio per aggiungere una nuova azione
def add_action_action():
    print("Add Action action triggered")
    # Qui puoi aggiungere logica per aggiungere un'azione
    action_content = beliefs_text_field.get("1.0", tk.END).strip()

    # Imposta il contenuto nel campo belief_field
    action_field.delete("1.0", tk.END)  # Pulisce il campo precedente
    action_field.insert(tk.END, action_content)  # Inserisce il contenuto nel campo belief_field



# Campi con icone
belief_field = add_labeled_field(right_frame, "🧠 Beliefs:")
goal_field = add_labeled_field(right_frame, "🎯 Goal:")
action_field = add_labeled_field(right_frame, "⚙️ Action:")
plan_field = add_labeled_field(right_frame, "📋 Plan:")

# Percorso dell'immagine .jpg
image_path = "images/noimage.jpg"  # <-- Cambia con il percorso della tua immagine
load_image(image_path)

def on_select_images():
    file_paths = filedialog.askopenfilenames(
        title="Seleziona immagini",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    if file_paths:
        print("Selected images:")
        for path in file_paths:
            print(path)
        # Volendo puoi caricare la prima immagine selezionata
        global image_path
        image_path = file_paths[0]
        load_image(image_path)


button_frame = tk.Frame(left_frame)
button_frame.pack(pady=(5, 20))

acquire_button = tk.Button(button_frame, text="Acquire image", command=on_acquire_image)
acquire_button.pack(side="left", padx=5)

select_button = tk.Button(button_frame, text="Select images", command=on_select_images)
select_button.pack(side="left", padx=5)

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
tk.Label(control_frame, text="Temperature:").pack(side="left", padx=(10, 2))
temp_entry = tk.Entry(control_frame, width=5)
temp_entry.insert(0, image_temp)
temp_entry.pack(side="left")

# Aggiunta della label "Prediction" sopra il text_field
tk.Label(root, text="Multi-modal inference ("+multimodal_model+")", font=("Arial", 14, "bold")).pack(pady=(10, 5))

# Campo di testo per il risultato dell'inferenza
text_field = tk.Text(root, height=4, width=140, wrap=tk.WORD)
text_field.pack(pady=10)

# Sezione controlli per Achieve Beliefs
beliefs_control_frame = tk.Frame(root)
beliefs_control_frame.pack(pady=10, fill=tk.X, padx=10)

# Callback per il cambio del tipo di prediction
def on_prediction_type_change(value):
    beliefs_prompt_entry.delete(0, tk.END)
    beliefs_prompt_entry.insert(0, prediction_prompts.get(value, ""))

# Bottone "Achieve Beliefs"
achieve_beliefs_button = tk.Button(beliefs_control_frame, text="Achieve", command=achieve_beliefs)
achieve_beliefs_button.pack(side="left", padx=(5, 10), pady=(0, 5))

# Menù a tendina per selezione tipo prediction
tk.Label(beliefs_control_frame, text="Prediction type:").pack(side="left")
prediction_type_var = tk.StringVar(root)
prediction_type_var.set("beliefs")  # default
prediction_menu = tk.OptionMenu(beliefs_control_frame, prediction_type_var, "beliefs", "goal", "action", command=on_prediction_type_change)
prediction_menu.pack(side="left")

# Campo prompt per beliefs
tk.Label(beliefs_control_frame, text="System:").pack(side="left", padx=(10, 2))
beliefs_prompt_entry = tk.Entry(beliefs_control_frame, width=65)
beliefs_prompt_entry.insert(0, prediction_prompts["beliefs"])  # Default prompt
beliefs_prompt_entry.pack(side="left")

# Bottone per modificare il beliefs_prompt
edit_button = tk.Button(beliefs_control_frame, text="Change", command=edit_beliefs_prompt)
edit_button.pack(side="left", padx=5)

# Campo temperatura per beliefs
tk.Label(beliefs_control_frame, text="Temperature:").pack(side="left", padx=(10, 2))
beliefs_temp_entry = tk.Entry(beliefs_control_frame, width=5)
beliefs_temp_entry.insert(0, beliefs_temp)
beliefs_temp_entry.pack(side="left")

# Aggiunta della label "Prediction" sopra il text_field
tk.Label(root, text="Inference from Multi-modal inference ("+text_model+")", font=("Arial", 14, "bold")).pack(pady=(10, 5))


# Campo di testo per il risultato dei beliefs
beliefs_text_field = tk.Text(root, height=4, width=140, wrap=tk.WORD)
beliefs_text_field.pack(padx=10)
beliefs_text_field.config(state="disabled", fg="black")

# Frame orizzontale per i pulsanti
buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=(5, 10), anchor="w", padx=10)

# Aggiungi i pulsanti nel frame orizzontale
add_beliefs_button = tk.Button(buttons_frame, text="Add beliefs", command=lambda: add_belief_action())
add_beliefs_button.pack(side="left", padx=(0, 10))

change_goal_button = tk.Button(buttons_frame, text="Add Goal", command=lambda: change_goal_action())
change_goal_button.pack(side="left", padx=(0, 10))

add_action_button = tk.Button(buttons_frame, text="Add Action", command=lambda: add_action_action())
add_action_button.pack(side="left", padx=(0, 10))


# Avvio del loop dell'interfaccia
root.mainloop()
