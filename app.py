import streamlit as st
import urllib.parse

# 1. CONFIGURATION
st.set_page_config(
    page_title="CHIC Graphic & Print",
    page_icon="🎨",
    layout="wide",
)

# 2. DESIGN PERSONNALISÉ (Inspiré de tes blocs de stats)
st.markdown("""
    <style>
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="stToolbar"] {display: none;}
    
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;700&display=swap');

    :root {
        --dark-blue: #0C4A6E;
        --accent: #38BDF8;
        --soft-blue: #E0F2FE;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #ffffff;
    }

    /* MENU STYLE STATS */
    div.stButton > button {
        background-color: var(--soft-blue) !important;
        color: var(--dark-blue) !important;
        border: 2px solid transparent !important;
        border-radius: 12px !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 800 !important;
        width: 100% !important;
        height: 50px !important;
        transition: 0.3s !important;
    }

    div.stButton > button:hover {
        border-color: var(--accent) !important;
        background-color: white !important;
    }

    /* SECTIONS */
    .hero-container {
        background: linear-gradient(135deg, #0C4A6E 0%, #0369A1 100%);
        border-radius: 30px;
        padding: 50px 40px;
        color: white;
        margin-bottom: 30px;
    }
    
    .card {
        background: var(--soft-blue);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #bae6fd;
        margin-bottom: 20px;
        height: 100%;
    }

    .stat-card {
        background: var(--soft-blue);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #bae6fd;
    }
    .stat-val { font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 800; color: var(--dark-blue); display: block; }
    </style>
""", unsafe_allow_html=True)

# 3. NAVIGATION (Logique de changement de page)
if 'current_page' not in st.session_state:
    st.session_state.current_page = "ACCUEIL"

st.markdown("<h1 style='font-family:Syne; text-align:center; color:#0C4A6E; margin-bottom:20px;'>CHIC GRAPHIC & PRINT</h1>", unsafe_allow_html=True)

# Barre de navigation
m1, m2, m3, m4, m5 = st.columns(5)
with m1: 
    if st.button("🏠 ACCUEIL"): st.session_state.current_page = "ACCUEIL"
with m2: 
    if st.button("⚙️ SERVICES"): st.session_state.current_page = "SERVICES"
with m3: 
    if st.button("📸 PROJETS"): st.session_state.current_page = "PROJETS"
with m4: 
    if st.button("📅 DEVIS"): st.session_state.current_page = "DEVIS"
with m5: 
    if st.button("✉️ CONTACT"): st.session_state.current_page = "CONTACT"

st.markdown("---")

# 4. AFFICHAGE DES SECTIONS (Toutes sont maintenant connectées)
page = st.session_state.current_page

if page == "ACCUEIL":
    st.markdown("""
        <div class="hero-container">
            <h1 style='font-family:Syne; font-size: clamp(2rem, 5vw, 3.5rem); color:white;'>L'audace visuelle<br>au service de votre marque.</h1>
            <p style='font-size:1.2rem; opacity:0.9;'>Impression et Design Premium à Dakar.</p>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown("<div class='stat-card'><span class='stat-val'>100%</span>Qualité</div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='stat-card'><span class='stat-val'>24h</span>Livraison</div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='stat-card'><span class='stat-val'>PRO</span>Design</div>", unsafe_allow_html=True)
    with c4: st.markdown("<div class='stat-card'><span class='stat-val'>DKR</span>Sénégal</div>", unsafe_allow_html=True)

elif page == "SERVICES":
    st.markdown("<h2 style='font-family:Syne; color:#0C4A6E;'>Nos Services</h2>", unsafe_allow_html=True)
    s1, s2 = st.columns(2)
    with s1:
        st.markdown('<div class="card"><h3>🎨 Branding</h3><p>Création de logos et chartes graphiques pour une identité forte.</p></div>', unsafe_allow_html=True)
        st.write("")
        st.markdown('<div class="card"><h3>📦 Packaging</h3><p>Design d\'emballages qui font vendre vos produits.</p></div>', unsafe_allow_html=True)
    with s2:
        st.markdown('<div class="card"><h3>🖨️ Print</h3><p>Impression haute qualité : flyers, cartes de visite, brochures.</p></div>', unsafe_allow_html=True)
        st.write("")
        st.markdown('<div class="card"><h3>🏢 Signalétique</h3><p>Habillage de vitrines, enseignes et stands d\'exposition.</p></div>', unsafe_allow_html=True)

elif page == "PROJETS":
    st.markdown("<h2 style='font-family:Syne; color:#0C4A6E;'>Réalisations</h2>", unsafe_allow_html=True)
    photos = ["photo10.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg", "photo5.jpg", "photo6.jpg", "photo7.jpg", "photo8.jpg", "photo9.jpg"]
    cols = st.columns(3)
    for i, p in enumerate(photos):
        cols[i % 3].image(p, use_container_width=True)

elif page == "DEVIS":
    st.markdown("<h2 style='font-family:Syne; color:#0C4A6E;'>Devis Express</h2>", unsafe_allow_html=True)
    with st.form("devis_form"):
        nom = st.text_input("Votre Nom / Entreprise")
        service = st.multiselect("Service souhaité", ["Logo", "Flyer", "Packaging", "Enseigne"])
        details = st.text_area("Détails du projet")
        if st.form_submit_button("🚀 Envoyer la demande"):
            msg = f"Bonjour CHIC G&P, je souhaite un devis pour {', '.join(service)}. Projet : {nom}."
            link = f"https://wa.me/221778615900?text={urllib.parse.quote(msg)}"
            st.markdown(f'<a href="{link}" target="_blank" style="background:#25D366; color:white; padding:15px; border-radius:10px; display:block; text-align:center; text-decoration:none; font-weight:bold;">VALIDER SUR WHATSAPP</a>', unsafe_allow_html=True)

elif page == "CONTACT":
    st.markdown("<h2 style='font-family:Syne; color:#0C4A6E;'>Contactez-nous</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div class="card">
            <h3>📍 Localisation</h3>
            <p>Dakar, Sénégal</p>
            <h3>📞 Téléphone</h3>
            <p>+221 77 861 59 00</p>
            <h3>📧 Email</h3>
            <p>contact@chic-graphic.sn</p>
            <h3>🕒 Horaires</h3>
            <p>Lundi - Samedi : 09h00 - 19h00</p>
        </div>
    """, unsafe_allow_html=True)
