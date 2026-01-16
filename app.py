import streamlit as st
import sqlite3
import pandas as pd
import urllib.parse
import datetime
import base64

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Menu-Express", 
    page_icon="🥘", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 🔴 CONFIGURATION PERSONNELLE
NUMERO_WHATSAPP = "221778615900"
NUMERO_APPEL = "778615900"

# Sécurité : Le mot de passe est géré via st.secrets sur le Cloud
try:
    ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]
except:
    ADMIN_PASSWORD = "admin123"

# --- 2. STYLE CSS (Menu Latéral & Design Sénégal) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@300;400;700&display=swap');
    
    .stApp { background-color: #0c0c0c; color: #f0f0f0; font-family: 'Lato', sans-serif; }
    h1, h2, h3 { font-family: 'Playfair Display', serif; color: #d4af37; text-align: center; }

    /* Barre latérale (Menu Hamburger) */
    [data-testid="stSidebar"] { background-color: #1a1a1a; border-right: 1px solid #d4af37; }
    
    /* Cartes des plats avec photos */
    .plat-card {
        background:#1a1a1a; border-radius:15px; overflow:hidden;
        margin-bottom:25px; border: 1px solid #333; transition: 0.3s;
    }
    .plat-img { width: 100%; height: 220px; object-fit: cover; }
    .plat-info { padding: 15px; text-align: center; }
    
    /* Boutons personnalisés */
    .btn-whatsapp { display: block; width: 100%; background-color: #25D366; color: white !important; text-align: center; padding: 15px; border-radius: 12px; font-weight: bold; text-decoration: none; margin-top: 10px; }
    .btn-call { display: block; width: 100%; background-color: transparent; color: #d4af37 !important; text-align: center; padding: 10px; border-radius: 12px; font-weight: bold; text-decoration: none; border: 2px solid #d4af37; margin: 20px 0; }
    
    .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. GESTION BASE DE DONNÉES ---
def get_connection():
    return sqlite3.connect('teranga_resto.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS menu (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prix REAL, desc TEXT, img TEXT)')
    c.execute('''CREATE TABLE IF NOT EXISTS commandes 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, articles TEXT, total REAL, 
                  type_commande TEXT, detail_logistique TEXT, date DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()

init_db()

# --- 4. LOGIQUE DU PANIER ---
if 'cart' not in st.session_state:
    st.session_state.cart = []

def add_to_cart(item):
    for p in st.session_state.cart:
        if p['id'] == item['id']:
            p['qty'] += 1
            st.toast(f"➕ {item['nom']} ajouté !")
            return
    new_item = item.copy()
    new_item['qty'] = 1
    st.session_state.cart.append(new_item)
    st.toast(f"✅ {item['nom']} au panier")

def remove_from_cart(index):
    if st.session_state.cart[index]['qty'] > 1:
        st.session_state.cart[index]['qty'] -= 1
    else:
        st.session_state.cart.pop(index)
    st.rerun()

# --- 5. NAVIGATION (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h2 style='text-align:left;'>Teranga Gourmet</h2>", unsafe_allow_html=True)
    nb_items = sum(item['qty'] for item in st.session_state.cart)
    page = st.radio("Navigation", ["Accueil", "La Carte", "Réserver", f"Panier ({nb_items})", "Admin"])
    st.write("---")
    st.markdown(f'<a href="tel:{NUMERO_APPEL}" class="btn-call">📞 APPELER</a>', unsafe_allow_html=True)

# --- PAGES ---

if page == "Accueil":
    st.image("https://www.luxe-infinity-afrique.com/wp-content/uploads/2025/08/La-Cuisine-Africaine-Conquiert-la-France-1200x675.webp", use_container_width=True)
    st.markdown("<h1>L'Authenticité du Sénégal</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Bienvenue chez Teranga Gourmet. Goûtez à la passion de notre terroir.</p>", unsafe_allow_html=True)

elif page == "La Carte":
    st.image("https://i.pinimg.com/736x/bf/0b/1c/bf0b1c9a8bcac534c692d3e627b5275b.jpg", use_container_width=True)
    st.header("Notre Menu")
    
    df_menu = pd.read_sql('SELECT * FROM menu', get_connection())
    if df_menu.empty:
        st.info("Le gérant prépare le menu...")
    else:
        for index, row in df_menu.iterrows():
            # Affichage en carte avec image
            img = row['img'] if row['img'] else "https://via.placeholder.com/400x250?text=Teranga+Gourmet"
            st.markdown(f'''
                <div class="plat-card">
                    <img src="{img}" class="plat-img">
                    <div class="plat-info">
                        <h3>{row['nom']}</h3>
                        <p style="color:#d4af37; font-size:1.2rem; font-weight:bold;">{int(row['prix'])} FCFA</p>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
            if st.button(f"Choisir {row['nom']}", key=f"btn_{row['id']}", use_container_width=True):
                add_to_cart({"id": row['id'], "nom": row['nom'], "prix": row['prix']})

elif page == "Réserver":
    st.image("https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=2070", use_container_width=True)
    st.header("Réserver une table")
    with st.form("res_form"):
        nom = st.text_input("Votre Nom")
        date = st.date_input("Date")
        heure = st.time_input("Heure")
        pers = st.number_input("Nombre de personnes", 1, 20, 2)
        if st.form_submit_button("Envoyer la demande"):
            msg = f"📝 *RÉSERVATION*\n👤 Nom: {nom}\n📅 Date: {date}\n⏰ Heure: {heure}\n👥 Pers: {pers}"
            link = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg)}"
            st.markdown(f'<a href="{link}" target="_blank" class="btn-whatsapp">CONFIRMER SUR WHATSAPP</a>', unsafe_allow_html=True)

elif "Panier" in page:
    st.header("Votre Panier")
    if not st.session_state.cart:
        st.write("Votre panier est vide.")
    else:
        total = 0
        txt_items = ""
        for i, item in enumerate(st.session_state.cart):
            sub = item['prix'] * item['qty']
            total += sub
            txt_items += f"- {item['nom']} (x{item['qty']})\n"
            c1, c2, c3 = st.columns([3, 1, 1])
            c1.write(f"**{item['nom']}**")
            c2.write(f"x{item['qty']}")
            if c3.button("➖", key=f"del_{i}"): remove_from_cart(i)
        
        st.write("---")
        st.markdown(f"### Total: {int(total)} FCFA")
        
        mode = st.radio("Option", ["Sur place", "Livraison"])
        info = st.text_input("N° Table ou Adresse & Tél")
        
        if st.button("🚀 VALIDER LA COMMANDE"):
            if not info: st.error("Précisez l'adresse ou la table.")
            else:
                conn = get_connection()
                conn.cursor().execute('INSERT INTO commandes (articles, total, type_commande, detail_logistique) VALUES (?,?,?,?)', (txt_items, total, mode, info))
                conn.commit()
                msg = f"🥘 *COMMANDE*\n{txt_items}💰 Total: {int(total)} F\n📍 {mode}\n📝 {info}"
                link = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg)}"
                st.markdown(f'<a href="{link}" target="_blank" class="btn-whatsapp">ENVOYER VIA WHATSAPP</a>', unsafe_allow_html=True)

elif page == "Admin":
    st.header("Espace Gérant")
    if st.text_input("Code secret", type="password") == ADMIN_PASSWORD:
        tab_menu, tab_histo = st.tabs(["Gestion Menu", "Historique Commandes"])
        
        with tab_menu:
            st.subheader("Ajouter un plat")
            with st.form("add_form", clear_on_submit=True):
                nom = st.text_input("Nom du plat")
                prix = st.number_input("Prix (FCFA)", step=500)
                img = st.text_input("Lien de l'image (URL)")
                if st.form_submit_button("Enregistrer"):
                    conn = get_connection()
                    conn.cursor().execute('INSERT INTO menu (nom, prix, img) VALUES (?,?,?)', (nom, prix, img))
                    conn.commit()
                    st.rerun()
            
            st.write("---")
            df_m = pd.read_sql('SELECT * FROM menu', get_connection())
            for _, r in df_m.iterrows():
                c1, c2, c3 = st.columns([1, 3, 1])
                if r['img']: c1.image(r['img'], width=80)
                c2.write(f"**{r['nom']}** - {int(r['prix'])} F")
                if c3.button("🗑️", key=f"m_{r['id']}"):
                    get_connection().cursor().execute('DELETE FROM menu WHERE id=?', (r['id'],)).connection.commit()
                    st.rerun()

        with tab_histo:
            df_c = pd.read_sql('SELECT * FROM commandes ORDER BY id DESC', get_connection())
            st.dataframe(df_c, use_container_width=True)


