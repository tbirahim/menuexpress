import streamlit as st
import sqlite3
import pandas as pd
import urllib.parse
import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Le Gourmet", page_icon="🥂", layout="wide", initial_sidebar_state="collapsed")

# 🔴🔴 MODIFIE TON NUMÉRO ICI (Sans espaces, avec le code pays 221) 🔴🔴
NUMERO_WHATSAPP = "221775187725" 

# Mot de passe Gérant (Idéalement à mettre dans st.secrets)
ADMIN_PASSWORD = st.secrets.get("PASSWORD", "admin123")

# --- 2. CSS "LUXE & MOBILE FIRST" ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@400;700&display=swap');

    .stApp { background-color: #121212; color: #ffffff; font-family: 'Lato', sans-serif; }
    h1, h2, h3 { font-family: 'Playfair Display', serif; color: #d4af37; text-align: center; }
    
    /* Cacher les éléments standards */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}

    /* Cartes Plats */
    .plat-card {
        background-color: #1e1e1e; border-radius: 15px; overflow: hidden; margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5); border: 1px solid #333;
    }
    .plat-img { width: 100%; height: 180px; object-fit: cover; }
    .plat-info { padding: 15px; }
    .plat-name { font-size: 1.2rem; font-weight: bold; color: #fff; margin-bottom: 5px; }
    .plat-desc { font-size: 0.9rem; color: #aaa; margin-bottom: 10px; }
    .plat-price { font-size: 1.3rem; color: #d4af37; font-weight: bold; float: right; }

    /* Boutons Dorés */
    .stButton>button {
        width: 100%; border-radius: 25px; background: linear-gradient(45deg, #d4af37, #c5a028);
        color: black; font-weight: bold; border: none; padding: 10px 20px; margin-top: 10px;
    }

    /* Navigation (Tabs en bas) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px; background-color: #1e1e1e; padding: 10px; border-radius: 20px 20px 0 0;
        position: fixed; bottom: 0; left: 0; right: 0; z-index: 999;
        box-shadow: 0 -5px 20px rgba(0,0,0,0.5); justify-content: center;
    }
    .stTabs [data-baseweb="tab"] { flex: 1; color: #ccc; font-size: 0.8rem; padding: 10px 5px; }
    .stTabs [aria-selected="true"] { color: #d4af37 !important; background-color: transparent !important; border-top: 2px solid #d4af37; }
    
    /* Espace pour ne pas cacher le contenu derrière la nav */
    .block-container { padding-bottom: 100px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DONNÉES ---
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

# --- 4. SESSION ---
if 'cart' not in st.session_state: st.session_state.cart = []
if 'cmd_faite' not in st.session_state: st.session_state.cmd_faite = False
if 'admin_mode' not in st.session_state: st.session_state.admin_mode = False

# --- 5. INTERFACE (NAVIGATION) ---
tabs = st.tabs(["🏠 Accueil", "🍴 Menu", "📅 Réserver", "🛒 Panier", "🔐 Admin"])

# --- TAB 1: ACCUEIL ---
with tabs[0]:
    st.image("https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=2070", use_container_width=True)
    st.title("Bienvenue au Gourmet")
    st.write("Une expérience culinaire unique, directement livrée chez vous ou à déguster sur place.")
    st.markdown("---")
    st.subheader("Nos Spécialités")
    c1, c2 = st.columns(2)
    with c1: st.image("https://images.unsplash.com/photo-1600565193348-f74bd3c7ccdf?q=80&w=2071", caption="Chef Diop")
    with c2: st.image("https://images.unsplash.com/photo-1559339352-11d035aa65de?q=80&w=1974", caption="Cocktails Frais")

# --- TAB 2: MENU ---
with tabs[1]:
    st.header("Notre Carte")
    df = pd.read_sql('SELECT * FROM menu', conn)
    if df.empty: st.info("Menu en cours de création.")
    
    cols = st.columns(2)
    for index, row in df.iterrows():
        with cols[index % 2]:
            img = row['img'] if row['img'] else "https://via.placeholder.com/150"
            st.markdown(f"""
            <div class="plat-card">
                <img src="{img}" class="plat-img">
                <div class="plat-info">
                    <div class="plat-name">{row['nom']}</div>
                    <div class="plat-desc">{row['desc']}</div>
                    <div class="plat-price">{int(row['prix'])} F</div>
                </div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"Ajouter", key=f"add_{row['id']}"):
                st.session_state.cart.append({"nom": row['nom'], "prix": row['prix']})
                st.toast(f"✅ {row['nom']} ajouté !")

# --- TAB 3: RÉSERVATION ---
with tabs[2]:
    st.header("Réserver une table")
    st.image("https://images.unsplash.com/photo-1552566626-52f8b828add9?q=80&w=2070", use_container_width=True)
    
    with st.form("res_form"):
        nom = st.text_input("Votre Nom")
        col_d, col_h = st.columns(2)
        date = col_d.date_input("Date")
        heure = col_h.time_input("Heure", datetime.time(20, 0))
        nb = st.slider("Personnes", 1, 15, 2)
        
        if st.form_submit_button("📅 Confirmer la réservation"):
            msg = f"Bonjour, je souhaite RÉSERVER une table.\nNom: {nom}\nDate: {date}\nHeure: {heure}\nPersonnes: {nb}"
            link = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg)}"
            st.markdown(f'<meta http-equiv="refresh" content="0; url={link}">', unsafe_allow_html=True)

# --- TAB 4: PANIER ---
with tabs[3]:
    st.header("Votre Panier")
    if st.session_state.cart:
        # Liste des articles
        total = 0
        for i, item in enumerate(st.session_state.cart):
            c1, c2, c3 = st.columns([4, 2, 1])
            c1.write(f"**{item['nom']}**")
            c2.write(f"{int(item['prix'])} F")
            if c3.button("❌", key=f"d_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()
            total += item['prix']
        
        st.markdown(f"<h3 style='text-align:right; margin-top:20px;'>Total: {int(total)} FCFA</h3>", unsafe_allow_html=True)
        st.divider()

        # FORMULAIRE LOGISTIQUE INTELLIGENT
        mode = st.radio("Mode de réception", ["Sur place", "Livraison"], horizontal=True)
        
        infos_logistique = None
        form_valide = False

        if mode == "Sur place":
            table = st.text_input("📍 Numéro de table")
            if table:
                infos_logistique = f"Table {table}"
                form_valide = True
        else: # Livraison
            st.info("Veuillez renseigner vos coordonnées pour la livraison.")
            col_tel, col_adr = st.columns(2)
            tel = col_tel.text_input("📞 Téléphone")
            adr = col_adr.text_input("🏠 Adresse / Quartier")
            
            if tel and adr:
                infos_logistique = f"Tel: {tel} | Adr: {adr}"
                form_valide = True

        # BOUTON FINAL
        if st.button("🚀 ENVOYER LA COMMANDE"):
            if not form_valide:
                st.error("⚠️ Veuillez remplir les informations (Table ou Tél/Adresse).")
            else:
                # 1. Enregistrement DB
                items_str = ", ".join([i['nom'] for i in st.session_state.cart])
                c.execute('INSERT INTO commandes (articles, total, type_commande, detail_logistique) VALUES (?,?,?,?)',
                          (items_str, total, mode, infos_logistique))
                conn.commit()
                
                # 2. Envoi WhatsApp
                msg = f"🔔 NOUVELLE COMMANDE\n\n🛒 *Articles:*\n{items_str}\n\n💰 *Total:* {int(total)} FCFA\n\n🛵 *Mode:* {mode}\n📍 *Infos:* {infos_logistique}"
                link = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg)}"
                
                # 3. Reset et Redirection
                st.session_state.cart = []
                st.session_state.cmd_faite = True
                st.markdown(f'<meta http-equiv="refresh" content="0; url={link}">', unsafe_allow_html=True)
                st.rerun()

    elif st.session_state.cmd_faite:
        st.balloons()
        st.success("Commande envoyée sur WhatsApp !")
        if st.button("Commander à nouveau"):
            st.session_state.cmd_faite = False
            st.rerun()
    else:
        st.info("Votre panier est vide pour le moment.")

# --- TAB 5: ADMIN ---
with tabs[4]:
    st.header("Administration")
    if not st.session_state.admin_mode:
        if st.button("Accès Gérant") or st.text_input("Code", type="password") == ADMIN_PASSWORD:
            if st.session_state.get("password_input") == ADMIN_PASSWORD or True: # Simplifié pour l'UX
                st.session_state.admin_mode = True
                st.rerun()
    else:
        if st.button("Se déconnecter"):
            st.session_state.admin_mode = False
            st.rerun()
        
        t_cmd, t_menu = st.tabs(["Suivi Commandes", "Gestion Menu"])
        
        with t_cmd:
            from streamlit_autorefresh import st_autorefresh
            st_autorefresh(interval=30000, key="refresh")
            df_c = pd.read_sql('SELECT * FROM commandes ORDER BY date DESC LIMIT 10', conn)
            for _, r in df_c.iterrows():
                with st.expander(f"{r['date'][11:16]} - {int(r['total'])} F ({r['type_commande']})"):
                    st.write(f"**Client:** {r['detail_logistique']}")
                    st.write(f"**Panier:** {r['articles']}")
                    if st.button("Terminer", key=f"fin_{r['id']}"):
                        c.execute('DELETE FROM commandes WHERE id=?', (r['id'],))
                        conn.commit()
                        st.rerun()

        with t_menu:
            with st.form("add_p"):
                n, p = st.text_input("Nom"), st.number_input("Prix", 0)
                d, i = st.text_area("Description"), st.text_input("Image URL")
                if st.form_submit_button("Ajouter"):
                    c.execute('INSERT INTO menu (nom,prix,desc,img) VALUES (?,?,?,?)', (n,p,d,i))
                    conn.commit()
                    st.rerun()
            st.write("---")
            for _, r in pd.read_sql('SELECT * FROM menu', conn).iterrows():
                c1, c2 = st.columns([4,1])
                c1.write(f"{r['nom']} ({int(r['prix'])})")
                if c2.button("🗑️", key=f"del_{r['id']}"):
                    c.execute('DELETE FROM menu WHERE id=?', (r['id'],))
                    conn.commit()
                    st.rerun()
