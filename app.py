import streamlit as st
import re
import urllib.parse
import logging

# ─────────────────────────────────────────────
# CONFIGURATION ET JOURNALISATION
# ─────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Chic Chic ULTRA | Agence Créative",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CONSTANTES CENTRALES
# ─────────────────────────────────────────────
WHATSAPP_NUMBER = "221788377676"
EMAIL = "contact@chicchic.sn"
LOCATION = "Dakar, Sénégal"

# ─────────────────────────────────────────────
# GESTION D'ÉTAT (SESSION STATE)
# ─────────────────────────────────────────────
if "devis_nom" not in st.session_state:
    st.session_state.devis_nom = ""
if "devis_desc" not in st.session_state:
    st.session_state.devis_desc = ""

# ─────────────────────────────────────────────
# CSS GLOBAL
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --rouge:   #38BDF8;
    --bleu:    #0284C7;
    --noir:    #0C4A6E;
    --blanc:   #FFFFFF;
    --gris:    #E0F2FE;
    --muted:   #64A4C4;
    --radius:  14px;
    --shadow:  0 8px 30px rgba(2,132,199,0.12);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--blanc);
    color: var(--noir);
}

h1, h2, h3 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    letter-spacing: -0.02em;
}

/* ── Sidebar ───────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0C4A6E 0%, #075985 100%) !important;
    border-right: 3px solid var(--rouge);
}
section[data-testid="stSidebar"] * {
    color: var(--blanc) !important;
}
section[data-testid="stSidebar"] .stRadio label {
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    letter-spacing: 0.04em;
    padding: 6px 0;
    transition: color 0.2s;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    color: var(--rouge) !important;
}

/* ── Boutons ───────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, var(--rouge), var(--bleu));
    color: #fff !important;
    border: none;
    border-radius: var(--radius);
    padding: 0.65rem 1.6rem;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    letter-spacing: 0.05em;
    transition: transform 0.2s, box-shadow 0.2s;
    cursor: pointer;
}
.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 28px rgba(56,189,248,0.45);
}

/* ── Cards ─────────────────────────────────── */
.card {
    background: #fff;
    border-radius: var(--radius);
    padding: 24px;
    box-shadow: var(--shadow);
    border: 1px solid #eee;
    transition: transform 0.25s, box-shadow 0.25s;
    height: 100%;
}
.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.12);
    border-color: var(--rouge);
}
.card h3 { font-size: 1.05rem; margin: 0 0 8px; }
.card p  { font-size: 0.87rem; color: var(--muted); margin: 0; }

/* ── Hero ───────────────────────────────────── */
.hero {
    background: linear-gradient(135deg, #0C4A6E 0%, #075985 60%, #0369A1 100%);
    color: #fff;
    border-radius: 20px;
    padding: 64px 48px;
    margin-bottom: 40px;
    position: relative;
    overflow: hidden;
}
.hero h1 { font-size: 3rem; margin-bottom: 12px; color: #fff; }
.hero p  { font-size: 1.15rem; opacity: 0.75; max-width: 480px; }

/* ── Badge catégorie ────────────────────────── */
.badge {
    display: inline-block;
    background: linear-gradient(135deg, var(--rouge), var(--bleu));
    color: #fff;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 8px;
}

/* ── Section UI ──────────────────────────── */
.section-title { font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 800; margin-bottom: 6px; }
.section-sub { color: var(--muted); font-size: 0.95rem; margin-bottom: 32px; }
.divider { width: 48px; height: 4px; background: linear-gradient(90deg, var(--rouge), var(--bleu)); border-radius: 4px; margin: 10px 0 28px; }

.stat { background: var(--gris); border-radius: 12px; padding: 18px 24px; text-align: center; }
.stat .num { font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 800; background: linear-gradient(135deg, var(--rouge), var(--bleu)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.stat .desc { font-size: 0.82rem; color: var(--muted); margin-top: 4px; }

.testimonial { background: var(--gris); border-radius: var(--radius); padding: 24px; border-left: 4px solid var(--rouge); font-style: italic; color: #333; font-size: 0.93rem; }
.testimonial .author { font-style: normal; font-weight: 700; color: var(--noir); margin-top: 12px; font-size: 0.88rem; }

/* ── Footer ──────────────────────────────────── */
.footer { background: linear-gradient(135deg, #0C4A6E, #075985); color: #BAE6FD; border-radius: var(--radius); padding: 32px 40px; margin-top: 60px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; }
.footer a { color: #38BDF8; text-decoration: none; }
.footer .brand { font-family: 'Syne', sans-serif; font-size: 1.3rem; font-weight: 800; color: #fff; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def render_section_header(title: str, subtitle: str = ""):
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<div class='section-sub'>{subtitle}</div>", unsafe_allow_html=True)

def render_card(icon: str, title: str, desc: str):
    st.markdown(f"""
    <div class="card">
        <div style='font-size:2rem;margin-bottom:10px'>{icon}</div>
        <h3>{title}</h3>
        <p>{desc}</p>
    </div><br>
    """, unsafe_allow_html=True)

def generate_whatsapp_link(message: str, phone: str = WHATSAPP_NUMBER) -> str:
    encoded = urllib.parse.quote(message)
    return f"https://wa.me/{phone}?text={encoded}"

def validate_contact_form(name, phone, email, msg):
    errors = []
    if not name.strip(): errors.append("Le nom est requis.")
    if not phone.strip(): errors.append("Téléphone requis.")
    if not email.strip() or "@" not in email: errors.append("E-mail invalide.")
    if not msg.strip(): errors.append("Le message est requis.")
    return errors

# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_services():
    return {
        "🎨 Logo & Identité": {"icon": "🎨", "desc": "Création complète de votre identité de marque."},
        "🖨️ Flyer / Affiche": {"icon": "🖨️", "desc": "Supports print impactants pour vos campagnes."},
        "🌐 Site web":         {"icon": "🌐", "desc": "Site vitrine ou e-commerce clé en main."},
        "📦 Packaging":        {"icon": "📦", "desc": "Design d'emballage produit attractif et pro."},
        "📱 Social Media Kit": {"icon": "📱", "desc": "Pack visuel complet pour vos réseaux sociaux."},
        "📊 Présentation PPT": {"icon": "📊", "desc": "Slides professionnelles pour vos pitchs."},
    }

SERVICES = load_services()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"<div style='text-align:center;padding:16px 0 24px'><div style='font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;color:#fff;'>✦ Chic Chic<br><span style='color:#38BDF8'>ULTRA</span></div></div>", unsafe_allow_html=True)
    menu = st.radio("Navigation", ["🏠 Accueil", "⚙️ Services", "📅 Demander un Devis", "🗂️ Portfolio", "✉️ Contact"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown(f"**📍 {LOCATION}**\n📲 [WhatsApp](https://wa.me/{WHATSAPP_NUMBER})\n📧 {EMAIL}")

# ─────────────────────────────────────────────
# PAGES
# ─────────────────────────────────────────────
if menu == "🏠 Accueil":
    st.markdown("""<div class="hero"><h1>L'agence créative<br>qui fait la différence ✦</h1><p>Design · Branding · Impression · Marketing Digital</p></div>""", unsafe_allow_html=True)
    render_section_header("Nos résultats")
    cols = st.columns(4)
    stats = [("150+", "Projets"), ("98%", "Satisfaction"), ("5 ans", "Expertise"), ("24h", "Réactivité")]
    for col, (n, d) in zip(cols, stats):
        col.markdown(f"<div class='stat'><div class='num'>{n}</div><div class='desc'>{d}</div></div>", unsafe_allow_html=True)

elif menu == "⚙️ Services":
    render_section_header("Nos Services", "Des solutions sur mesure pour votre image.")
    cols = st.columns(3)
    for i, (name, info) in enumerate(SERVICES.items()):
        with cols[i % 3]:
            render_card(info['icon'], name.split(' ', 1)[1], info['desc'])

elif menu == "📅 Demander un Devis":
    render_section_header("Votre Projet", "Décrivez-nous vos besoins pour recevoir une proposition adaptée.")
    col1, col2 = st.columns([3, 2])
    with col1:
        svc = st.selectbox("📌 Service", list(SERVICES.keys()))
        nom = st.text_input("👤 Votre nom", key="devis_nom")
        desc = st.text_area("📝 Détails du projet", key="devis_desc", placeholder="Objectifs, supports souhaités...")
        if st.button("🚀 Envoyer ma demande via WhatsApp"):
            message = f"Bonjour Chic Chic ULTRA !\n\nJe souhaite un devis pour : {svc}\nNom : {nom}\nProjet : {desc}"
            st.markdown(f"[👉 Envoyer la demande]({generate_whatsapp_link(message)})")
    with col2:
        st.info("💡 Une réponse vous sera envoyée sous 24h avec une proposition tarifaire détaillée.")

elif menu == "🗂️ Portfolio":
    render_section_header("Portfolio", "Aperçu de nos dernières créations.")
    st.warning("Section en cours de mise à jour avec nos nouveaux visuels.")

elif menu == "✉️ Contact":
    render_section_header("Contact", "Une question ? Écrivez-nous.")
    with st.form("contact"):
        n = st.text_input("Nom complet")
        e = st.text_input("Email")
        m = st.text_area("Message")
        if st.form_submit_button("Envoyer"):
            errs = validate_contact_form(n, "00", e, m)
            if errs: [st.error(er) for er in errs]
            else: st.success("Message envoyé !"); st.balloons()

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown(f"<div class='footer'><div class='brand'>✦ Chic Chic ULTRA</div><div>© 2026 · {LOCATION}</div></div>", unsafe_allow_html=True)
