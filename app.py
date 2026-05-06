import streamlit as st
import urllib.parse

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="CHIC Graphic & Print | Agence Créative",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. DESIGN "CARTE BLANCHE" (CSS PERSONNALISÉ)
st.markdown("""
    <style>
    /* Importation des polices Google */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&family=Syne:wght@700;800&display=swap');

    /* Variables de couleurs */
    :root {
        --primary: #38BDF8;
        --dark-bg: #0F172A;
        --sidebar-bg: #1E293B;
        --text-main: #1E293B;
        --text-light: #64748B;
    }

    /* Nettoyage de l'interface Streamlit */
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="stToolbar"] {display: none;}
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}

    /* Style global */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: var(--text-main);
    }

    /* BARRE LATÉRALE (SIDEBAR) */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    [data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }

    /* Boutons du Menu (Radio boutons cachés pour faire un menu propre) */
    div[data-testid="stSidebarUserContent"] .stRadio > div {
        background-color: transparent !important;
    }

    /* HERO SECTION DYNAMIQUE */
    .hero-container {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        padding: 100px 60px;
        border-radius: 32px;
        color: white;
        margin-bottom: 40px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .hero-container::after {
        content: "";
        position: absolute;
        top: -50%;
        right: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.2) 0%, transparent 70%);
        z-index: 0;
    }

    .hero-title {
        font-family: 'Syne', sans-serif;
        font-size: 4.5rem;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 20px;
        background: linear-gradient(to right, #FFFFFF, #38BDF8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* CARTES DE SERVICE */
    .service-card {
        background: #FFFFFF;
        border: 1px solid #F1F5F9;
        border-radius: 24px;
        padding: 40px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        height: 100%;
    }

    .service-card:hover {
        transform: translateY(-12px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        border-color: var(--primary);
    }

    /* PORTFOLIO IMAGES */
    .stImage > img {
        border-radius: 20px;
        transition: transform 0.6s ease;
    }
    .stImage > img:hover {
        transform: scale(1.02);
    }

    /* BOUTON WHATSAPP */
    .btn-wa {
        background: #25D366;
        color: white !important;
        padding: 18px 32px;
        border-radius: 16px;
        text-decoration: none;
        font-weight: 700;
        display: block;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(37, 211, 102, 0.3);
        transition: 0.3s;
    }
    .btn-wa:hover {
        background: #1eb954;
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# 3. SIDEBAR NAVIGATION
with st.sidebar:
    st.markdown("""
        <div style='padding: 20px 0; text-align: center;'>
            <h1 style='font-family:Syne; font-size:2.2rem; margin-bottom:0;'>CHIC</h1>
            <p style='color:#38BDF8 !important; font-weight:600; letter-spacing:2px; font-size:0.8rem; margin-top:0;'>GRAPHIC & PRINT</p>
        </div>
        <div style='height:2px; background:rgba(255,255,255,0.1); margin-bottom:30px;'></div>
    """, unsafe_allow_html=True)
    
    menu = st.radio(
        "NAVIGUER",
        ["ACCUEIL", "SERVICES", "RÉALISATIONS", "DEVIS", "CONTACT"],
        label_visibility="collapsed"
    )
    
    st.markdown("""
        <div style='position: fixed; bottom: 20px; left: 20px; font-size: 0.8rem; opacity: 0.5;'>
            📍 Dakar, Sénégal<br>© 2026 CHIC G&P
        </div>
    """, unsafe_allow_html=True)

# 4. CONTENU DES PAGES
if menu == "ACCUEIL":
    st.markdown(f"""
        <div class="hero-container">
            <h1 class="hero-title">On ne crée pas de<br>design. On crée de<br>l'influence.</h1>
            <p style="font-size:1.4rem; opacity:0.8; max-width:600px; line-height:1.6;">
                L'agence de référence à Dakar pour vos projets de branding, packaging et impression haute fidélité.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Qualité", "ULTRA HD")
    with c2: st.metric("Livraison", "SOUS 24H")
    with c3: st.metric("Satisfaction", "100%")

elif menu == "SERVICES":
    st.markdown("<h2 style='font-family:Syne; font-size:3rem; margin-bottom:40px;'>Nos Expertises</h2>", unsafe_allow_html=True)
    s1, s2 = st.columns(2)
    with s1:
        st.markdown("""
            <div class="service-card">
                <span style='font-size:3rem;'>🎨</span>
                <h3>Branding & Identité</h3>
                <p style='color:#64748B;'>Logos, chartes graphiques et direction artistique pour marques ambitieuses.</p>
            </div><br>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class="service-card">
                <span style='font-size:3rem;'>📦</span>
                <h3>Packaging Design</h3>
                <p style='color:#64748B;'>Conception d'emballages qui captivent l'œil et boostent vos ventes.</p>
            </div>
        """, unsafe_allow_html=True)
    with s2:
        st.markdown("""
            <div class="service-card">
                <span style='font-size:3rem;'>🖨️</span>
                <h3>Impression Print</h3>
                <p style='color:#64748B;'>Flyers, cartes de visite et supports marketing avec une finition irréprochable.</p>
            </div><br>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class="service-card">
                <span style='font-size:3rem;'>🏢</span>
                <h3>Signalétique</h3>
                <p style='color:#64748B;'>Habillage de façades, enseignes lumineuses et décoration d'intérieur.</p>
            </div>
        """, unsafe_allow_html=True)

elif menu == "RÉALISATIONS":
    st.markdown("<h2 style='font-family:Syne; font-size:3rem;'>Portfolio</h2><br>", unsafe_allow_html=True)
    photos = ["photo10.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg", "photo5.jpg", "photo6.jpg", "photo7.jpg", "photo8.jpg", "photo9.jpg"]
    p1, p2 = st.columns(2)
    for i, p in enumerate(photos):
        if i % 2 == 0: p1.image(p, use_container_width=True)
        else: p2.image(p, use_container_width=True)

elif menu == "DEVIS":
    st.markdown("<h2 style='font-family:Syne;'>Lancer votre projet</h2>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='service-card'>", unsafe_allow_html=True)
        with st.form("wa_form"):
            name = st.text_input("Nom de l'entreprise")
            serv = st.multiselect("Service souhaité", ["Logo", "Flyer", "Packaging", "Enseigne"])
            det = st.text_area("Détails du projet")
            submit = st.form_submit_button("🚀 Valider la demande")
            
            if submit:
                msg = f"Bonjour CHIC G&P, je souhaite un devis pour {', '.join(serv)}. Entreprise : {name}. Détails : {det}"
                url = f"https://wa.me/221778615900?text={urllib.parse.quote(msg)}"
                st.markdown(f'<a href="{url}" target="_blank" class="btn-wa">ENVOYER PAR WHATSAPP MAINTENANT</a>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

elif menu == "CONTACT":
    st.markdown("<h2 style='font-family:Syne;'>Parlons de vous</h2>", unsafe_allow_html=True)
    st.info("📍 Situé à Dakar, Sénégal")
    st.markdown("""
        <div class="service-card">
            <h3>Coordonnées directes</h3>
            <p>📞 +221 77 861 59 00</p>
            <p>📧 contact@chic-graphic.sn</p>
            <p>🕒 Lun - Sam | 09:00 - 19:00</p>
        </div>
    """, unsafe_allow_html=True)
