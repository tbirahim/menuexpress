import streamlit as st
import sqlite3
import pandas as pd
import urllib.parse
import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Menu Express", 
    page_icon="🥘", 
    layout="wide", 
    initial_sidebar_state="collapsed" # C'est ça qui crée les "3 traits" fermés par défaut
)

# 🔴 TES INFOS
NUMERO_WHATSAPP = "221778615900"
NUMERO_APPEL = "778615900"

# GESTION MOT DE PASSE (Sécurité)
try:
    ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]
except:
    ADMIN_PASSWORD = "admin123"

# --- 2. STYLE CSS (SPECIAL MENU LATERAL) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@300;400;700&display=swap');
    
    .stApp { background-color: #0c0c0c; color: #f0f0f0; font-family: 'Lato', sans-serif; }
    h1, h2, h3 { font-family: 'Playfair Display', serif; color: #d4af37; text-align: center; }

    /* Style de la Sidebar (Menu 3 traits) */
    [data-testid="stSidebar"] {
        background-color: #1a1a1a;
        border-right: 1px solid #d4af37;
    }
    .css-1d391kg { padding-top: 3rem; }
    
    /* Cartes Plats */
    .plat-card {
        background:#1a1a1a; padding:0; border-radius:15px; overflow:hidden;
        margin-bottom:20px; border: 1px solid #333;
    }
    .plat-img { width: 100%; height: 200px; object-fit: cover; }
    .plat-body { padding: 15px; }
    
    /* Boutons */
    .btn-whatsapp { display: block; width: 100%; background-color: #25D366; color: white !important; text-align: center; padding: 15px; border-radius: 12px; font-weight: bold; text-decoration: none; margin-top: 10px; }
    .btn-call { display: block; width: 100%; background-color: transparent; color: #d4af37 !important; text-align: center; padding: 10px; border-radius: 12px; font-weight: bold; text-decoration: none; border: 2px solid #d4af37; margin-top: 20px; }

    /* Bannière Haut de page */
    .top-banner { width: 100%; height: 180px; object-fit: cover; border-radius: 0 0 20px 20px; margin-bottom: 20px; opacity: 0.8; }
    
    .block-container { padding-top: 0px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DONNÉES ---
def get_connection():
    return sqlite3.connect('expres_resto.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    # Ajout colonne img si absente
    try:
        c.execute('ALTER TABLE menu ADD COLUMN img TEXT')
    except:
        pass
    c.execute('CREATE TABLE IF NOT EXISTS menu (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prix REAL, desc TEXT, img TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS commandes (id INTEGER PRIMARY KEY AUTOINCREMENT, articles TEXT, total REAL, type_commande TEXT, detail_logistique TEXT, statut TEXT DEFAULT "En attente", date DATETIME DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()

init_db()

# --- 4. FONCTIONS PANIER ---
def add_to_cart(item):
    if 'cart' not in st.session_state: st.session_state.cart = []
    for p in st.session_state.cart:
        if p['id'] == item['id']:
            p['qty'] += 1
            st.toast(f"➕ {item['nom']} (x{p['qty']})"); return
    new_item = item.copy(); new_item['qty'] = 1
    st.session_state.cart.append(new_item); st.toast(f"✅ {item['nom']} ajouté")

def remove_from_cart(index):
    if st.session_state.cart[index]['qty'] > 1: st.session_state.cart[index]['qty'] -= 1
    else: st.session_state.cart.pop(index)
    st.rerun()

# --- 5. NAVIGATION (MENU LATÉRAL) ---
if 'cart' not in st.session_state: st.session_state.cart = []

# Calcul du nombre d'articles pour l'affichage
nb_items = sum(item['qty'] for item in st.session_state.cart)
label_panier = f"🛒 Mon Panier ({nb_items})" if nb_items > 0 else "🛒 Mon Panier"

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1046/1046771.png", width=100) # Logo fictif
    st.write("### MENU")
    page = st.radio(
        "", 
        ["🏠 Accueil", "🍴 La Carte", "📅 Réserver", label_panier, "🔐 Admin"],
        label_visibility="collapsed"
    )
    st.write("---")
    st.write("📞 **Service Client**")
    st.write(f"{NUMERO_APPEL}")

# --- PAGE 1: ACCUEIL ---
if "Accueil" in page:
    st.image("https://www.luxe-infinity-afrique.com/wp-content/uploads/2025/08/La-Cuisine-Africaine-Conquiert-la-France-1200x675.webp", class_label="top-banner")
    st.markdown("<h1 style='margin-top:-10px;'>TERANGA GOURMET</h1>", unsafe_allow_html=True)
    st.write("### L'Authenticité du Sénégal")
    
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <p style="color: #ccc;">Bienvenue chez vous. Savourez nos plats traditionnels préparés avec amour et passion.</p>
        <br>
        <p style="color: #d4af37; font-weight: bold; border: 1px solid #d4af37; padding: 10px; border-radius: 10px; display: inline-block;">
            📍 Mboro<br>⏰ 12h00 - 23h00
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- PAGE 2: LA CARTE (AVEC PHOTOS) ---
elif "Carte" in page:
    st.image("https://images.unsplash.com/photo-1555939594-58d7cb561ad1?q=80&w=1974", class_label="top-banner")
    st.header("Notre Menu")
    
    df_menu = pd.read_sql('SELECT * FROM menu', get_connection())
    if df_menu.empty:
        st.info("Menu en cours de création.")
    else:
        for index, row in df_menu.iterrows():
            # Image par défaut si vide
            img_url = row['img'] if row['img'] and str(row['img']).startswith('http') else "https://via.placeholder.com/400x200?text=Plat+Senegalais"
            
            st.markdown(f'''
                <div class="plat-card">
                    <img src="{img_url}" class="plat-img">
                    <div class="plat-body">
                        <span style="font-size:1.3rem; font-weight:bold; color: white;">{row["nom"]}</span>
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px;">
                            <span style="color:#d4af37; font-size:1.2rem; font-weight:bold;">{int(row["prix"])} FCFA</span>
                        </div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
            
            # Bouton séparé pour la logique Python
            item_dict = {"id": row['id'], "nom": row['nom'], "prix": row['prix']}
            st.button(f"AJOUTER AU PANIER", key=f"add_{row['id']}", on_click=add_to_cart, args=(item_dict,), use_container_width=True)
            st.write("---")

# --- PAGE 3: RÉSERVATION ---
elif "Réserver" in page:
    st.image("https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=2070", class_label="top-banner")
    st.header("Réserver une Table")
    
    with st.form("res_form"):
        nom = st.text_input("Votre Nom")
        col1, col2 = st.columns(2)
        d = col1.date_input("Date")
        h = col2.time_input("Heure")
        p = st.slider("Nombre de personnes", 1, 15, 2)
        
        if st.form_submit_button("VALIDER LA DEMANDE", use_container_width=True):
            msg = f"📝 *RÉSERVATION*\n👤 {nom}\n📅 {d}\n⏰ {h}\n👥 {p} pers"
            link = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg)}"
            st.markdown(f'<a href="{link}" target="_blank" class="btn-whatsapp">✅ CONFIRMER SUR WHATSAPP</a>', unsafe_allow_html=True)

# --- PAGE 4: PANIER ---
elif "Panier" in page:
    st.image("https://images.unsplash.com/photo-1504674900247-0877df9cc836?q=80&w=2070", class_label="top-banner")
    st.header("Votre Panier")
    
    if st.session_state.cart:
        total = 0
        txt_items = ""
        for i, item in enumerate(st.session_state.cart):
            subtotal = item['prix'] * item['qty']
            total += subtotal
            txt_items += f"- {item['nom']} (x{item['qty']})\n"
            
            c1, c2, c3, c4 = st.columns([3, 1, 2, 1])
            c1.write(f"**{item['nom']}**")
            c2.write(f"x{item['qty']}")
            c3.write(f"{int(subtotal)} F")
            if c4.button("➖", key=f"rem_{i}"): remove_from_cart(i)
        
        st.divider()
        st.markdown(f"<h2 style='text-align:right; color:#d4af37;'>Total: {int(total)} FCFA</h2>", unsafe_allow_html=True)
        
        mode = st.radio("Mode de réception", ["Sur place", "Livraison"])
        log, ok = "", False
        
        if mode == "Sur place":
            t = st.text_input("Numéro de table")
            if t: log = f"Table {t}"; ok = True
        else:
            tel = st.text_input("Téléphone")
            adr = st.text_input("Adresse de livraison")
            if tel and adr: log = f"Tél: {tel} | Adr: {adr}"; ok = True
            
        if st.button("🚀 VALIDER LA COMMANDE", use_container_width=True):
            if not ok: st.error("Veuillez remplir les informations manquantes.")
            else:
                conn = get_connection()
                conn.cursor().execute('INSERT INTO commandes (articles, total, type_commande, detail_logistique) VALUES (?,?,?,?)', (txt_items, total, mode, log))
                conn.commit()
                msg = f"🥘 *COMMANDE*\n{txt_items}\n💰 *TOTAL:* {int(total)} F\n📍 {mode}\n📝 {log}"
                link = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg)}"
                st.markdown(f'<a href="{link}" target="_blank" class="btn-whatsapp">✅ ENVOYER SUR WHATSAPP</a>', unsafe_allow_html=True)
    else:
        st.info("Votre panier est vide pour le moment.")
    
    st.markdown(f'<a href="tel:{NUMERO_APPEL}" class="btn-call">📞 APPELER LE RESTAURANT</a>', unsafe_allow_html=True)

# --- PAGE 5: ADMIN (AJOUT PHOTOS) ---
elif "Admin" in page:
    st.header("Administration")
    
    pwd = st.text_input("Code Admin", type="password")
    if pwd == ADMIN_PASSWORD:
        st.success("Mode Gérant Activé")
        
        tab1, tab2 = st.tabs(["➕ Ajouter Plat", "📋 Historique"])
        
        with tab1:
            st.write("### Ajouter un nouveau plat")
            with st.form("add_dish", clear_on_submit=True):
                n = st.text_input("Nom du plat (ex: Thieboudienne)")
                p = st.number_input("Prix", step=500)
                # Champ pour l'image
                img = st.text_input("Lien de l'image (URL Internet)", placeholder="https://...")
                st.caption("Astuce : Copiez le lien d'une image sur Google Images ou Unsplash.")
                
                if st.form_submit_button("Enregistrer le plat"):
                    conn = get_connection()
                    conn.cursor().execute('INSERT INTO menu (nom, prix, img) VALUES (?,?,?)', (n, p, img))
                    conn.commit()
                    st.success("Plat ajouté avec succès !")
                    st.rerun()
            
            st.write("---")
            st.write("### Menu Actuel")
            df_m = pd.read_sql('SELECT * FROM menu', get_connection())
            for _, r in df_m.iterrows():
                c1, c2, c3 = st.columns([1, 3, 1])
                # Affiche petite image si dispo
                if r['img']: c1.image(r['img'], use_container_width=True)
                c2.write(f"**{r['nom']}** - {int(r['prix'])} F")
                if c3.button("🗑️", key=f"del_{r['id']}"):
                    conn = get_connection()
                    conn.cursor().execute('DELETE FROM menu WHERE id=?', (r['id'],))
                    conn.commit()
                    st.rerun()

        with tab2:
            if st.button("Actualiser la liste"): st.rerun()
            df_c = pd.read_sql('SELECT * FROM commandes ORDER BY id DESC', get_connection())
            st.dataframe(df_c)
