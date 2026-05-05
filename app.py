import streamlit as st
import re
from datetime import datetime

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Chic Chic ULTRA | Agence Créative",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CSS GLOBAL
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --rouge:   #E30613;
    --bleu:    #0020C2;
    --noir:    #0A0A0A;
    --blanc:   #FAFAFA;
    --gris:    #F2F2F0;
    --muted:   #888888;
    --radius:  14px;
    --shadow:  0 8px 30px rgba(0,0,0,0.09);
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
    background: var(--noir) !important;
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
    box-shadow: 0 12px 28px rgba(227,6,19,0.35);
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
    background: linear-gradient(135deg, var(--noir) 60%, #1a1a2e);
    color: #fff;
    border-radius: 20px;
    padding: 64px 48px;
    margin-bottom: 40px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(227,6,19,0.35), transparent 70%);
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: -40px;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0,32,194,0.30), transparent 70%);
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

/* ── Devis box ──────────────────────────────── */
.price-box {
    background: linear-gradient(135deg, var(--rouge), var(--bleu));
    color: #fff;
    border-radius: var(--radius);
    padding: 28px 32px;
    text-align: center;
}
.price-box .amount {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: -0.03em;
}
.price-box .label { font-size: 0.9rem; opacity: 0.85; margin-top: 4px; }

/* ── Stat chips ─────────────────────────────── */
.stat {
    background: var(--gris);
    border-radius: 12px;
    padding: 18px 24px;
    text-align: center;
}
.stat .num {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--rouge), var(--bleu));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.stat .desc { font-size: 0.82rem; color: var(--muted); margin-top: 4px; }

/* ── Section title ──────────────────────────── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    margin-bottom: 6px;
}
.section-sub {
    color: var(--muted);
    font-size: 0.95rem;
    margin-bottom: 32px;
}

/* ── Divider ─────────────────────────────────── */
.divider {
    width: 48px; height: 4px;
    background: linear-gradient(90deg, var(--rouge), var(--bleu));
    border-radius: 4px;
    margin: 10px 0 28px;
}

/* ── Témoignages ─────────────────────────────── */
.testimonial {
    background: var(--gris);
    border-radius: var(--radius);
    padding: 24px;
    border-left: 4px solid var(--rouge);
    font-style: italic;
    color: #333;
    font-size: 0.93rem;
}
.testimonial .author {
    font-style: normal;
    font-weight: 700;
    color: var(--noir);
    margin-top: 12px;
    font-size: 0.88rem;
}

/* ── Formulaire ──────────────────────────────── */
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    border-radius: 10px !important;
    border: 1.5px solid #ddd !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: border-color 0.2s !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--rouge) !important;
    box-shadow: 0 0 0 3px rgba(227,6,19,0.10) !important;
}

/* ── Footer ──────────────────────────────────── */
.footer {
    background: var(--noir);
    color: #aaa;
    border-radius: var(--radius);
    padding: 32px 40px;
    margin-top: 60px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
}
.footer a { color: var(--rouge); text-decoration: none; }
.footer .brand {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 800;
    color: #fff;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def valid_email(email: str) -> bool:
    return bool(re.match(r"[^@\s]+@[^@\s]+\.[^@\s]+", email))

def fcfa(amount: int) -> str:
    """Format a number as FCFA currency."""
    return f"{amount:,}".replace(",", " ") + " FCFA"


# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────
SERVICES = {
    "🎨 Logo & Identité":    {"icon": "🎨", "desc": "Création complète de votre identité de marque.", "base": 60_000},
    "🖨️ Flyer / Affiche":    {"icon": "🖨️", "desc": "Supports print impactants pour vos campagnes.",  "base": 25_000},
    "🌐 Site web":            {"icon": "🌐", "desc": "Site vitrine ou e-commerce clé en main.",        "base": 200_000},
    "📦 Packaging":           {"icon": "📦", "desc": "Design d'emballage produit attractif et pro.",   "base": 90_000},
    "📱 Social Media Kit":    {"icon": "📱", "desc": "Pack visuel complet pour vos réseaux sociaux.",  "base": 45_000},
    "🚗 Branding Véhicule":   {"icon": "🚗", "desc": "Covering et marquage graphique de véhicule.",   "base": 120_000},
    "🏢 Signalétique":        {"icon": "🏢", "desc": "Panneaux, enseignes et supports événementiels.", "base": 75_000},
    "📊 Présentation PPT":    {"icon": "📊", "desc": "Slides professionnelles pour vos pitchs.",       "base": 35_000},
}

PROJECTS = [
    {"title": "Identité visuelle — Savanna Grill",  "image": "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=600",  "category": "Branding",      "client": "Savanna Grill", "desc": "Logo + charte graphique complète.",  "result": "Image forte & mémorable"},
    {"title": "Flyer Black Friday",                  "image": "https://images.unsplash.com/photo-1607082349566-187342175e2f?w=600",  "category": "Print",         "client": "Dakar Shop",    "desc": "Flyer promotionnel haute impact.",    "result": "+60 % de trafic en magasin"},
    {"title": "Instagram Branding",                  "image": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=600",  "category": "Social Media",  "client": "Queen Style",   "desc": "Feed harmonisé + templates Reels.",  "result": "×3 sur l'engagement"},
    {"title": "Packaging Jus Naturel",               "image": "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=600",  "category": "Packaging",     "client": "Fresh Juice",   "desc": "Étiquette produit bio & colorée.",   "result": "Mise en rayon réussie"},
    {"title": "Signalétique Event Dakar",            "image": "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=600",  "category": "Signalétique",  "client": "Dakar Event",   "desc": "Supports visuels pour 3 000 pers.", "result": "Visibilité maximale"},
    {"title": "Logo TechNova",                       "image": "https://images.unsplash.com/photo-1559028012-481c04fa702d?w=600",  "category": "Logo",          "client": "TechNova",      "desc": "Logo minimaliste + motion design.",  "result": "Image tech & moderne"},
]

TESTIMONIALS = [
    {"text": "Chic Chic ULTRA a transformé notre marque en quelques jours. Résultat au-delà de nos attentes !",  "author": "Aminata D. — Queen Style"},
    {"text": "Professionnalisme, créativité et réactivité. Notre packaging se vend maintenant tout seul.",       "author": "Moussa K. — Fresh Juice"},
    {"text": "Le meilleur investissement que j'ai fait pour mon restaurant. Le logo est parfait.",               "author": "Ibrahim S. — Savanna Grill"},
]

STATS = [
    {"num": "150+", "desc": "Projets livrés"},
    {"num": "98 %", "desc": "Clients satisfaits"},
    {"num": "5 ans", "desc": "D'expérience"},
    {"num": "24 h",  "desc": "Délai livraison rapide"},
]


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:16px 0 24px'>
        <div style='font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;color:#fff;letter-spacing:-0.02em;'>
            ✦ Chic Chic<br><span style='color:#E30613'>ULTRA</span>
        </div>
        <div style='font-size:0.78rem;opacity:0.5;margin-top:4px;'>AGENCE CRÉATIVE</div>
    </div>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "Navigation",
        ["🏠 Accueil", "⚙️ Services", "💰 Devis", "🗂️ Portfolio", "✉️ Contact"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("**📍 Dakar, Sénégal**")
    st.markdown("📲 [WhatsApp](https://wa.me/221770000000)")
    st.markdown("📧 contact@chicchic.sn")
    st.markdown("🕐 Lun–Sam · 8h–20h")
    st.markdown("---")
    st.markdown("<div style='font-size:0.75rem;opacity:0.4;'>© 2026 Chic Chic ULTRA</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE : ACCUEIL
# ─────────────────────────────────────────────
if menu == "🏠 Accueil":

    # Hero
    st.markdown("""
    <div class="hero">
        <h1>L'agence créative<br>qui fait la différence ✦</h1>
        <p>Design · Branding · Impression · Marketing Digital<br>
        Nous donnons vie à vos idées avec excellence.</p>
    </div>
    """, unsafe_allow_html=True)

    # CTA rapide
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("💰 Obtenir un devis"):
            st.info("👈 Rendez-vous dans l'onglet **Devis**")
    with c2:
        if st.button("🗂️ Voir le portfolio"):
            st.info("👈 Cliquez sur **Portfolio** dans le menu")

    st.markdown("<br>", unsafe_allow_html=True)

    # Chiffres clés
    st.markdown("<div class='section-title'>En chiffres</div><div class='divider'></div>", unsafe_allow_html=True)
    cols = st.columns(4)
    for col, s in zip(cols, STATS):
        with col:
            st.markdown(f"""
            <div class="stat">
                <div class="num">{s['num']}</div>
                <div class="desc">{s['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Témoignages
    st.markdown("<div class='section-title'>Ils nous font confiance</div><div class='divider'></div>", unsafe_allow_html=True)
    cols = st.columns(3)
    for col, t in zip(cols, TESTIMONIALS):
        with col:
            st.markdown(f"""
            <div class="testimonial">
                "{t['text']}"
                <div class="author">— {t['author']}</div>
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE : SERVICES
# ─────────────────────────────────────────────
elif menu == "⚙️ Services":
    st.markdown("<div class='section-title'>Nos Services</div>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Des solutions créatives complètes pour booster votre image de marque.</div>", unsafe_allow_html=True)

    cols = st.columns(3)
    for i, (name, info) in enumerate(SERVICES.items()):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="card">
                <div style='font-size:2rem;margin-bottom:10px'>{info['icon']}</div>
                <h3>{name.split(' ', 1)[1]}</h3>
                <p>{info['desc']}</p>
                <p style='margin-top:14px;font-weight:700;color:#E30613'>
                    Dès {fcfa(info['base'])}
                </p>
            </div><br>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE : DEVIS
# ─────────────────────────────────────────────
elif menu == "💰 Devis":
    st.markdown("<div class='section-title'>Devis Instantané</div>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Configurez votre projet et obtenez une estimation en temps réel.</div>", unsafe_allow_html=True)

    col_form, col_result = st.columns([3, 2])

    with col_form:
        service_choice = st.selectbox("📌 Type de service", list(SERVICES.keys()))
        urgence = st.selectbox("⏱️ Délai de livraison", [
            "Normal (5–7 jours)",
            "Rapide (2–3 jours, +30 %)",
            "Urgent (24 h, +60 %)",
        ])
        revisions = st.selectbox("🔁 Nombre de révisions incluses", [
            "1 révision (incluse)",
            "3 révisions (+15 %)",
            "Révisions illimitées (+30 %)",
        ])
        format_livraison = st.multiselect(
            "📂 Formats de livraison",
            ["PDF", "PNG/JPG", "SVG (vectoriel)", "Fichiers sources (AI/PSD)", "Pack réseaux sociaux"],
            default=["PDF", "PNG/JPG"],
        )
        st.text_input("👤 Votre nom (optionnel)", key="devis_nom")
        st.text_area("📝 Brève description du projet", height=100, key="devis_desc",
                     placeholder="Ex : Logo pour une boutique de mode féminine à Dakar…")

    with col_result:
        base = SERVICES[service_choice]["base"]

        mult_urgence = 1.0
        if "30 %" in urgence:   mult_urgence = 1.30
        if "60 %" in urgence:   mult_urgence = 1.60

        mult_revisions = 1.0
        if "15 %" in revisions: mult_revisions = 1.15
        if "30 %" in revisions: mult_revisions = 1.30

        mult_formats = 1.0
        if "Fichiers sources (AI/PSD)" in format_livraison: mult_formats += 0.20
        if "Pack réseaux sociaux"      in format_livraison: mult_formats += 0.10

        total = int(base * mult_urgence * mult_revisions * mult_formats)

        st.markdown(f"""
        <div class="price-box">
            <div style='font-size:0.85rem;opacity:0.8;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px'>
                Estimation
            </div>
            <div class="amount">{fcfa(total)}</div>
            <div class="label">{service_choice.split(' ', 1)[1]}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Récapitulatif
        with st.expander("📋 Voir le récapitulatif"):
            st.write(f"**Service :** {service_choice}")
            st.write(f"**Base :** {fcfa(base)}")
            st.write(f"**Délai :** {urgence}")
            st.write(f"**Révisions :** {revisions}")
            st.write(f"**Formats :** {', '.join(format_livraison) if format_livraison else 'Aucun sélectionné'}")
            st.write(f"**Total estimé :** {fcfa(total)}")

        if st.button("📩 Envoyer ce devis par WhatsApp"):
            msg = (
                f"Bonjour Chic Chic ULTRA !%0A"
                f"Service : {service_choice}%0A"
                f"Délai : {urgence}%0A"
                f"Révisions : {revisions}%0A"
                f"Formats : {', '.join(format_livraison)}%0A"
                f"Budget estimé : {fcfa(total)}"
            )
            wa_link = f"https://wa.me/221770000000?text={msg}"
            st.markdown(f"[👉 Ouvrir WhatsApp]({wa_link})", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE : PORTFOLIO
# ─────────────────────────────────────────────
elif menu == "🗂️ Portfolio":
    st.markdown("<div class='section-title'>Nos Réalisations</div>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Découvrez quelques projets qui illustrent notre savoir-faire.</div>", unsafe_allow_html=True)

    categories = ["Tous"] + sorted(set(p["category"] for p in PROJECTS))
    choice = st.pills("Filtrer par catégorie", categories, default="Tous")

    filtered = PROJECTS if choice == "Tous" else [p for p in PROJECTS if p["category"] == choice]

    cols = st.columns(3)
    for i, p in enumerate(filtered):
        with cols[i % 3]:
            st.image(p["image"], use_container_width=True)
            st.markdown(f"""
            <div class="card" style='margin-top:0;border-radius:0 0 {12}px {12}px;'>
                <div class="badge">{p['category']}</div>
                <h3 style='margin:6px 0 4px'>{p['title']}</h3>
                <p><strong>Client :</strong> {p['client']}</p>
                <p style='margin-top:6px'>{p['desc']}</p>
                <p style='margin-top:10px;font-weight:700;color:#E30613'>✓ {p['result']}</p>
            </div><br>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE : CONTACT
# ─────────────────────────────────────────────
elif menu == "✉️ Contact":
    st.markdown("<div class='section-title'>Parlons de votre projet</div>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Remplissez le formulaire ci-dessous, nous vous répondons sous 24 h.</div>", unsafe_allow_html=True)

    col_form, col_info = st.columns([3, 2])

    with col_form:
        with st.form("contact_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("👤 Nom complet *")
            with c2:
                phone = st.text_input("📲 Téléphone *")

            email = st.text_input("📧 Adresse e-mail *")

            service_contact = st.selectbox("🎯 Service souhaité", ["— Sélectionner —"] + list(SERVICES.keys()))

            budget = st.select_slider(
                "💰 Budget estimé",
                options=["< 25 000 FCFA", "25–75 k FCFA", "75–200 k FCFA", "> 200 k FCFA"],
            )

            msg = st.text_area("💬 Décrivez votre projet *", height=130,
                               placeholder="Parlez-nous de votre activité, vos objectifs…")

            fichier = st.file_uploader("📎 Joindre un fichier (optionnel)", type=["pdf", "png", "jpg", "docx"])

            send = st.form_submit_button("🚀 Envoyer le message")

            if send:
                errors = []
                if not name.strip():   errors.append("Le nom est requis.")
                if not phone.strip():  errors.append("Le téléphone est requis.")
                if not email.strip():  errors.append("L'e-mail est requis.")
                elif not valid_email(email): errors.append("L'adresse e-mail est invalide.")
                if not msg.strip():    errors.append("Le message est requis.")

                if errors:
                    for e in errors:
                        st.error(e)
                else:
                    st.success("✅ Message envoyé ! Nous vous contacterons dans les 24 h.")
                    st.balloons()

    with col_info:
        st.markdown("""
        <div class="card">
            <h3>📍 Nous trouver</h3>
            <p style='margin-top:12px'>Dakar, Sénégal<br>Plateau – Centre Ville</p>

            <h3 style='margin-top:24px'>🕐 Horaires</h3>
            <p>Lundi – Samedi<br>08h00 – 20h00</p>

            <h3 style='margin-top:24px'>📲 Contact direct</h3>
            <p><a href='https://wa.me/221770000000' style='color:#E30613;font-weight:700;text-decoration:none'>
                WhatsApp →
            </a></p>
            <p style='margin-top:8px'><a href='mailto:contact@chicchic.sn' style='color:#0020C2;font-weight:700;text-decoration:none'>
                contact@chicchic.sn →
            </a></p>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div>
        <div class="brand">✦ Chic Chic ULTRA</div>
        <div style='font-size:0.8rem;margin-top:4px;opacity:0.5'>Agence Créative — Dakar, Sénégal</div>
    </div>
    <div style='font-size:0.85rem'>
        <a href='https://wa.me/221770000000'>WhatsApp</a> &nbsp;·&nbsp;
        <a href='mailto:contact@chicchic.sn'>Email</a> &nbsp;·&nbsp;
        <a href='#'>Instagram</a> &nbsp;·&nbsp;
        <a href='#'>Facebook</a>
    </div>
    <div style='font-size:0.78rem;opacity:0.45'>© 2026 Chic Chic ULTRA · Tous droits réservés</div>
</div>
""", unsafe_allow_html=True)
