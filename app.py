import streamlit as st
import urllib.parse

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="CHIC Graphic & Print | Agence Créative",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. STYLE CSS (Design Pro & Menu Visible)
st.markdown("""
    <style>
    footer {visibility: hidden;}
    div[data-testid="stToolbar"] {display: none;}
    .block-container {padding-top: 2rem;}
    
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

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

    .hero {
        background: linear-gradient(135deg, #0C4A6E 0%, #075985 60%, #0369A1 100%);
        color: #fff;
        border-radius: 24px;
        padding: 80px 50px;
        margin-bottom: 40px;
        box-shadow: 0 20px 40px rgba(12, 74, 110, 0.2);
    }
    .hero h1 { font-size: 3.5rem; margin-bottom: 10px; color: #fff; line-height: 1.1; }

    .card {
        background: #fff;
        border-radius: var(--radius);
        padding: 30px;
        box-shadow: 0 10px 30px rgba(2,132,199,0.08);
        border: 1px solid #f0f9ff;
        transition: all 0.3s ease;
        height: 100%;
    }

    .stat-box {
        background: var(--bg-alt);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
    }

    section[data-testid="stSidebar"] {
        background-color: #0C4A6E !important;
        border-right: 4px solid var(--primary);
    }
    section[data-testid="stSidebar"] * { color: white !important; }

    .footer-pro {
        background: var(--dark);
        color: #fff;
        border-radius: 20px;
        padding: 40px;
        margin-top: 60px;
        text-align: center;
    }

    /* Style des images pour qu'elles soient grandes et belles */
    [data-testid="stImage"] {
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# 3. DONNÉES ET CONSTANTES
BRAND_NAME = "CHIC Graphic & Print"
WHATSAPP_NUMBER = "221778615900" 
LOCATION = "Dakar, Sénégal"

# 4. BARRE LATÉRALE
with st.sidebar:
    st.markdown(f"""
        <div style='text-align:center; padding:20px 0'>
            <div style='font-family:Syne; font-size:1.6rem; font-weight:800; line-height:1;'>CHIC<br><span style='color:#38BDF8'>Graphic & Print</span></div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("MENU", ["🏠 ACCUEIL", "⚙️ SERVICES", "📸 RÉALISATIONS", "📅 DEVIS EXPRESS", "✉️ CONTACT"])
    st.markdown("---")
    st.markdown(f"📍 {LOCATION}")

# 5. LOGIQUE DES PAGES

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
    st.markdown("<h2 style='font-size:2.5rem'>Nos Solutions</h2><br>", unsafe_allow_html=True)
    services = [
        ("🎨", "Branding & Logo", "Création d'identités visuelles uniques."),
        ("🖨️", "Impression Print", "Flyers, cartes de visite et affiches."),
        ("📦", "Packaging", "Conception d'emballages valorisants."),
        ("🏢", "Signalétique", "Habillage de boutiques et enseignes.")
    ]
    cols = st.columns(2)
    for i, (icon, title, desc) in enumerate(services):
        with cols[i % 2]:
            st.markdown(f'<div class="card"><div style="font-size:2rem">{icon}</div><h3>{title}</h3><p>{desc}</p></div><br>', unsafe_allow_html=True)

elif menu == "📸 RÉALISATIONS":
    st.markdown("<h2 style='font-size:2.5rem'>Notre Portfolio</h2><br>", unsafe_allow_html=True)
    
    # On liste tes fichiers tels qu'ils sont sur GitHub
    # J'ai ajouté photo10 en premier car elle est en haut de ta liste
    photos = ["photo10.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg", "photo5.jpg", 
              "photo6.jpg", "photo7.jpg", "photo8.jpg", "photo9.jpg"]
    
    col1, col2 = st.columns(2)
    
    for i, p in enumerate(photos):
        if i % 2 == 0:
            col1.image(p, use_container_width=True)
        else:
            col2.image(p, use_container_width=True)

elif menu == "📅 DEVIS EXPRESS":
    st.markdown("<h2>Obtenir un Devis Gratuit</h2>", unsafe_allow_html=True)
    with st.form("devis_form"):
        nom = st.text_input("Nom du Projet")
        type_projet = st.multiselect("Services", ["Logo", "Flyers", "Cartes", "Autre"])
        details = st.text_area("Détails du besoin")
        submit = st.form_submit_button("🚀 Préparer mon devis")
        if submit:
            msg = f"Devis pour : {', '.join(type_projet)}. Projet : {nom}. Détails : {details}"
            link = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(msg)}"
            st.success("Cliquez ci-dessous pour envoyer")
            st.markdown(f"<a href='{link}' target='_blank'><div style='background:#38BDF8; color:white; padding:15px; text-align:center; border-radius:10px; font-weight:bold;'>ENVOYER SUR WHATSAPP</div></a>", unsafe_allow_html=True)

elif menu == "✉️ CONTACT":
    st.markdown("<h2>Contactez-nous</h2>", unsafe_allow_html=True)
    st.markdown(f'<div class="card">📍 {LOCATION}<br>📧 contact@chic-graphic.sn<br>📞 +221 77 861 59 00</div>', unsafe_allow_html=True)

# 6. FOOTER
st.markdown(f"""
    <div class="footer-pro">
        <div style="font-family:Syne; font-size:1.5rem; font-weight:800;">{BRAND_NAME}</div>
        <p>© 2026 · {LOCATION}</p>
    </div>
""", unsafe_allow_html=True)
