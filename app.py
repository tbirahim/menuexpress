import streamlit as st
import urllib.parse

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="CHIC Graphic & Print",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. NETTOYAGE TOTAL ET DESIGN (Cache GitHub, Menu Streamlit, etc.)
st.markdown("""
    <style>
    /* CACHER LES LOGOS GITHUB ET MENUS STREAMLIT */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="stToolbar"] {display: none;}
    div[data-testid="stDecoration"] {display: none;}
    button[title="View source on GitHub"] {display: none;}
    
    /* FORCE LE MODE CLAIR */
    .stApp { background-color: white !important; color: #0C4A6E !important; }

    /* BOUTON MENU MOBILE VISIBLE (Rond Bleu) */
    button[kind="headerNoPadding"] {
        background-color: #38BDF8 !important;
        color: white !important;
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        position: fixed !important;
        top: 15px !important;
        left: 15px !important;
        z-index: 999999 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* BARRE LATÉRALE */
    [data-testid="stSidebar"] {
        background-color: #0C4A6E !important;
        border-right: 5px solid #38BDF8;
    }
    [data-testid="stSidebar"] * { color: white !important; }

    /* HERO SECTION */
    .hero {
        background: linear-gradient(135deg, #0C4A6E 0%, #0369A1 100%);
        color: white !important;
        border-radius: 25px;
        padding: 40px 30px;
        margin-bottom: 25px;
        margin-top: 20px;
    }
    .hero h1 { color: white !important; font-family: 'Syne', sans-serif; font-size: 2.5rem; }

    /* FORMULAIRE DE DEVIS */
    .stForm {
        background-color: #F0F9FF !important;
        border-radius: 20px !important;
        padding: 20px !important;
        border: 1px solid #E0F2FE !important;
    }

    .stat-box {
        background: #E0F2FE;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border: 1px solid #bae6fd;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. BARRE LATÉRALE
with st.sidebar:
    st.markdown("<h1 style='text-align:center; font-family:Syne;'>CHIC</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#38BDF8; font-weight:700;'>GRAPHIC & PRINT</p>", unsafe_allow_html=True)
    st.write("---")
    menu = st.radio("NAVIGATION", ["🏠 ACCUEIL", "⚙️ SERVICES", "📸 RÉALISATIONS", "📅 DEVIS EXPRESS", "✉️ CONTACT"])
    st.write("---")
    st.caption("Dakar, Sénégal")

# 4. CONTENU DES PAGES
if menu == "🏠 ACCUEIL":
    st.markdown('<div class="hero"><h1>L\'audace visuelle<br>au service de votre marque.</h1><p>Impression & Design Haut de Gamme à Dakar.</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.markdown("<div class='stat-box'><h2 style='margin:0; color:#0C4A6E;'>100%</h2><p style='margin:0;'>Qualité</p></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='stat-box'><h2 style='margin:0; color:#0C4A6E;'>24h</h2><p style='margin:0;'>Livraison</p></div>", unsafe_allow_html=True)

elif menu == "⚙️ SERVICES":
    st.markdown("<h2 style='color:#0C4A6E;'>Nos Services</h2>", unsafe_allow_html=True)
    st.info("🎨 Branding | 🖨️ Print | 📦 Packaging | 🏢 Signalétique")

elif menu == "📸 RÉALISATIONS":
    st.markdown("<h2 style='color:#0C4A6E;'>Portfolio</h2>", unsafe_allow_html=True)
    # Note: Assure-toi que les photos sont bien à la racine de ton GitHub
    photos = ["photo10.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg", "photo5.jpg"]
    cols = st.columns(2)
    for i, p in enumerate(photos):
        cols[i%2].image(p, use_container_width=True)

elif menu == "📅 DEVIS EXPRESS":
    st.markdown("<h2 style='color:#0C4A6E;'>Demander un devis</h2>", unsafe_allow_html=True)
    with st.form("my_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            nom = st.text_input("Nom de l'entreprise / Projet")
        with col_b:
            contact_info = st.text_input("Votre numéro ou email")
        
        services = st.multiselect("Services souhaités", ["Logo", "Flyers", "Packaging", "Enseigne", "Autre"])
        details = st.text_area("Précisez votre demande (quantité, support...)")
        
        submitted = st.form_submit_button("🚀 Envoyer ma demande")
        
        if submitted:
            if nom and services:
                message = f"Bonjour CHIC G&P, devis pour {nom}. Services: {', '.join(services)}. Détails: {details}. Contact: {contact_info}"
                url = f"https://wa.me/221778615900?text={urllib.parse.quote(message)}"
                st.success("Demande prête !")
                st.markdown(f'<a href="{url}" target="_blank" style="background:#25D366; color:white; padding:15px; border-radius:10px; display:block; text-align:center; text-decoration:none; font-weight:bold;">CLIQUEZ ICI POUR WHATSAPP</a>', unsafe_allow_html=True)
            else:
                st.warning("Veuillez remplir le nom et choisir un service.")

elif menu == "✉️ CONTACT":
    st.markdown("<h2 style='color:#0C4A6E;'>Contact</h2>", unsafe_allow_html=True)
    st.write("📍 Dakar, Sénégal")
    st.write("📞 +221 77 861 59 00")
