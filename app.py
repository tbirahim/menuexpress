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
    page_title="CHIC Graphic & Print | Expertise Visuelle",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CONSTANTES CENTRALES
# ─────────────────────────────────────────────
BRAND_NAME = "CHIC Graphic & Print"
WHATSAPP_NUMBER = "221788377676"
EMAIL = "contact@chic-graphic.sn"
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
    --primary:  #38BDF8;
    --secondary: #0284C7;
    --dark:     #0C4A6E;
    --light:    #FFFFFF;
    --bg-alt:   #E0F2FE;
    --muted:    #64A4C4;
    --radius:   14px;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--light);
    color: var(--dark);
}

h1, h2, h3 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
}

/* ── Sidebar ───────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0C4A6E 0%, #075985 100%) !important;
    border-right: 3px solid var(--primary);
}
section[data-testid="stSidebar"] * {
    color: var(--light) !important;
}

/* ── Cards ─────────────────────────────────── */
.card {
    background: #fff;
    border-radius: var(--radius);
    padding: 24px;
    box-shadow: 0 8px 30px rgba(2,132,199,0.12);
    border: 1px solid #eee;
    transition: transform 0.25s;
    height: 100%;
}
.card:hover {
    transform: translateY(-6px);
    border-color: var(--primary);
}

/* ── Hero ───────────────────────────────────── */
.hero {
    background: linear-gradient(135deg, #0C4A6E 0%, #075985 60%, #0369A1 100%);
    color: #fff;
    border-radius: 20px;
    padding: 60px 40px;
    margin-bottom: 40px;
}
.hero h1 { font-size: 3rem; margin-bottom: 10px; color: #fff; }

/* ── UI Elements ───────────────────────────── */
.section-title { font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 800; }
.divider { width: 48px; height: 4px; background: linear-gradient(90deg, var(--primary), var(--secondary)); border-radius: 4px; margin: 10px 0 25px; }

.stat { background: var(--bg-alt); border-radius: 12px; padding: 20px; text-align: center; }
.stat .num { font-size: 2rem; font-weight: 800; color: var(--secondary); }

/* ── Footer ──────────────────────────────────── */
.footer { background: var(--dark); color: #BAE6FD; border-radius: var(--radius); padding: 30px; margin-top: 50px; text-align: center; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def render_header(title, sub=""):
    st.markdown(f"<div class='section-title'>{title}</div><div class='divider'></div>", unsafe_allow_html=True)
    if sub: st.markdown(f"<p style='color:var(--muted); margin-bottom:30px'>{sub}</p>", unsafe_allow_html=True)

def generate_wa_link(msg):
    return f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(msg)}"

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"<div style='text-align:center;padding:20px 0'><div style='font-family:Syne,sans-serif;font-size:1.4rem;font-weight:800;line-height:1.1'>{BRAND_NAME}</div><div style='font-size:0.8rem; opacity:0.7; margin-top:5px'>GRAPHISME & IMPRESSION</div></div>", unsafe_allow_html=True)
    menu = st.radio("Navigation", ["🏠 Accueil", "⚙️ Services", "📅 Devis Express", "🗂️ Portfolio", "✉️ Contact"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown(f"📍 {LOCATION}\n\n📧 {EMAIL}")

# ─────────────────────────────────────────────
# PAGES
# ─────────────────────────────────────────────
if menu == "🏠 Accueil":
    st.markdown(f"""<div class="hero"><h1>Donnez du relief à vos idées ✦</h1><p>{BRAND_NAME} : Votre partenaire premium pour toute création graphique et impression haute définition à Dakar.</p></div>""", unsafe_allow_html=True)
    
    render_header("Pourquoi nous choisir ?")
    c1, c2, c3, c4 = st.columns(4)
    for col, (n, d) in zip([c1, c2, c3, c4], [("100%", "Qualité"), ("24h", "Réactivité"), ("PRO", "Design"), ("HD", "Impression")]):
        col.markdown(f"<div class='stat'><div class='num'>{n}</div><div style='font-weight:700'>{d}</div></div>", unsafe_allow_html=True)

elif menu == "⚙️ Services":
    render_header("Nos Solutions", "De la conception à l'impression finale.")
    services = [
        ("🎨", "Identité Visuelle", "Logos, charte graphique et branding complet."),
        ("🖨️", "Supports Print", "Flyers, affiches, cartes de visite de haute qualité."),
        ("📦", "Packaging", "Design d'emballages innovants pour vos produits."),
        ("🏢", "Signalétique", "Habillage de vitrines, enseignes et stands."),
        ("👕", "Textile & Objets", "Personnalisation de t-shirts et cadeaux d'entreprise."),
        ("🌐", "Web Design", "Maquettes UI/UX et interfaces modernes.")
    ]
    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(services):
        with cols[i % 3]:
            st.markdown(f"<div class='card'><div style='font-size:2rem'>{icon}</div><h3 style='margin:10px 0'>{title}</h3><p style='font-size:0.9rem; color:var(--muted)'>{desc}</p></div><br>", unsafe_allow_html=True)

elif menu == "📅 Devis Express":
    render_header("Demande de devis", "Réponse rapide garantie via WhatsApp.")
    c1, c2 = st.columns([2, 1])
    with c1:
        type_p = st.selectbox("Type de projet", ["Identité Visuelle / Logo", "Impression (Flyer, Affiche...)", "Packaging", "Autre"])
        nom = st.text_input("Nom de votre entreprise / projet")
        detail = st.text_area("Description de vos besoins")
        if st.button("🚀 Obtenir mon devis sur WhatsApp"):
            msg = f"Bonjour {BRAND_NAME} !\n\nJe souhaite un devis pour :\nProjet : {type_p}\nClient : {nom}\nDétails : {detail}"
            st.markdown(f"[👉 Cliquez ici pour envoyer sur WhatsApp]({generate_wa_link(msg)})")
    with c2:
        st.markdown(f"""<div class='card'><h4>Processus</h4><ol style='font-size:0.85rem; color:var(--muted)'><li>Envoi de la demande</li><li>Briefing rapide</li><li>Estimation gratuite</li><li>Lancement du projet</li></ol></div>""", unsafe_allow_html=True)

elif menu == "🗂️ Portfolio":
    render_header("Portfolio", "Nos dernières réalisations marquantes.")
    st.info("Mise à jour de la galerie en cours... Revenez très bientôt !")

elif menu == "✉️ Contact":
    render_header("Contact", "Parlons de votre prochain succès.")
    with st.form("contact"):
        name = st.text_input("Nom complet")
        email = st.text_input("Email")
        message = st.text_area("Message")
        if st.form_submit_button("Envoyer"):
            st.success("Merci ! Votre message a bien été reçu. Nous reviendrons vers vous très vite.")

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown(f"<div class='footer'><strong>{BRAND_NAME}</strong><br><span style='font-size:0.8rem; opacity:0.6'>© 2026 · Excellence en Graphisme & Impression · {LOCATION}</span></div>", unsafe_allow_html=True)
