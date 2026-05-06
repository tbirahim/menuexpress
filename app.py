import streamlit as st
import urllib.parse

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="CHIC Graphic & Print | Agence Créative",
    page_icon="🎨",
    layout="wide",
)

# 2. STYLE CSS (Menu Haut avec design "Stat Boxes")
st.markdown("""
    <style>
    footer {visibility: hidden;}
    div[data-testid="stToolbar"] {display: none;}
    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}

    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    :root {
        --primary:  #38BDF8;
        --secondary: #0284C7;
        --dark:     #0C4A6E;
        --light:    #FFFFFF;
        --bg-alt:   #E0F2FE;
        --radius:   20px;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: var(--light);
        color: var(--dark);
    }

    /* --- BARRE DE NAVIGATION EN HAUT --- */
    .nav-top {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: #0C4A6E;
        padding: 15px 0;
        z-index: 9999;
        border-bottom: 3px solid #38BDF8;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }

    /* Style des boutons du menu inspiré des Stat Boxes */
    div.stButton > button {
        background-color: var(--bg-alt) !important; /* Fond bleu très clair comme les stats */
        color: var(--secondary) !important;       /* Texte bleu foncé comme les stats */
        border: 1px solid #E0F2FE !important;
        border-radius: 12px !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 800 !important;
        font-size: 0.9rem !important;
        width: 100% !important;
        transition: 0.3s !important;
        height: 45px !important;
    }

    div.stButton > button:hover {
        background-color: var(--primary) !important;
        color: white !important;
        transform: translateY(-2px);
    }

    .main-content {
        margin-top: 100px;
    }

    /* Hero Section */
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
        line-height: 1.1;
        color: white;
    }

    .card {
        background: #fff;
        border-radius: var(--radius);
        padding: 35px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        border: 1px solid #f0f9ff;
    }

    /* Les Stat Boxes originales */
    .stat-box {
        background: var(--bg-alt);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border: 1px solid #E0F2FE;
    }
    .stat-num { font-family: 'Syne', sans-serif; font-size: 2.2rem; font-weight: 800; color: var(--secondary); display: block; }
    
    .wa-button {
        background-color: #25D366;
        color: white !important;
        padding: 15px;
        border-radius: 10px;
        text-decoration: none;
        font-weight: bold;
        display: block;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 3. GESTION DE LA NAVIGATION
if 'page' not in st.session_state:
    st.session_state.page = "🏠 ACCUEIL"

def set_page(name):
    st.session_state.page = name

# 4. BARRE DE NAVIGATION EN HAUT
st.markdown('<div class="nav-top">', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
with c1: st.button("ACCUEIL", on_click=set_page, args=("🏠 ACCUEIL",))
with c2: st.button("SERVICES", on_click=set_page, args=("⚙️ SERVICES",))
with c3: st.button("PROJETS", on_click=set_page, args=("📸 RÉALISATIONS",))
with c4: st.button("DEVIS", on_click=set_page, args=("📅 DEVIS EXPRESS",))
with c5: st.button("CONTACT", on_click=set_page, args=("✉️ CONTACT",))
st.markdown('</div>', unsafe_allow_html=True)

# 5. CONTENU PRINCIPAL
st.markdown('<div class="main-content">', unsafe_allow_html=True)

menu = st.session_state.page

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
    st.markdown("<h2 style='font-family:Syne; font-size:2.5rem'>Nos Expertises</h2><br>", unsafe_allow_html=True)
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
    st.markdown("<h2 style='font-family:Syne; font-size:2.5rem'>Portfolio</h2><br>", unsafe_allow_html=True)
    photos = ["photo10.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg", "photo5.jpg", 
              "photo6.jpg", "photo7.jpg", "photo8.jpg", "photo9.jpg"]
    col1, col2 = st.columns(2)
    for i, p in enumerate(photos):
        if i % 2 == 0: col1.image(p, use_container_width=True)
        else: col2.image(p, use_container_width=True)

elif menu == "📅 DEVIS EXPRESS":
    st.markdown("<h2 style='font-family:Syne;'>Lancer votre projet</h2>", unsafe_allow_html=True)
    with st.form("devis_form"):
        nom = st.text_input("Projet / Entreprise")
        type_p = st.multiselect("Services", ["Branding", "Print", "Packaging", "Signalétique"])
        details = st.text_area("Détails")
        submit = st.form_submit_button("🚀 Valider")
        if submit:
            msg = f"Bonjour CHIC G&P, je souhaite un devis pour : {', '.join(type_p)}. Projet : {nom}."
            link = f"https://wa.me/221778615900?text={urllib.parse.quote(msg)}"
            st.markdown(f"<a href='{link}' target='_blank' class='wa-button'>ENVOYER SUR WHATSAPP</a>", unsafe_allow_html=True)

elif menu == "✉️ CONTACT":
    st.markdown("<h2 style='font-family:Syne;'>Contact</h2>", unsafe_allow_html=True)
    st.markdown(f'<div class="card">📍 Dakar, Sénégal<br>📧 contact@chic-graphic.sn<br>📞 +221 77 861 59 00</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
