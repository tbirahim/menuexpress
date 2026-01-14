import streamlit as st
import sqlite3
import pandas as pd
import urllib.parse
import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Teranga Gourmet", page_icon="🥘", layout="wide", initial_sidebar_state="collapsed")

NUMERO_WHATSAPP = "221775187725" 
NUMERO_APPEL = "775187725"
ADMIN_PASSWORD = st.secrets.get("PASSWORD", "admin123")

# --- 2. STYLE CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@300;400;700&display=swap');
    .stApp {{ background-color: #0c0c0c; color: #f0f0f0; font-family: 'Lato', sans-serif; }}
    h1, h2, h3 {{ font-family: 'Playfair Display', serif; color: #d4af37; text-align: center; }}
    .btn-whatsapp {{ display: block; width: 100%; background-color: #25D366; color: white !important; text-align: center; padding: 15px; border-radius: 12px; font-weight: bold; text-decoration: none; margin-top: 10px; }}
    .btn-call {{ display: block; width: 100%; background-color: transparent; color: #d4af37 !important; text-align: center; padding: 10px; border-radius: 12px; font-weight: bold; text-decoration: none; border: 2px solid #d4af37; margin-top: 20px; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 0px; background-color: #000; position: fixed; bottom: 0; left: 0; right: 0; z-index: 9999; border-top: 1px solid #d4af37; }}
    .stTabs [data-baseweb="tab"] {{ flex: 1; color: #888; padding: 15px 0; }}
    .stTabs [aria-selected="true"] {{ color: #d4af37 !important; background-color: #1a1a1a !important; }}
    .block-container {{ padding-bottom: 150px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. FONCTIONS BASE DE DONNÉES ---
def get_connection():
    return sqlite3.connect('teranga_resto.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS menu (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prix REAL, desc TEXT, img TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS commandes (id INTEGER PRIMARY KEY AUTOINCREMENT, articles TEXT, total REAL, type_commande TEXT, detail_logistique TEXT, date DATETIME DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()

init_db()

# --- 4. NAVIGATION ---
tabs = st.tabs(["🏠 Accueil", "🍴 Menu", "📅 Réserver", "🛒 Panier", "🔐 Admin"])

# --- TAB 1: ACCUEIL ---
with tabs[0]:
    st.markdown('<h1 style="font-size: 2.5rem; margin-top:30px;">TERANGA GOURMET</h1>', unsafe_allow_html=True)
    st.image("https://static.wixstatic.com/media/504b32_37032d2ff43f4a54ae496d02b2137a52~mv2.jpg/v1/fill/w_528,h_294,al_c,q_80,usm_0.66_1.00_0.01,enc_avif,quality_auto/504b32_37032d2ff43f4a54ae496d02b2137a52~mv2.jpg", use_container_width=True)

# --- TAB 2: MENU ---
with tabs[1]:
    st.header("La Carte")
    conn = get_connection()
    df_menu = pd.read_sql('SELECT * FROM menu', conn)
    if df_menu.empty:
        st.info("Le menu est vide. Ajoutez des plats dans l'onglet Admin.")
    else:
        for _, row in df_menu.iterrows():
            st.markdown(f'<div style="background:#1a1a1a; padding:15px; border-radius:10px; margin-bottom:10px; border-left: 4px solid #d4af37;"><b>{row["nom"]}</b><br><span style="color:#d4af37;">{int(row["prix"])} FCFA</span></div>', unsafe_allow_html=True)
            if st.button(f"Ajouter au panier", key=f"shop_{row['id']}"):
                if 'cart' not in st.session_state: st.session_state.cart = []
                st.session_state.cart.append(row)
                st.toast(f"✅ {row['nom']} ajouté !")

# --- TAB 3: RÉSERVATION ---
with tabs[2]:
    st.header("Réserver")
    with st.form("res_v5"):
        nom_r = st.text_input("Nom")
        date_r = st.date_input("Date")
        heure_r = st.time_input("Heure")
        btn_res = st.form_submit_button("VALIDER")
        if btn_res:
            msg = f"📝 *RÉSERVATION*\n👤 Client: {nom_r}\n📅 Date: {date_r}\n⏰ Heure: {heure_r}"
            link = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg)}"
            st.markdown(f'<a href="{link}" target="_blank" class="btn-whatsapp">👉 CONFIRMER SUR WHATSAPP</a>', unsafe_allow_html=True)

# --- TAB 4: PANIER ---
with tabs[3]:
    st.header("Mon Panier")
    if 'cart' in st.session_state and st.session_state.cart:
        total = 0
        txt_items = ""
        for i, item in enumerate(st.session_state.cart):
            st.write(f"○ {item['nom']} ({int(item['prix'])} F)")
            total += item['prix']
            txt_items += f"- {item['nom']}\n"
        st.write(f"### Total : {int(total)} FCFA")
        
        mode = st.radio("Mode", ["Sur place", "Livraison"], horizontal=True)
        if mode == "Sur place":
            log = st.text_input("N° Table")
        else:
            t = st.text_input("Tél")
            a = st.text_input("Adresse")
            log = f"Tél: {t} | Adr: {a}"

        if st.button("🚀 ENVOYER"):
            msg_cmd = f"🥘 *COMMANDE*\n{txt_items}💰 *TOTAL :* {int(total)} F\n📍 *MODE :* {mode}\n📝 *INFOS :* {log}"
            link_cmd = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg_cmd)}"
            st.markdown(f'<a href="{link_cmd}" target="_blank" class="btn-whatsapp">✅ ENVOYER SUR WHATSAPP</a>', unsafe_allow_html=True)
    else:
        st.info("Panier vide.")
    st.markdown(f'<a href="tel:{NUMERO_APPEL}" class="btn-call">📞 APPELER LE RESTAURANT</a>', unsafe_allow_html=True)

# --- TAB 5: ADMIN (CORRIGÉ) ---
with tabs[4]:
    st.header("Gestion du Restaurant")
    pwd = st.text_input("Code secret", type="password")
    
    if pwd == ADMIN_PASSWORD:
        st.divider()
        st.subheader("➕ Ajouter un plat")
        with st.form("form_add_plat", clear_on_submit=True):
            n = st.text_input("Nom du plat (ex: Thieboudienne)")
            p = st.number_input("Prix (FCFA)", min_value=0, step=500)
            d = st.text_area("Description")
            i = st.text_input("Lien image (Optionnel)")
            submitted = st.form_submit_button("Enregistrer le plat")
            
            if submitted and n:
                conn = get_connection()
                c = conn.cursor()
                c.execute('INSERT INTO menu (nom, prix, desc, img) VALUES (?,?,?,?)', (n, p, d, i))
                conn.commit()
                st.success(f"Plat '{n}' ajouté !")
                st.rerun()

        st.divider()
        st.subheader("📋 Menu Actuel")
        conn = get_connection()
        df_edit = pd.read_sql('SELECT * FROM menu', conn)
        
        for _, row in df_edit.iterrows():
            col1, col2 = st.columns([4, 1])
            col1.write(f"**{row['nom']}** - {int(row['prix'])} F")
            if col2.button("🗑️", key=f"del_{row['id']}"):
                conn = get_connection()
                c = conn.cursor()
                c.execute('DELETE FROM menu WHERE id=?', (row['id'],))
                conn.commit()
                st.warning(f"Plat supprimé.")
                st.rerun()
