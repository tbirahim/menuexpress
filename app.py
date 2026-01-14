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
            <p style="font-size: 1.2rem; color: #aaa;">Ouvert tous les jours • </p>
        </div>
    """, unsafe_allow_html=True)

    st.write("##")

    # Section 1 : Thieboudienne (Le plat national)
    st.image("https://www.instagram.com/p/Ce4sVN4KH0T/", use_container_width=True) # Image Thieb/Riz poisson
    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">Thieboudienne Royal</div>
            <div class="feature-desc">Découvrez l'authenticité de notre riz au poisson national, cuisiné avec les légumes frais du marché et un savoir-faire traditionnel.</div>
        </div>
    """, unsafe_allow_html=True)

    # Section 2 : Yassa & Pastels
    st.image("data:image/jpeg;base64,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", use_container_width=True) # Image poulet/épices
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

