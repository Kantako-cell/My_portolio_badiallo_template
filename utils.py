# Mes imports
import streamlit as st
import streamlit.components.v1 as components 
import json
import urllib.request
import urllib.error
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
import requests  # pour récupérer l'IP
from my_data import FORBIDDEN_WORDS

def get_secret(key):
    """
    Récupère une clé API ou un mot de passe depuis le gestionnaire 
    de secrets de Streamlit de manière sécurisée, sans faire planter l'application en cas d'erreur.
    """
    try:
        return st.secrets[key].strip()
    except Exception:
        return ""

GEMINI_KEY      = get_secret("GEMINI_API_KEY")
GROQ_KEY        = get_secret("GROQ_API_KEY")
OPENROUTER_KEY  = get_secret("OPENROUTER_API_KEY")
CEREBRAS_KEY    = get_secret("CEREBRAS_API_KEY")
HUGGING_FACE_KEY    = get_secret("HUGGING_FACE_API_KEY")

########## Mes fonctions utilitaires de l'interface ############

def display_pdf(file_path):
    """
    Convertit un fichier PDF local en format base64 afin de l'afficher 
    directement dans une fenêtre intégrée (iframe) sur l'interface du portfolio.
    """
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def load_css(file_name):
    """
    Charge et injecte un fichier CSS externe pour personnaliser 
    l'esthétique et les couleurs de l'application Streamlit.
    """
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def display_floating_chat_invite():
    """
    Génère un bouton flottant animé en bas de l'écran. 
    Lorsqu'un visiteur clique dessus, un script JavaScript le redirige 
    automatiquement vers le 7ème onglet (celui du chatbot Kanty) et remonte en haut de page.
    """
    html_code = """
    <style>
    .kanty-badge {
        position: fixed; bottom: 30px; right: 30px; z-index: 999999;
        background: linear-gradient(135deg, #C4704A, #6B3F2A); 
        color: #FAF7F2; padding: 12px 22px; border-radius: 50px;
        font-family: 'DM Sans', sans-serif; font-size: 14px; font-weight: 500;
        box-shadow: 0 8px 25px rgba(196, 112, 74, 0.45); cursor: pointer;
        display: flex; align-items: center; gap: 10px; transition: 0.3s ease;
        animation: float-kanty 3s ease-in-out infinite; border: 1px solid #E8D5C0;
    }
    
    .kanty-badge:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 12px 30px rgba(107, 63, 42, 0.6); animation: none;
    }
    
    .kanty-dot {
        width: 8px; height: 8px; background-color: #D4A847; 
        border-radius: 50%; box-shadow: 0 0 8px #D4A847;
    }
    
    @keyframes float-kanty {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-6px); }
    }
    </style>
    
    <div id="kanty-floating-badge" class="kanty-badge">
        <div class="kanty-dot"></div>
        Discuter avec mon assistant Kanty ✨!
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)
    
    js_code = """
    <script>
    function activerBouton() {
        const doc = window.parent.document;
        const badge = doc.getElementById('kanty-floating-badge');
        
        if (badge) {
            badge.onclick = function() {
                const tabs = doc.querySelectorAll('button[data-baseweb="tab"]');
                if(tabs.length >= 7) { 
                    tabs[6].click(); 
                    doc.defaultView.scrollTo({top: 0, behavior: 'smooth'}); 
                }
            };
        } else {
            setTimeout(activerBouton, 100);
        }
    }
    
    activerBouton();
    </script>
    """
    components.html(js_code, height=0, width=0)


############### Fonctions utilisées dans mon chatbot #################

def handle_enter():
    """
    Intercepte la validation du champ de saisie du chat.
    Sauvegarde la question de l'utilisateur en mémoire et vide immédiatement 
    la barre de saisie pour une meilleure fluidité.
    """
    if st.session_state.chat_input.strip():
        st.session_state.question_finale = st.session_state.chat_input.strip()
        st.session_state.chat_input = "" 

def contains_forbidden_words(text):
    """
    Analyse le texte soumis par l'utilisateur en le comparant 
    à une liste de mots interdits (FORBIDDEN_WORDS) pour filtrer les messages inappropriés.
    """
    lower_text = text.lower()
    for word in FORBIDDEN_WORDS:
        if word in lower_text:
            return True
    return False

def call_gemini(messages, system):
    """Envoie l'historique de la conversation à l'API Google Gemini et retourne sa réponse générée."""
    if not GEMINI_KEY or not GEMINI_SDK:
        raise Exception("Gemini non disponible")
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_KEY)

    model = genai.GenerativeModel('gemini-2.5-flash-lite', system_instruction=system)
    history = []
    for m in messages[:-1]:
        history.append({"role": "user" if m["role"] == "user" else "model",
                        "parts": [m["content"]]})
    chat = model.start_chat(history=history)
    resp = chat.send_message(messages[-1]["content"])
    return resp.text
 
def call_openrouter(messages, system):
    """Envoie la requête via OpenRouter pour interroger le modèle spécifié (ici owl-alpha)."""
    if not OPENROUTER_KEY:
        raise Exception("OpenRouter non disponible")
    payload = json.dumps({
        "model": "openrouter/owl-alpha",
        "messages": [{"role": "system", "content": system}] + messages,
        "max_tokens": 700
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=payload,
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {OPENROUTER_KEY}",
                 "HTTP-Referer": "https://portfolio-badiallo.streamlit.app"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        res = json.loads(r.read().decode())
    return res["choices"][0]["message"]["content"]

def call_groq(messages, system):
    """Passe par l'API ultra-rapide de Groq pour interroger le modèle Llama 3.3."""
    if not GROQ_KEY or not GROQ_SDK:
        raise Exception("Groq non disponible")
    client = Groq(api_key=GROQ_KEY)
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system}] + messages,
        max_tokens=700,
        temperature=0.65
    )
    return resp.choices[0].message.content
 
def call_cerebras(messages, system):
    """Fait appel à l'API de Cerebras pour générer une réponse via le modèle gpt-oss-120b."""
    if not CEREBRAS_KEY or not CEREBRAS_SDK:
        raise Exception("Cerebras non disponible")
    client = Cerebras(api_key=CEREBRAS_KEY)
    resp = client.chat.completions.create(
        model="gpt-oss-120b",
        messages=[{"role": "system", "content": system}] + messages,
        max_tokens=700
    )
    return resp.choices[0].message.content

def call_huggingface(messages, system):
    """Interroge l'API de Hugging Face avec le modèle Meta-Llama-3-8B-Instruct."""
    if not HUGGING_FACE_KEY:
        raise Exception("Hugging Face non disponible")
    client = InferenceClient(api_key=HUGGING_FACE_KEY)
    response = client.chat_completion(
        model="meta-llama/Meta-Llama-3-8B-Instruct",
        messages=[{"role": "system", "content": system}] + messages,
        max_tokens=700,
        temperature=0.65
    )
    return response.choices[0].message.content

def chat_with_fallback(messages, system):
    """
    Fonction centrale de Kanty : gère la logique de secours (fallback).
    Tente de contacter les différents fournisseurs d'IA séquentiellement.
    Si le premier échoue ou est surchargé, elle passe silencieusement au suivant
    pour garantir que l'utilisateur reçoive toujours une réponse.
    """
    limited_messages = messages[-MAX_HISTORY_TURNS*2:] if len(messages) > MAX_HISTORY_TURNS*2 else messages
    providers = [
        ("Google ✨", call_gemini, "Gemini 2.5 Flash"),
        ("OpenRouter ⚡", call_openrouter, "owl-alpha"),
        ("Groq ⚡", call_groq, "Llama 3.3 70B"),
        ("Hugging Face 🤗", call_huggingface, "Meta-Llama-3-8B"),
        ("Cerebras 🧠", call_cerebras, "gpt-oss-120b"),
    ]
    
    erreurs_rencontrees = []
    for name, fn, model_name in providers:
        try:
            reply = fn(messages, system)
            return reply, f"{name} ({model_name})"
        
        except Exception as e:
            erreurs_rencontrees.append(f"❌ {name} ({model_name}) -> {str(e)}")
            continue
                    
    rapport_erreurs: str = "\n".join(erreurs_rencontrees)
    message_final = (
                f"Désolé, tous les serveurs de l'application sont saturés ou indisponibles actuellement.\n\n"
                f"📋 **Détail technique des erreurs :**\n{rapport_erreurs}"
            )
    return message_final, "❌"

def send_alert_email(user_message, user_ip="Inconnue"):
    """
    Envoie automatiquement un email d'alerte à l'administrateur 
    (via le serveur SMTP configuré) lorsqu'un message inapproprié 
    ou malveillant est détecté sur le chatbot.
    """
    try:
        sender = st.secrets["SMTP_USER"]
        password = st.secrets["SMTP_PASSWORD"]
        recipient = st.secrets["ALERT_EMAIL"]
        server = st.secrets["SMTP_SERVER"]
        port = st.secrets["SMTP_PORT"]

        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = recipient
        msg["Subject"] = "🚨 Alerte chatbot - message inapproprié"

        body = f"""
        Un message inapproprié a été détecté sur le portfolio de Badiallo.

        IP utilisateur : {user_ip}
        Message : 
        {user_message}

        ---
        Ce message a été automatiquement envoyé par le système de sécurité.
        """
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(server, port) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Erreur d'envoi d'email (administrateur): {e}")
        return False