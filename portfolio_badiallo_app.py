# Mes imports
import streamlit as st
import plotly.graph_objects as go
import base64
import os
import markdown
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import requests  # pour récupérer l'IP
from my_data import PROFILE, POURQUOI_MOI, JOURNEY, INTRO_EXPERIENCES, EXPERIENCES, INTRO_PROJECTS, PROJECTS, SKILLS_DETAILED, JOBS, INTERESTS, CHATBOT_CONTEXT, FORBIDDEN_WORDS
from utils import (
    load_css, display_pdf, display_floating_chat_invite, 
    chat_with_fallback, handle_enter, contains_forbidden_words, 
    send_alert_email,get_secret
)

st.set_page_config(
    page_title="Badiallo Kantako · Portfolio",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# GEMINI_KEY      = get_secret("GEMINI_API_KEY")
# GROQ_KEY        = get_secret("GROQ_API_KEY")
# OPENROUTER_KEY  = get_secret("OPENROUTER_API_KEY")
# CEREBRAS_KEY    = get_secret("CEREBRAS_API_KEY")
# HUGGING_FACE_KEY    = get_secret("HUGGING_FACE_API_KEY")

if "welcome_shown" not in st.session_state:
    st.toast("Bienvenue sur mon Portfolio ! 👋", icon="🌟")
    st.session_state.welcome_shown = True

# Mon CSS — DESIGN TERRACOTTA / CREAM + ANIMATIONS

load_css('style.css')

# ###################### SESSION STATE ##############################
if "messages" not in st.session_state:
    st.session_state.messages = []
if "provider_used" not in st.session_state:
    st.session_state.provider_used = []

############################### HERO ###########################################@#

# Préparation de ma photo
photo_path = "photo.jpg" 
if os.path.exists(photo_path):
    with open(photo_path, "rb") as image_file:
        encoded_img = base64.b64encode(image_file.read()).decode("utf-8")
    mime_type = "image/png" if photo_path.lower().endswith(".png") else "image/jpeg"
    photo_html = f'<img src="data:{mime_type};base64,{encoded_img}" class="hero-photo" alt="Photo de Badiallo">'
else:
    photo_html = '<div class="hero-photo-placeholder">B</div>'
# Préparation des logos en orbite
tools = [
    {"top": "-30%",  "left": "50%",  "icon": "outils/python.png"},      
    {"top": "5%",    "left": "100%",  "icon": "outils/R.png"},           
    {"top": "33%",   "left": "110%", "icon": "outils/sas.png"},        
    {"top": "64%",   "left": "100%", "icon": "outils/sql.png"},         
    {"top": "45%",   "left": "-30%",  "icon": "outils/databricks.png"},  
    {"top": "15%",  "left": "-22%",  "icon": "outils/stata.jpeg"},       
    {"top": "-15%",   "left": "80%",  "icon": "outils/excel.jpeg"},       
    {"top": "-10%",   "left": "-10%",   "icon": "outils/powerbi.jpeg"},    
    {"top": "-26%",   "left": "20%",   "icon": "outils/git.png"}  
]

# Génération HTML orbite
orbit_html = '<div class="orbit-container">'
orbit_html += f'<div class="center-photo">{photo_html}</div>'

for t in tools:
    # Conversion locale en base64 pour chaque image
    if os.path.exists(t['icon']):
        with open(t['icon'], "rb") as f:
            b64_img = base64.b64encode(f.read()).decode("utf-8")
        # On définit le mime type dynamiquement
        mime = "image/jpeg" if t['icon'].endswith(".jpeg") else "image/png"
        orbit_html += f'''
        <div class="tool-orbite" style="top:{t['top']}; left:{t['left']};">
            <img src="data:{mime};base64,{b64_img}" style="width: 60%; height: auto; object-fit: contain;">
        </div>'''
orbit_html += '</div>'

# Affichage du bandeau
st.markdown(f"""
<div class="hero">
  <div class="hero-grid">
    <div class="hero-left">
      <div class="hero-tag">✦ Portfolio · Data Science · IA · Statistique · Économétrie · Analyse quantitative </div>
      <h1 class="hero-name">Badiallo <span>Kantako</span></h1>
      <p class="hero-sub">{PROFILE['title']}<br>{PROFILE['seeking']}</p>
      <div class="hero-badges">
        <span class="badge">📍 Mobilité partout en France</span>
        <span class="badge"> 📅 Disponibilité à partir de mi-septembre</span>
        <span class="badge">🇲🇱 Bamako → 🇫🇷 France</span>. 
        <span class="badge">Python · R · SQL · SAS · STATA · Excel · Power BI</span>
        <span class="badge">🌍 FR · EN</span>
      </div>
      <div style="display:flex;gap:12px;margin-top:16px;flex-wrap:wrap;">
        <a href="mailto:{PROFILE['email']}" style="font-size:12px;color:#E8D5C0;opacity:0.8;text-decoration:none;">📧 {PROFILE['email']}</a>
        <a href="{PROFILE['linkedin']}" target="_blank" style="font-size:12px;color:#C4704A;text-decoration:none;font-weight:500;">💼 LinkedIn</a>
        <a href="{PROFILE['github']}" target="_blank" style="font-size:12px;color:#C4704A;text-decoration:none;font-weight:500;">💻 GitHub</a>
      </div>
    </div>
    <div class="hero-right">
      {orbit_html}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
 
######################## TABS ##########################
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "👤 Qui suis-je", "🎓 Mon parcours", "💼 Expériences", "📁 Projets", "🛠️ Compétences","🎯 Intérêts & Postes", "🤖 Chatbot"
])


###################### TAB 1 — QUI SUIS-JE ######################
with tab1:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 2], gap="large")

    with col1:
        st.markdown('<div class="section-label">À propos</div>', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">Data Scientist <em>& Économètre</em></h2>', unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:justify;'>{PROFILE['summary']}</p>", unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">🚀 Pourquoi <em>vous êtes au bon endroit ?</em></h2>', unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:justify;'>{POURQUOI_MOI}</p>", unsafe_allow_html=True)

        # Qualités / défauts
        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
        qa1, qa2 = st.columns(2)
        with qa1:
            st.markdown('<div class="section-label">Qualités</div>', unsafe_allow_html=True)
            for q in PROFILE["qualities"]:
                st.markdown(f'<div style="background:white;border:1px solid #E8D5C0;border-left:3px solid #C4704A;padding:8px 14px;margin-bottom:8px;border-radius:2px;font-size:13px;">✦ {q}</div>', unsafe_allow_html=True)
        with qa2:
            st.markdown('<div class="section-label">Axes d\'amélioration</div>', unsafe_allow_html=True)
            for w in PROFILE["weaknesses"]:
                st.markdown(f'<div style="background:white;border:1px solid #E8D5C0;border-left:3px solid #D4A847;padding:8px 14px;margin-bottom:8px;border-radius:2px;font-size:13px;">→ {w}</div>', unsafe_allow_html=True)

        st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="section-label">Formation</div>', unsafe_allow_html=True)
        for year, degree, school, current in [
            ("2025–2026", "Master 2 Économétrie & Statistiques", "TSE · 80% anglais", True),
            ("2024–2025", "Master 1 Économétrie & Statistiques", "Toulouse School of Economics", False),
            ("2023–2024", "Licence 3 Économie ", "Toulouse School of Economics", False),
            ("2021–2023", "Licence 1&2 ", "Université Grenoble Alpes", False),
            ("2020", "BAC Sciences et Technologie de Gestion", "Lycée TechniqueGanga, Mali", False),
        ]:
            brd = "border-left:3px solid #C4704A;" if current else ""
            st.markdown(f"""
            <div style="background:white;border:1px solid #E8D5C0;border-radius:4px;padding:14px 18px;margin-bottom:8px;{brd}">
                <div style="font-size:10px;color:#C4704A;letter-spacing:2px;text-transform:uppercase;font-weight:500;margin-bottom:2px;">{year} {"· EN COURS" if current else ""}</div>
                <div style="font-family:'Cormorant Garamond',serif;font-size:15px;font-weight:600;color:#1A1208;margin-bottom:1px;">{degree}</div>
                <div style="font-size:11px;color:#999;">{school}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-label" style="margin-top:16px;">Distinctions</div>', unsafe_allow_html=True)
        for icon, title, desc in [
            ("🥇", "1ère nationale · Bac technique malien", "Prix d'Assitan N'Fagnanama Koné 2020"),
            ("🏆", "Concours d'Excellence Mali 2021", "Bourse d'études pour la France"),
        ]:
            st.markdown(f'<div class="award"><div style="font-size:24px;margin-bottom:6px;">{icon}</div><div class="award-title">{title}</div><div class="award-desc">{desc}</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Aspirations</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="background:linear-gradient(135deg,#1A1208,#3D2010);border-radius:6px;padding:20px 24px;color:#FAF7F2;font-size:13px;line-height:1.8;font-style:italic;">{PROFILE["aspirations"]}</div>', unsafe_allow_html=True)
        # Contact + LinkedIn
        st.markdown('<div class="section-label" style="margin-top:16px;">Contact & Liens</div>', unsafe_allow_html=True)
        for icon, text, link in [
            ("📧", PROFILE['email'], f"mailto:{PROFILE['email']}"),
            ("📞", PROFILE['phone'], None),
            ("📍", "Toulouse · Nantes", None),
            ("💼", "LinkedIn", PROFILE['linkedin']),
        ]:
            if link:
                st.markdown(f'<div style="font-size:13px;color:#31333F;margin-bottom:8px;">{icon} &nbsp; <a href="{link}" target="_blank" style="color:#C4704A;text-decoration:none;">{text}</a></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="font-size:13px;color:#31333F;margin-bottom:8px;">{icon} &nbsp; {text}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

###################### TAB 2 — PARCOURS ######################

with tab2:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">De Bamako à Nantes</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Mon <em>histoire</em></h2>', unsafe_allow_html=True)

    st.markdown("""
    <div class="journey-map">
      <div style="font-size:10px;letter-spacing:3px;text-transform:uppercase;color:#C4704A;margin-bottom:18px;font-weight:500;">Itinéraire géographique</div>
      <div style="display:flex;align-items:center;flex-wrap:wrap;gap:4px;">
        <div class="journey-city"><span>🇲🇱 Mali</span>Bamako</div><span class="year-badge">2021</span>
        <div class="journey-arrow">→</div>
        <div class="journey-city"><span>🇫🇷</span>Valence</div><span class="year-badge">2023</span>
        <div class="journey-arrow">→</div>
        <div class="journey-city"><span>🇫🇷</span>Toulouse</div><span class="year-badge">2025</span>
        <div class="journey-arrow">→</div>
        <div class="journey-city"><span>⚡ ENGIE</span>Nantes</div><span class="year-badge">2026</span>
        <div class="journey-arrow">→</div>
        <div class="journey-city" style="background:#C4704A;"><span style="color:rgba(255,255,255,0.7);">🚀 2026</span>CDI/GP</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_tl, col_aside = st.columns([3, 2], gap="large")
    
    with col_tl:
        st.markdown('<div class="timeline">', unsafe_allow_html=True)
        for item in JOURNEY:
            dc = "timeline-dot gold" if item.get("gold") else "timeline-dot"
            st.markdown(f"""
            <div class="timeline-item">
                <div class="{dc}"></div>
                <div class="timeline-year">{item['year']}</div>
                <div class="timeline-title">{item['emoji']} {item['title']}</div>
                <div class="timeline-place">📍 {item['place']}</div>
                <div class="timeline-desc">{item['desc']}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_aside:
        st.markdown("""<div style="background:linear-gradient(135deg,#1A1208,#3D2010);border-radius:8px;padding:24px;color:#FAF7F2;margin-top:8px;">
            <div style="font-size:10px;letter-spacing:3px;text-transform:uppercase;color:#C4704A;margin-bottom:16px;">En chiffres</div>""", unsafe_allow_html=True)
        for num, label in [("4", "villes"), ("Des", "mentions"), ("1ère", "nationale Mali"), ("10+", "projets"), ("4+", "expériences")]:
            st.markdown(f"""
            <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:12px;border-bottom:1px solid rgba(255,255,255,0.07);padding-bottom:12px;">
                <div style="font-family:'Cormorant Garamond',serif;font-size:32px;font-weight:300;color:#C4704A;line-height:1;">{num}</div>
                <div style="font-size:12px;color:#E8D5C0;opacity:0.85;">{label}</div>
            </div>""", unsafe_allow_html=True)
        
        # --- AJOUT DU DÉTAIL DES COURS SOUS LA TIMELINE ---
        st.markdown("---")
        st.markdown("<h3 style='color:#C4704A; margin-top: 20px; margin-bottom: 20px; font-family:serif;'>📚 Détail du programme académique</h3>", unsafe_allow_html=True)

        with st.expander("🎓 Master 2 : Statistique, Économétrie (TSE - Alternance)",expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Semestre 3**")
                st.info("- Data Mining\n Survey Sampling\n- Analyse des durées de vie\n- Économétrie du Marketing\n- Économétrie des variables qualitatives\n- Données de Panel\n- Softwares (SAS, R, Python)\n- Anglais")
            with c2:
                st.markdown("**Semestre 4**")
                st.success("- Non-parametric models\n- Geomarketing\n- Scoring\n- Spatial Econometrics\n- Data bases\n - Web mining\n- Graph Analysis\n- Analyse de valeurs extrêmes\n- Rapport d'activité")

        with st.expander("🎓 Master 1 : Statistique, Économétrie (TSE)",expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Semestre 1**")
                st.info("- Probability & Stats for Data Science\n- Software for Data science ( R, Python & SAS )\n- Économétrie approfondie\n- Applied Econometrics\n- Game Theory\n- Options: Markov Chains")
            with c2:
                st.markdown("**Semestre 2**")
                st.success("- Foundations of Machine Learning\n- Time Series\n- Applied Econometrics\n- Évaluation des politiques publiques\n- Option: High Dimensional Data & ML\n-option: Market Finance\n-option: Data Bases ")

        with st.expander("🎓 Licence 3 : Économie (TSE)",expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Semestre 5**")
                st.info("- Microéconomie 5\n- Macro 1\n- Mathématiques\n- Probabilité Statistique\n- APP (Apprentissage par projets)\n- Option: Analyse des données et tests statistiques\n-  Anglais")
            with c2:
                st.markdown("**Semestre 6**")
                st.success("- Économie Industrielle\n- Macro 2\n- Introductory Econometrics\n- Optimisation\n- APP \n- Option: Introduction à la Finance\n- Anglais")

        with st.expander("🎓 Licence 2 : Économie et Gestion (UGA)"):
            c1, c2 = st.columns(2)
            with c1:
                st.info("- **Semestre 3 :** Macroéconomie 1, Microéconomie 1, Monnaie et Finance 1, Comptabilité financière 1, Droit des affaires, Mathématiques 3, Compétences numériques 2, Anglais 2, Russe.")
            with c2:
                st.info("- **Semestre 4 :** Macroéconomie 2, Microéconomie 2, Monnaie et Finance 2, Comptabilité financière 2, Mathématiques appliquées à la gestion, Statistiques inférentielles, Anglais 3, Russe, Géostratégie.")

        with st.expander("🎓 Licence 1 : Économie et Gestion (UGA)"):
            c1, c2 = st.columns(2)
            with c1:
                st.info("- **Semestre 1 :** Analyse économique 1, Questions économiques contemporaines, Histoire des faits économiques et sociaux, Introduction à la gestion d'entreprise 1, Mathématiques 1, Compétences numériques 1, Anglais.")
            with c2:
                st.info("- **Semestre 2 :** Analyse économique 2, Introduction à la macroéconomie, Introduction à la microéconomie, Introduction à la gestion d'entreprise 2, Statistiques descriptives, Mathématiques 2, Anglais 1, Russe, Géostratégie.")
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

######################## TAB 3 — EXPÉRIENCES ##########################
with tab3:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Parcours professionnel</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Mes <em>expériences</em></h2>', unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:justify;'>{INTRO_EXPERIENCES}</p>", unsafe_allow_html=True)

    for exp in EXPERIENCES:
        tags_html = "".join([f'<span class="pill">{t}</span>' for t in exp["tags"]])
        desc_html = exp["desc"].replace("\n","<br>")
        st.markdown(f"""
        <div class="card">
            <div class="card-title">{exp['title']}</div>
            <div class="card-sub">{exp['company']}</div>
            <div class="card-date">📅 {exp['date']}</div>
            <div class="card-desc">{desc_html}</div>
            <div class="pills" style="margin-top:12px;">{tags_html}</div>
        </div>""", unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div class="card"><div class="card-title">Chargée de partenariats</div><div class="card-sub">Cellule pour le Développement du Mali</div><div class="card-desc">Engagée pour le développement socio-économique du Mali.</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card"><div class="card-title"> Trésorière </div><div class="card-sub">SAY it Aloud · TSE · 2024-2025 </div><div class="card-desc">Gestion financière et administrative de l\'association de prise de parole de TSE.</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# #################################### TAB 4 — PROJETS ################################################

# TAB 4 — PROJETS & TRAVAUX
with tab4:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Travaux académiques & professionnels</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Mes <em>projets</em></h2>', unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:justify;'>{INTRO_PROJECTS}</p>", unsafe_allow_html=True)
    # Dossier où se trouvent tes fichiers
    REPORT_DIR = "rapports"

    for i, proj in enumerate(PROJECTS):
        # Génération des tags (pills)
        tools_html = "".join([f'<span class="pill hot">{t}</span>' for t in proj["tools"]])
        
        # Expander pour chaque projet
        with st.expander(f"{'0' if i+1<10 else ''}{i+1} · {proj['title']} — {proj['level']}", expanded=(i<1)):
            
            # Badge "Highlight" 
            highlight_html = f'<div style="background:rgba(196,112,74,0.08);border-left:3px solid #C4704A;padding:10px 14px;border-radius:0 4px 4px 0;font-size:13px;color:#6B3F2A;font-style:italic;margin-bottom:10px;">💡 {proj["highlight"]}</div>'
            
            # Nettoyage de la description (gestion des sauts de ligne)
            desc_html = proj["desc"].replace("\n", "<br>")
            
            st.markdown(f"""
            <div style="padding:4px 0;">
                {highlight_html}
                <div class="card-desc" style="margin-bottom:15px; text-align:justify;">{desc_html}</div>
                <div style="font-size:13px; color:#C4704A; font-weight:600; margin-bottom:12px;">📊 Résultat : {proj['result']}</div>
                <div class="pills" style="margin-bottom:20px;">{tools_html}</div>
            </div>""", unsafe_allow_html=True)

            # --- GESTION DU RAPPORT PDF ---
            filename = proj.get("report_file")
            if filename:
                filepath = os.path.join(REPORT_DIR, filename)
                
                if os.path.exists(filepath):
                    c1, c2 = st.columns(2)
                    with c1:
                        # Bouton de téléchargement natif
                        with open(filepath, "rb") as f:
                            st.download_button(
                                label="📥 Télécharger le PDF",
                                data=f,
                                file_name=filename,
                                mime="application/pdf",
                                key=f"dl_{i}",
                                use_container_width=True
                            )
                    with c2:
                        # Bouton pour afficher le PDF dans la page
                        if st.button("👁️ Visualiser en ligne", key=f"btn_{i}", use_container_width=True):
                            st.markdown("---")
                            display_pdf(filepath)
                else:
                    st.caption(f"ℹ️ Le fichier '{filename}' est introuvable dans le dossier /rapports.")
            else:
                st.caption("🔒 Rapport confidentiel ou non disponible.")

    st.markdown('</div>', unsafe_allow_html=True)
    
################################# TAB 5 — COMPÉTENCES ##########################################

with tab5:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Outils & savoir-faire</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Mes <em>compétences</em></h2>', unsafe_allow_html=True)

    # Radar chart
    categories = ["Python/R", "Machine Learning", "Économétrie", "BI/Dataviz", "Recherche", "Data & IA"]
    values = [90, 95, 95, 90, 90, 95]
    fig_radar = go.Figure(go.Scatterpolar(
        r=values + [values[0]], theta=categories + [categories[0]],
        fill='toself', fillcolor='rgba(196,112,74,0.15)',
        line=dict(color='#C4704A', width=2),
        marker=dict(color='#C4704A', size=6)
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0,100],tickfont=dict(size=8, color="#E8D5C0"), tickfont_size=8, gridcolor="#021615"),
                   angularaxis=dict(tickfont_size=11,tickfont=dict(size=11, color="#624005"))),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=20,b=20,l=40,r=40), height=300,
        showlegend=False
    )
    col_r1, col_r2 = st.columns([1, 2], gap="large")
    with col_r1:
        st.plotly_chart(fig_radar, use_container_width=True)
    with col_r2:
        col_s1, col_s2 = st.columns(2)
        skill_items = list(SKILLS_DETAILED.items())
        for i, (group, skills) in enumerate(skill_items):
            col = col_s1 if i % 2 == 0 else col_s2
            with col:
                st.markdown(f'<div style="font-size:10px;letter-spacing:3px;text-transform:uppercase;color:#6B3F2A;font-weight:500;margin-bottom:12px;padding-bottom:6px;border-bottom:1px solid #E8D5C0;">{group}</div>', unsafe_allow_html=True)
                for skill, level in skills:
                    # Génération des points (4/5 donne ●●●●○)
                    dots = '<span style="color:#C4704A;">' + '●' * level + '</span>' + '<span style="color:#E8D5C0;">' + '●' * (5 - level) + '</span>'
                    st.markdown(f"""
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;font-size:13px;color:#1A1208;">
                        <span>{skill}</span>
                        <span style="font-size:10px;letter-spacing:2px;">{dots}</span>
                    </div>""", unsafe_allow_html=True)
                st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    # Langues
    st.markdown('<div class="section-label" style="margin-top:8px;">Langues</div>', unsafe_allow_html=True)
    lc1, lc2, lc3 = st.columns(3)
    for lang, flag, level, pct, col in [
        ("Français", "🇫🇷", "Natif", 100, lc1),
        ("Anglais", "🇬🇧", "B2 - 80% cours TSE", 70, lc2),
        ("Bambara", "🇲🇱", "Langue maternelle", 100, lc3),
    ]:
        with col:
            st.markdown(f"""
            <div style="background:white;border:1px solid #E8D5C0;padding:18px;border-radius:4px;text-align:center;">
                <div style="font-size:32px;margin-bottom:6px;">{flag}</div>
                <div style="font-family:'Cormorant Garamond',serif;font-size:17px;color:#1A1208;">{lang}</div>
                <div style="font-size:11px;color:#C4704A;margin-top:3px;">{level}</div>
                <div style="background:#F2EBE3;border-radius:2px;height:4px;margin-top:8px;">
                    <div style="background:#C4704A;height:4px;border-radius:2px;width:{pct}%"></div>
                </div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 6 — INTÉRÊTS & POSTES
with tab6:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Ma formation ouvre les portes vers</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Postes <em>ciblés</em></h2>', unsafe_allow_html=True)

    jc1, jc2 = st.columns(2)
    for i, job in enumerate(JOBS):
        with (jc1 if i % 2 == 0 else jc2):
            st.markdown(f"""
            <div class="job-card" style="padding:24px; height:100%;">
                <div class="job-icon" style="font-size:32px; margin-bottom:12px;">{job["icon"]}</div>
                <div>
                    <div class="job-title" style="font-size:19px; margin-bottom:8px;">{job["title"]}</div>
                    <div style="font-size:11px; color:#C4704A; font-weight:600; text-transform:uppercase; letter-spacing:1px; margin-bottom:4px;">{job["match"]}</div>
                    <div class="job-desc" style="font-size:13px; line-height:1.6;">{job["desc"]}</div>
                </div>
            </div>""", unsafe_allow_html=True)

    # Centres d'intérêt
    st.markdown('<div style="height:32px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Au-delà du travail</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Centres <em>d\'intérêt</em></h2>', unsafe_allow_html=True)
    ic = st.columns(3)
    for i, interest in enumerate(INTERESTS):
        with ic[i % 3]:
            st.markdown(f"""
            <div class="interest-card" style="margin-bottom:12px;">
                <div class="interest-icon">{interest['icon']}</div>
                <div class="interest-title">{interest['title']}</div>
                <div class="interest-desc">{interest['desc']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style="background:linear-gradient(135deg,#1A1208,#3D2010);border-radius:8px;padding:36px;text-align:center;margin-top:28px;color:#FAF7F2;">
        <div style="font-size:10px;letter-spacing:3px;text-transform:uppercase;color:#C4704A;margin-bottom:14px;">Ma philosophie</div>
        <div style="font-family:'Cormorant Garamond',serif;font-size:26px;font-weight:300;font-style:italic;line-height:1.5;max-width:580px;margin:0 auto;">
                "When you want something, give yourself the means to achieve it. Courage and self-belief always pay off. Keep going, and finish what you start."
        </div>
        <div style="font-size:12px;color:#E8D5C0;opacity:0.7;margin-top:14px;">— Badiallo Kantako</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
#"La curiosité est le moteur de l'apprentissage, la rigueur est la clé de l'excellence, et l'humilité est la porte de la sagesse."
############################### TAB 7 — CHATBOT (multi-provider avec fallback) #################################
with tab7:
    st.markdown('<div class="section" id="chatbot">', unsafe_allow_html=True)
    col_chat, col_info = st.columns([3, 2], gap="large")

    with col_chat:
        st.markdown('<div class="section-label">Assistant IA · Multi-provider</div>', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">Posez vos <em>questions</em></h2>', unsafe_allow_html=True)

        st.markdown("""
        <div class="chat-wrap">
            <div class="chat-head">
                <div class="chat-avatar">K</div>
                <div>
                    <div style="font-family:'Cormorant Garamond',serif;font-size:19px;color:#FAF7F2;">Kanty · Assistant IA</div>
                    <div style="font-size:11px;color:#E8D5C0;opacity:0.75;">Gemini 2.5 Flash → owl-alpha → Llama 3.3 70B → Meta-Llama-3-8B → gpt-oss-120b · FR & EN</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        # ---------- INITIALISATION DES COMPTEURS (CAPTCHA) ----------
        if "msg_count" not in st.session_state:
            st.session_state.msg_count = 0
        if "captcha_ok" not in st.session_state:
            st.session_state.captcha_ok = False
        
        # Variable pour capturer l'entrée 
        if "question_finale" not in st.session_state:
            st.session_state.question_finale = None

        # AFFICHAGE DES MESSAGES
        if not st.session_state.messages:
            st.markdown("""
            <div class="msg-bot" style="margin-top:10px;">
                👋 Bonjour ! Je suis <strong>Kanty</strong>, l'assistant virtuel de <strong>Badiallo Kantako</strong>.<br>
                Je suis prêt à répondre à toutes vos questions professionnelles !<br>
                <em>I also answer in English 🇬🇧</em>
            </div>""", unsafe_allow_html=True)
        else:
            for idx, msg in enumerate(st.session_state.messages):
                css = "msg-user" if msg["role"] == "user" else "msg-bot"
                content = markdown.markdown(msg["content"] or "")
                content = content.replace("<p>", "").replace("</p>", "").replace("\n", "<br>")
                #content = (msg["content"] or "").replace("\n", "<br>")
                provider = ""
                if msg["role"] == "assistant" and idx//2 < len(st.session_state.provider_used):
                    provider = f'<div class="provider-badge">via {st.session_state.provider_used[idx//2]}</div>'
                st.markdown(f'<div class="{css}">{provider}{content}</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        #  ZONE DE SAISIE & SUGGESTIONS AVEC GESTION CAPTCHA
        SEUIL = 3 
        
        if st.session_state.msg_count >= SEUIL and not st.session_state.captcha_ok:
            st.error("🔒 Vérification anti-robot (après 3 messages) : Combien font 1+1 ?")
            captcha_answer = st.text_input("Votre réponse", key="captcha_answer", placeholder="Entrez le nombre")
            if st.button("Vérifier", key="verify_btn"):
                if captcha_answer.strip() == "2":
                    st.session_state.captcha_ok = True
                    st.success("✅ Vérification réussie ! Vous pouvez continuer.")
                    st.rerun()
                else:
                    st.error("❌ Mauvaise réponse. Réessayez.")
        else:
            
            user_input = st.text_input(
                "", 
                placeholder="Ex: Quelles sont ses compétences ? / What projects has she done?", 
                label_visibility="collapsed", 
                key="chat_input",
                on_change=handle_enter
            )
            
            cb1, cb2 = st.columns([1.5,4.5], gap="small")
            with cb1:
                send = st.button("Envoyer ✦", use_container_width=True)
                if send and user_input.strip():
                    st.session_state.question_finale = user_input.strip()

            # Les boutons de suggestions 
            st.markdown('<div class="section-label" style="margin-top:20px;">Questions suggérées</div>', unsafe_allow_html=True)
            suggestions = [
                "Qui est Badiallo Kantako ?",
                "Pourquoi choisir Badiallo pour un poste en data science ?",
                "Pourquoi choisir Badiallo pour un poste en analyse quantitative ?",
                "What are her Machine Learning and Deep Learning skills?",
                "What kind of position is she looking for?",
                "What projects has she done?"
            ] 
            
            
            sc1, sc2 = st.columns(2)
            for i, s in enumerate(suggestions):
                with (sc1 if i%2==0 else sc2):
                    if st.button(s, key=f"sug_{i}", use_container_width=True):
                        st.session_state.question_finale = s

            # 3. L'Entonnoir : Si une question est posée (via input ou suggestions), elle est traitée ici
            if st.session_state.question_finale:
                question_active = st.session_state.question_finale
                st.session_state.question_finale = None # Reset immédiat
                #st.session_state.question_finale = user_input.strip()

                if contains_forbidden_words(question_active):
                    try: ip = requests.get("https://api.ipify.org").text
                    except: ip = "Indisponible"
                    send_alert_email(question_active, ip)
                    # Réponse à la question hors contexte selon mes consignes
                    st.session_state.messages.append({"role": "user", "content": question_active})
                    with st.spinner("Réflexion en cours..."):
                        reply, provider_name = chat_with_fallback(
                            [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                            CHATBOT_CONTEXT
                        )
                        reply = reply or "Désolé, une erreur technique est survenue."
                    st.session_state.messages.append({"role": "assistant", "content": reply or "⚠️ Réponse vide."})
                    st.session_state.provider_used.append(provider_name)
                    st.session_state.msg_count += 1 
                    st.markdown("""
                        <div style="
                            background-color: #ffeeba; 
                            color: #000000; 
                            padding: 15px; 
                            border-radius: 5px; 
                            border-left: 5px solid #ffc107;
                            font-weight: 500;
                            margin-bottom: 20px;
                        ">
                            ⚠️ Veuillez rester professionnel dans vos échanges.
                        </div>
                    """, unsafe_allow_html=True)
                    st.rerun()
                else:
                    st.session_state.messages.append({"role": "user", "content": question_active})
                    with st.spinner("Réflexion en cours..."):
                        reply, provider_name = chat_with_fallback(
                            [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                            CHATBOT_CONTEXT
                        )
                        reply = reply or "Désolé, une erreur technique est survenue."
                    st.session_state.messages.append({"role": "assistant", "content": reply or "⚠️ Réponse vide."})
                    st.session_state.provider_used.append(provider_name)
                    st.session_state.msg_count += 1
                    st.rerun()

        # l'historique
        if st.session_state.messages:
            if st.button("🗑️ Effacer l'historique"):
                st.session_state.messages = []
                st.session_state.provider_used = []
                st.session_state.msg_count = 0 
                st.session_state.captcha_ok = False 
                st.rerun()

    # COLONNE DROITE
    with col_info:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#1A1208,#3D2010);border-radius:8px;padding:28px;color:#FAF7F2;">
            <div style="font-size:10px;letter-spacing:3px;text-transform:uppercase;color:#C4704A;margin-bottom:14px;">Système Multi-IA</div>
            <div style="font-family:'Cormorant Garamond',serif;font-size:20px;font-weight:300;margin-bottom:18px;line-height:1.3;">
                5 providers<br><em style="color:#C4704A;">en cascade</em>
            </div>
        """, unsafe_allow_html=True)
        for num, name, desc in [
            ("1", "Gemini 2.5 Flash", "Priorité — Google AI avec le modèle Gemini 2.5 Flash"),
            ("2", "owl-alpha", "Via OpenRouter avec le modèle owl-alpha si Gemini indispo"),
            ("3", "Llama 3.3 70B", "Via Groq avec le modèle Llama 3.3 70B si owl-alpha indispo"),
            ("4", "Meta-Llama-3-8B", "Via Hugging Face avec le modèle Meta-Llama-3-8B si Llama 3.3 70B indispo"),
            ("5", "gpt-oss-120b", "Via Cerebras avec le modèle gpt-oss-120b si dernier recours"),
        ]:
            st.markdown(f"""
            <div style="display:flex;gap:12px;align-items:flex-start;margin-bottom:12px;">
                <div style="background:rgba(196,112,74,0.3);color:#C4704A;font-size:11px;font-weight:700;padding:3px 7px;border-radius:2px;flex-shrink:0;">{num}</div>
                <div>
                    <div style="font-size:13px;color:#FAF7F2;font-weight:500;">{name}</div>
                    <div style="font-size:11px;color:#C4704A;opacity:0.75;">{desc}</div>
                </div>
            </div>""", unsafe_allow_html=True)
        st.markdown("""
            <div style="border-top:1px solid rgba(255,255,255,0.08);padding-top:14px;margin-top:6px;">
                <div style="font-size:11px;color:#C4704A;margin-bottom:10px;">L'assistant répond sur :</div>
        """, unsafe_allow_html=True)
        for t in ["🎓 Formation & diplômes", "💼 Expériences", "🛠️ Compétences", "📁 Projets", "🎯 Postes visés", "💡 Pourquoi m'embaucher ?", 
        "📅 Disponibilités"]:
            st.markdown(f'<div style="font-size:11px;color:#31333F;margin-bottom:6px;opacity:0.85;">✦ {t}</div>', unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)
        # # Status des providers afin de vérifier que mes clés sont bien disponible
        # st.markdown('<div class="section-label" style="margin-top:16px;">Status des clés API</div>', unsafe_allow_html=True)
        # for name, key in [("Google API", GEMINI_KEY), ("OpenRouter API", OPENROUTER_KEY),("Groq API", GROQ_KEY),("Hugging Face API", HUGGING_FACE_KEY),("Cerebras API", CEREBRAS_KEY)]:
        #     ok = "✅" if key else "❌"
        #     st.markdown(f'<div style="font-size:12px;color:#31333F;margin-bottom:6px;">{ok} {name} {"· configuré" if key else "· manquant"}</div>', unsafe_allow_html=True)


    # FORMULAIRE DE CONTACT (avec envoi d'email via SMTP)
    st.markdown("---")

    st.markdown("""
    <div class="chat-wrap">
        <div class="chat-head">
            <div class="chat-avatar">M</div>
            <div>
                <div style="font-family:'Cormorant Garamond',serif;font-size:30px;color:#FAF7F2;"> 💬 Un mot, un message ?</div>
                <div style="font-size:11px;color:#E8D5C0;opacity:0.75;"> </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <p style="color: #6B3F2A; font-size: 16px; margin-bottom: 16px;">Un conseil, une suggestion d'amélioration, ou juste un retour sur ce portfolio ? N'hésitez pas à m'écrire, je suis toujours preneuse de retours constructifs !</p>""",
        unsafe_allow_html=True
    )
    st.markdown('<div class="contact-form">', unsafe_allow_html=True)
    with st.form(key="contact_form", clear_on_submit=True):
        st.markdown('<p style="color:#6B3F2A; font-size:16px; margin-bottom: 2px;">Votre nom (optionnel)</p>', unsafe_allow_html=True)
        name = st.text_input("nom_input", placeholder="ex: Badiallo Kantako", label_visibility="collapsed")
        st.markdown('<p style="color:#6B3F2A; font-size:16px; margin-bottom: 2px; margin-top: 10px;">Votre message</p>', unsafe_allow_html=True)
        message = st.text_area("message_input", height=120, placeholder="Écrivez ici... (n'hésitez pas à mettre votre email pour que je puisse vous répondre)", label_visibility="collapsed")
        submitted = st.form_submit_button("Envoyer 📩 🚀", use_container_width=True)

        if submitted:
            if not message.strip():
                st.warning("✏️ Écris un message avant d'envoyer.", icon="⚠️")
            else:
                # Récupération des secrets
                SMTP_SERVER = st.secrets["SMTP_SERVER"]
                SMTP_PORT = st.secrets["SMTP_PORT"]
                SMTP_EMAIL = st.secrets["SMTP_EMAIL"]
                SMTP_PASSWORD = st.secrets["SMTP_PASSWORD"]
                RECIPIENT_EMAIL = st.secrets["RECIPIENT_EMAIL"]

                email_msg = EmailMessage()
                email_msg["From"] = SMTP_EMAIL
                email_msg["To"] = RECIPIENT_EMAIL
                email_msg["Subject"] = f"📩 💼 Nouveau message depuis ton portfolio"
                text_fallback = f"Bonjour Badiallo, {name} t'a envoyé un message : {message}"
                email_msg.set_content(text_fallback)
                html_body = f"""
                <div style="font-family: sans-serif; line-height: 1.6; color: #333; max-width: 600px; padding: 20px; border: 1px solid #C4704A; border-radius: 10px;">
                    <h2 style="color: #C4704A;">👋 Bonjour Badiallo,</h2>
                    <p>Quelqu'un vient de visiter ton portfolio et a laissé un message :</p>
                    <div style="background-color: #f9f9f9; padding: 15px; border-left: 5px solid #C4704A;">
                        <p><b>{name if name else 'Un visiteur'}</b> : <i>"{message}"</i></p>
                    </div>
                    <p>Passe une excellente journée ! 🚀</p>
                </div>
                """
                email_msg.add_alternative(html_body, subtype="html")

                try:
                    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                        server.starttls()
                        server.login(SMTP_EMAIL, SMTP_PASSWORD)
                        server.send_message(email_msg)
                    st.success("✅ Message envoyé !", icon="🎉")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Erreur technique. Merci d'écrire directement à {RECIPIENT_EMAIL}.", icon="📧")
                    print(f"SMTP error: {e}")
        
    
    st.markdown('</div>', unsafe_allow_html=True)
display_floating_chat_invite()