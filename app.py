import streamlit as st
import urllib.parse

# 1. CONFIGURATION
st.set_page_config(
    page_title="CHIC Graphic & Print",
    page_icon="🎨",
    layout="wide",
)

# 2. DESIGN PERSONNALISÉ (Sans Sidebar)
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

    /* BARRE DE NAVIGATION FIXE HAUT */
    .nav-wrapper {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background: white;
        z-index: 1000;
        padding: 10px 0;
        border-bottom: 2px solid var(--soft-blue);
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    /* Style pour transformer les boutons radio en menu horizontal chic */
    div[data-testid="stHorizontalBlock"] {
        background: var(--dark-blue);
        padding: 10px;
        border-radius: 15px;
        margin-bottom: 30px;
    }

    /* BOUTONS STYLE "STATS" (24H LIVRAISON) */
    div.stButton > button {
        background-color: var(--soft-blue) !important;
        color: var(--dark-blue) !important;
        border: 2px solid transparent !important;
        border-radius: 12px !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 800 !important;
        transition: 0.3s !important;
        width: 100% !important;
        height: 50px !important;
    }

    div.stButton > button:hover {
        border-color: var(--accent) !important;
        background-color: white !important;
        transform: translateY(-3px);
    }

    /* SECTION HERO */
    .hero-container {
        margin-top: 20px;
        background: linear-gradient(135deg, #0C4A6E 0%, #0369A1 100%);
        border-radius: 30px;
        padding: 60px 40px;
        color: white;
        text-align: left;
    }
    
    .hero-container h1 {
        font-family: 'Syne', sans-serif;
        font-size: clamp(2rem, 6vw, 3.8rem);
        line-height: 1.1;
        margin-bottom: 20px;
    }

    /* STATS BOXES */
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

# 3. NAVIGATION (Alternative à la sidebar)
# On crée un menu horizontal qui reste toujours propre
st.markdown("<h2 style='font-family:Syne; text-align:center; color:#0C4A6E;'>CHIC GRAPHIC & PRINT</h2>", unsafe_allow_html=True)

if 'current_page' not in st.session_state:
    st.session_state.current_page = "ACCUEIL"

# Création des colonnes pour le menu (s'adapte au mobile)
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

# 4. AFFICHAGE DES PAGES
page = st.session_state.current_page

if page == "ACCUEIL":
    st.markdown("""
        <div class="hero-container">
            <h1>L'audace visuelle<br>au service de votre marque.</h1>
            <p style='font-size:1.2rem; opacity:0.9;'>Impression et Design Premium à Dakar.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown("<div class='stat-card'><span class='stat-val'>100%</span>Qualité</div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='stat-card'><span class='stat-val'>24h</span>Livraison</div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='stat-card'><span class='stat-val'>PRO</span>Design</div>", unsafe_allow_html=True)
    with c4: st.markdown("<div class='stat-card'><span class='stat-val'>DKR</span>Sénégal</div>", unsafe_allow_html=True)

elif page == "PROJETS":
    st.markdown("<h2 style='font-family:Syne;'>Nos Réalisations</h2>", unsafe_allow_html=True)
    photos = ["photo10.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg", "photo5.jpg", "photo6.jpg", "photo7.jpg", "photo8.jpg", "photo9.jpg"]
    cols = st.columns(3)
    for i, p in enumerate(photos):
        cols[i % 3].image(p, use_container_width=True)

elif page == "DEVIS":
    st.markdown("<h2 style='font-family:Syne;'>Devis Express</h2>", unsafe_allow_html=True)
    with st.form("wa_form"):
        nom = st.text_input("Entreprise / Projet")
        besoin = st.multiselect("Services", ["Logo", "Flyers", "Packaging", "Enseigne"])
        if st.form_submit_button("🚀 Valider"):
            msg = f"Bonjour CHIC G&P, devis pour {nom}."
            st.markdown(f'<a href="https://wa.me/221778615900?text={urllib.parse.quote(msg)}" style="background:#25D366; color:white; padding:15px; border-radius:10px; display:block; text-align:center; text-decoration:none; font-weight:bold;">ENVOYER SUR WHATSAPP</a>', unsafe_allow_html=True)
