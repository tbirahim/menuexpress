import streamlit as st
import urllib.parse

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="CHIC Graphic & Print | Agence Créative",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="auto",
)

# 2. STYLE CSS (Barre Latérale + Optimisation Mobile + Glassmorphism)
st.markdown("""
    <style>
    /* Masquer les éléments natifs */
    footer {visibility: hidden;}
    div[data-testid="stToolbar"] {display: none;}
    
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;700&display=swap');

    :root {
        --primary:  #38BDF8;
        --dark:     #0C4A6E;
        --bg-stats: #E0F2FE;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #ffffff;
    }

    /* --- SIDEBAR DESIGN --- */
    [data-testid="stSidebar"] {
        background-color: var(--dark) !important;
        border-right: 4px solid var(--primary);
    }
    [data-testid="stSidebar"] * { color: white !important; }

    /* --- HERO SECTION ADAPTABLE --- */
    .hero {
        background: linear-gradient(135deg, #0C4A6E 0%, #075985 50%, #0369A1 100%);
        color: #fff;
        border-radius: 25px;
        padding: clamp(30px, 5vw, 60px);
        margin-bottom: 30px;
        box-shadow: 0 20px 40px rgba(12, 74, 110, 0.2);
    }
    .hero h1 { 
        font-family: 'Syne', sans-serif; 
        font-size: clamp(2.2rem, 7vw, 4rem); 
        font-weight: 800; 
        line-height: 1;
        margin-bottom: 20px;
    }

    /* --- STATS BLOCKS (Design demandé) --- */
    .stat-box {
        background: var(--bg-stats);
        border-radius: 18px;
        padding: 25px 15px;
        text-align: center;
        border: 1px solid #bae6fd;
        margin-bottom: 20px;
        transition: 0.3s ease;
    }
    .stat-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(56, 189, 248, 0.15);
    }
    .stat-num { 
        font-family: 'Syne', sans-serif; 
        font-size: 2.2rem; 
        font-weight: 800; 
        color: var(--dark); 
        display: block; 
    }

    /* --- CARTES SERVICES --- */
    .card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.03);
        border: 1px solid #f0f9ff;
        margin-bottom: 25px;
    }

    /* BOUTON WHATSAPP PREMIUM */
    .wa-button {
        background: linear-gradient(90deg, #25D366, #128C7E);
        color: white !important;
        padding: 18px;
        border-radius: 15px;
        text-decoration: none;
        font-weight: 700;
        display: block;
        text-align: center;
        box-shadow: 0 10px 20px rgba(37, 211, 102, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# 3. SIDEBAR (MENU LATÉRAL)
with st.sidebar:
    st.markdown("<h1 style='font-family:Syne; text-align:center;'>CHIC</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#38BDF8 !important; font-weight:700;'>GRAPHIC & PRINT</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    menu = st.radio(
        "NAVIGATION",
        ["🏠 ACCUEIL", "⚙️ SERVICES", "📸 RÉALISATIONS", "📅 DEVIS EXPRESS", "✉️ CONTACT"],
        label_visibility="collapsed"
    )
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("📍 Dakar, Sénégal")
    st.markdown("📞 +221 77 861 59 00")

# 4. CONTENU
if menu == "🏠 ACCUEIL":
    st.markdown(f"""
        <div class="hero">
            <h1>L'audace visuelle<br>au service de votre marque.</h1>
            <p style="opacity:0.9; max-width:650px; font-size:1.1rem;">
                Designers et imprimeurs passionnés basés à Dakar, nous transformons vos idées en supports percutants.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Grille de stats (2x2 sur mobile, 4x1 sur ordi)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown("<div class='stat-box'><span class='stat-num'>100%</span><b>Qualité HD</b></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='stat-box'><span class='stat-num'>24h</span><b>Livraison</b></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='stat-box'><span class='stat-num'>PRO</span><b>Expertise</b></div>", unsafe_allow_html=True)
    with c4: st.markdown("<div class='stat-box'><span class='stat-num'>Dakar</span><b>Local</b></div>", unsafe_allow_html=True)

elif menu == "⚙️ SERVICES":
    st.markdown("<h2 style='font-family:Syne;'>Expertises</h2>", unsafe_allow_html=True)
    colA, colB = st.columns(2)
    with colA:
        st.markdown('<div class="card"><h3>🎨 Branding</h3><p>Identité visuelle et logos uniques.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><h3>📦 Packaging</h3><p>Emballages produits sur-mesure.</p></div>', unsafe_allow_html=True)
    with colB:
        st.markdown('<div class="card"><h3>🖨️ Print</h3><p>Flyers, brochures et cartes premium.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><h3>🏢 Signalétique</h3><p>Enseignes et habillage de vitrines.</p></div>', unsafe_allow_html=True)

elif menu == "📸 RÉALISATIONS":
    st.markdown("<h2 style='font-family:Syne;'>Portfolio</h2>", unsafe_allow_html=True)
    # Liste de tes photos sur GitHub
    photos = ["photo10.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg", "photo5.jpg", "photo6.jpg", "photo7.jpg", "photo8.jpg", "photo9.jpg"]
    # Affichage en colonnes (3 sur ordi, s'ajuste sur mobile)
    cols = st.columns(3)
    for i, photo in enumerate(photos):
        cols[i % 3].image(photo, use_container_width=True)

elif menu == "📅 DEVIS EXPRESS":
    st.markdown("<h2 style='font-family:Syne;'>Votre Devis</h2>", unsafe_allow_html=True)
    with st.form("devis"):
        nom = st.text_input("Nom de l'entreprise")
        besoin = st.multiselect("Services", ["Logo", "Flyer", "Emballage", "Enseigne"])
        details = st.text_area("Détails")
        if st.form_submit_button("🚀 Lancer la demande"):
            msg = f"Bonjour CHIC G&P, je souhaite un devis pour {', '.join(besoin)} au nom de {nom}."
            st.markdown(f'<a href="https://wa.me/221778615900?text={urllib.parse.quote(msg)}" target="_blank" class="wa-button">FINALISER SUR WHATSAPP</a>', unsafe_allow_html=True)

elif menu == "✉️ CONTACT":
    st.markdown("<h2 style='font-family:Syne;'>Contact</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div class="card">
            <p>📍 Dakar, Sénégal</p>
            <p>📧 contact@chic-graphic.sn</p>
            <p>📞 +221 77 861 59 00</p>
            <p>⌚ Lun - Sam : 09h - 19h</p>
        </div>
    """, unsafe_allow_html=True)
