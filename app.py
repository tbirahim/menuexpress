import streamlit as st
import urllib.parse

# 1. CONFIGURATION STRICTE
st.set_page_config(
    page_title="CHIC Graphic & Print",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded", # On demande à Streamlit de l'ouvrir d'office
)

# 2. CSS "FORCE BRUTE" POUR LA BARRE LATÉRALE ET LE NETTOYAGE
st.markdown("""
    <style>
    /* --- 1. CACHER LES LOGOS GITHUB ET MENU STREAMLIT --- */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    div[data-testid="stToolbar"] {display: none !important;}
    div[data-testid="stDecoration"] {display: none !important;}

    /* --- 2. FORCER LE BOUTON DE LA BARRE LATÉRALE SUR MOBILE --- */
    /* Ce code rend le bouton (les 3 traits) très gros et bleu sur ton téléphone */
    button[kind="headerNoPadding"] {
        display: flex !important;
        background-color: #38BDF8 !important; /* Bleu clair CHIC */
        color: white !important;
        border-radius: 50% !important;
        width: 60px !important;
        height: 60px !important;
        position: fixed !important;
        top: 15px !important;
        left: 15px !important;
        z-index: 9999999 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important;
    }
    
    /* Icône à l'intérieur du bouton */
    button[kind="headerNoPadding"] svg {
        width: 30px !important;
        height: 30px !important;
        fill: white !important;
    }

    /* --- 3. DESIGN DE LA BARRE LATÉRALE --- */
    [data-testid="stSidebar"] {
        background-color: #0C4A6E !important; /* Bleu foncé */
        border-right: 5px solid #38BDF8 !important;
        z-index: 1000000 !important;
    }
    
    /* Force le texte en blanc dans la barre */
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* --- 4. FIX POUR LE MODE CLAIR --- */
    .stApp {
        background-color: white !important;
        color: #0C4A6E !important;
    }

    /* Style des blocs Accueil */
    .hero {
        background: linear-gradient(135deg, #0C4A6E 0%, #0369A1 100%);
        border-radius: 25px;
        padding: 40px;
        color: white !important;
        margin-top: 50px; /* Espace pour le bouton menu */
    }
    </style>
""", unsafe_allow_html=True)

# 3. CONTENU DE LA BARRE LATÉRALE
with st.sidebar:
    st.markdown("<h1 style='text-align:center; font-family:Syne; color:white;'>CHIC</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#38BDF8; font-weight:700;'>GRAPHIC & PRINT</p>", unsafe_allow_html=True)
    st.write("---")
    
    # Navigation
    menu = st.radio("MENU", ["🏠 ACCUEIL", "⚙️ SERVICES", "📸 RÉALISATIONS", "📅 DEVIS EXPRESS", "✉️ CONTACT"])
    
    st.write("---")
    st.write("📍 Dakar, Sénégal")
    st.write("📞 +221 77 861 59 00")

# 4. LOGIQUE DES PAGES
if menu == "🏠 ACCUEIL":
    st.markdown('<div class="hero"><h1>L\'audace visuelle<br>au service de votre marque.</h1><p>Design & Impression Premium.</p></div>', unsafe_allow_html=True)
    
    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        st.info("**100% Qualité**")
    with col2:
        st.info("**24h Livraison**")

elif menu == "📅 DEVIS EXPRESS":
    st.markdown("<h2 style='color:#0C4A6E;'>Demander un devis</h2>", unsafe_allow_html=True)
    with st.form("form_devis"):
        nom = st.text_input("Nom / Entreprise")
        services = st.multiselect("Services", ["Logo", "Print", "Packaging", "Enseigne"])
        details = st.text_area("Détails")
        
        submitted = st.form_submit_button("🚀 Envoyer sur WhatsApp")
        if submitted:
            if nom and services:
                message = f"Bonjour CHIC, devis pour {nom}. Services: {', '.join(services)}. {details}"
                url = f"https://wa.me/221778615900?text={urllib.parse.quote(message)}"
                st.markdown(f'<a href="{url}" target="_blank" style="background:#25D366; color:white; padding:15px; border-radius:10px; display:block; text-align:center; text-decoration:none; font-weight:bold;">CLIQUEZ ICI POUR WHATSAPP</a>', unsafe_allow_html=True)
