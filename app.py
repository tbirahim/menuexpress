import streamlit as st
import urllib.parse

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="CHIC Graphic & Print | Agence Créative",
    page_icon="🎨",
    layout="wide",
)

# 2. STYLE CSS (Barre Premium Intégrée)
st.markdown("""
    <style>
    footer {visibility: hidden;}
    div[data-testid="stToolbar"] {display: none;}
    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}

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

    /* --- LA NOUVELLE BARRE DE NAVIGATION --- */
    .nav-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: var(--dark);
        padding: 10px 0px;
        z-index: 9999;
        border-bottom: 4px solid var(--primary);
    }

    /* Style des boutons pour imiter les blocs 24h/Livraison */
    div.stButton > button {
        background-color: var(--bg-stats) !important;
        color: var(--dark) !important;
        border: none !important;
        border-radius: 12px !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 800 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        height: 45px !important;
        width: 100% !important;
    }

    div.stButton > button:hover {
        background-color: var(--primary) !important;
        color: white !important;
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(56, 189, 248, 0.4);
    }

    .main-content {
        margin-top: 110px;
    }

    /* Hero Section (Design de ta photo) */
    .hero {
        background: linear-gradient(135deg, #0C4A6E 0%, #075985 50%, #0369A1 100%);
        color: #fff;
        border-radius: 40px;
        padding: 70px 50px;
        margin-bottom: 40px;
        box-shadow: 0 20px 40px rgba(12, 74, 110, 0.2);
    }
    .hero h1 { 
        font-family: 'Syne', sans-serif; 
        font-size: 3.8rem; 
        font-weight: 800; 
        line-height: 1.1;
        margin-bottom: 25px;
    }

    .stat-box {
        background: var(--bg-stats);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border: 1px solid #bae6fd;
    }
    .stat-num { font-family: 'Syne', sans-serif; font-size: 2.2rem; font-weight: 800; color: var(--dark); display: block; }
    </style>
""", unsafe_allow_html=True)

# 3. LOGIQUE DE NAVIGATION
if 'page' not in st.session_state:
    st.session_state.page = "🏠 ACCUEIL"

def set_page(name):
    st.session_state.page = name

# 4. BARRE DE NAVIGATION (DANS LE HEADER FIXE)
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
# Centrage des boutons
_, center_col, _ = st.columns([1, 8, 1])
with center_col:
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
            <p style="font-size:1.2rem; opacity:0.9; max-width:700px;">
                CHIC Graphic & Print fusionne créativité et précision technique pour offrir des solutions 
                d'impression et de design qui marquent les esprits à Dakar.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    stats = [("100%", "Qualité HD"), ("24h", "Livraison"), ("PRO", "Expertise"), ("Dakar", "Local")]
    for col, (val, label) in zip([c1, c2, c3, c4], stats):
        col.markdown(f"<div class='stat-box'><span class='stat-num'>{val}</span><span style='font-weight:700; color:#0369A1'>{label}</span></div>", unsafe_allow_html=True)

elif menu == "📸 RÉALISATIONS":
    st.markdown("<h2 style='font-family:Syne; font-size:2.5rem'>Nos Réalisations</h2><br>", unsafe_allow_html=True)
    photos = [f"photo{i}.jpg" for i in range(2, 11)]
    cols = st.columns(3)
    for i, p in enumerate(photos):
        cols[i % 3].image(p, use_container_width=True)

# ... (les autres pages restent identiques)
st.markdown('</div>', unsafe_allow_html=True)
