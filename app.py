import streamlit as st

# 1. Configuration de la page
st.set_page_config(
    page_title="Chic Chic | Graphic & Print",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS Personnalisé (Synchronisé avec les couleurs du logo)
st.markdown("""
    <style>
    /* Couleurs principales basées sur le logo: 
       Rouge: #E30613 | Vert: #009640 | Bleu: #0020C2 | Noir: #000000 
    */
    
    h1, h2, h3 {
        color: #000000;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
    }
    .subtitle {
        color: #4A4A4A;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    /* Bouton principal (Rouge du logo) */
    .stButton>button {
        background-color: #E30613; 
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: white;
        color: #E30613;
        border: 2px solid #E30613;
    }
    /* Cartes de services avec les couleurs des gouttes du logo */
    .service-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #fcfcfc;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .card-red { border-left: 6px solid #E30613; }
    .card-green { border-left: 6px solid #009640; }
    .card-blue { border-left: 6px solid #0020C2; }
    .card-black { border-left: 6px solid #000000; }
    </style>
""", unsafe_allow_html=True)

# 3. Navigation dans la barre latérale
# On affiche le logo que tu as fourni
try:
    # Remplace la ligne st.sidebar.image par celle-ci :
st.sidebar.image("https://files.catbox.moe/p9o48g.png", use_container_width=True)
except FileNotFoundError:
    st.sidebar.error("⚠️ Image 'logo.png' introuvable. Place le logo dans le même dossier.")

st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Navigation",
    ["Accueil", "Nos Services", "Nos Réalisations", "Contact"]
)
st.sidebar.markdown("---")
st.sidebar.info("📍 Basé au Sénégal\n\n📞 +221 XX XXX XX XX\n\n✉️ contact@chicchic.sn")

# 4. Contenu des pages

if menu == "Accueil":
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.title("L'art de l'impression et du design.")
        st.markdown('<p class="subtitle">Chic Chic Graphic & Print est votre studio créatif pour des supports de communication qui marquent les esprits.</p>', unsafe_allow_html=True)
        if st.button("Découvrir nos services 🚀"):
            st.success("Naviguez vers l'onglet 'Nos Services' dans le menu à gauche !")
            
    with col2:
        # Image d'illustration (tu pourras remplacer par une photo de tes machines ou de ton équipe)
        st.image("https://images.unsplash.com/photo-1561070791-2526d30994b5?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", use_container_width=True)
        
    st.markdown("---")
    
    st.subheader("Pourquoi choisir Chic Chic ?")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### 🎨 Créativité")
        st.write("Des designs uniques, aussi vibrants que nos couleurs, pour refléter l'ADN de votre marque.")
    with c2:
        st.markdown("### 🖨️ Qualité Premium")
        st.write("Impression haute définition sur des supports soigneusement sélectionnés pour un rendu impeccable.")
    with c3:
        st.markdown("### ⚡ Réactivité")
        st.write("Une équipe engagée pour livrer vos projets professionnels dans les meilleurs délais.")

elif menu == "Nos Services":
    st.title("Nos Domaines d'Expertise 🛠️")
    st.markdown("Découvrez nos solutions sur-mesure pour votre communication.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="service-card card-red">
            <h3 style="color: #E30613;">🖨️ Impression Numérique</h3>
            <p>De la petite à la grande série, nous imprimons vos documents avec une précision absolue : affiches, flyers, brochures...</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="service-card card-green">
            <h3 style="color: #009640;">🎨 Conception Graphique</h3>
            <p>Création de logos, chartes graphiques, et identités visuelles. Notre studio donne vie à vos idées.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="service-card card-blue">
            <h3 style="color: #0020C2;">📢 Supports Grand Format</h3>
            <p>Bâches, roll-ups, vitrophanie et habillage de véhicules pour maximiser votre visibilité.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="service-card card-black">
            <h3 style="color: #000000;">📦 Packaging & Étiquettes</h3>
            <p>Sublimez vos produits avec des emballages personnalisés professionnels et attractifs.</p>
        </div>
        """, unsafe_allow_html=True)

elif menu == "Nos Réalisations":
    st.title("Notre Portfolio 🖼️")
    st.write("Un aperçu de nos récents projets d'impression et de design.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("https://images.unsplash.com/photo-1626785774573-4b799315345d?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80", caption="Identité Visuelle")
        st.image("https://images.unsplash.com/photo-1586717791821-3f44a563fa4c?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80", caption="Impression Brochures")
        
    with col2:
        st.image("https://images.unsplash.com/photo-1600880292203-757bb62b4baf?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80", caption="Packaging Sur-Mesure")
        st.image("https://images.unsplash.com/photo-1542744173-8e7e53415bb0?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80", caption="Affiches & Grand Format")
        
    with col3:
        st.image("https://images.unsplash.com/photo-1629429408209-1f912961dbd8?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80", caption="Cartes de Visite")
        st.image("https://images.unsplash.com/photo-1611162617474-5b21e879e113?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80", caption="Flyers Événementiels")

elif menu == "Contact":
    st.title("Parlons de votre projet ☕")
    st.write("Laissez-nous un message, l'équipe Chic Chic vous répondra rapidement.")
    
    col_form, col_info = st.columns([2, 1])
    
    with col_form:
        with st.form("contact_form"):
            nom = st.text_input("Votre Nom / Entreprise")
            email = st.text_input("Votre Email")
            besoin = st.selectbox("Quel est votre besoin principal ?", 
                                  ["Impression Numérique", "Conception Graphique", "Création de Logo", "Support Grand Format", "Autre"])
            message = st.text_area("Décrivez votre projet")
            
            submit_button = st.form_submit_button("Envoyer la demande")
            
            if submit_button:
                if nom and email and message:
                    st.success(f"Merci {nom} ! Votre demande a bien été envoyée. Nous vous contacterons sous peu.")
                    st.balloons()
                else:
                    st.error("Veuillez remplir tous les champs obligatoires.")
                    
    with col_info:
        st.markdown("### 📍 Chic Chic Graphic & Print")
        st.write("Quartier des Affaires")
        st.write("Sénégal")
        st.markdown("---")
        st.write("🕒 **Horaires :**")
        st.write("Lun - Ven : 09h00 - 18h00")
        st.write("Samedi : 09h00 - 13h00")
        st.markdown("---")
        st.write("Suivez-nous sur les réseaux sociaux pour découvrir nos dernières créations !")

# Footer
st.markdown("""
    <div style="text-align: center; margin-top: 50px; color: #888; border-top: 1px solid #ddd; padding-top: 20px;">
        <small>© 2026 Chic Chic Graphic & Print. Tous droits réservés.</small>
    </div>
""", unsafe_allow_html=True)
