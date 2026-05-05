import streamlit as st
import urllib.parse

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="CHIC Graphic & Print | Expertise Visuelle",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. NETTOYAGE PROFESSIONNEL (Suppression GitHub, Menu et Footer)
hide_st_style = """
            <style>
            /* Masquer le bouton GitHub et le menu Streamlit en haut à droite */
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            
            /* Masquer le footer "Made with Streamlit" */
            footer {visibility: hidden;}
            
            /* Supprimer l'espace vide en haut créé par le header masqué */
            .block-container {
                padding-top: 2rem;
                padding-bottom: 0rem;
            }
            
            /* Masquer la barre de déploiement (le petit triangle en haut à gauche sur mobile) */
            div[data-testid="stToolbar"] {
                display: none;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. CONSTANTES
BRAND_NAME = "CHIC Graphic & Print"
WHATSAPP_NUMBER = "221772472704"
EMAIL = "contact@chic-graphic.sn"
LOCATION = "Dakar, Sénégal"

# 4. CSS DE L'INTERFACE (Ton style personnalisé)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --primary:  #38BDF8;
    --dark:     #0C4A6E;
    --light:    #FFFFFF;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--light);
}

.hero {
    background: linear-gradient(135deg, #0C4A6E 0%, #075985 100%);
    color: #fff;
    border-radius: 20px;
    padding: 60px 40px;
    margin-bottom: 40px;
}

.footer-pro {
    background: var(--dark);
    color: #BAE6FD;
    border-radius: 15px;
    padding: 30px;
    text-align: center;
    margin-top: 50px;
}
</style>
""", unsafe_allow_html=True)

# 5. NAVIGATION LATÉRALE
with st.sidebar:
    st.markdown(f"<div style='text-align:center;padding:20px 0'><div style='font-family:Syne,sans-serif;font-size:1.4rem;font-weight:800;'>{BRAND_NAME}</div></div>", unsafe_allow_html=True)
    menu = st.radio("Navigation", ["🏠 Accueil", "⚙️ Services", "📅 Devis Express", "✉️ Contact"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown(f"📍 {LOCATION}\n\n📧 {EMAIL}")

# 6. CONTENU DES PAGES
if menu == "🏠 Accueil":
    st.markdown(f"""<div class="hero"><h1>L'art de l'impression ✦</h1><p>Solutions graphiques premium pour entreprises exigeantes.</p></div>""", unsafe_allow_html=True)
    st.subheader("Nos piliers")
    c1, c2, c3 = st.columns(3)
    c1.metric("Qualité", "Premium")
    c2.metric("Délais", "24/48h")
    c3.metric("Support", "Dakar")

elif menu == "⚙️ Services":
    st.title("Nos Services")
    st.write("Conception de logos, flyers, packaging et impression grand format.")

elif menu == "📅 Devis Express":
    st.title("Demande de Devis")
    with st.container():
        nom = st.text_input("Votre Nom")
        projet = st.selectbox("Type de projet", ["Logo", "Flyer", "Packaging", "Autre"])
        if st.button("Demander via WhatsApp"):
            msg = f"Bonjour, je souhaite un devis pour {projet}. Nom: {nom}"
            st.markdown(f"[Cliquer ici pour envoyer](https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(msg)})")

elif menu == "✉️ Contact":
    st.title("Contactez-nous")
    st.write(f"Email : {EMAIL}")
    st.write(f"Localisation : {LOCATION}")

# 7. FOOTER PERSONNALISÉ (Remplace le footer Streamlit)
st.markdown(f"<div class='footer-pro'><strong>{BRAND_NAME}</strong><br>© 2026 · Excellence Graphique</div>", unsafe_allow_html=True)
