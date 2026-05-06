import streamlit as st
import urllib.parse

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="CHIC Graphic & Print | Agence Créative",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. STYLE CSS AVANCÉ (Menu Fixe et Design Premium)
st.markdown("""
    <style>
    /* Cacher les éléments inutiles de Streamlit */
    footer {visibility: hidden;}
    div[data-testid="stToolbar"] {display: none;}
    header {visibility: hidden;}
    
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    :root {
        --primary:  #38BDF8;
        --secondary: #0284C7;
        --dark:     #0C4A6E;
        --light:    #FFFFFF;
        --bg-alt:   #E0F2FE;
        --radius:   20px;
    }

    /* Fixer la barre latérale pour qu'elle ne bouge pas */
    [data-testid="stSidebar"] {
        position: fixed;
        background-color: #0C4A6E !important;
        border-right: 4px solid var(--primary);
    }
    
    section[data-testid="stSidebar"] * { color: white !important; }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: var(--light);
        color: var(--dark);
    }

    /* Accueil - Hero Section */
    .hero {
        background: linear-gradient(135deg, #0C4A6E 0%, #075985 50%, #0369A1 100%);
        color: #fff;
        border-radius: 30px;
        padding: 100px 60px;
        margin-bottom: 50px;
        box-shadow: 0 25px 50px -12px rgba(12, 74, 110, 0.4);
        position: relative;
        overflow: hidden;
    }
    .hero h1 { 
        font-family: 'Syne', sans-serif; 
        font-size: 4rem; 
        font-weight: 800; 
        margin-bottom: 20px; 
        line-height: 1;
        color: white;
    }
    .hero p { font-size: 1.3rem; opacity: 0.9; max-width: 650px; line-height: 1.6; }

    /* Cartes de Services */
    .card {
        background: #fff;
        border-radius: var(--radius);
        padding: 40px;
        box-shadow: 0 15px 35px rgba(2,132,199,0.06);
        border: 1px solid #f0f9ff;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: 100%;
    }
    .card:hover {
        transform: translateY(-15px);
        box-shadow: 0 30px 60px rgba(2,132,199,0.12);
        border-color: var(--primary);
    }
    .card h3 { font-family: 'Syne', sans-serif; font-size: 1.5rem; margin-top: 15px; }

    /* Stats */
    .stat-box {
        background: white;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        border: 2px solid #E0F2FE;
        transition: 0.3s;
    }
    .stat-box:hover { border-color: var(--primary); background: #F0F9FF; }
    .stat-num { font-family: 'Syne', sans-serif; font-size: 2.5rem; font-weight: 800; color: var(--secondary); display: block; }

    /* Images */
    [data-testid="stImage"] img {
        border-radius: 15px;
        transition: transform 0.5s ease;
    }
    [data-testid="stImage"] img:hover {
        transform: scale(1.03);
    }
    
    .footer-pro {
        background: var(--dark);
        color: #fff;
        border-radius: 25px;
        padding: 50px;
        margin-top: 80px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 3. DONNÉES
BRAND_NAME = "CHIC Graphic & Print"
WHATSAPP_NUMBER = "221778615900" 
LOCATION = "Dakar, Sénégal"

# 4. BARRE LATÉRALE (MENU FIXE)
with st.sidebar:
    st.markdown(f"""
        <div style='text-align:center; padding:30px 0'>
            <div style='font-family:Syne; font-size:2rem; font-weight:800; line-height:0.9;'>CHIC<br><span style='color:#38BDF8; font-size:1.4rem'>Graphic & Print</span></div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    menu = st.radio("NAVIGATION", ["🏠 ACCUEIL", "⚙️ SERVICES", "📸 RÉALISATIONS", "📅 DEVIS EXPRESS", "✉️ CONTACT"])
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; font-size:0.8rem; opacity:0.7'>📍 {LOCATION}</div>", unsafe_allow_html=True)

# 5. PAGES

if menu == "🏠 ACCUEIL":
    st.markdown(f"""
        <div class="hero">
            <h1>L'audace visuelle<br>au service de votre marque.</h1>
            <p>CHIC Graphic & Print fusionne créativité et précision technique pour offrir des solutions d'impression et de design qui marquent les esprits à Dakar.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='margin-bottom:30px'>Notre Impact en chiffres</h3>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    stats = [("100%", "Qualité Premium"), ("24h", "Délai Express"), ("+500", "Projets livrés"), ("Dakar", "Ancrage Local")]
    for col, (val, label) in zip([c1, c2, c3, c4], stats):
        col.markdown(f"<div class='stat-box'><span class='stat-num'>{val}</span><span style='font-weight:600; color:#64A4C4'>{label}</span></div>", unsafe_allow_html=True)

elif menu == "⚙️ SERVICES":
    st.markdown("<h2 style='font-size:3rem'>Nos Expertise</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64A4C4; font-size:1.2rem'>Des solutions complètes pour une communication percutante.</p><br>", unsafe_allow_html=True)
    
    services = [
        ("🎨", "Branding & Logo", "Nous créons des logos uniques et des chartes graphiques qui racontent votre histoire."),
        ("🖨️", "Impression Print", "Supports marketing de haute qualité : flyers, cartes de visite, affiches et brochures."),
        ("📦", "Packaging & Luxe", "Conception d'emballages innovants qui transforment l'expérience client."),
        ("🏢", "Signalétique Pro", "Visibilité maximale pour votre commerce avec nos enseignes et habillages de vitrine.")
    ]
    
    cols = st.columns(2)
    for i, (icon, title, desc) in enumerate(services):
        with cols[i % 2]:
            st.markdown(f"""
                <div class="card">
                    <div style="font-size:3rem">{icon}</div>
                    <h3>{title}</h3>
                    <p style="color:#64A4C4; line-height:1.6">{desc}</p>
                </div><br>
            """, unsafe_allow_html=True)

elif menu == "📸 RÉALISATIONS":
    st.markdown("<h2 style='font-size:3rem'>Notre Portfolio</h2><br>", unsafe_allow_html=True)
    photos = ["photo10.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg", "photo5.jpg", 
              "photo6.jpg", "photo7.jpg", "photo8.jpg", "photo9.jpg"]
    col1, col2 = st.columns(2)
    for i, p in enumerate(photos):
        if i % 2 == 0:
            col1.image(p, use_container_width=True)
        else:
            col2.image(p, use_container_width=True)

elif menu == "📅 DEVIS EXPRESS":
    st.markdown("<h2>Lancez votre projet maintenant</h2>", unsafe_allow_html=True)
    with st.form("devis_form"):
        nom = st.text_input("Nom de l'entreprise ou Projet")
        type_projet = st.multiselect("Services souhaités", ["Branding", "Print", "Packaging", "Signalétique", "Autre"])
        details = st.text_area("Décrivez vos besoins (quantités, formats...)")
        submit = st.form_submit_button("🚀 Recevoir mon devis via WhatsApp")
        if submit:
            msg = f"Bonjour CHIC Graphic & Print, je souhaite un devis pour : {', '.join(type_projet)}. Projet : {nom}. Détails : {details}"
            link = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(msg)}"
            st.markdown(f"<a href='{link}' target='_blank' style='text-decoration:none;'><div style='background:#38BDF8; color:white; padding:18px; text-align:center; border-radius:12px; font-weight:bold; font-size:1.1rem'>VALIDER ET ENVOYER SUR WHATSAPP</div></a>", unsafe_allow_html=True)

elif menu == "✉️ CONTACT":
    st.markdown("<h2>Travaillons ensemble</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
            <div class="card">
                <h3>Contact</h3>
                <p>📍 {LOCATION}</p>
                <p>📧 contact@chic-graphic.sn</p>
                <p>📞 +221 77 861 59 00</p>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.success("🕒 Horaires d'ouverture : Lundi - Samedi : 09h00 - 19h00")

# 6. FOOTER
st.markdown(f"""
    <div class="footer-pro">
        <div style="font-family:Syne; font-size:2rem; font-weight:800;">{BRAND_NAME}</div>
        <p style="opacity:0.6; margin-top:10px;">© 2026 · Experts en solutions visuelles · {LOCATION}</p>
    </div>
""", unsafe_allow_html=True)
