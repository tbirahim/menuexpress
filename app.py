import streamlit as st
import urllib.parse

# ─────────────────────────────────────────────
# 1. CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="CHIC Graphic & Print",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# 2. CSS GLOBAL — Design Premium
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & Variables ── */
:root {
    --navy:    #0C4A6E;
    --blue:    #0369A1;
    --cyan:    #38BDF8;
    --ice:     #E0F2FE;
    --white:   #FFFFFF;
    --text:    #0C4A6E;
    --muted:   #64748B;
    --radius:  18px;
    --shadow:  0 8px 32px rgba(12,74,110,0.12);
}

/* ── Hide Streamlit chrome ── */
header, footer,
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
#MainMenu { visibility: hidden !important; display: none !important; }

/* ── Global typography ── */
html, body, .stApp {
    font-family: 'DM Sans', sans-serif;
    background: #F0F9FF !important;
    color: var(--text) !important;
}

/* ── Mobile hamburger button ── */
button[data-testid="stSidebarCollapseButton"] {
    background: linear-gradient(135deg, var(--cyan), var(--blue)) !important;
    color: white !important;
    border-radius: 50% !important;
    width: 52px !important;
    height: 52px !important;
    position: fixed !important;
    top: 16px !important;
    left: 16px !important;
    z-index: 9999999 !important;
    box-shadow: 0 4px 20px rgba(56,189,248,0.45) !important;
    border: none !important;
}
button[data-testid="stSidebarCollapseButton"] svg {
    fill: white !important;
    width: 26px !important;
    height: 26px !important;
}

/* ─────────────────────────────────────────
   SIDEBAR
───────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A3D5C 0%, #0C4A6E 60%, #0369A1 100%) !important;
    border-right: none !important;
    box-shadow: 4px 0 30px rgba(3,105,161,0.3) !important;
}
[data-testid="stSidebar"] > div {
    padding: 0 !important;
}
[data-testid="stSidebar"] * {
    color: white !important;
}

/* Logo area */
.sidebar-logo {
    padding: 36px 24px 20px;
    text-align: center;
    border-bottom: 1px solid rgba(56,189,248,0.25);
    margin-bottom: 12px;
}
.sidebar-logo h1 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.4rem;
    letter-spacing: 4px;
    margin: 0;
    color: white !important;
    text-shadow: 0 0 30px rgba(56,189,248,0.6);
}
.sidebar-logo p {
    font-size: 0.72rem;
    letter-spacing: 3px;
    color: var(--cyan) !important;
    font-weight: 700;
    margin: 4px 0 0;
}

/* Nav radio ── style the labels */
[data-testid="stSidebar"] .stRadio > label {
    font-family: 'Syne', sans-serif;
    font-size: 0.78rem;
    letter-spacing: 3px;
    font-weight: 700;
    color: rgba(255,255,255,0.55) !important;
    padding: 0 24px;
    margin-bottom: 4px;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
    gap: 4px;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    background: transparent !important;
    border-radius: 12px !important;
    padding: 12px 20px !important;
    margin: 0 12px !important;
    transition: background 0.2s, transform 0.15s !important;
    cursor: pointer;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background: rgba(56,189,248,0.12) !important;
    transform: translateX(4px) !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-baseweb="radio"] span:first-child {
    border-color: var(--cyan) !important;
}

/* Sidebar footer info */
.sidebar-info {
    padding: 20px 24px;
    border-top: 1px solid rgba(56,189,248,0.2);
    margin-top: 16px;
}
.sidebar-info p {
    font-size: 0.82rem;
    color: rgba(255,255,255,0.7) !important;
    margin: 6px 0;
}

/* ─────────────────────────────────────────
   MAIN CONTENT AREA
───────────────────────────────────────── */
.block-container {
    padding: 3rem 2.5rem 2rem !important;
    max-width: 1100px;
}

/* ── HERO ── */
.hero {
    background: linear-gradient(135deg, #0C4A6E 0%, #0369A1 55%, #0EA5E9 100%);
    border-radius: 28px;
    padding: 56px 48px;
    color: white !important;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(12,74,110,0.35);
    animation: heroIn 0.7s cubic-bezier(.22,1,.36,1) both;
}
@keyframes heroIn {
    from { opacity:0; transform: translateY(24px); }
    to   { opacity:1; transform: translateY(0);    }
}
.hero::before {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 340px; height: 340px;
    background: radial-gradient(circle, rgba(56,189,248,0.22) 0%, transparent 70%);
    border-radius: 50%;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 30%;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(255,255,255,0.07) 0%, transparent 70%);
    border-radius: 50%;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: clamp(2rem, 5vw, 3.2rem);
    line-height: 1.15;
    margin: 0 0 16px;
    color: white !important;
    position: relative; z-index: 1;
}
.hero p {
    font-size: 1.05rem;
    opacity: 0.85;
    margin: 0 0 28px;
    position: relative; z-index: 1;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 50px;
    padding: 8px 20px;
    font-size: 0.82rem;
    letter-spacing: 1.5px;
    font-weight: 700;
    color: white !important;
    position: relative; z-index: 1;
}

/* ── STAT PILLS ── */
.stats-row {
    display: flex;
    gap: 16px;
    margin-top: 28px;
    flex-wrap: wrap;
}
.stat-pill {
    background: white;
    border-radius: 50px;
    padding: 14px 24px;
    flex: 1;
    min-width: 140px;
    text-align: center;
    box-shadow: var(--shadow);
    border: 1px solid rgba(56,189,248,0.2);
    animation: fadeUp 0.6s ease both;
}
.stat-pill:nth-child(1) { animation-delay: 0.1s; }
.stat-pill:nth-child(2) { animation-delay: 0.2s; }
.stat-pill:nth-child(3) { animation-delay: 0.3s; }
@keyframes fadeUp {
    from { opacity:0; transform:translateY(16px); }
    to   { opacity:1; transform:translateY(0);    }
}
.stat-pill .num {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--blue);
    display: block;
}
.stat-pill .lbl {
    font-size: 0.75rem;
    color: var(--muted);
    letter-spacing: 1px;
    font-weight: 500;
}

/* ── PAGE TITLE ── */
.page-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2rem;
    color: var(--navy);
    margin: 0 0 6px;
    letter-spacing: -0.5px;
}
.page-subtitle {
    color: var(--muted);
    font-size: 0.92rem;
    margin: 0 0 28px;
}
.cyan-line {
    width: 48px;
    height: 4px;
    background: linear-gradient(90deg, var(--cyan), var(--blue));
    border-radius: 4px;
    margin-bottom: 28px;
}

/* ── SERVICE CARDS ── */
.service-card {
    background: white;
    border-radius: var(--radius);
    padding: 28px;
    border: 1.5px solid var(--ice);
    box-shadow: var(--shadow);
    margin-bottom: 18px;
    transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
    display: flex;
    gap: 20px;
    align-items: flex-start;
    animation: fadeUp 0.5s ease both;
}
.service-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 48px rgba(12,74,110,0.16);
    border-color: var(--cyan);
}
.service-icon {
    font-size: 2rem;
    width: 56px;
    height: 56px;
    background: var(--ice);
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.service-body h3 {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.05rem;
    margin: 0 0 6px;
    color: var(--navy);
}
.service-body p {
    font-size: 0.88rem;
    color: var(--muted);
    margin: 0;
    line-height: 1.6;
}
.service-tag {
    display: inline-block;
    background: var(--ice);
    color: var(--blue);
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-top: 8px;
}

/* ── PORTFOLIO GRID ── */
.portfolio-img {
    border-radius: var(--radius);
    overflow: hidden;
    box-shadow: var(--shadow);
    position: relative;
}

/* ── FORM ELEMENTS ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    border: 1.5px solid #BAE6FD !important;
    border-radius: 12px !important;
    background: white !important;
    color: var(--navy) !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 12px 16px !important;
    transition: border-color 0.2s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.15) !important;
}
.stMultiSelect > div {
    border: 1.5px solid #BAE6FD !important;
    border-radius: 12px !important;
    background: white !important;
}
.stFormSubmitButton > button {
    background: linear-gradient(135deg, var(--blue), var(--navy)) !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 14px 32px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    border: none !important;
    width: 100% !important;
    font-size: 0.95rem !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
    box-shadow: 0 4px 16px rgba(3,105,161,0.35) !important;
}
.stFormSubmitButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(3,105,161,0.45) !important;
}

/* ── CONTACT CARD ── */
.contact-card {
    background: white;
    border-radius: var(--radius);
    padding: 32px;
    border: 1.5px solid var(--ice);
    box-shadow: var(--shadow);
    margin-bottom: 16px;
}
.contact-item {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 0;
    border-bottom: 1px solid var(--ice);
    color: var(--navy);
    font-size: 0.95rem;
}
.contact-item:last-child { border-bottom: none; }
.contact-icon {
    width: 40px;
    height: 40px;
    background: var(--ice);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    flex-shrink: 0;
}

/* ── WA BUTTON ── */
.wa-btn {
    display: block;
    background: linear-gradient(135deg, #22C55E, #16A34A);
    color: white !important;
    text-align: center;
    border-radius: 14px;
    padding: 18px;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.5px;
    text-decoration: none !important;
    box-shadow: 0 6px 24px rgba(34,197,94,0.4);
    transition: transform 0.2s, box-shadow 0.2s;
    margin-top: 8px;
}
.wa-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 32px rgba(34,197,94,0.5);
    color: white !important;
}

/* ── INFO BOXES ── */
.info-box {
    background: white;
    border-left: 4px solid var(--cyan);
    border-radius: 0 var(--radius) var(--radius) 0;
    padding: 16px 20px;
    box-shadow: var(--shadow);
    font-size: 0.9rem;
    color: var(--navy);
    font-weight: 500;
}

/* ── SECTION DIVIDER ── */
.section-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, var(--ice), transparent);
    margin: 24px 0;
}

/* ── RESPONSIVE ── */
@media (max-width: 768px) {
    .block-container { padding: 4rem 1rem 2rem !important; }
    .hero { padding: 36px 24px; }
    .stats-row { gap: 10px; }
    .service-card { flex-direction: column; }
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 3. SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div class="sidebar-logo">
            <h1>CHIC</h1>
            <p>GRAPHIC &amp; PRINT</p>
        </div>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "NAVIGATION",
        ["🏠  ACCUEIL", "⚙️  SERVICES", "📸  RÉALISATIONS", "📅  DEVIS EXPRESS", "✉️  CONTACT"],
        label_visibility="visible"
    )

    st.markdown("""
        <div class="sidebar-info">
            <p>📍 &nbsp;Dakar, Sénégal</p>
            <p>📞 &nbsp;+221 77 861 59 00</p>
            <p>📧 &nbsp;contact@chic-graphic.sn</p>
        </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 4. PAGES
# ─────────────────────────────────────────────

# ── ACCUEIL ──────────────────────────────────
if menu == "🏠  ACCUEIL":
    st.markdown("""
    <div class="hero">
        <span class="hero-badge">✦ &nbsp;DAKAR · SÉNÉGAL</span>
        <h1>L'audace visuelle<br>au service de votre marque.</h1>
        <p>Design &amp; Impression Premium · Identité, Print, Packaging.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="stats-row">
        <div class="stat-pill">
            <span class="num">500+</span>
            <span class="lbl">PROJETS LIVRÉS</span>
        </div>
        <div class="stat-pill">
            <span class="num">24h</span>
            <span class="lbl">DÉLAI LIVRAISON</span>
        </div>
        <div class="stat-pill">
            <span class="num">100%</span>
            <span class="lbl">QUALITÉ HD</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="info-box">🎨 &nbsp;<strong>Branding sur-mesure</strong> — Logos, chartes graphiques, déclinaisons print & digital.</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="info-box">🖨️ &nbsp;<strong>Impression haute définition</strong> — Flyers, bâches, affiches, packaging.</div>', unsafe_allow_html=True)

# ── SERVICES ─────────────────────────────────
elif menu == "⚙️  SERVICES":
    st.markdown('<p class="page-title">Nos Services</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Des solutions graphiques complètes pour votre image de marque.</p>', unsafe_allow_html=True)
    st.markdown('<div class="cyan-line"></div>', unsafe_allow_html=True)

    services = [
        ("🎨", "Branding & Identité", "Création de logos, chartes graphiques et systèmes visuels cohérents qui reflètent l'ADN de votre marque.", "LOGO · CHARTE · GUIDELINES"),
        ("🖨️", "Print & Imprimerie", "Flyers, cartes de visite, brochures, affiches et catalogues imprimés en haute définition.", "FLYER · CARTE · AFFICHE"),
        ("📦", "Packaging Design", "Conception d'emballages personnalisés qui séduisent en rayon et renforcent la perception premium.", "BOÎTE · ÉTIQUETTE · SACHET"),
        ("🪟", "Enseignes & Bâches", "Signalétique extérieure, bâches publicitaires et enseignes lumineuses pour une visibilité maximale.", "BÂCHE · ENSEIGNE · KAKÉMONO"),
        ("📱", "Digital & Réseaux", "Visuels pour Instagram, Facebook, LinkedIn — contenus optimisés pour chaque plateforme.", "POSTS · STORIES · BANNIÈRES"),
    ]

    for icon, title, desc, tags in services:
        st.markdown(f"""
        <div class="service-card">
            <div class="service-icon">{icon}</div>
            <div class="service-body">
                <h3>{title}</h3>
                <p>{desc}</p>
                <span class="service-tag">{tags}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── RÉALISATIONS ─────────────────────────────
elif menu == "📸  RÉALISATIONS":
    st.markdown('<p class="page-title">Portfolio</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Quelques-unes de nos créations récentes.</p>', unsafe_allow_html=True)
    st.markdown('<div class="cyan-line"></div>', unsafe_allow_html=True)

    photos = ["photo2.jpg", "photo3.jpg", "photo4.jpg", "photo10.jpg"]
    cols = st.columns(2)
    for i, p in enumerate(photos):
        try:
            cols[i % 2].image(p, use_container_width=True)
        except Exception:
            cols[i % 2].markdown(
                f'<div style="background:var(--ice);height:200px;border-radius:14px;display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:0.85rem;margin-bottom:16px;">Image : {p}</div>',
                unsafe_allow_html=True
            )

# ── DEVIS EXPRESS ─────────────────────────────
elif menu == "📅  DEVIS EXPRESS":
    st.markdown('<p class="page-title">Devis Express</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Remplissez le formulaire — nous vous répondons sous 2h.</p>', unsafe_allow_html=True)
    st.markdown('<div class="cyan-line"></div>', unsafe_allow_html=True)

    col_form, col_info = st.columns([2, 1])

    with col_form:
        with st.form("form_devis", clear_on_submit=False):
            nom     = st.text_input("🏢  Nom de l'entreprise / Client *")
            tel     = st.text_input("📞  Numéro WhatsApp")
            services_list = st.multiselect(
                "⚙️  Services souhaités *",
                ["Logo & Branding", "Flyers & Print", "Packaging", "Enseigne & Bâche", "Digital & Réseaux"]
            )
            budget  = st.selectbox("💰  Budget estimatif", ["À définir", "< 50 000 FCFA", "50k – 150k FCFA", "150k – 500k FCFA", "> 500k FCFA"])
            details = st.text_area("📝  Décrivez votre projet", placeholder="Couleurs, formats, quantités, délai souhaité...", height=130)
            submitted = st.form_submit_button("🚀  Envoyer ma demande de devis")

            if submitted:
                if nom and services_list:
                    msg = (
                        f"Bonjour CHIC Graphic & Print 👋\n\n"
                        f"*Demande de devis*\n"
                        f"• Client : {nom}\n"
                        f"• Services : {', '.join(services_list)}\n"
                        f"• Budget : {budget}\n"
                        f"• Projet : {details if details else 'Non précisé'}"
                    )
                    url = f"https://wa.me/221778615900?text={urllib.parse.quote(msg)}"
                    st.markdown(f'<a href="{url}" target="_blank" class="wa-btn">💬 &nbsp;Ouvrir WhatsApp pour envoyer</a>', unsafe_allow_html=True)
                else:
                    st.error("⚠️  Veuillez renseigner le nom et choisir au moins un service.")

    with col_info:
        st.markdown("""
        <div class="contact-card" style="margin-top:0;">
            <div class="contact-item"><div class="contact-icon">⚡</div><div><strong>Réponse rapide</strong><br><span style="color:var(--muted);font-size:.82rem;">Sous 2h en semaine</span></div></div>
            <div class="contact-item"><div class="contact-icon">🔒</div><div><strong>Confidentiel</strong><br><span style="color:var(--muted);font-size:.82rem;">Vos infos restent privées</span></div></div>
            <div class="contact-item"><div class="contact-icon">✅</div><div><strong>Sans engagement</strong><br><span style="color:var(--muted);font-size:.82rem;">Devis 100% gratuit</span></div></div>
        </div>
        """, unsafe_allow_html=True)

# ── CONTACT ──────────────────────────────────
elif menu == "✉️  CONTACT":
    st.markdown('<p class="page-title">Contactez-nous</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Nous sommes disponibles 7j/7 pour vos projets.</p>', unsafe_allow_html=True)
    st.markdown('<div class="cyan-line"></div>', unsafe_allow_html=True)

    c1, c2 = st.columns([3, 2])

    with c1:
        st.markdown("""
        <div class="contact-card">
            <div class="contact-item">
                <div class="contact-icon">📞</div>
                <div>
                    <strong>Téléphone / WhatsApp</strong><br>
                    <span>+221 77 861 59 00</span>
                </div>
            </div>
            <div class="contact-item">
                <div class="contact-icon">📧</div>
                <div>
                    <strong>Email</strong><br>
                    <span>contact@chic-graphic.sn</span>
                </div>
            </div>
            <div class="contact-item">
                <div class="contact-icon">📍</div>
                <div>
                    <strong>Adresse</strong><br>
                    <span>Dakar, Sénégal</span>
                </div>
            </div>
            <div class="contact-item">
                <div class="contact-icon">⏰</div>
                <div>
                    <strong>Horaires</strong><br>
                    <span>Lun – Sam : 8h00 – 20h00</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        wa_url = f"https://wa.me/221778615900?text={urllib.parse.quote('Bonjour CHIC Graphic & Print, je souhaite vous contacter.')}"
        st.markdown(f"""
        <div class="contact-card" style="text-align:center; padding: 36px 24px;">
            <div style="font-size:2.5rem; margin-bottom:12px;">💬</div>
            <p style="font-family:'Syne',sans-serif; font-weight:700; font-size:1rem; color:var(--navy); margin:0 0 6px;">Discussion directe</p>
            <p style="color:var(--muted); font-size:0.85rem; margin:0 0 20px;">Obtenez une réponse immédiate via WhatsApp.</p>
            <a href="{wa_url}" target="_blank" class="wa-btn">WhatsApp maintenant</a>
        </div>
        """, unsafe_allow_html=True)
