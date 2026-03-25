import streamlit as st
import re

# CONFIG
st.set_page_config(page_title="Chic Chic ULTRA", page_icon="🎨", layout="wide")

# CSS PREMIUM
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #ffffff, #f5f7fa);
}
h1 {
    font-size: 2.8rem;
    font-weight: 800;
}

.stButton>button {
    background: linear-gradient(90deg, #E30613, #0020C2);
    color: white;
    border-radius: 12px;
    padding: 0.7rem;
    border: none;
    font-weight: bold;
}

.card {
    padding: 20px;
    border-radius: 15px;
    background: white;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    transition: 0.3s;
}
.card:hover {
    transform: translateY(-8px) scale(1.03);
}
</style>
""", unsafe_allow_html=True)

# SIDEBAR
st.sidebar.title("🎨 Chic Chic ULTRA")
menu = st.sidebar.radio("Navigation", ["Accueil", "Services", "Devis", "Portfolio", "Contact"])

st.sidebar.markdown("---")
st.sidebar.markdown("📲 WhatsApp : https://wa.me/22177XXXXXX")
st.sidebar.markdown("📍 Dakar, Sénégal")

# EMAIL VALIDATION
def valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# =========================
# DATA PORTFOLIO
# =========================
projects = [
    {
        "title": "Identité visuelle - Savanna Grill",
        "image": "https://images.unsplash.com/photo-1552566626-52f8b828add9",
        "category": "Branding",
        "client": "Savanna Grill",
        "description": "Création d’un logo et charte moderne.",
        "result": "Image forte et mémorable"
    },
    {
        "title": "Flyer Black Friday",
        "image": "https://images.unsplash.com/photo-1607082349566-187342175e2f",
        "category": "Print",
        "client": "Dakar Shop",
        "description": "Flyer promotionnel impactant.",
        "result": "+60% trafic"
    },
    {
        "title": "Instagram Branding",
        "image": "https://images.unsplash.com/photo-1521335629791-ce4aec67dd47",
        "category": "Social Media",
        "client": "Queen Style",
        "description": "Feed Instagram harmonisé.",
        "result": "x3 engagement"
    },
    {
        "title": "Packaging Jus",
        "image": "https://images.unsplash.com/photo-1582719478170-3e6c7d0b6f79",
        "category": "Packaging",
        "client": "Fresh Juice",
        "description": "Design étiquette produit bio.",
        "result": "Produit attractif"
    },
    {
        "title": "Signalétique Event",
        "image": "https://images.unsplash.com/photo-1542744173-8e7e53415bb0",
        "category": "Signalétique",
        "client": "Dakar Event",
        "description": "Supports visuels événementiels.",
        "result": "Visibilité maximale"
    },
    {
        "title": "Logo Tech",
        "image": "https://images.unsplash.com/photo-1559028012-481c04fa702d",
        "category": "Logo",
        "client": "TechNova",
        "description": "Logo minimaliste.",
        "result": "Image moderne"
    }
]

# =========================
# ACCUEIL
# =========================
if menu == "Accueil":
    st.title("Agence Créative Nouvelle Génération 🚀")
    st.write("Design • Branding • Impression • Marketing")

    if st.button("💰 Obtenir un devis"):
        st.info("Va dans l’onglet Devis 👈")

# =========================
# SERVICES
# =========================
elif menu == "Services":
    st.title("Nos Services")

    cols = st.columns(3)
    services = [
        "🎨 Design Graphique",
        "🖨️ Impression",
        "📦 Packaging",
        "📢 Marketing Visuel",
        "🚗 Branding véhicule",
        "🏢 Corporate"
    ]

    for i, s in enumerate(services):
        with cols[i % 3]:
            st.markdown(f"<div class='card'><h3>{s}</h3></div>", unsafe_allow_html=True)

# =========================
# DEVIS
# =========================
elif menu == "Devis":
    st.title("💰 Devis Automatique")

    service = st.selectbox("Service", ["Logo", "Flyer", "Site web", "Packaging"])
    urgence = st.selectbox("Délai", ["Normal", "Urgent (+50%)"])

    prices = {
        "Logo": 50000,
        "Flyer": 25000,
        "Site web": 150000,
        "Packaging": 80000
    }

    total = prices[service]

    if urgence == "Urgent (+50%)":
        total *= 1.5

    st.success(f"💵 Prix estimé : {int(total)} FCFA")

# =========================
# PORTFOLIO
# =========================
elif menu == "Portfolio":
    st.title("Nos Réalisations")

    categories = list(set([p["category"] for p in projects]))
    choice = st.selectbox("Filtrer", ["Tous"] + categories)

    filtered = projects if choice == "Tous" else [p for p in projects if p["category"] == choice]

    cols = st.columns(3)

    for i, p in enumerate(filtered):
        with cols[i % 3]:
            st.image(p["image"])
            st.markdown(f"### {p['title']}")
            st.write(f"**Client :** {p['client']}")
            st.write(p["description"])
            st.success(p["result"])

# =========================
# CONTACT
# =========================
elif menu == "Contact":
    st.title("Contact")

    with st.form("form"):
        name = st.text_input("Nom")
        email = st.text_input("Email")
        msg = st.text_area("Projet")

        send = st.form_submit_button("Envoyer")

        if send:
            if not name or not email or not msg:
                st.error("Remplis tous les champs")
            elif not valid_email(email):
                st.error("Email invalide")
            else:
                st.success("Message envoyé ✅")
                st.balloons()

# FOOTER
st.markdown("---")
st.markdown("© 2026 Chic Chic ULTRA 🚀")
