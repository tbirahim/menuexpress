import streamlit as st
import sqlite3
import pandas as pd
import urllib.parse
import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Teranga Gourmet", page_icon="🥘", layout="wide", initial_sidebar_state="collapsed")

# 🔴 TON NUMÉRO (Format international sans le + pour WhatsApp)
NUMERO_WHATSAPP = "221775187725" 
# 📞 TON NUMÉRO POUR APPEL (Format standard)
NUMERO_APPEL = "775187725"

ADMIN_PASSWORD = st.secrets.get("PASSWORD", "admin123")

# --- 2. CSS CUSTOM ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@300;400;700&display=swap');
    .stApp {{ background-color: #0c0c0c; color: #f0f0f0; font-family: 'Lato', sans-serif; }}
    h1, h2, h3 {{ font-family: 'Playfair Display', serif; color: #d4af37; text-align: center; }}
    
    /* Bouton d'Appel Spécial */
    .call-button {{
        display: flex; align-items: center; justify-content: center;
        background-color: #25D366; color: white !important;
        padding: 15px; border-radius: 10px; text-decoration: none;
        font-weight: bold; margin-top: 20px; border: 1px solid #ffffff33;
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0px; background-color: #000; position: fixed; bottom: 0; left: 0; right: 0; z-index: 9999;
        border-top: 1px solid #d4af37;
    }}
    .block-container {{ padding-bottom: 150px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DONNÉES ---
def init_db():
    conn = sqlite3.connect('teranga_resto.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS menu (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prix REAL, desc TEXT, img TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS commandes (id INTEGER PRIMARY KEY AUTOINCREMENT, articles TEXT, total REAL, type_commande TEXT, detail_logistique TEXT, date DATETIME DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    return conn

conn = init_db()
c = conn.cursor()

# --- 4. NAVIGATION ---
tabs = st.tabs(["🏠 Accueil", "🍴 Menu", "📅 Réserver", "🛒 Panier", "🔐 Admin"])

# --- TAB 1: ACCUEIL ---
with tabs[0]:
    st.markdown('<h1 style="margin-top:20px;">Teranga Gourmet</h1>', unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1627308595186-e6bb36712645?q=80&w=1974", use_container_width=True)
    st.markdown('<p style="text-align:center; color:#d4af37; letter-spacing:2px;">OUVERT 12H - 23H</p>', unsafe_allow_html=True)

# --- TAB 2: MENU ---
with tabs[1]:
    st.header("La Carte")
    df = pd.read_sql('SELECT * FROM menu', conn)
    for _, row in df.iterrows():
        col_img, col_txt = st.columns([1, 3])
        if row['img']: col_img.image(row['img'], use_container_width=True)
        col_txt.write(f"**{row['nom']}**")
        col_txt.write(f"{int(row['prix'])} FCFA")
        if col_txt.button(f"Ajouter", key=f"add_{row['id']}"):
            if 'cart' not in st.session_state: st.session_state.cart = []
            st.session_state.cart.append(row)
            st.toast("Ajouté !")

# --- TAB 3: RÉSERVATION ---
with tabs[2]:
    st.header("Réserver")
    with st.form("res_v3"):
        nom = st.text_input("Votre Nom")
        d = st.date_input("Date")
        h = st.time_input("Heure")
        p = st.number_input("Personnes", 1, 15, 2)
        if st.form_submit_button("VALIDER SUR WHATSAPP"):
            msg = f"📝 *RÉSERVATION*\n👤 Nom: {nom}\n📅 Date: {d.strftime('%d/%m')}\n⏰ Heure: {h.strftime('%H:%M')}\n👥 Pers: {p}"
            st.markdown(f'<meta http-equiv="refresh" content="0; url=https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg)}">', unsafe_allow_html=True)

# --- TAB 4: PANIER & APPEL ---
with tabs[3]:
    st.header("Panier")
    if 'cart' in st.session_state and st.session_state.cart:
        total = 0
        txt_items = ""
        for i, item in enumerate(st.session_state.cart):
            st.write(f"• {item['nom']} ({int(item['prix'])} F)")
            total += item['prix']
            txt_items += f"- {item['nom']}\n"
        
        st.write(f"### Total: {int(total)} F")
        mode = st.radio("Option", ["Sur place", "Livraison"], horizontal=True)
        
        log, ok = "", False
        if mode == "Sur place":
            t = st.text_input("Numéro de table")
            if t: log = f"Table {t}"; ok = True
        else:
            tel = st.text_input("Téléphone")
            adr = st.text_input("Adresse")
            if tel and adr: log = f"Tél: {tel} | Adr: {adr}"; ok = True
            
        if st.button("🚀 ENVOYER LA COMMANDE"):
            if not ok: st.error("Infos manquantes")
            else:
                msg = f"🥘 *COMMANDE*\n{txt_items}💰 *Total:* {int(total)} F\n📍 *Mode:* {mode}\n📝 *Infos:* {log}"
                c.execute('INSERT INTO commandes (articles, total, type_commande, detail_logistique) VALUES (?,?,?,?)', (txt_items, total, mode, log))
                conn.commit()
                st.session_state.cart = []
                st.markdown(f'<meta http-equiv="refresh" content="0; url=https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg)}">', unsafe_allow_html=True)
    else:
        st.write("Votre panier est vide.")

    # --- SECTION APPEL (TOUJOURS VISIBLE) ---
    st.markdown("---")
    st.write("📞 Un problème ? Une question ?")
    st.markdown(f'<a href="tel:{NUMERO_APPEL}" class="call-button">📞 APPELER LE RESTAURANT</a>', unsafe_allow_html=True)

# --- TAB 5: ADMIN ---
with tabs[4]:
    if st.text_input("Admin Code", type="password") == ADMIN_PASSWORD:
        st.write("### Gestion Commandes")
        cmds = pd.read_sql('SELECT * FROM commandes ORDER BY id DESC LIMIT 5', conn)
        st.table(cmds)
        if st.button("Vider l'historique"):
            c.execute("DELETE FROM commandes"); conn.commit(); st.rerun()
