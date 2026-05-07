import streamlit as st
import urllib.parse

# 1. CONFIGURATION DE LA PAGE (Force le mode clair et la sidebar)
st.set_page_config(
    page_title="CHIC Graphic & Print | Agence Créative",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded", # Force l'ouverture au démarrage
)

# 2. STYLE CSS (Forçage du Mode Clair + Design Premium)
st.markdown("""
    <style>
    /* Force le fond blanc sur toute l'application */
    .stApp {
        background-color: white !important;
        color: #0C4A6E !important;
    }

    /* Style de la barre latérale */
    [data-testid="stSidebar"] {
        background-color: #0C4A6E !important;
        border-right: 5px solid #38BDF8;
        min-width: 250px !important;
    }
    
    /* Force le texte de la sidebar en blanc */
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Masquer les éléments inutiles */
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="stToolbar"] {display: none;}

    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;700&display=swap');

    /* Design des blocs de statistiques et des cartes */
    .hero {
        background: linear-gradient(135deg, #0C4A6E 0%, #075985 50%, #0369A1 100%);
        color: white !important;
        border-radius: 30px;
        padding: 60px 40px;
        margin-bottom: 40px;
    }
    
    .hero h1 { 
        font-family: 'Syne', sans-serif; 
        font-size: clamp(2rem, 5vw, 3.5rem); 
        color: white !important;
    }

    .stat-box {
        background: #E0F2FE;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border: 1px solid #bae6fd;
        margin-bottom: 10px;
    }
    
    .stat-num { 
        font-family: 'Syne', sans-serif; 
        font-size: 2.2rem; 
        font-weight: 800; 
        color: #0C4A6E !important; 
        display: block; 
    }

    .card {
        background: #F8FAFC;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #E0F2FE;
        margin-bottom: 20px;
    }

    /* Bouton WhatsApp */
    .wa-button {
        background-color: #25D366;
        color: white !important;
        padding: 15px;
        border-radius: 12px;
        text-decoration: none;
        font-weight: 700;
        display: block;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 3. BARRE LATÉRALE (SIDEBAR)
with st.sidebar:
    st.markdown("<h1 style='font-family:Syne; text-align:center;'>CHIC</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#38BDF8 !important; font-weight:700;'>GRAPHIC & PRINT</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Navigation par radio (le plus stable pour la sidebar)
    menu = st.radio(
        "NAVIGATION",
        ["🏠 ACCUEIL", "⚙️ SERVICES", "📸 RÉALISATIONS", "📅 DEVIS EXPRESS", "✉️ CONTACT"]
    )
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("📍 Dakar, Sénégal")
    st.markdown("📞 +221 77 861 59 00")

# 4. CONTENU DES PAGES
if menu == "🏠 ACCUEIL":
    st.markdown("""
        <div class="hero">
            <h1>L'audace visuelle<br>au service de votre marque.</h1>
            <p style="font-size:1.2rem; opacity:0.9;">Impression & Design Haut de Gamme.</p>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown("<div class='stat-box'><span class='stat-num'>100%</span><b>Qualité</b></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='stat-box'><span class='stat-num'>24h</span><b>Livraison</b></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='stat-box'><span class='stat-num'>PRO</span><b>Expertise</b></div>", unsafe_allow_html=True)
    with c4: st.markdown("<div class='stat-box'><span class='stat-num'>DKR</span><b>Sénégal</b></div>", unsafe_allow_html=True)

elif menu == "⚙️ SERVICES":
    st.markdown("<h2 style='font-family:Syne; color:#0C4A6E;'>Nos Expertises</h2>", unsafe_allow_html=True)
    s1, s2 = st.columns(2)
    with s1:
        st.markdown('<div class="card"><h3>🎨 Branding</h3><p>Logos et chartes graphiques.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><h3>📦 Packaging</h3><p>Design d\'emballages personnalisés.</p></div>', unsafe_allow_html=True)
    with s2:
        st.markdown('<div class="card"><h3>🖨️ Print</h3><p>Flyers, cartes de visite, brochures.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><h3>🏢 Signalétique</h3><p>Enseignes et habillage vitrine.</p></div>', unsafe_allow_html=True)

elif menu == "📸 RÉALISATIONS":
    st.markdown("<h2 style='font-family:Syne; color:#0C4A6E;'>Portfolio</h2>", unsafe_allow_html=True)
    photos = ["photo10.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg", "photo5.jpg", "photo6.jpg", "photo7.jpg", "photo8.jpg", "photo9.jpg"]
    cols = st.columns(3)
    for i, p in enumerate(photos):
        cols[i % 3].image(p, use_container_width=True)

elif menu == "📅 DEVIS EXPRESS":
    st.markdown("<h2 style='font-family:Syne; color:#0C4A6E;'>Demander un devis</h2>", unsafe_allow_html=True)
    with st.form("devis_form"):
        nom = st.text_input("Nom / Entreprise")
        besoin = st.multiselect("Service", ["Logo", "Print", "Packaging", "Autre"])
        if st.form_submit_button("🚀 Valider"):
            msg = f"Bonjour CHIC G&P, devis pour {nom} ({', '.join(besoin)})."
            link = f"https://wa.me/221778615900?text={urllib.parse.quote(msg)}"
            st.markdown(f'<a href="{link}" target="_blank" class="wa-button">FINALISER SUR WHATSAPP</a>', unsafe_allow_html=True)

elif menu == "✉️ CONTACT":
    st.markdown("<h2 style='font-family:Syne; color:#0C4A6E;'>Contact</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div class="card">
            <p>📍 <b>Localisation :</b> Dakar, Sénégal</p>
            <p>📞 <b>Téléphone :</b> +221 77 861 59 00</p>
            <p>📧 <b>Email :</b> contact@chic-graphic.sn</p>
        </div>
    """, unsafe_allow_html=True)
