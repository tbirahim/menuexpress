import streamlit as st
import sqlite3
import pandas as pd
import urllib.parse
import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Teranga Gourmet", page_icon="🥘", layout="wide", initial_sidebar_state="collapsed")

# 🔴🔴 TON NUMÉRO WHATSAPP ICI 🔴🔴
NUMERO_WHATSAPP = "221775187725" 

# Mot de passe Gérant
ADMIN_PASSWORD = st.secrets.get("PASSWORD", "admin123")

# --- 2. CSS "DARK LUXE SÉNÉGAL" ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@300;400;700&display=swap');

    .stApp { background-color: #0c0c0c; color: #f0f0f0; font-family: 'Lato', sans-serif; }
    
    h1, h2, h3 { font-family: 'Playfair Display', serif; color: #ffffff; text-align: center; font-weight: 700; }
    
    .gold-text { color: #d4af37; font-weight: bold; font-size: 1.1rem; text-align: center; text-transform: uppercase; letter-spacing: 2px; }

    /* Suppression du bloc blanc - Remplacé par un titre élégant sur fond noir */
    .hero-header {
        padding: 60px 20px;
        text-align: center;
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url("https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?q=80&w=2070");
        background-size: cover;
        border-bottom: 1px solid #333;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}

    /* Cartes Images Accueil */
    .feature-card { margin-bottom: 50px; text-align: center; padding: 0 15px; }
    .feature-img { width: 100%; border-radius: 15px; margin-bottom: 20px; border: 1px solid #d4af37; }
    .feature-title { font-family: 'Playfair Display', serif; font-size: 1.8rem; margin-bottom: 10px; color: #d4af37; }
    .feature-desc { font-size: 1rem; color: #ccc; line-height: 1.6; }

    /* Cartes Menu */
    .plat-card {
        background-color: #1a1a1a; border-radius: 12px; overflow: hidden; margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5); border: 1px solid #333; display: flex; align-items: center;
    }
    .plat-img-mini { width: 100px; height: 100px; object-fit: cover; }
    .plat-info { padding: 10px 15px; flex: 1; }
    .plat-name { font-size: 1.1rem; font-weight: bold; color: #fff; margin: 0; }
    .plat-price { font-size: 1.1rem; color: #d4af37; font-weight: bold; }

    /* Boutons */
    .stButton>button {
        width: 100%; border-radius: 5px; background-color: #d4af37;
        color: black; font-weight: bold; border: none; padding: 12px;
    }
    
    /* Nav en bas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px; background-color: #000; position: fixed; bottom: 0; left: 0; right: 0; z-index: 9999;
        border-top: 1px solid #d4af37;
    }
    .stTabs [data-baseweb="tab"] { flex: 1; color: #888; padding: 15px 0; }
    .stTabs [aria-selected="true"] { color: #d4af37 !important; background-color: #1a1a1a !important; }
    
    .block-container { padding-bottom: 120px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DONNÉES ---
def init_db():
    conn = sqlite3.connect('teranga_resto.db', check_same_thread=False)
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
tabs = st.tabs(["🏠 Accueil", "🍴 Menu", "📅 Réserver", "🛒 Panier", "🔐 Admin"])

# --- TAB 1: ACCUEIL (SÉNÉGAL DESIGN) ---
with tabs[0]:
    # Header sans bloc blanc
    st.markdown("""
        <div class="hero-header">
            <p class="gold-text">L'Art de la Cuisine Sénégalaise</p>
            <h1 style="font-size: 3rem;">Teranga Gourmet</h1>
            <p style="font-size: 1.2rem; color: #aaa;">Ouvert tous les jours • 12h - 23h</p>
        </div>
    """, unsafe_allow_html=True)

    st.write("##")

    # Section 1 : Thieboudienne (Le plat national)
    st.image("https://images.unsplash.com/photo-1627308595186-e6bb36712645?q=80&w=1974", use_container_width=True) # Image Thieb/Riz poisson
    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">Thieboudienne Royal</div>
            <div class="feature-desc">Découvrez l'authenticité de notre riz au poisson national, cuisiné avec les légumes frais du marché et un savoir-faire traditionnel.</div>
        </div>
    """, unsafe_allow_html=True)

    # Section 2 : Yassa & Pastels
    st.image("https://images.unsplash.com/photo-1604329760661-e71dc83f8f26?q=80&w=2070", use_container_width=True) # Image poulet/épices
    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">Saveurs de la Teranga</div>
            <div class="feature-desc">Du Yassa au poulet citronné aux Pastels croustillants, chaque bouchée est un voyage vers les côtes de Dakar.</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="gold-text" style="margin-bottom:30px;">Cuisine Fraîche • Livraison Rapide • Sur Place</div>', unsafe_allow_html=True)

# --- TAB 2: MENU ---
with tabs[1]:
    st.header("Notre Carte")
    df = pd.read_sql('SELECT * FROM menu', conn)
    if df.empty:
        st.info("Ajoutez des plats via l'onglet Admin.")
    else:
        for _, row in df.iterrows():
            img = row['img'] if row['img'] else "https://via.placeholder.com/150"
            st.markdown(f"""
            <div class="plat-card">
                <img src="{img}" class="plat-img-mini">
                <div class="plat-info">
                    <div class="plat-name">{row['nom']}</div>
                    <div class="plat-price">{int(row['prix'])} F</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"AJOUTER AU PANIER", key=f"add_{row['id']}"):
                st.session_state.cart.append({"nom": row['nom'], "prix": row['prix']})
                st.toast(f"✅ {row['nom']} ajouté !")

# --- TAB 3: RÉSERVATION ---
with tabs[2]:
    st.header("Réserver une table")
    with st.form("res_form"):
        nom = st.text_input("Votre Nom")
        col1, col2 = st.columns(2)
        date = col1.date_input("Date")
        heure = col2.time_input("Heure")
        nb = st.slider("Nombre de convives", 1, 12, 2)
        if st.form_submit_button("CONFIRMER SUR WHATSAPP"):
            msg = f"Bonjour, je souhaite RÉSERVER.\nNom: {nom}\nDate: {date}\nHeure: {heure}\nPers: {nb}"
            link = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg)}"
            st.markdown(f'<meta http-equiv="refresh" content="0; url={link}">', unsafe_allow_html=True)

# --- TAB 4: PANIER & LIVRAISON SÉPARÉE ---
with tabs[3]:
    st.header("Votre Commande")
    if st.session_state.cart:
        total = 0
        for i, item in enumerate(st.session_state.cart):
            c1, c2, c3 = st.columns([4, 2, 1])
            c1.write(f"**{item['nom']}**")
            c2.write(f"{int(item['prix'])} F")
            if c3.button("🗑️", key=f"del_{i}"):
                st.session_state.cart.pop(i); st.rerun()
            total += item['prix']
        
        st.markdown(f"<h2 style='text-align:right; color:#d4af37'>{int(total)} FCFA</h2>", unsafe_allow_html=True)
        st.divider()

        mode = st.radio("Mode de réception", ["Sur place", "Livraison"], horizontal=True)
        logistique, valid = "", False

        if mode == "Sur place":
            table = st.text_input("Numéro de table")
            if table: logistique = f"Table {table}"; valid = True
        else:
            col_t, col_a = st.columns(2)
            tel = col_t.text_input("Votre Téléphone")
            adr = col_a.text_input("Adresse exacte")
            if tel and adr: logistique = f"Tél: {tel} | Adr: {adr}"; valid = True

        if st.button("🚀 VALIDER & ENVOYER"):
            if not valid: st.error("Champs manquants")
            else:
                items = ", ".join([i['nom'] for i in st.session_state.cart])
                c.execute('INSERT INTO commandes (articles, total, type_commande, detail_logistique) VALUES (?,?,?,?)', (items, total, mode, logistique))
                conn.commit()
                msg = f"COMMANDE: {items}\nTotal: {total}F\nMode: {mode}\nInfos: {logistique}"
                link = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg)}"
                st.session_state.cart = []; st.session_state.cmd_faite = True
                st.markdown(f'<meta http-equiv="refresh" content="0; url={link}">', unsafe_allow_html=True)

    elif st.session_state.cmd_faite:
        st.balloons(); st.success("Commande envoyée !"); st.button("Nouvelle commande", on_click=lambda: st.session_state.update({"cmd_faite": False}))
    else: st.write("Panier vide.")

# --- TAB 5: ADMIN ---
with tabs[4]:
    st.header("Gérant")
    if not st.session_state.admin_mode:
        if st.text_input("Password", type="password") == ADMIN_PASSWORD:
            st.session_state.admin_mode = True; st.rerun()
    else:
        if st.button("Quitter"): st.session_state.admin_mode = False; st.rerun()
        t1, t2 = st.tabs(["Commandes", "Menu"])
        with t1:
            df_c = pd.read_sql('SELECT * FROM commandes ORDER BY date DESC', conn)
            for _, r in df_c.iterrows():
                with st.expander(f"{r['date']} - {r['total']}F"):
                    st.write(f"Client: {r['detail_logistique']}\nArticles: {r['articles']}")
                    if st.button("Archiver", key=f"a_{r['id']}"):
                        c.execute('DELETE FROM commandes WHERE id=?', (r['id'],)); conn.commit(); st.rerun()
        with t2:
            with st.form("add"):
                n, p = st.text_input("Nom"), st.number_input("Prix", 0)
                d, i = st.text_area("Description"), st.text_input("Image URL")
                if st.form_submit_button("Ajouter"):
                    c.execute('INSERT INTO menu (nom,prix,desc,img) VALUES (?,?,?,?)', (n,p,d,i)); conn.commit(); st.rerun()
