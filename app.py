import streamlit as st
import urllib.parse

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="CHIC Graphic & Print | Agence Créative",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="auto",
)

# 2. STYLE CSS (Barre Latérale + Optimisation Mobile)
st.markdown("""
    <style>
    /* Masquer les éléments inutiles de Streamlit */
    footer {visibility: hidden;}
    div[data-testid="stToolbar"] {display: none;}
    header {background: rgba(255,255,255,0);}

    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;700&display=swap');

    :root {
        --primary:  #38BDF8;
        --dark:     #0C4A6E;
        --bg-stats: #E0F2FE;
    }

    /* Style Global */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #ffffff;
        color: var(--dark);
    }

    /* --- STYLE DE LA BARRE LATÉRALE (SIDEBAR) --- */
    [data-testid="stSidebar"] {
        background-color: var(--dark) !important;
        border-right: 4px solid var(--primary);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Style des boutons radio du menu pour ressembler à des onglets */
    div.stRadio > div {
        gap: 10px;
    }

    /* --- ADAPTATION MOBILE & DESIGN --- */
    .hero {
        background: linear-gradient(135deg, #0C4A6E 0%, #075985 50%, #0369A1 100%);
        color: #fff;
        border-radius: 25px;
        padding: 40px 30px;
        margin-bottom: 30px;
        box-shadow: 0 15px 30px rgba(12, 74, 110, 0.2);
    }

    /* Taille de texte adaptable */
    .hero h1 { 
        font-family: 'Syne', sans-serif; 
        font-size: clamp(2rem, 8vw, 3.5rem); 
        font-weight: 800; 
        line-height: 1.1;
        margin-bottom: 20px;
    }

    .hero p {
        font-size: clamp(1rem, 4vw, 1.2rem);
        opacity: 0.9;
    }

    /* Style des Blocs de Stats (Adaptés du menu précédent) */
    .stat-box {
        background: var(--bg-stats);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border: 1px solid #bae6fd;
        margin-bottom: 15px;
    }
    .stat-num { 
        font-family: 'Syne', sans-serif; 
        font-size: 2rem; 
        font-weight: 800; 
        color: var(--dark); 
        display: block; 
    }

    .card {
        background: #fff;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.05);
        border: 1px solid #f0f9ff;
        margin-bottom: 20px;
    }

    /* Bouton WhatsApp Vert */
    .wa-button {
        background-color: #25D366;
        color: white !important;
        padding: 15px;
        border-radius: 12px;
        text-decoration: none;
        font-weight: 700;
        display: block;
        text-align: center;
        transition: 0.3s;
    }
    
    /* Correction pour mobile : Empêcher le débordement horizontal */
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# 3. BARRE LATÉRALE (SIDEBAR)
with st.sidebar:
    st.markdown(f"""
        <div style='text-align:center; padding-bottom:20px'>
            <h2 style='font-family:Syne; margin-bottom:0;'>CHIC</h2>
            <p style='color:var(--primary) !important; font-weight:700; font-size:0.8rem; letter-spacing:1px;'>GRAPHIC & PRINT</p>
        </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio(
        "MENU PRINCIPAL",
        ["🏠 ACCUEIL", "⚙️ SERVICES", "📸 RÉALISATIONS", "📅 DEVIS EXPRESS", "✉️ CONTACT"]
    )
    
    st.markdown("---")
    st.markdown("📍 Dakar, Sénégal")
    st.markdown("📞 +221 77 861 59 00")

# 4. LOGIQUE DES PAGES
if menu == "🏠 ACCUEIL":
    st.markdown(f"""
        <div class="hero">
            <h1>L'audace visuelle<br>au service de votre marque.</h1>
            <p>Solutions d'impression et de design haut de gamme à Dakar.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Utilisation de colonnes qui s'empilent sur mobile
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='stat-box'><span class='stat-num'>100%</span><b>Qualité HD</b></div>", unsafe_allow_html=True)
        st.markdown("<div class='stat-box'><span class='stat-num'>PRO</span><b>Expertise</b></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='stat-box'><span class='stat-num'>24h</span><b>Livraison</b></div>", unsafe_allow_html=True)
        st.markdown("<div class='stat-box'><span class='stat-num'>Dakar</span><b>Local</b></div>", unsafe_allow_html=True)

elif menu == "⚙️ SERVICES":
    st.markdown("<h2 style='font-family:Syne;'>Nos Services</h2>", unsafe_allow_html=True)
    services = [
        ("🎨", "Branding", "Logos et identités visuelles."),
        ("🖨️", "Print", "Flyers et cartes de visite."),
        ("📦", "Packaging", "Emballages personnalisés."),
        ("🏢", "Signalétique", "Enseignes et vitrines.")
    ]
    for icon, title, desc in services:
        st.markdown(f'<div class="card"><span style="font-size:2rem">{icon}</span><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)

elif menu == "📸 RÉALISATIONS":
    st.markdown("<h2 style='font-family:Syne;'>Portfolio</h2>", unsafe_allow_html=True)
    photos = ["photo10.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg", "photo5.jpg", "photo6.jpg", "photo7.jpg", "photo8.jpg", "photo9.jpg"]
    # Sur mobile, une seule colonne est préférable
    for p in photos:
        st.image(p, use_container_width=True)

elif menu == "📅 DEVIS EXPRESS":
    st.markdown("<h2 style='font-family:Syne;'>Demander un Devis</h2>", unsafe_allow_html=True)
    with st.form("devis_mobile"):
        nom = st.text_input("Votre nom")
        service = st.multiselect("Service", ["Branding", "Print", "Packaging", "Signalétique"])
        submit = st.form_submit_button("🚀 Valider")
        
        if submit:
            msg = f"Bonjour, je souhaite un devis pour {', '.join(service)} au nom de {nom}."
            url = f"https://wa.me/221778615900?text={urllib.parse.quote(msg)}"
            st.markdown(f'<a href="{url}" target="_blank" class="wa-button">ENVOYER VIA WHATSAPP</a>', unsafe_allow_html=True)

elif menu == "✉️ CONTACT":
    st.markdown("<h2 style='font-family:Syne;'>Contactez-nous</h2>", unsafe_allow_html=True)
    st.markdown('<div class="card">📍 Dakar, Sénégal<br>📧 contact@chic-graphic.sn<br>📞 +221 77 861 59 00</div>', unsafe_allow_html=True)
