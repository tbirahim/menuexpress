import streamlit as st

# 1. Configuration de la page (DOIT être la première commande)
st.set_page_config(
    page_title="Chic Chic | Studio Créatif & Impression",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS Personnalisé pour un rendu "Chic" et professionnel
st.markdown("""
    <style>
    /* Couleurs et typographie */
    h1, h2, h3 {
        color: #1E1E1E;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
    }
    .subtitle {
        color: #666666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    /* Boutons personnalisés */
    .stButton>button {
        background-color: #D4AF37; /* Or chic */
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1E1E1E;
        color: #D4AF37;
        border: 1px solid #D4AF37;
    }
    /* Cartes de services */
    .service-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f9f9f9;
        border-left: 5px solid #D4AF37;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Navigation dans la barre latérale
st.sidebar.image("https://images.unsplash.com/photo-1600132806370-bf17e65e942f?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&q=80", use_container_width=True) # Image d'illustration stylée
st.sidebar.title("✨ Chic Chic")
st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Navigation",
    ["Accueil", "Nos Services", "Nos Réalisations", "Contact"]
)
st.sidebar.markdown("---")
st.sidebar.info("📍 Basé au Sénégal\n\n📞 +221 XX XXX XX XX\n\n✉️ contact@chicchic.sn")

# 4. Contenu des pages

if menu == "Accueil":
    # Section Hero
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.title("Donnez vie à vos idées avec Élégance.")
        st.markdown('<p class="subtitle">Chic Chic est votre partenaire privilégié pour l\'impression numérique, la conception graphique et tous vos supports de communication.</p>', unsafe_allow_html=True)
        if st.button("Découvrir nos services 🚀"):
            st.success("Naviguez vers l'onglet 'Nos Services' dans le menu à gauche !")
            
    with col2:
        # Image d'illustration créative (remplace l'URL par ton propre logo ou image)
        st.image("https://images.unsplash.com/photo-1561070791-2526d30994b5?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", use_container_width=True)
        
    st.markdown("---")
    
    # Section Pourquoi nous ?
    st.subheader("Pourquoi choisir Chic Chic ?")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### 🎨 Créativité")
        st.write("Des designs uniques et sur-mesure qui reflètent l'ADN de votre marque.")
    with c2:
        st.markdown("### 🖨️ Qualité Premium")
        st.write("Une impression numérique haute définition sur des supports soigneusement sélectionnés.")
    with c3:
        st.markdown("### ⚡ Réactivité")
        st.write("Une équipe dédiée pour livrer vos projets dans les meilleurs délais sans compromis.")

elif menu == "Nos Services":
    st.title("Nos Domaines d'Expertise 🛠️")
    st.markdown("Découvrez comment nous pouvons transformer votre communication visuelle.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="service-card">
            <h3>🖨️ Impression Numérique</h3>
            <p>De la petite à la grande série, nous imprimons vos documents avec une précision inégalée. Affiches, flyers, brochures, cartes de visite...</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="service-card">
            <h3>📦 Packaging & Étiquettes</h3>
            <p>Sublimez vos produits avec des emballages personnalisés et des étiquettes qui attirent l'œil en rayon.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="service-card">
            <h3>🎨 Conception Graphique</h3>
            <p>Création de logos, chartes graphiques, et identités visuelles complètes. Notre studio donne une âme à votre marque.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="service-card">
            <h3>📢 Supports Grand Format</h3>
            <p>Bâches, roll-ups, vitrophanie et habillage de véhicules pour une visibilité maximale lors de vos événements.</p>
        </div>
        """, unsafe_allow_html=True)

elif menu == "Nos Réalisations":
    st.title("Notre Portfolio 🖼️")
    st.write("Un aperçu de nos récents projets créatifs.")
    
    # Création d'une grille d'images (3 colonnes)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("https://images.unsplash.com/photo-1626785774573-4b799315345d?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80", caption="Branding Corporate")
        st.image("https://images.unsplash.com/photo-1586717791821-3f44a563fa4c?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80", caption="Design Éditorial")
        
    with col2:
        st.image("https://images.unsplash.com/photo-1600880292203-757bb62b4baf?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80", caption="Packaging Produit")
        st.image("https://images.unsplash.com/photo-1542744173-8e7e53415bb0?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80", caption="Campagne d'Affichage")
        
    with col3:
        st.image("https://images.unsplash.com/photo-1629429408209-1f912961dbd8?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80", caption="Cartes de Visite Premium")
        st.image("https://images.unsplash.com/photo-1611162617474-5b21e879e113?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80", caption="Communication Réseaux Sociaux")

elif menu == "Contact":
    st.title("Parlons de votre projet ☕")
    st.write("Laissez-nous un message et notre équipe vous recontactera très vite.")
    
    col_form, col_info = st.columns([2, 1])
    
    with col_form:
        # Formulaire de contact
        with st.form("contact_form"):
            nom = st.text_input("Votre Nom / Entreprise")
            email = st.text_input("Votre Email")
            besoin = st.selectbox("Quel est votre besoin principal ?", 
                                  ["Impression Numérique", "Conception Graphique", "Création de Logo", "Support Grand Format", "Autre"])
            message = st.text_area("Décrivez votre projet")
            
            submit_button = st.form_submit_button("Envoyer la demande")
            
            if submit_button:
                if nom and email and message:
                    st.success(f"Merci {nom} ! Votre demande a bien été envoyée à l'équipe Chic Chic.")
                    st.balloons()
                else:
                    st.error("Veuillez remplir tous les champs obligatoires (Nom, Email, Message).")
                    
    with col_info:
        st.markdown("### 📍 Notre Agence")
        st.write("**Chic Chic**")
        st.write("Quartier des Affaires")
        st.write("Sénégal")
        st.markdown("---")
        st.write("🕒 **Horaires :**")
        st.write("Lun - Ven : 09h00 - 18h00")
        st.write("Samedi : Sur rendez-vous")

# Footer caché ou discret
st.markdown("""
    <div style="text-align: center; margin-top: 50px; color: #888;">
        <small>© 2026 Chic Chic. Tous droits réservés.</small>
    </div>
""", unsafe_allow_html=True)
