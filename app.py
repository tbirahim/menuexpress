import streamlit as st
import urllib.parse

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="CHIC Graphic & Print",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded", # Essaye de forcer l'ouverture
)

# 2. STYLE CSS (Correction Mobile + Formulaire)
st.markdown("""
    <style>
    /* Force le mode clair */
    .stApp { background-color: white !important; color: #0C4A6E !important; }

    /* RENDRE LE BOUTON MENU (LES 3 TRAITS) TRÈS VISIBLE SUR MOBILE */
    button[kind="headerNoPadding"] {
        background-color: #38BDF8 !important;
        color: white !important;
        border-radius: 50% !important;
        width: 45px !important;
        height: 45px !important;
        position: fixed !important;
        top: 10px !important;
        left: 10px !important;
        z-index: 1000001 !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2) !important;
    }

    /* Style de la barre latérale */
    [data-testid="stSidebar"] {
        background-color: #0C4A6E !important;
        border-right: 5px solid #38BDF8;
    }
    [data-testid="stSidebar"] * { color: white !important; }

    /* Correction des champs de texte pour qu'ils soient visibles sur mobile */
    .stTextInput input, .stTextArea textarea, .stMultiSelect div {
        background-color: #F0F9FF !important;
        color: #0C4A6E !important;
        border: 2px solid #E0F2FE !important;
        border-radius: 10px !important;
    }

    /* Design des blocs */
    .hero {
        background: linear-gradient(135deg, #0C4A6E 0%, #0369A1 100%);
        color: white !important;
        border-radius: 25px;
        padding: 30px;
        margin-bottom: 20px;
    }

    .stat-box {
        background: #E0F2FE;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border: 1px solid #bae6fd;
        margin-bottom: 15px;
    }
    
    .wa-button {
        background-color: #25D366;
        color: white !important;
        padding: 15px;
        border-radius: 12px;
        text-decoration: none;
        font-weight: 700;
        display: block;
        text-align: center;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. BARRE LATÉRALE
with st.sidebar:
    st.markdown("<h1 style='text-align:center;'>CHIC</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#38BDF8; font-weight:700;'>GRAPHIC & PRINT</p>", unsafe_allow_html=True)
    st.write("---")
    menu = st.radio("MENU", ["🏠 ACCUEIL", "⚙️ SERVICES", "📸 RÉALISATIONS", "📅 DEVIS EXPRESS", "✉️ CONTACT"])

# 4. CONTENU
if menu == "🏠 ACCUEIL":
    st.markdown('<div class="hero"><h1>L\'audace visuelle<br>au service de votre marque.</h1><p>Impression & Design Haut de Gamme.</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.markdown("<div class='stat-box'><h2 style='color:#0C4A6E;'>100%</h2><b>Qualité</b></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='stat-box'><h2 style='color:#0C4A6E;'>24h</h2><b>Livraison</b></div>", unsafe_allow_html=True)

elif menu == "📅 DEVIS EXPRESS":
    st.markdown("<h2 style='color:#0C4A6E; font-family:Syne;'>Demander un devis</h2>", unsafe_allow_html=True)
    
    # Formulaire complet avec plusieurs champs
    with st.form("form_devis"):
        nom = st.text_input("Nom de votre entreprise / Projet")
        services = st.multiselect("Quels services vous intéressent ?", 
                                ["Logo & Branding", "Flyers / Cartes", "Packaging", "Signalétique", "Autre"])
        details = st.text_area("Décrivez votre besoin (quantité, dimensions...)")
        
        # Le bouton de validation
        submitted = st.form_submit_button("🚀 Préparer mon message WhatsApp")
        
        if submitted:
            if nom and services:
                texte = f"Bonjour CHIC G&P, je souhaite un devis pour : {', '.join(services)}. \nProjet : {nom}. \nDétails : {details}"
                lien_wa = f"https://wa.me/221778615900?text={urllib.parse.quote(texte)}"
                st.markdown(f'<a href="{lien_wa}" target="_blank" class="wa-button">CLIQUEZ ICI POUR ENVOYER SUR WHATSAPP</a>', unsafe_allow_html=True)
            else:
                st.error("Veuillez remplir au moins le nom et un service.")

# ... (Garder les autres sections SERVICES, REALISATIONS et CONTACT comme avant)
