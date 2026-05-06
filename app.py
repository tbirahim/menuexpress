import streamlit as st
import urllib.parse

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="CHIC Graphic & Print | Agence Créative",
    page_icon="🎨",
    layout="wide",
)

# 2. STYLE CSS POUR LE MENU HORIZONTAL EN HAUT
st.markdown("""
    <style>
    /* Cacher les éléments par défaut de Streamlit */
    footer {visibility: hidden;}
    div[data-testid="stToolbar"] {display: none;}
    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;} /* On cache totalement la barre latérale */

    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    :root {
        --primary:  #38BDF8;
        --dark:     #0C4A6E;
        --light:    #FFFFFF;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: white;
    }

    /* Menu Horizontal Fixe en haut */
    .nav-bar {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: var(--dark);
        padding: 15px 50px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 1000;
        border-bottom: 3px solid var(--primary);
    }
    .nav-logo {
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        color: white;
        font-size: 1.2rem;
    }
    
    /* Espacement pour ne pas que le contenu soit sous le menu */
    .main-content {
        margin-top: 100px;
    }

    .hero {
        background: linear-gradient(135deg, #0C4A6E 0%, #0369A1 100%);
        color: #fff;
        border-radius: 25px;
        padding: 60px 40px;
        margin-bottom: 40px;
    }
    
    .card {
        background: #f8fafc;
        border-radius: 15px;
        padding: 30px;
        border: 1px solid #e2e8f0;
        height: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# 3. BARRE DE NAVIGATION EN HAUT (DANS LE CORPS DE LA PAGE)
st.markdown(f"""
    <div class="nav-bar">
        <div class="nav-logo">CHIC Graphic & Print</div>
        <div style="color: #38BDF8; font-weight: bold; font-size: 0.9rem;">📍 Dakar, Sénégal</div>
    </div>
""", unsafe_allow_html=True)

# On utilise des boutons Streamlit pour la navigation en haut
st.markdown('<div class="main-content">', unsafe_allow_html=True)
cols_menu = st.columns([1,1,1,1,1])
with cols_menu[0]: menu = "🏠 ACCUEIL" if st.button("ACCUEIL", use_container_width=True) else ""
with cols_menu[1]: 
    if st.button("SERVICES", use_container_width=True): menu = "⚙️ SERVICES"
with cols_menu[2]: 
    if st.button("RÉALISATIONS", use_container_width=True): menu = "📸 RÉALISATIONS"
with cols_menu[3]: 
    if st.button("DEVIS", use_container_width=True): menu = "📅 DEVIS EXPRESS"
with cols_menu[4]: 
    if st.button("CONTACT", use_container_width=True): menu = "✉️ CONTACT"

# Système de gestion d'état pour le menu
if 'choice' not in st.session_state:
    st.session_state.choice = "🏠 ACCUEIL"
if menu != "":
    st.session_state.choice = menu

current_page = st.session_state.choice

# 4. LOGIQUE DES PAGES
if current_page == "🏠 ACCUEIL":
    st.markdown(f"""
        <div class="hero">
            <h1 style="font-family:Syne; font-size:3rem; color:white;">L'audace visuelle.</h1>
            <p>CHIC Graphic & Print : Excellence en design et impression à Dakar.</p>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Qualité", "100% HD")
    c2.metric("Délai", "24h/48h")
    c3.metric("Expertise", "Premium")

elif current_page == "⚙️ SERVICES":
    st.markdown("## Nos Services")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown('<div class="card"><h3>🎨 Branding</h3><p>Logos et chartes graphiques.</p></div>', unsafe_allow_html=True)
    with col_s2:
        st.markdown('<div class="card"><h3>🖨️ Print</h3><p>Flyers et cartes de visite.</p></div>', unsafe_allow_html=True)

elif current_page == "📸 RÉALISATIONS":
    st.markdown("## Notre Portfolio")
    photos = ["photo10.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg", "photo5.jpg", 
              "photo6.jpg", "photo7.jpg", "photo8.jpg", "photo9.jpg"]
    col1, col2 = st.columns(2)
    for i, p in enumerate(photos):
        if i % 2 == 0:
            col1.image(p, use_container_width=True)
        else:
            col2.image(p, use_container_width=True)

elif current_page == "📅 DEVIS EXPRESS":
    st.markdown("## Devis Gratuit")
    with st.form("devis"):
        nom = st.text_input("Nom")
        besoin = st.text_area("Votre besoin")
        if st.form_submit_button("🚀 Préparer"):
            st.success("Prêt à l'envoi WhatsApp !")

elif current_page == "✉️ CONTACT":
    st.markdown("## Contact")
    st.info("📍 Dakar, Sénégal | 📞 +221 77 861 59 00")

st.markdown('</div>', unsafe_allow_html=True) # Fin du main-content

# FOOTER
st.markdown("""
    <div style="text-align:center; padding:40px; color:#64A4C4; font-size:0.8rem;">
        © 2026 CHIC Graphic & Print · Dakar
    </div>
""", unsafe_allow_html=True)
