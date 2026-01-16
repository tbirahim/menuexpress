import streamlit as st
import sqlite3
import pandas as pd
import urllib.parse
import datetime

# --- 1. CONFIGURATION & SÉCURITÉ ---
st.set_page_config(page_title="Menu express", page_icon="🥘", layout="wide", initial_sidebar_state="collapsed")

# 🔴 CONFIGURATION
NUMERO_WHATSAPP = "221778615900"
NUMERO_APPEL = "778615900"

# GESTION SÉCURISÉE DU MOT DE PASSE
# Créez un fichier .streamlit/secrets.toml pour le définir
try:
    ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]
except FileNotFoundError:
    # Fallback pour le développement local si pas de fichier secrets
    ADMIN_PASSWORD = "admin123" 

# --- 2. CSS LUXE SÉNÉGAL ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@300;400;700&display=swap');
    
    .stApp {{ background-color: #0c0c0c; color: #f0f0f0; font-family: 'Lato', sans-serif; }}
    h1, h2, h3 {{ font-family: 'Playfair Display', serif; color: #d4af37; text-align: center; }}
    
    /* Boutons */
    .btn-whatsapp {{ display: block; width: 100%; background-color: #25D366; color: white !important; text-align: center; padding: 15px; border-radius: 12px; font-weight: bold; text-decoration: none; margin-top: 10px; }}
    .btn-call {{ display: block; width: 100%; background-color: transparent; color: #d4af37 !important; text-align: center; padding: 10px; border-radius: 12px; font-weight: bold; text-decoration: none; border: 2px solid #d4af37; margin-top: 20px; }}
    
    /* Navigation */
    .stTabs [data-baseweb="tab-list"] {{ gap: 0px; background-color: #000; position: fixed; bottom: 0; left: 0; right: 0; z-index: 9999; border-top: 1px solid #d4af37; }}
    .stTabs [data-baseweb="tab"] {{ flex: 1; color: #888; padding: 15px 0; }}
    .stTabs [aria-selected="true"] {{ color: #d4af37 !important; background-color: #1a1a1a !important; }}

    /* Hero & Cards */
    .hero-senegal {{
        text-align: center; padding: 60px 20px; border-bottom: 1px solid #333;
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("https://images.unsplash.com/photo-1599481238640-4c1288750d7a?q=80&w=2070");
        background-size: cover; border-radius: 0 0 30px 30px;
    }}
    .plat-card {{ background:#1a1a1a; padding:15px; border-radius:10px; margin-bottom:10px; border-left: 4px solid #d4af37; }}
    
    .block-container {{ padding-bottom: 150px; padding-top: 0px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DONNÉES & FONCTIONS ---
def get_connection():
    return sqlite3.connect('teranga_resto.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS menu (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prix REAL, desc TEXT, img TEXT)')
    c.execute('''CREATE TABLE IF NOT EXISTS commandes 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, articles TEXT, total REAL, 
                  type_commande TEXT, detail_logistique TEXT, 
                  statut TEXT DEFAULT 'En attente', date DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()

init_db()

# Gestion du Panier (Ajout Intelligent)
def add_to_cart(item):
    if 'cart' not in st.session_state: st.session_state.cart = []
    
    # Vérifie si l'article existe déjà
    for p in st.session_state.cart:
        if p['id'] == item['id']:
            p['qty'] += 1
            st.toast(f"➕ Quantité augmentée : {item['nom']}")
            return
            
    # Sinon, ajoute le nouvel article
    new_item = item.copy()
    new_item['qty'] = 1
    st.session_state.cart.append(new_item)
    st.toast(f"✅ {item['nom']} ajouté au panier")

# Gestion du Panier (Retrait)
def remove_from_cart(index):
    if st.session_state.cart[index]['qty'] > 1:
        st.session_state.cart[index]['qty'] -= 1
    else:
        st.session_state.cart.pop(index)
    st.rerun()

# --- 4. NAVIGATION ---
if 'cart' not in st.session_state: st.session_state.cart = []
tabs = st.tabs(["🏠 Accueil", "🍴 Menu", "📅 Réserver", "🛒 Panier", "🔐 Admin"])

# --- TAB 1: ACCUEIL ---
with tabs[0]:
    st.markdown("""
        <div class="hero-senegal">
            <h1 style="font-size: 2.8rem; margin-bottom:0;">TERANGA GOURMET</h1>
            <p style="color: #d4af37; letter-spacing: 4px; font-weight: bold; font-size:0.9rem;">SAVEURS AUTHENTIQUES</p>
        </div>
    """, unsafe_allow_html=True)
    st.write("##")
    st.image("https://www.luxe-infinity-afrique.com/wp-content/uploads/2025/08/La-Cuisine-Africaine-Conquiert-la-France-1200x675.webp", use_container_width=True)
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h2 style="color: #fff;">Bienvenue</h2>
        <p style="color: #ccc;">Découvrez le meilleur de la gastronomie sénégalaise dans un cadre d'exception.</p>
        <p style="color: #d4af37; font-weight: bold;">📍 Mboro • 12h - 23h</p>
    </div>
    """, unsafe_allow_html=True)

# --- TAB 2: MENU ---
with tabs[1]:
    st.header("La Carte")
    df_menu = pd.read_sql('SELECT * FROM menu', get_connection())
    if df_menu.empty:
        st.info("Menu vide. Ajoutez des plats via l'Admin.")
    else:
        for index, row in df_menu.iterrows():
            st.markdown(f'''
                <div class="plat-card">
                    <span style="font-size:1.1rem; font-weight:bold;">{row["nom"]}</span><br>
                    <span style="color:#d4af37;">{int(row["prix"])} FCFA</span>
                </div>
            ''', unsafe_allow_html=True)
            # Conversion de la row pandas en dict pour le panier
            item_dict = {"id": row['id'], "nom": row['nom'], "prix": row['prix']}
            st.button(f"Ajouter", key=f"add_{row['id']}", on_click=add_to_cart, args=(item_dict,))

# --- TAB 3: RÉSERVATION ---
with tabs[2]:
    st.header("Réserver")
    with st.form("res_form"):
        nom = st.text_input("Nom")
        col1, col2 = st.columns(2)
        d = col1.date_input("Date")
        h = col2.time_input("Heure")
        p = st.slider("Personnes", 1, 20, 2)
        if st.form_submit_button("VALIDER"):
            msg = f"📝 *RÉSERVATION*\n👤 {nom}\n📅 {d}\n⏰ {h}\n👥 {p} pers"
            link = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg)}"
            st.success("Cliquez ci-dessous :")
            st.markdown(f'<a href="{link}" target="_blank" class="btn-whatsapp">👉 CONFIRMER SUR WHATSAPP</a>', unsafe_allow_html=True)

# --- TAB 4: PANIER (AMÉLIORÉ) ---
with tabs[3]:
    st.header("Mon Panier")
    if st.session_state.cart:
        total = 0
        txt_items = ""
        
        # Affichage des articles
        for i, item in enumerate(st.session_state.cart):
            subtotal = item['prix'] * item['qty']
            total += subtotal
            txt_items += f"- {item['nom']} (x{item['qty']})\n"
            
            # Ligne Panier : Nom | Qté | Prix | [-]
            c1, c2, c3, c4 = st.columns([3, 1, 2, 1])
            c1.write(f"**{item['nom']}**")
            c2.write(f"x{item['qty']}")
            c3.write(f"{int(subtotal)} F")
            if c4.button("➖", key=f"rem_{i}"):
                remove_from_cart(i)
        
        st.divider()
        st.markdown(f"<h2 style='text-align:right;'>Total: {int(total)} FCFA</h2>", unsafe_allow_html=True)
        
        # Formulaire Commande
        mode = st.radio("Mode", ["Sur place", "Livraison"], horizontal=True)
        log, ok = "", False
        
        if mode == "Sur place":
            t = st.text_input("Table N°")
            if t: log = f"Table {t}"; ok = True
        else:
            c_a, c_b = st.columns(2)
            tel = c_a.text_input("Tél")
            adr = c_b.text_input("Adresse")
            if tel and adr: log = f"Tél: {tel} | Adr: {adr}"; ok = True
            
        if st.button("🚀 COMMANDER"):
            if not ok:
                st.error("Merci de compléter les informations manquantes.")
            else:
                # 1. Enregistrement DB
                conn = get_connection()
                conn.cursor().execute('INSERT INTO commandes (articles, total, type_commande, detail_logistique) VALUES (?,?,?,?)', 
                                     (txt_items, total, mode, log))
                conn.commit()
                
                # 2. Lien WhatsApp
                msg = f"🥘 *COMMANDE*\n{txt_items}\n💰 *TOTAL:* {int(total)} F\n📍 {mode}\n📝 {log}"
                link = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg)}"
                st.markdown(f'<a href="{link}" target="_blank" class="btn-whatsapp">✅ ENVOYER LA COMMANDE</a>', unsafe_allow_html=True)
                
                # Option pour vider
                if st.button("Vider le panier"):
                    st.session_state.cart = []
                    st.rerun()
    else:
        st.info("Votre panier est vide.")
    
    st.markdown(f'<a href="tel:{NUMERO_APPEL}" class="btn-call">📞 APPELER LE RESTAURANT</a>', unsafe_allow_html=True)

# --- TAB 5: ADMIN (HISTORIQUE) ---
with tabs[4]:
    st.header("Administration")
    
    # Vérification mot de passe
    pwd = st.text_input("Mot de passe", type="password")
    if pwd == ADMIN_PASSWORD:
        st.success("Connecté")
        
        tab_menu, tab_histo = st.tabs(["Gérer le Menu", "Historique Commandes"])
        
        # --- SOUS-TAB: MENU ---
        with tab_menu:
            with st.form("add_plat", clear_on_submit=True):
                n = st.text_input("Nom")
                p = st.number_input("Prix", step=500)
                if st.form_submit_button("Ajouter"):
                    conn = get_connection()
                    conn.cursor().execute('INSERT INTO menu (nom, prix) VALUES (?,?)', (n,p))
                    conn.commit()
                    st.rerun()
            
            st.write("---")
            df_m = pd.read_sql('SELECT * FROM menu', get_connection())
            for _, r in df_m.iterrows():
                c1, c2 = st.columns([4,1])
                c1.write(f"{r['nom']} - {int(r['prix'])} F")
                if c2.button("🗑️", key=f"del_m_{r['id']}"):
                    get_connection().cursor().execute('DELETE FROM menu WHERE id=?', (r['id'],)).connection.commit()
                    st.rerun()

        # --- SOUS-TAB: HISTORIQUE ---
        with tab_histo:
            if st.button("🔄 Actualiser"): st.rerun()
            
            df_c = pd.read_sql('SELECT * FROM commandes ORDER BY id DESC', get_connection())
            
            # Calcul du Chiffre d'Affaires
            ca_total = df_c['total'].sum() if not df_c.empty else 0
            st.metric("Chiffre d'Affaires Total", f"{int(ca_total)} FCFA")
            
            st.dataframe(df_c, use_container_width=True)
            
            st.write("### Dernières Commandes")
            for _, r in df_c.head(5).iterrows():
                with st.expander(f"{r['date']} | {int(r['total'])} F | {r['type_commande']}"):
                    st.write(f"**Client:** {r['detail_logistique']}")
                    st.text(r['articles'])
                    if st.button("Supprimer l'historique", key=f"del_c_{r['id']}"):
                         get_connection().cursor().execute('DELETE FROM commandes WHERE id=?', (r['id'],)).connection.commit()
                         st.rerun()
    elif pwd:
        st.error("Mot de passe incorrect")
