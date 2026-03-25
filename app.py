import streamlit as st
import re

# CONFIG
st.set_page_config(page_title="Chic Chic ULTRA", layout="wide")

# PREMIUM CSS
st.markdown("""
<style>
.main {background: linear-gradient(135deg, #ffffff, #f5f7fa);} 
h1 {font-size: 3rem; font-weight: 800;}

.stButton>button {
    background: linear-gradient(90deg, #E30613, #0020C2);
    color: white;
    border-radius: 12px;
    padding: 0.8rem;
    border: none;
    font-weight: bold;
}

.card {
    padding: 25px;
    border-radius: 20px;
    background: white;
    box-shadow: 0 15px 40px rgba(0,0,0,0.08);
    transition: 0.3s;
}
.card:hover {transform: translateY(-10px) scale(1.04);} 
</style>
""", unsafe_allow_html=True)

# SIDEBAR
st.sidebar.title("🚀 Chic Chic ULTRA")
menu = st.sidebar.radio("Navigation", ["Accueil", "Services", "Devis", "Portfolio", "Contact"])

st.sidebar.markdown("---")
st.sidebar.markdown("📲 WhatsApp: https://wa.me/22177XXXXXX")
st.sidebar.markdown("📍 Dakar, Sénégal")

# EMAIL CHECK

def valid_email(e):
    return re.match(r"[^@]+@[^@]+\.[^@]+", e)

# ACCUEIL
if menu == "Accueil":
    st.title("Agence Créative Nouvelle Génération")
    st.write("Design • Branding • Impression • Stratégie")

    if st.button("Obtenir un devis rapide"):
        st.session_state["menu"] = "Devis"

# SERVICES
elif menu == "Services":
    st.title("Nos Expertises")

    cols = st.columns(3)
    data = [
        ("🎨 Design", "Identité visuelle pro"),
        ("🖨️ Impression", "Qualité premium"),
        ("📦 Packaging", "Produits attractifs"),
        ("📢 Marketing", "Stratégie visuelle"),
        ("🚗 Branding véhicule", "Impact maximal"),
        ("🏢 Corporate", "Image professionnelle")
    ]

    for i, (t, d) in enumerate(data):
        with cols[i % 3]:
            st.markdown(f"""<div class='card'><h3>{t}</h3><p>{d}</p></div>""", unsafe_allow_html=True)

# DEVIS INTELLIGENT
elif menu == "Devis":
    st.title("💰 Devis Automatique")

    service = st.selectbox("Service", ["Logo", "Flyer", "Site web", "Packaging"])
    urgence = st.selectbox("Délai", ["Normal", "Urgent (+50%)"])

    base_prices = {
        "Logo": 50000,
        "Flyer": 25000,
        "Site web": 150000,
        "Packaging": 80000
    }

    price = base_prices[service]

    if urgence == "Urgent (+50%)":
        price *= 1.5

    st.success(f"💵 Prix estimé : {int(price)} FCFA")

# PORTFOLIO
elif menu == "Portfolio":
    st.title("Nos Réalisations")
    st.image("https://images.unsplash.com/photo-1600585154340-be6161a56a0c")

# CONTACT + LEAD CAPTURE
elif menu == "Contact":
    st.title("Contact Premium")

    with st.form("lead"):
        name = st.text_input("Nom")
        email = st.text_input("Email")
        budget = st.selectbox("Budget", ["<50k", "50k-150k", "150k+"])
        msg = st.text_area("Projet")

        ok = st.form_submit_button("Envoyer")

        if ok:
            if not name or not email or not msg:
                st.error("Remplis tous les champs")
            elif not valid_email(email):
                st.error("Email invalide")
            else:
                st.success("🔥 Lead enregistré !")
                st.balloons()

# FOOTER
st.markdown("---")
st.markdown("🔥 Chic Chic ULTRA — Machine à clients")
