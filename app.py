import streamlit as st

# 1. Configuration de la page
st.set_page_config(
    page_title="Chic Chic | Graphic & Print",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS Personnalisé (Couleurs synchronisées avec le logo Chic Chic)
st.markdown("""
    <style>
    /* Couleurs Logo : Rouge (#E30613), Vert (#009640), Bleu (#0020C2), Noir (#000000) */
    
    /* Global */
    .main { background-color: #ffffff; }
    h1, h2, h3 { color: #000000; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* Bouton Principal - ROUGE CHIC */
    .stButton>button {
        background-color: #E30613;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.6rem 2rem;
        font-weight: bold;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #000000;
        color: #E30613;
        border: 1px solid #E30613;
    }

    /* Cartes de Services */
    .service-card {
        padding: 25px;
        border-radius: 12px;
        background-color: #f8f9fa;
        margin-bottom: 20px;
        box-shadow: 2px 2px 15px rgba(0,0,0,0.05);
        transition: transform 0.3s;
    }
    .service-card:hover { transform: translateY(-5px); }
    
    .border-red { border-top: 5px solid #E30613; }
    .border-green { border-top: 5px solid #009640; }
    .border-blue { border-top: 5px solid #0020C2; }
    .border-black { border-top: 5px solid #000000; }

    /* Barre latérale */
    section[data-testid="stSidebar"] {
        background-color: #f0f2f6;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Barre latérale (Sidebar)
# Utilisation du lien direct pour éviter les erreurs de fichier local
logo_url = "https://files.catbox.moe/p9o48g.png" 
st.sidebar.image(logo_url, use_container_width=True)

st.sidebar.markdown("<h2 style='text-align: center; color: #000;'>Menu Principal</h2>", unsafe_allow_html=True)
menu = st.sidebar.radio(
    "",
    ["🏠 Accueil", "🛠️ Nos Services", "🖼️ Portfolio", "📩 Contact"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**📍 Localisation** Dakar, Sénégal  

**📞 Contact** +221 77 XXX XX XX  

**📧 Email** contact@chicchic.sn
""")

# 4. Logique des pages

if menu == "🏠 Accueil":
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.title("L'expertise Graphique & Print qui fait la différence.")
        st.write("""
        Bienvenue chez **Chic Chic**. Nous transformons vos concepts en réalité visuelle. 
        Que ce soit pour de l'impression grand format ou une identité visuelle complète, 
        notre équipe met sa créativité au service de votre succès.
        """)
        if st.button("Voir nos offres"):
            st.info("Utilisez le menu à gauche pour explorer nos services !")
            
    with col2:
        # Image d'ambiance professionnelle
        st.image("https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=600&q=80")

    st.markdown("---")
    st.subheader("Nos engagements")
    c1, c2, c3 = st.columns(3)
    c1.metric("Qualité", "Premium")
    c2.metric("Délais", "Express")
    c3.metric("Support", "24/7")

elif menu == "🛠️ Nos Services":
    st.title("Nos Solutions de Communication")
    
    colA, colB = st.columns(2)
    
    with colA:
        st.markdown("""
        <div class="service-card border-red">
            <h3 style="color:#E30613">🖨️ Impression Numérique</h3>
            <p>Cartes de visite, flyers, brochures et catalogues. Une finition haut de gamme pour tous vos documents.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="service-card border-blue">
            <h3 style="color:#0020C2">📢 Signalétique & Grand Format</h3>
            <p>Bâches, Roll-up, habillage de vitrines et de véhicules. Soyez visible de loin !</p>
        </div>
        """, unsafe_allow_html=True)

    with colB:
        st.markdown("""
        <div class="service-card border-green">
            <h3 style="color:#009640">🎨 Conception Graphique</h3>
            <p>Création de logos, charte graphique et réseaux sociaux. Une identité unique pour votre entreprise.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="service-card border-black">
            <h3 style="color:#000000">📦 Packaging</h3>
            <p>Conception d'emballages personnalisés et étiquettes produits pour une présentation irréprochable.</p>
        </div>
        """, unsafe_allow_html=True)

elif menu == "🖼️ Portfolio":
    st.title("Nos Réalisations")
    st.write("Découvrez quelques projets signés Chic Chic.")
    
    tabs = st.tabs(["Print", "Design", "Signalétique"])
    
    with tabs[0]:
        c1, c2 = st.columns(2)
        c1.image("https://images.unsplash.com/photo-1593642532842-98d0fd5ebc1a?auto=format&fit=crop&w=500", caption="Flyers Premium")
        c2.image("https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?auto=format&fit=crop&w=500", caption="Cartes de Visite")
        
    with tabs[1]:
        st.image("https://images.unsplash.com/photo-1626785774573-4b799315345d?auto=format&fit=crop&w=1000", caption="Branding complet pour client Corporate")

    with tabs[2]:
        st.image("https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&w=1000", caption="Pose de signalétique événementielle")

elif menu == "📩 Contact":
    st.title("Prêt à démarrer un projet ?")
    
    with st.form("form_contact"):
        name = st.text_input("Nom ou Entreprise")
        email = st.text_input("Email de contact")
        service = st.multiselect("Services souhaités", ["Impression", "Logo/Design", "Signalétique", "Packaging"])
        msg = st.text_area("Dites-nous en plus sur votre besoin")
        
        submitted = st.form_submit_button("Envoyer mon message")
        if submitted:
            if name and email and msg:
                st.success(f"Merci {name} ! Votre message a été transmis. L'équipe Chic Chic vous recontactera sur {email}.")
                st.balloons()
            else:
                st.warning("Veuillez remplir les champs obligatoires.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>© 2026 Chic Chic Graphic & Print - Créativité & Professionnalisme</p>", unsafe_allow_html=True)
