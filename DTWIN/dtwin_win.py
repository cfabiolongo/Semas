import tkinter as tk
from PIL import Image, ImageTk
import os
import base64
import requests
import threading


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

# Percorso dell'immagine .jpg
image_path = os.path.join("images", "immagine_webcam.jpg")

# Creazione della finestra principale
root = tk.Tk()
root.title("DTwin Assessment")
root.geometry("1200x800")

image_path = "images/immagine_webcam.jpg"  # <-- Cambia con il percorso della tua immagine

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
    descrizione = describe_image(image_path, prompt, temperature)
    root.after(0, lambda: update_beliefs_result(descrizione))

def update_beliefs_result(descrizione):
    beliefs_text_field.config(state="normal", fg="black")
    beliefs_text_field.delete("1.0", tk.END)
    beliefs_text_field.insert(tk.END, descrizione)
    beliefs_text_field.config(state="disabled")
    achieve_beliefs_button.config(state="normal")


# Caricamento e visualizzazione dell'immagine .jpg
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

# Frame che contiene il pulsante e il textfield
control_frame = tk.Frame(root)
control_frame.pack(pady=10, fill=tk.X)

# Bottone "Achieve" in alto a sinistra
achieve_button = tk.Button(control_frame, text="Achieve description", command=on_achieve)
achieve_button.pack(anchor="w", padx=10, pady=(0, 5))

# Campo prompt
tk.Label(control_frame, text="Prompt:").pack(side="left", padx=(10, 2))
prompt_entry = tk.Entry(control_frame, width=100)
prompt_entry.insert(0, "Describe briefly the picture, with no further text.")
prompt_entry.pack(side="left")

# Campo temperatura
tk.Label(control_frame, text="Temperatura:").pack(side="left", padx=(10, 2))
temp_entry = tk.Entry(control_frame, width=5)
temp_entry.insert(0, "0.8")
temp_entry.pack(side="left")

# Campo di testo ampio sotto l'immagine
text_field = tk.Text(root, height=4, width=140, wrap=tk.WORD)
text_field.pack(pady=10)


# === Sezione controlli per Achieve Beliefs ===
beliefs_control_frame = tk.Frame(root)
beliefs_control_frame.pack(pady=10, fill=tk.X, padx=10)

# Bottone "Achieve Beliefs"
achieve_beliefs_button = tk.Button(beliefs_control_frame, text="Achieve Beliefs", command=achieve_beliefs)
achieve_beliefs_button.pack(side="left")

# Campo prompt per beliefs
tk.Label(beliefs_control_frame, text="Prompt:").pack(side="left", padx=(10, 2))
beliefs_prompt_entry = tk.Entry(beliefs_control_frame, width=40)
beliefs_prompt_entry.insert(0, "Describe briefly the picture in terms of beliefs.")
beliefs_prompt_entry.pack(side="left")

# Campo temperatura per beliefs
tk.Label(beliefs_control_frame, text="Temperatura:").pack(side="left", padx=(10, 2))
beliefs_temp_entry = tk.Entry(beliefs_control_frame, width=5)
beliefs_temp_entry.insert(0, "0.7")
beliefs_temp_entry.pack(side="left")

# === Campo output per beliefs ===
beliefs_text_field = tk.Text(root, height=4, width=140, wrap=tk.WORD)
beliefs_text_field.pack(padx=10)
beliefs_text_field.config(state="disabled", fg="black")


# Avvio del loop dell'interfaccia
root.mainloop()
