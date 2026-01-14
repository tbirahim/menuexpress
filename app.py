import streamlit as st
import sqlite3
import pandas as pd
import urllib.parse
import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Teranga Gourmet", page_icon="🥘", layout="wide", initial_sidebar_state="collapsed")

# 🔴 CONFIGURATION NUMÉROS (Change-les ici)
NUMERO_WHATSAPP = "221775187725" # Format: 221 + numéro sans espaces
NUMERO_APPEL = "775187725"
ADMIN_PASSWORD = st.secrets.get("PASSWORD", "admin123")

# --- 2. STYLE CSS SÉNÉGAL LUXE ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@300;400;700&display=swap');
    
    .stApp {{ background-color: #0c0c0c; color: #f0f0f0; font-family: 'Lato', sans-serif; }}
    h1, h2, h3 {{ font-family: 'Playfair Display', serif; color: #d4af37; text-align: center; }}
    
    /* Bouton WhatsApp de secours */
    .btn-whatsapp {{
        display: block; width: 100%; background-color: #25D366; color: white !important;
        text-align: center; padding: 18px; border-radius: 12px; font-weight: bold;
        text-decoration: none; font-size: 1.1rem; border: 2px solid #ffffff44; margin-top: 10px;
    }}
    
    /* Bouton d'Appel */
    .btn-call {{
        display: block; width: 100%; background-color: transparent; color: #d4af37 !important;
        text-align: center; padding: 12px; border-radius: 12px; font-weight: bold;
        text-decoration: none; border: 2px solid #d4af37; margin-top: 20px;
    }}

    /* Navigation Mobile en bas */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0px; background-color: #000; position: fixed; bottom: 0; left: 0; right: 0; z-index: 9999;
        border-top: 1px solid #d4af37;
    }}
    .stTabs [data-baseweb="tab"] {{ flex: 1; color: #888; padding: 15px 0; }}
    .stTabs [aria-selected="true"] {{ color: #d4af37 !important; background-color: #1a1a1a !important; }}

    .hero-senegal {{
        text-align: center; padding: 40px 10px; border-bottom: 1px solid #333;
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("https://images.unsplash.com/photo-1599481238640-4c1288750d7a?q=80&w=2070");
        background-size: cover;
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

# --- 4. NAVIGATION ---
tabs = st.tabs(["🏠 Accueil", "🍴 Menu", "📅 Réserver", "🛒 Panier", "🔐 Admin"])

# --- TAB 1: ACCUEIL (SÉNÉGAL DESIGN) ---
with tabs[0]:
    st.markdown("""
        <div class="hero-senegal">
            <h1 style="font-size: 2.5rem; margin-bottom:0;">TERANGA GOURMET</h1>
            <p style="color: #d4af37; letter-spacing: 3px; font-weight: bold;">L'AUTHENTICITÉ DU SÉNÉGAL</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("##")
    # Image d'un plat sénégalais (Thiéboudienne ou Yassa)
    st.image("https://images.unsplash.com/photo-1627308595186-e6bb36712645?q=80&w=1974", caption="Notre célèbre Thiéboudienne Rouge", use_container_width=True)
    
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h3>Bienvenue chez Vous</h3>
        <p style="color: #ccc;">Découvrez une cuisine généreuse, faite avec les meilleurs produits du terroir sénégalais. Du riz au poisson au Yassa fumant, chaque plat raconte une histoire.</p>
        <p style="color: #d4af37; font-weight: bold;">📍 Dakar, Sénégal • ⏰ 12h00 - 23h30</p>
    </div>
    """, unsafe_allow_html=True)

# --- TAB 2: MENU ---
with tabs[1]:
    st.header("La Carte")
    df = pd.read_sql('SELECT * FROM menu', conn)
    for _, row in df.iterrows():
        st.markdown(f'''
            <div style="background:#1a1a1a; padding:15px; border-radius:10px; margin-bottom:10px; border-left: 4px solid #d4af37;">
                <span style="font-size:1.2rem; font-weight:bold;">{row['nom']}</span><br>
                <span style="color:#d4af37; font-size:1.1rem;">{int(row['prix'])} FCFA</span>
            </div>
        ''', unsafe_allow_html=True)
        if st.button(f"Ajouter au panier", key=f"add_{row['id']}"):
            if 'cart' not in st.session_state: st.session_state.cart = []
            st.session_state.cart.append(row)
            st.toast(f"✅ {row['nom']} ajouté !")

# --- TAB 3: RÉSERVATION (CONFIRMATION FIXÉE) ---
with tabs[2]:
    st.header("Réserver une table")
    with st.form("res_v4"):
        nom_r = st.text_input("Nom Complet")
        col_d, col_h = st.columns(2)
        date_r = col_d.date_input("Date")
        heure_r = col_h.time_input("Heure")
        pers_r = st.slider("Nombre de personnes", 1, 10, 2)
        btn_res = st.form_submit_button("VALIDER LA RÉSERVATION")
        
        if btn_res:
            msg_res = f"📝 *NOUVELLE RÉSERVATION*\n👤 Client: {nom_r}\n📅 Date: {date_r.strftime('%d/%m')}\n⏰ Heure: {heure_r.strftime('%H:%M')}\n👥 Nombre: {pers_r} personnes"
            link_res = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg_res)}"
            
            st.success("Cliquez sur le bouton ci-dessous pour confirmer")
            st.markdown(f'<a href="{link_res}" target="_blank" class="btn-whatsapp">👉 CONFIRMER SUR WHATSAPP</a>', unsafe_allow_html=True)

# --- TAB 4: PANIER & VALIDATION (CONFIRMATION FIXÉE) ---
with tabs[3]:
    st.header("Mon Panier")
    if 'cart' in st.session_state and st.session_state.cart:
        total = 0
        txt_items = ""
        for i, item in enumerate(st.session_state.cart):
            st.write(f"○ {item['nom']} - {int(item['prix'])} F")
            total += item['prix']
            txt_items += f"- {item['nom']}\n"
        
        st.write(f"### Total : {int(total)} FCFA")
        st.divider()
        
        mode = st.radio("Mode de réception", ["Sur place", "Livraison"], horizontal=True)
        log, ok = "", False
        
        if mode == "Sur place":
            t = st.text_input("N° de Table")
            if t: log = f"Table {t}"; ok = True
        else:
            c1, c2 = st.columns(2)
            tel = c1.text_input("Téléphone")
            adr = c2.text_input("Adresse de livraison")
            if tel and adr: log = f"Tél: {tel} | Adr: {adr}"; ok = True

        if st.button("🚀 PRÉPARER LA COMMANDE"):
            if not ok:
                st.error("⚠️ Veuillez remplir les informations demandées.")
            else:
                msg_cmd = f"🥘 *COMMANDE TERANGA*\n--------------------------\n{txt_items}\n💰 *TOTAL :* {int(total)} FCFA\n📍 *MODE :* {mode}\n📝 *INFOS :* {log}\n--------------------------"
                link_cmd = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg_cmd)}"
                
                # Sauvegarde en DB
                c = conn.cursor()
                c.execute('INSERT INTO commandes (articles, total, type_commande, detail_logistique) VALUES (?,?,?,?)', (txt_items, total, mode, log))
                conn.commit()
                
                st.markdown(f'<a href="{link_cmd}" target="_blank" class="btn-whatsapp">✅ ENVOYER SUR WHATSAPP</a>', unsafe_allow_html=True)
                if st.button("Vider le panier"):
                    st.session_state.cart = []
                    st.rerun()
    else:
        st.info("Votre panier est vide.")

    # Bouton d'appel direct toujours présent
    st.markdown(f'<a href="tel:{NUMERO_APPEL}" class="btn-call">📞 APPELER LE RESTAURANT</a>', unsafe_allow_html=True)

# --- TAB 5: ADMIN ---
with tabs[4]:
    if st.text_input("Code Gérant", type="password") == ADMIN_PASSWORD:
        st.header("Gestion")
        st.write("---")
        if st.button("Tout supprimer"):
            conn.cursor().execute("DELETE FROM commandes"); conn.commit(); st.rerun()
        df_adm = pd.read_sql('SELECT * FROM commandes ORDER BY id DESC', conn)
        st.dataframe(df_adm)
