import streamlit as st
import sqlite3
import pandas as pd
import urllib.parse
import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Le Gourmet", page_icon="🍽️", layout="wide", initial_sidebar_state="collapsed")

# 🔴🔴 TON NUMÉRO WHATSAPP ICI 🔴🔴
NUMERO_WHATSAPP = "221775187725" 

# Mot de passe Gérant
ADMIN_PASSWORD = st.secrets.get("PASSWORD", "admin123")

# --- 2. CSS "LUXE & MOBILE" (Style Vidéo) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@300;400;700&display=swap');

    /* Fond et Texte Général */
    .stApp { background-color: #121212; color: #f0f0f0; font-family: 'Lato', sans-serif; }
    
    /* Titres */
    h1, h2, h3 { font-family: 'Playfair Display', serif; color: #ffffff; text-align: center; font-weight: 700; letter-spacing: 1px; }
    
    /* Sous-titres dorés */
    .gold-text { color: #d4af37; font-weight: bold; font-size: 1.2rem; text-align: center; margin-bottom: 5px; }

    /* Cacher les éléments standards */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}

    /* Bloc "Heures d'ouverture" (Style Vidéo) */
    .hours-card {
        background-color: #ffffff; color: #000000; 
        padding: 40px 20px; text-align: center; 
        border-radius: 0px; margin-bottom: 30px;
    }
    .hours-title { font-family: 'Playfair Display', serif; font-size: 2.5rem; margin: 0; }
    .hours-sub { font-size: 1.2rem; font-weight: 300; text-transform: uppercase; letter-spacing: 2px; }

    /* Cartes Images Accueil */
    .feature-card { margin-bottom: 40px; text-align: center; }
    .feature-img { width: 100%; border-radius: 4px; margin-bottom: 15px; }
    .feature-title { font-family: 'Playfair Display', serif; font-size: 1.8rem; margin-bottom: 10px; color: #fff; }
    .feature-desc { font-size: 1rem; color: #ccc; line-height: 1.6; padding: 0 10px; }

    /* Cartes Menu */
    .plat-card {
        background-color: #1e1e1e; border-radius: 12px; overflow: hidden; margin-bottom: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3); border: 1px solid #333; display: flex; align-items: center;
    }
    .plat-img-mini { width: 90px; height: 90px; object-fit: cover; }
    .plat-info { padding: 10px 15px; flex: 1; }
    .plat-name { font-size: 1.1rem; font-weight: bold; color: #fff; margin: 0; }
    .plat-desc { font-size: 0.8rem; color: #aaa; margin: 3px 0; }
    .plat-price { font-size: 1.1rem; color: #d4af37; font-weight: bold; }

    /* Boutons */
    .stButton>button {
        width: 100%; border-radius: 0px; background-color: #d4af37;
        color: black; font-weight: bold; border: none; padding: 12px 20px;
        text-transform: uppercase; letter-spacing: 1px;
    }
    
    /* Navigation Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px; background-color: #000; padding: 5px; border-radius: 0;
        position: fixed; bottom: 0; left: 0; right: 0; z-index: 9999;
        border-top: 1px solid #333;
    }
    .stTabs [data-baseweb="tab"] { flex: 1; color: #888; font-size: 0.8rem; padding: 15px 0; border: none; }
    .stTabs [aria-selected="true"] { color: #d4af37 !important; background-color: transparent !important; }
    
    .block-container { padding-bottom: 100px; padding-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DONNÉES ---
def init_db():
    conn = sqlite3.connect('restaurant_v2.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS menu (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prix REAL, desc TEXT, img TEXT)')
    c.execute('''CREATE TABLE IF NOT EXISTS commandes 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, articles TEXT, total REAL, 
                  type_commande TEXT, detail_logistique TEXT, date DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    return conn

conn = init_db()
c = conn.cursor()

# --- 4. SESSION ---
if 'cart' not in st.session_state: st.session_state.cart = []
if 'cmd_faite' not in st.session_state: st.session_state.cmd_faite = False
if 'admin_mode' not in st.session_state: st.session_state.admin_mode = False

# --- 5. NAVIGATION ---
tabs = st.tabs(["Accueil", "Menu", "Réserver", "Panier", "Admin"])

# --- TAB 1: ACCUEIL (STYLE VIDÉO) ---
with tabs[0]:
    # Section Blanche (Horaires)
    st.markdown("""
        <div class="hours-card">
            <h1 class="hours-title">De 12h à 23h</h1>
            <p class="hours-sub">Tous les Jours</p>
        </div>
    """, unsafe_allow_html=True)

    # Section Image + Texte 1
    st.image("https://images.unsplash.com/photo-1559339352-11d035aa65de?q=80&w=1974", use_container_width=True)
    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">Cuisine fraîche et locale</div>
            <div class="feature-desc">Nous utilisons uniquement des ingrédients de saison, locaux et de haute qualité pour garantir des saveurs authentiques.</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Section Image + Texte 2
    st.image("https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=2070", use_container_width=True)
    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">Ambiance conviviale</div>
            <div class="feature-desc">Notre restaurant offre une atmosphère chaleureuse et accueillante, parfaite pour toutes vos occasions.</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

    # Section Happy Hour
    st.markdown('<div class="gold-text">HAPPY HOUR</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-desc" style="text-align:center;">Profitez de nos réductions sur les boissons de 17h à 19h.</div>', unsafe_allow_html=True)


# --- TAB 2: MENU (STYLE APP) ---
with tabs[1]:
    st.header("Notre Carte")
    
    df = pd.read_sql('SELECT * FROM menu', conn)
    if df.empty:
        st.info("Le menu est vide.")
    else:
        for _, row in df.iterrows():
            img = row['img'] if row['img'] else "https://via.placeholder.com/150"
            # Carte horizontale plus compacte
            st.markdown(f"""
            <div class="plat-card">
                <img src="{img}" class="plat-img-mini">
                <div class="plat-info">
                    <div class="plat-name">{row['nom']}</div>
                    <div class="plat-desc">{row['desc']}</div>
                    <div class="plat-price">{int(row['prix'])} F</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"AJOUTER", key=f"add_{row['id']}"):
                st.session_state.cart.append({"nom": row['nom'], "prix": row['prix']})
                st.toast(f"✅ {row['nom']} ajouté !")

# --- TAB 3: RÉSERVATION ---
with tabs[2]:
    st.header("Réserver une table")
    st.write("Réservez en quelques clics.")
    
    with st.form("res_form"):
        nom = st.text_input("Votre Nom")
        col_d, col_h = st.columns(2)
        date = col_d.date_input("Date")
        heure = col_h.time_input("Heure", datetime.time(20, 0))
        nb = st.slider("Nombre de personnes", 1, 10, 2)
        
        if st.form_submit_button("CONFIRMER LA RÉSERVATION"):
            msg = f"Bonjour, je souhaite RÉSERVER une table.\nNom: {nom}\nDate: {date}\nHeure: {heure}\nPersonnes: {nb}"
            link = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg)}"
            st.markdown(f'<meta http-equiv="refresh" content="0; url={link}">', unsafe_allow_html=True)

# --- TAB 4: PANIER ---
with tabs[3]:
    st.header("Votre Commande")
    
    if st.session_state.cart:
        total = 0
        for i, item in enumerate(st.session_state.cart):
            c1, c2, c3 = st.columns([4, 2, 1])
            c1.write(f"**{item['nom']}**")
            c2.write(f"{int(item['prix'])} F")
            if c3.button("x", key=f"del_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()
            total += item['prix']
        
        st.markdown(f"<h2 style='text-align:right; color:#d4af37'>Total: {int(total)} FCFA</h2>", unsafe_allow_html=True)
        st.divider()

        mode = st.radio("Mode de réception", ["Sur place", "Livraison"], horizontal=True)
        
        logistique = ""
        valid = False

        if mode == "Sur place":
            table = st.text_input("Numéro de table")
            if table:
                logistique = f"Table {table}"
                valid = True
        else:
            col1, col2 = st.columns(2)
            tel = col1.text_input("Téléphone")
            adr = col2.text_input("Adresse")
            if tel and adr:
                logistique = f"Tél: {tel} | Adr: {adr}"
                valid = True

        if st.button("VALIDER LA COMMANDE"):
            if not valid:
                st.error("Merci de remplir les informations (Table ou Tél/Adresse)")
            else:
                items = ", ".join([i['nom'] for i in st.session_state.cart])
                c.execute('INSERT INTO commandes (articles, total, type_commande, detail_logistique) VALUES (?,?,?,?)',
                          (items, total, mode, logistique))
                conn.commit()
                
                msg = f"NOUVELLE COMMANDE\n\n*Articles:* {items}\n*Total:* {int(total)} FCFA\n*Mode:* {mode}\n*Infos:* {logistique}"
                link = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg)}"
                
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
        st.write("Votre panier est vide.")

# --- TAB 5: ADMIN ---
with tabs[4]:
    st.header("Gestion")
    if not st.session_state.admin_mode:
        if st.text_input("Mot de passe", type="password") == ADMIN_PASSWORD:
            st.session_state.admin_mode = True
            st.rerun()
    else:
        if st.button("Déconnexion"):
            st.session_state.admin_mode = False
            st.rerun()
        
        t1, t2 = st.tabs(["Commandes", "Menu"])
        
        with t1:
            from streamlit_autorefresh import st_autorefresh
            st_autorefresh(interval=30000)
            df = pd.read_sql('SELECT * FROM commandes ORDER BY date DESC LIMIT 10', conn)
            for _, r in df.iterrows():
                st.info(f"{r['date']} | {int(r['total'])}F | {r['type_commande']}")
                st.write(r['articles'])
                st.write(f"📍 {r['detail_logistique']}")
                if st.button("Archiver", key=f"arch_{r['id']}"):
                    c.execute('DELETE FROM commandes WHERE id=?', (r['id'],))
                    conn.commit()
                    st.rerun()
        
        with t2:
            with st.form("add"):
                n = st.text_input("Nom")
                p = st.number_input("Prix", 0)
                d = st.text_area("Desc")
                i = st.text_input("Image URL")
                if st.form_submit_button("Ajouter"):
                    c.execute('INSERT INTO menu (nom, prix, desc, img) VALUES (?,?,?,?)', (n,p,d,i))
                    conn.commit()
                    st.rerun()
            
            st.write("---")
            menu = pd.read_sql('SELECT * FROM menu', conn)
            for _, r in menu.iterrows():
                c1, c2 = st.columns([3,1])
                c1.write(f"{r['nom']} - {int(r['prix'])}F")
                if c2.button("X", key=f"del_{r['id']}"):
                    c.execute('DELETE FROM menu WHERE id=?', (r['id'],))
                    conn.commit()
                    st.rerun()
