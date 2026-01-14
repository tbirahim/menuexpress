import streamlit as st
import sqlite3
import pandas as pd
import urllib.parse
import datetime

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Le Gourmet", page_icon="🥂", layout="wide", initial_sidebar_state="collapsed")

# --- 2. GESTION MOT DE PASSE ADMIN ---
# (À mettre dans les secrets sur le cloud, ici en dur pour test)
ADMIN_PASSWORD = st.secrets.get("PASSWORD", "admin123")

# --- 3. CSS "STYLE APP MOBILE" (LE SECRET DU DESIGN) ---
st.markdown("""
    <style>
    /* Importation d'une belle police */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@400;700&display=swap');

    /* Fond général sombre et texte */
    .stApp {
        background-color: #121212;
        color: #ffffff;
        font-family: 'Lato', sans-serif;
    }
    
    /* Titres élégants */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        color: #d4af37; /* Couleur Or */
        text-align: center;
    }

    /* Cacher le menu hamburger standard et le footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;} /* On cache la barre latérale classique */

    /* Style des cartes de plats */
    .plat-card {
        background-color: #1e1e1e;
        border-radius: 15px;
        overflow: hidden;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        border: 1px solid #333;
        transition: transform 0.2s;
    }
    .plat-card:active {
        transform: scale(0.98);
    }
    .plat-img {
        width: 100%;
        height: 180px;
        object-fit: cover;
    }
    .plat-info {
        padding: 15px;
    }
    .plat-name {
        font-size: 1.2rem;
        font-weight: bold;
        color: #fff;
        margin-bottom: 5px;
    }
    .plat-desc {
        font-size: 0.9rem;
        color: #aaa;
        margin-bottom: 10px;
        line-height: 1.4;
    }
    .plat-price {
        font-size: 1.3rem;
        color: #d4af37;
        font-weight: bold;
        float: right;
    }

    /* Bouton d'action (Ajouter, Valider) */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        background: linear-gradient(45deg, #d4af37, #c5a028);
        color: black;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
        margin-top: 10px;
    }

    /* Style pour la section Hero (Accueil) */
    .hero-text {
        font-size: 1.1rem;
        text-align: center;
        color: #ccc;
        margin-bottom: 30px;
        padding: 0 20px;
    }
    
    /* Navigation par onglets personnalisée */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #1e1e1e;
        padding: 10px;
        border-radius: 20px;
        position: fixed; 
        bottom: 20px; 
        left: 50%;
        transform: translateX(-50%);
        z-index: 999;
        box-shadow: 0 5px 20px rgba(0,0,0,0.5);
        width: 90%;
        max-width: 500px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        border-radius: 10px;
        color: #fff;
        flex: 1;
    }
    .stTabs [aria-selected="true"] {
        background-color: #d4af37 !important;
        color: #000 !important;
    }
    
    /* Espace en bas pour ne pas cacher le contenu derrière la nav */
    .block-container {
        padding-bottom: 100px;
    }

    </style>
    """, unsafe_allow_html=True)

# --- 4. BASE DE DONNÉES ---
def init_db():
    conn = sqlite3.connect('restaurant.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS menu (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prix REAL, desc TEXT, img TEXT)')
    c.execute('''CREATE TABLE IF NOT EXISTS commandes 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, articles TEXT, total REAL, 
                  type_commande TEXT, detail_logistique TEXT, date DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    return conn

conn = init_db()
c = conn.cursor()

# --- 5. GESTION DE SESSION ---
if 'cart' not in st.session_state: st.session_state.cart = []
if 'cmd_faite' not in st.session_state: st.session_state.cmd_faite = False
if 'wa_link' not in st.session_state: st.session_state.wa_link = ""
if 'admin_mode' not in st.session_state: st.session_state.admin_mode = False

# --- 6. INTERFACE PRINCIPALE (NAVIGATION TYPE APP) ---

# On utilise les Tabs pour simuler la barre de navigation du bas
# L'ordre est important : Accueil | Menu | Réservation | Panier
tabs = st.tabs(["🏠 Accueil", "🍴 Menu", "📅 Réserver", "🛒 Panier", "🔐 Admin"])

# --- PAGE 1: ACCUEIL (Comme dans la vidéo) ---
with tabs[0]:
    # Image de couverture (Hero)
    st.image("https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=2070&auto=format&fit=crop", use_container_width=True)
    
    st.title("Bienvenue au Gourmet")
    st.markdown('<p class="hero-text">Une cuisine fraîche et locale. Notre restaurant offre une atmosphère chaleureuse et accueillante, parfaite pour toutes vos occasions.</p>', unsafe_allow_html=True)

    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://images.unsplash.com/photo-1559339352-11d035aa65de?q=80&w=1974", use_container_width=True)
    with col2:
        st.subheader("Happy Hour")
        st.write("Profitez de nos cocktails de 17h à 19h.")

    st.markdown("---")
    
    st.subheader("Notre Équipe")
    st.write("Penda & Debo vous accueillent avec le sourire.")
    st.image("https://images.unsplash.com/photo-1600565193348-f74bd3c7ccdf?q=80&w=2071", use_container_width=True)


# --- PAGE 2: LE MENU (Carte interactive) ---
with tabs[1]:
    st.header("Notre Carte")
    
    df = pd.read_sql('SELECT * FROM menu', conn)
    if df.empty:
        st.info("Le menu est vide.")
    else:
        # Affichage en grille de 2 colonnes pour mobile
        cols = st.columns(2)
        for index, row in df.iterrows():
            with cols[index % 2]: # Alterne colonne 1 et 2
                img = row['img'] if row['img'] else "https://via.placeholder.com/150"
                # Carte HTML personnalisée
                st.markdown(f"""
                <div class="plat-card">
                    <img src="{img}" class="plat-img">
                    <div class="plat-info">
                        <div class="plat-name">{row['nom']}</div>
                        <div class="plat-desc">{row['desc']}</div>
                        <div class="plat-price">{int(row['prix'])} F</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Bouton Streamlit sous la carte HTML
                if st.button(f"Ajouter", key=f"add_{row['id']}"):
                    st.session_state.cart.append({"nom": row['nom'], "prix": row['prix']})
                    st.toast(f"✅ {row['nom']} ajouté !")

# --- PAGE 3: RÉSERVATION (Nouveau !) ---
with tabs[2]:
    st.header("Réserver une table")
    st.image("https://images.unsplash.com/photo-1552566626-52f8b828add9?q=80&w=2070", use_container_width=True)
    
    with st.form("reservation"):
        col_r1, col_r2 = st.columns(2)
        nom_resa = col_r1.text_input("Votre Nom")
        tel_resa = col_r2.text_input("Téléphone")
        
        col_d1, col_d2 = st.columns(2)
        date_resa = col_d1.date_input("Date", datetime.date.today())
        heure_resa = col_d2.time_input("Heure", datetime.time(20, 00))
        nb_pers = st.slider("Nombre de personnes", 1, 10, 2)
        
        if st.form_submit_button("Confirmer la réservation"):
            # Lien WhatsApp pour la réservation
            msg_resa = f"Bonjour, je souhaite réserver une table pour {nb_pers} personnes le {date_resa} à {heure_resa}. Nom: {nom_resa}"
            link_resa = f"https://wa.me/221778601569?text={urllib.parse.quote(msg_resa)}"
            st.success("Redirection vers WhatsApp...")
            st.markdown(f'<meta http-equiv="refresh" content="0; url={link_resa}">', unsafe_allow_html=True)

# --- PAGE 4: PANIER ---
with tabs[3]:
    st.header("Votre Panier")
    
    if st.session_state.cart:
        total = 0
        for i, item in enumerate(st.session_state.cart):
            col_p1, col_p2, col_p3 = st.columns([4, 2, 1])
            col_p1.write(f"**{item['nom']}**")
            col_p2.write(f"{int(item['prix'])} F")
            if col_p3.button("❌", key=f"del_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()
            total += item['prix']
        
        st.markdown(f"<h3 style='text-align:right'>Total: {int(total)} FCFA</h3>", unsafe_allow_html=True)
        
        st.divider()
        mode = st.radio("Mode", ["Sur place", "Livraison"], horizontal=True)
        infos_client = st.text_input("Numéro de table ou Adresse")
        
        if st.button("🚀 COMMANDER"):
            if not infos_client:
                st.error("Indiquez votre table ou adresse.")
            else:
                # Sauvegarde DB
                items_str = ", ".join([i['nom'] for i in st.session_state.cart])
                c.execute('INSERT INTO commandes (articles, total, type_commande, detail_logistique) VALUES (?,?,?,?)',
                          (items_str, total, mode, infos_client))
                conn.commit()
                
                # WhatsApp
                msg = f"Nouvelle commande:\n{items_str}\nTotal: {int(total)} F\nPour: {mode} ({infos_client})"
                link = f"https://wa.me/221778601569?text={urllib.parse.quote(msg)}"
                
                st.session_state.cart = []
                st.session_state.cmd_faite = True
                st.markdown(f'<meta http-equiv="refresh" content="0; url={link}">', unsafe_allow_html=True)
                st.rerun()
                
    elif st.session_state.cmd_faite:
        st.success("Commande envoyée !")
        if st.button("Nouvelle commande"):
            st.session_state.cmd_faite = False
            st.rerun()
    else:
        st.info("Votre panier est vide.")
        st.image("https://cdn-icons-png.flaticon.com/512/2038/2038854.png", width=100)

# --- PAGE 5: ADMIN (Protégée) ---
with tabs[4]:
    st.header("Espace Gérant")
    
    if not st.session_state.admin_mode:
        pwd = st.text_input("Mot de passe", type="password")
        if st.button("Connexion"):
            if pwd == ADMIN_PASSWORD:
                st.session_state.admin_mode = True
                st.rerun()
            else:
                st.error("Erreur")
    else:
        if st.button("Déconnexion"):
            st.session_state.admin_mode = False
            st.rerun()
            
        tab_a, tab_b = st.tabs(["Commandes", "Menu"])
        
        with tab_a:
             # Rafraichissement auto pour les commandes
            from streamlit_autorefresh import st_autorefresh
            st_autorefresh(interval=30000, key="admin_refresh")
            
            commandes = pd.read_sql('SELECT * FROM commandes ORDER BY date DESC LIMIT 20', conn)
            for _, row in commandes.iterrows():
                with st.expander(f"{row['date']} - {int(row['total'])} FCFA ({row['type_commande']})"):
                    st.write(f"**Client:** {row['detail_logistique']}")
                    st.write(f"**Articles:** {row['articles']}")
                    if st.button("Supprimer", key=f"del_cmd_{row['id']}"):
                        c.execute('DELETE FROM commandes WHERE id=?', (row['id'],))
                        conn.commit()
                        st.rerun()
                        
        with tab_b:
            with st.form("new_plat"):
                n = st.text_input("Nom")
                p = st.number_input("Prix", step=100)
                d = st.text_area("Description")
                i = st.text_input("URL Image")
                if st.form_submit_button("Ajouter"):
                    c.execute('INSERT INTO menu (nom, prix, desc, img) VALUES (?,?,?,?)', (n, p, d, i))
                    conn.commit()
                    st.rerun()
            
            st.write("---")
            all_plats = pd.read_sql('SELECT * FROM menu', conn)
            for _, r in all_plats.iterrows():
                c1, c2 = st.columns([3, 1])
                c1.write(f"{r['nom']} ({int(r['prix'])} F)")
                if c2.button("🗑️", key=f"del_p_{r['id']}"):
                    c.execute('DELETE FROM menu WHERE id=?', (r['id'],))
                    conn.commit()
                    st.rerun()

