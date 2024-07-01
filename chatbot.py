import gradio as gr
import ollama

css_path = "styles.css"

def format_history(msg: str, history: list[list[str, str]], system_prompt: str):
    chat_history = [{"role": "system", "content": system_prompt}]
    for query, response in history:
        chat_history.append({"role": "user", "content": query})
        chat_history.append({"role": "assistant", "content": response})  
    chat_history.append({"role": "user", "content": msg})
    return chat_history

def generate_response(msg: str, history: list[list[str, str]], system_prompt: str):
    chat_history = format_history(msg, history, system_prompt)
    response = ollama.chat(model='llama2', stream=True, messages=chat_history)
    message = ""
    for partial_resp in response:
        token = partial_resp["message"]["content"]
        message += token
        yield message

# Exemples correctement formatés
custom_examples = [
    ["Qui est Napoléon?"],
    ["Raconte-moi une blague."],
    ["Quelle est la capitale de la France?"]
]

chatbot = gr.ChatInterface(
    generate_response,
    chatbot=gr.Chatbot(
        avatar_images=["user.jpg", "chatbot.png"],
        height="64vh"
    ),
    additional_inputs=[
        gr.Textbox(
            "Tu es un assistant virtuel et tu es au services des autres. Tu dois répondre directement aux questions sans mimer tes expressions faciales. Tu ne dois répondre que en français. Lors de ta première réponse, tu devras commencer par 'Bonjour, je m'appelle Zeus'.",
            label="Ajouter prompt"
        )
    ],
    title="ZEUS AI",
    textbox=gr.Textbox(placeholder="Posez-moi une question", container=False, scale=7),
    description="Intelligence artificielle par Thibault Altaber",
    theme="Taithrah/Minimal",
    examples=custom_examples,  # Utiliser la liste de listes pour les exemples
    submit_btn="⬅ Envoyer",
    retry_btn="🔄 Rafraîchir Réponse",
    undo_btn="↩ Supprimer",
    clear_btn="🗑️ Nettoyer Chat",
    css=css_path
)

chatbot.launch()