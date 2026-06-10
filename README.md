# Portfolio Interactif - Badiallo Kantako

Bienvenue sur le code source de mon portfolio.

## L'origine du projet

L'idée de développer ce site m'est venue tout simplement parce qu'il fallait à chaque fois adapter et réduire mon CV en fonction des offres. J'ai eu l'occasion de faire tellement de projets intéressants durant ma formation que je trouvais dommage de devoir faire un tri pour tout faire tenir sur une page. Chaque projet m'a apporté des compétences techniques et analytiques qui peuvent servir dans beaucoup de domaines. Ce portfolio est donc le moyen de rentrer plus en profondeur dans mes compétences et d'expliquer ce que je fais réellement.

## La création du Chatbot

L'intégration de l'assistant IA vient d'une idée que j'ai eue après un cours de Web Mining. Avec mon groupe, on avait mis en place un système de questions-réponses basé sur un modèle hybride (BM25 et BERT). Le but était de traiter des requêtes pour ressortir les tweets les plus pertinents, classés par score. J'avais adoré faire ce projet, et ça m'a donné envie de créer un chatbot pour mon portfolio.

Au début, je pensais utiliser des modèles similaires construits de zéro, mais je me suis vite rendu compte que ce serait inutilement compliqué. Mon but ici n'était pas de classer des documents ou des tweets par score de pertinence, mais d'avoir un outil capable de tenir une vraie discussion fluide. 

J'ai donc changé d'approche et décidé d'utiliser directement les API de grands modèles de langage. 

## Ce que ce projet m'a appris

Ce changement de direction m'a permis d'apprendre énormément de choses sur la gestion et la sécurité des clés API. Ça m'a surtout permis de mettre en place une logique de "fallback" : le code alterne entre plusieurs modèles pour choisir ceux qui sont les plus adaptés à la discussion et garantir que le bot réponde toujours.

Enfin, je me suis beaucoup amusée à rajouter des couches de sécurité pour tester mes idées. J'ai par exemple développé et intégré un système qui détecte les mots inappropriés et une sécurité anti-bot. C'était l'occasion de tester mes idées de bout en bout et de voir que ça fonctionne super bien en pratique.

## Conception technique

La documentation de Streamlit, qui est très bien faite, m'a beaucoup facilité la construction de l'interface web. Pour le reste, que ce soit pour structurer certains éléments ou déboguer quand je bloquais, je me suis pas mal aidée de Gemini et claude pour mon sytle CSS, ce qui m'a permis d'avancer très efficacement sur le déploiement.



## 🛠️ Installation et configuration en local

Si vous souhaitez explorer le code ou faire tourner ce portfolio sur votre propre machine, voici la marche à suivre. Le projet utilisant plusieurs API pour l'intelligence artificielle, vous devrez configurer vos propres clés pour que le chatbot puisse fonctionner.

1. **Cloner le projet :**
```bash
   git clone https://github.com/Kantako-cell/My_portolio_badiallo_template.git
   cd My_portolio_badiallo_template
```

2. **Installer les dépendances :**
   L'application est développée en Python. Il suffit d'installer les bibliothèques requises (comme Streamlit, Plotly, et les SDK des modèles IA) :
```bash
   pip install -r requirements.txt
```
**3.	Configurer les clés d'environnement (Secrets) :**
Streamlit utilise un fonctionnement spécifique pour protéger les données sensibles en local afin qu'elles ne se retrouvent jamais sur GitHub. À la racine du projet, créez un dossier nommé .streamlit, puis à l'intérieur, un fichier secrets.toml. Voici la structure exacte à reproduire en remplaçant les valeurs par vos propres clés :
   ```bash
   # Fichier : .streamlit/secrets.toml

   # Clés API pour le fonctionnement de Kanty
   GEMINI_API_KEY = "votre_cle_api_gemini"
   GROQ_API_KEY = "votre_cle_api_groq"
   OPENROUTER_API_KEY = "votre_cle_api_openrouter"
   CEREBRAS_API_KEY = "votre_cle_api_cerebras"
   HUGGING_FACE_API_KEY = "votre_cle_api_hugging_face"

   # Configuration SMTP pour les alertes
   SMTP_USER = "votre_email@gmail.com"
   SMTP_PASSWORD = "votre_mot_de_passe_d_application" #Note : c'est possible de l'avoir que si vous activez votre authentification à deux facteurs de votre compte google.
   ALERT_EMAIL = "email_de_reception_des_alertes@domaine.com"
   SMTP_SERVER = "smtp.gmail.com"
   SMTP_PORT = 587
```
**Lancer l'application :**
Une fois l'environnement configuré, vous pouvez démarrer l'interface web en tapant simplement : 
```bash
   streamlit run app_top.py
```

🔒 À propos de ce dépôt (Version Publique)

Ce dépôt est une version publique et allégée (template) de mon portfolio. J'ai créé cette version pour partager mon code tout en protégeant mes données personnelles, mes clés d'API et ma configuration de déploiement.
Le développement réel de ce projet m'a pris plus d'un mois et a été réalisé sur un dépôt privé.

<img width="1232" height="717" alt="github-private" src="https://github.com/user-attachments/assets/92da7ee2-79fb-4dbc-9621-b535550cc255" />


