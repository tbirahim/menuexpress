import streamlit as st
import urllib.parse

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="CHIC Graphic & Print | Agence Créative",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded", # Le menu est ouvert au départ
)

# 2. STYLE CSS (Réajusté pour laisser apparaître le bouton Menu)
st.markdown("""
    <style>
    /* On ne cache plus l'en-tête (Header) pour laisser le bouton de menu (les 3 traits) visible */
    footer {visibility: hidden;}
    div[data-testid="stToolbar"] {display: none;}
    
    /* On stylise le bouton de menu pour qu'il soit plus visible */
    button[kind="headerNoPadding"] {
        background-color: #0C4A6E !important;
        color: white !important;
        border-radius: 5px;
    }

    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    :root {
        --primary:  #38BDF8;
        --secondary: #0284C7;
        --dark:     #0C4A6E;
        --light:    #FFFFFF;
        --bg-alt:   #E0F2FE;
        --radius:   20px;
    }

    /* Style de la barre latérale */
    section[data-testid="stSidebar"] {
        background-color: #0C4A6E !important;
        border-right: 4px solid var(--primary);
    }
    
    section[data-testid="stSidebar"] * { 
        color: white !important; 
    }

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
        padding: 80px 50px;
        margin-bottom: 50px;
        box-shadow: 0 25px 50px -12px rgba(12, 74, 110, 0.3);
    }
    .hero h1 { 
        font-family: 'Syne', sans-serif; 
        font-size: 3.5rem; 
        font-weight: 800; 
        margin-bottom: 20px; 
        line-height: 1.1;
        color: white;
    }

    .card {
        background: #fff;
        border-radius: var(--radius);
        padding: 35px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        border: 1px solid #f0f9ff;
        transition: 0.3s;
        height: 100%;
    }

    .stat-box {
        background: white;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border: 1px solid #E0F2FE;
    }
    .stat-num { font-family: 'Syne', sans-serif; font-size: 2.2rem; font-weight: 800; color: var(--secondary); display: block; }
    
    .footer-pro {
        background: var(--dark);
        color: #fff;
        border-radius: 25px;
        padding: 40px;
        margin-top: 60px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 3. DONNÉES
BRAND_NAME = "CHIC Graphic & Print"
WHATSAPP_NUMBER = "221778615900" 
LOCATION = "Dakar, Sénégal"

# 4. BARRE LATÉRALE (Contrôlable par l'utilisateur)
with st.sidebar:
    st.markdown(f"""
        <div style='text-align:center; padding:20px 0'>
            <div style='font-family:Syne; font-size:1.8rem; font-weight:800; line-height:1;'>CHIC<br><span style='color:#38BDF8; font-size:1.2rem'>Graphic & Print</span></div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("NAVIGATION", ["🏠 ACCUEIL", "⚙️ SERVICES", "📸 RÉALISATIONS", "📅 DEVIS EXPRESS", "✉️ CONTACT"])
    st.markdown("---")
    st.markdown(f"<div style='text-align:center; opacity:0.7'>📍 {LOCATION}</div>", unsafe_allow_html=True)

# 5. PAGES
if menu == "🏠 ACCUEIL":
    st.markdown(f"""
        <div class="hero">
            <h1>L'audace visuelle<br>au service de votre marque.</h1>
            <p>CHIC Graphic & Print fusionne créativité et précision technique pour offrir des solutions d'impression et de design qui marquent les esprits à Dakar.</p>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    stats = [("100%", "Qualité"), ("24h", "Livraison"), ("PRO", "Design"), ("Dakar", "Local")]
    for col, (val, label) in zip([c1, c2, c3, c4], stats):
        col.markdown(f"<div class='stat-box'><span class='stat-num'>{val}</span><span style='font-weight:600; color:#64A4C4'>{label}</span></div>", unsafe_allow_html=True)

elif menu == "⚙️ SERVICES":
    st.markdown("<h2 style='font-size:2.5rem'>Nos Expertises</h2><br>", unsafe_allow_html=True)
    services = [
        ("🎨", "Branding", "Logos et identités visuelles."),
        ("🖨️", "Print", "Flyers, cartes et brochures."),
        ("📦", "Packaging", "Emballages sur-mesure."),
        ("🏢", "Signalétique", "Enseignes et vitrines.")
    ]
    cols = st.columns(2)
    for i, (icon, title, desc) in enumerate(services):
        with cols[i % 2]:
            st.markdown(f'<div class="card"><div style="font-size:2.5rem">{icon}</div><h3>{title}</h3><p>{desc}</p></div><br>', unsafe_allow_html=True)

elif menu == "📸 RÉALISATIONS":
    st.markdown("<h2 style='font-size:2.5rem'>Notre Portfolio</h2><br>", unsafe_allow_html=True)
    # Liste de tes photos sur GitHub
    photos = ["photo10.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg", "photo5.jpg", 
              "photo6.jpg", "photo7.jpg", "photo8.jpg", "photo9.jpg"]
    col1, col2 = st.columns(2)
    for i, p in enumerate(photos):
        try:
            if i % 2 == 0:
                col1.image(p, use_container_width=True)
            else:
                col2.image(p, use_container_width=True)
        except:
            st.warning(f"Image {p} non trouvée.")

elif menu == "📅 DEVIS EXPRESS":
    st.markdown("<h2>Lancez votre projet</h2>", unsafe_allow_html=True)
    with st.form("devis_form"):
        nom = st.text_input("Projet")
        type_p = st.multiselect("Services", ["Branding", "Print", "Packaging", "Signalétique"])
        details = st.text_area("Détails")
        if st.form_submit_button("🚀 Envoyer"):
            msg = f"Devis pour : {', '.join(type_p)}. Projet : {nom}. Détails : {details}"
            link = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(msg)}"
            st.markdown(f"<a href='{link}' target='_blank' style='text-decoration:none;'><div style='background:#38BDF8; color:white; padding:15px; text-align:center; border-radius:10px; font-weight:bold;'>ENVOYER SUR WHATSAPP</div></a>", unsafe_allow_html=True)

elif menu == "✉️ CONTACT":
    st.markdown("<h2>Contact</h2>", unsafe_allow_html=True)
    st.markdown(f'<div class="card">📍 {LOCATION}<br>📧 contact@chic-graphic.sn<br>📞 +221 77 861 59 00</div>', unsafe_allow_html=True)

# 6. FOOTER
st.markdown(f"""
    <div class="footer-pro">
        <div style="font-family:Syne; font-size:1.5rem; font-weight:800;">{BRAND_NAME}</div>
        <p>© 2026 · {LOCATION}</p>
    </div>
""", unsafe_allow_html=True)
