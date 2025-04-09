import requests
import json

# Endpoint locale di Ollama
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# CONTEXTO GLOBALE — puoi personalizzarlo
system = """extract only beliefs (without other text), and single-word (possible other words as additional belief arguments), related to an agent
             from the text of a scene beliefs related to verb can have two arguments. For example: The car runs on the highway —→ AGENT(CAR),  RUN(CAR, HIGHWAY).
"""

# Manteniamo il contesto globale delle interazioni
conversation_history = []

# Funzione per inviare richieste in streaming
def ask_ollama_stream(user_prompt, model="qwen2.5:14b-instruct-q8_0"):
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

    try:
        risposta = ""
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

# Loop interattivo da linea di comando
if __name__ == "__main__":
    print("Chat con il modello (digita 'esci' per terminare)")
    while True:
        user_input = input("\nTu: ")
        if user_input.lower() in ["esci", "exit", "quit"]:
            print("Uscita dalla chat.")
            break
        ask_ollama_stream(user_input)
