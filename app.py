import streamlit as st
import urllib.parse

# 1. CONFIGURATION STRICTE
st.set_page_config(
    page_title="CHIC Graphic & Print",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. CSS CORRECTIF (Spécial Mobile + Suppression GitHub/Menus)
st.markdown("""
    <style>
    /* 1. CACHER LES ÉLÉMENTS STREAMLIT (Logo GitHub, Menu, etc.) */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    div[data-testid="stToolbar"] {display: none !important;}
    div[data-testid="stDecoration"] {display: none !important;}
    #MainMenu {visibility: hidden !important;}

    /* 2. FORCER LE BOUTON MENU SUR MOBILE */
    /* On cible le bouton par son rôle pour être sûr qu'il apparaisse */
    button[data-testid="stSidebarCollapseButton"] {
        background-color: #38BDF8 !important;
        color: white !important;
        border-radius: 50% !important;
        width: 55px !important;
        height: 55px !important;
        position: fixed !important;
        top: 15px !important;
        left: 15px !important;
        z-index: 9999999 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    button[data-testid="stSidebarCollapseButton"] svg {
        fill: white !important;
        width: 28px !important;
        height: 28px !important;
    }

    /* 3. DESIGN DE LA BARRE LATÉRALE */
    [data-testid="stSidebar"] {
        background-color: #0C4A6E !important;
        border-right: 4px solid #38BDF8 !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* 4. FIX MODE CLAIR */
    .stApp {
        background-color: white !important;
        color: #0C4A6E !important;
    }

    /* Style Hero et Cartes */
    .hero {
        background: linear-gradient(135deg, #0C4A6E 0%, #0369A1 100%);
        border-radius: 25px;
        padding: 35px;
        color: white !important;
        margin-top: 50px;
    }
    
    .card {
        background-color: #E0F2FE;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #bae6fd;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. CONTENU DE LA BARRE LATÉRALE
with st.sidebar:
    st.markdown("<h1 style='text-align:center; font-family:Syne;'>CHIC</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#38BDF8; font-weight:700;'>GRAPHIC & PRINT</p>", unsafe_allow_html=True)
    st.write("---")
    
    menu = st.radio("NAVIGATION", ["🏠 ACCUEIL", "⚙️ SERVICES", "📸 RÉALISATIONS", "📅 DEVIS EXPRESS", "✉️ CONTACT"])
    
    st.write("---")
    st.write("📍 Dakar, Sénégal")
    st.write("📞 +221 77 861 59 00")

# 4. LOGIQUE DES PAGES
if menu == "🏠 ACCUEIL":
    st.markdown('<div class="hero"><h1>L\'audace visuelle<br>au service de votre marque.</h1><p>Design & Impression Premium à Dakar.</p></div>', unsafe_allow_html=True)
    st.write("")
    c1, c2 = st.columns(2)
    with c1: st.info("**100% Qualité HD**")
    with c2: st.info("**Livraison 24h**")

elif menu == "⚙️ SERVICES":
    st.markdown("<h2 style='color:#0C4A6E;'>Nos Services</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div class="card"><h3>🎨 Branding</h3><p>Logos et identités visuelles.</p></div>
        <div class="card"><h3>🖨️ Print</h3><p>Flyers, cartes et brochures.</p></div>
        <div class="card"><h3>📦 Packaging</h3><p>Design d'emballages personnalisés.</p></div>
    """, unsafe_allow_html=True)

elif menu == "📸 RÉALISATIONS":
    st.markdown("<h2 style='color:#0C4A6E;'>Portfolio</h2>", unsafe_allow_html=True)
    # Remplacer par tes vrais noms de fichiers
    photos = ["photo2.jpg", "photo3.jpg", "photo4.jpg", "photo10.jpg"]
    cols = st.columns(2)
    for i, p in enumerate(photos):
        cols[i % 2].image(p, use_container_width=True)

elif menu == "📅 DEVIS EXPRESS":
    st.markdown("<h2 style='color:#0C4A6E;'>Demander un devis</h2>", unsafe_allow_html=True)
    with st.form("form_devis"):
        nom = st.text_input("Nom de l'entreprise")
        services = st.multiselect("Services", ["Logo", "Print", "Packaging", "Enseigne"])
        details = st.text_area("Détails du projet")
        submitted = st.form_submit_button("🚀 Valider la demande")
        
        if submitted:
            if nom and services:
                msg = f"Bonjour CHIC, devis pour {nom}. Services: {', '.join(services)}. {details}"
                url = f"https://wa.me/221778615900?text={urllib.parse.quote(msg)}"
                st.markdown(f'<a href="{url}" target="_blank" style="background:#25D366; color:white; padding:15px; border-radius:10px; display:block; text-align:center; text-decoration:none; font-weight:bold;">CLIQUEZ ICI POUR WHATSAPP</a>', unsafe_allow_html=True)
            else:
                st.error("Veuillez remplir les champs obligatoires.")

elif menu == "✉️ CONTACT":
    st.markdown("<h2 style='color:#0C4A6E;'>Contactez-nous</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div class="card">
            <p>📞 +221 77 861 59 00</p>
            <p>📧 contact@chic-graphic.sn</p>
            <p>📍 Dakar, Sénégal</p>
        </div>
    """, unsafe_allow_html=True)
