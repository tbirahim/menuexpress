import streamlit as st
import urllib.parse

# 1. CONFIGURATION ET NETTOYAGE RADICAL
st.set_page_config(
    page_title="CHIC Graphic & Print | Agence Créative",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# On garde le menu (header) mais on cache le Footer Streamlit et le bouton de déploiement
st.markdown("""
    <style>
    /* footer {visibility: hidden;}  <- Décommente cette ligne si tu veux cacher "Made with Streamlit" en bas */
    div[data-testid="stToolbar"] {display: none;}
    .block-container {padding-top: 2rem;}
    
    /* Import des polices */
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    /* Variables de couleurs */
    :root {
        --primary:  #38BDF8;
        --secondary: #0284C7;
        --dark:     #0C4A6E;
        --light:    #FFFFFF;
        --bg-alt:   #E0F2FE;
        --muted:    #64A4C4;
        --radius:   16px;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: var(--light);
        color: var(--dark);
    }

    h1, h2, h3 { font-family: 'Syne', sans-serif; font-weight: 800; }

    /* Hero Section */
    .hero {
        background: linear-gradient(135deg, #0C4A6E 0%, #075985 60%, #0369A1 100%);
        color: #fff;
        border-radius: 24px;
        padding: 80px 50px;
        margin-bottom: 40px;
        box-shadow: 0 20px 40px rgba(12, 74, 110, 0.2);
    }
    .hero h1 { font-size: 3.5rem; margin-bottom: 10px; color: #fff; line-height: 1.1; }
    .hero p { font-size: 1.2rem; opacity: 0.9; max-width: 600px; }

    /* Cards */
    .card {
        background: #fff;
        border-radius: var(--radius);
        padding: 30px;
        box-shadow: 0 10px 30px rgba(2,132,199,0.08);
        border: 1px solid #f0f9ff;
        transition: all 0.3s ease;
        height: 100%;
    }
    .card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(2,132,199,0.15);
        border-color: var(--primary);
    }

    /* Stats & Badges */
    .stat-box {
        background: var(--bg-alt);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border: 1px solid #bae6fd;
    }
    .stat-num { font-size: 2.2rem; font-weight: 800; color: var(--secondary); display: block; }

    /* Sidebar Pro */
    section[data-testid="stSidebar"] {
        background-color: #0C4A6E !important;
        border-right: 4px solid var(--primary);
    }
    section[data-testid="stSidebar"] * { color: white !important; }

    /* Footer Pro */
    .footer-pro {
        background: var(--dark);
        color: #fff;
        border-radius: 20px;
        padding: 40px;
        margin-top: 60px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 2. DONNÉES ET CONSTANTES
BRAND_NAME = "CHIC Graphic & Print"
WHATSAPP_NUMBER = "221778615900" 
LOCATION = "Dakar, Sénégal"

# 3. BARRE LATÉRALE
with st.sidebar:
    st.markdown(f"""
        <div style='text-align:center; padding:20px 0'>
            <div style='font-family:Syne; font-size:1.6rem; font-weight:800; line-height:1;'>CHIC<br><span style='color:#38BDF8'>Graphic & Print</span></div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("MENU", ["🏠 ACCUEIL", "⚙️ SERVICES", "📅 DEVIS EXPRESS", "✉️ CONTACT"])
    st.markdown("---")
    st.markdown(f"📍 {LOCATION}")

# 4. LOGIQUE DES PAGES
if menu == "🏠 ACCUEIL":
    st.markdown(f"""
        <div class="hero">
            <h1>L'excellence visuelle<br>à votre portée.</h1>
            <p>Nous transformons vos concepts en réalités tangibles grâce à un design audacieux et une impression haute définition.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Pourquoi nous faire confiance ?")
    c1, c2, c3, c4 = st.columns(4)
    stats = [("100%", "Qualité HD"), ("24h", "Livraison"), ("PRO", "Design"), ("Dakar", "Local")]
    for col, (val, label) in zip([c1, c2, c3, c4], stats):
        col.markdown(f"<div class='stat-box'><span class='stat-num'>{val}</span><span style='font-weight:600'>{label}</span></div>", unsafe_allow_html=True)

elif menu == "⚙️ SERVICES":
    st.markdown("<h2 style='font-size:2.5rem'>Nos Solutions</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64A4C4'>Une expertise complète pour votre image de marque.</p><br>", unsafe_allow_html=True)
    
    services = [
        ("🎨", "Branding & Logo", "Création d'identités visuelles uniques qui marquent les esprits."),
        ("🖨️", "Impression Print", "Flyers, cartes de visite et affiches sur supports premium."),
        ("📦", "Packaging Design", "Conception d'emballages qui valorisent vos produits."),
        ("🏢", "Signalétique", "Habillage de boutiques, enseignes et supports publicitaires.")
    ]
    
    cols = st.columns(2)
    for i, (icon, title, desc) in enumerate(services):
        with cols[i % 2]:
            st.markdown(f"""
                <div class="card">
                    <div style="font-size:2.5rem">{icon}</div>
                    <h3 style="margin:15px 0">{title}</h3>
                    <p style="color:#64A4C4; font-size:0.95rem">{desc}</p>
                </div><br>
            """, unsafe_allow_html=True)

elif menu == "📅 DEVIS EXPRESS":
    st.markdown("<h2>Obtenir un Devis Gratuit</h2>", unsafe_allow_html=True)
    st.markdown("<div style='background:white; padding:30px; border-radius:20px; border:1px solid #E0F2FE'>", unsafe_allow_html=True)
    
    with st.form("devis_form"):
        nom = st.text_input("Nom de l'entreprise ou Projet")
        type_projet = st.multiselect("Services souhaités", ["Logo", "Flyers", "Cartes de visite", "Packaging", "Autre"])
        details = st.text_area("Décrivez votre besoin (quantité, dimensions...)")
        submit = st.form_submit_button("🚀 Préparer mon devis")
        
        if submit:
            msg = f"Bonjour {BRAND_NAME}, je souhaite un devis pour : {', '.join(type_projet)}. Projet : {nom}. Détails : {details}"
            link = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(msg)}"
            st.success("Demande prête !")
            st.markdown(f"<a href='{link}' target='_blank' style='text-decoration:none;'><div style='background:#38BDF8; color:white; padding:15px; text-align:center; border-radius:10px; font-weight:bold;'>ENVOYER SUR WHATSAPP</div></a>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "✉️ CONTACT":
    st.markdown("<h2>Parlons de votre projet</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
            <div class="card">
                <h4>Nos coordonnées</h4>
                <p>📍 {LOCATION}</p>
                <p>📧 contact@chic-graphic.sn</p>
                <p>📞 +221 77 861 59 00</p>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.info("Nous sommes ouverts du Lundi au Samedi de 09h à 19h.")

# 5. FOOTER PROFESSIONNEL
st.markdown(f"""
    <div class="footer-pro">
        <div style="font-family:Syne; font-size:1.5rem; font-weight:800;">{BRAND_NAME}</div>
        <p style="opacity:0.6; font-size:0.9rem; margin-top:10px;">
            © 2026 · Créateur de solutions visuelles · {LOCATION}<br>
            Design by CHIC Graphic & Print
        </p>
    </div>
""", unsafe_allow_html=True)
