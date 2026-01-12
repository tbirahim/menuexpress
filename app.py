import streamlit as st
import sqlite3
import pandas as pd
import json
import urllib.parse
from datetime import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Menu Express PRO", page_icon="🥘", layout="wide")

# Vérification du mot de passe dans les secrets
if "PASSWORD" not in st.secrets:
    st.error("Erreur : Mot de passe non configuré.")
    st.stop()

# --- 2. STYLE CSS (DORÉ À GAUCHE / NETTETÉ À DROITE) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
* { font-family: 'Montserrat', sans-serif; }

/* Fond de l'application */
.stApp {
    background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
    url("https://images.unsplash.com/photo-1504674900247-0877df9cc836?q=80&w=2070");
    background-size: cover;
    background-attachment: fixed;
}

/* --- BARRE LATÉRALE (GAUCHE) : DORÉ SANS EFFET --- */
[data-testid="stSidebar"] * {
    color: #D4AF37 !important;
    font-weight: 700 !important;
    text-shadow: none !important;
}

/* --- CARTES DES PLATS --- */
.plat-card {
    padding: 25px;
    border-radius: 15px;
    background-color: rgba(0, 0, 0, 0.95); 
    border: 1px solid rgba(255, 255, 255, 0.2);
    margin-bottom: 15px;
    display: flex;
    align-items: center;
}

/* --- TEXTES DE DROITE : BLANC PUR SANS EFFET --- */
h1, h2, h3, p, label, span, .stMarkdown, .stExpander {
    color: #FFFFFF !important;
    text-shadow: none !important;
}

/* PRIX EN VERT */
.prix-vert {
    color: #00FF66 !important;
    font-size: 2rem;
    font-weight: bold;
    margin-left: auto;
}

/* BOUTONS BLANCS TEXTE NOIR */
.stButton>button {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    font-weight: bold;
    border-radius: 8px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# --- 3. GESTION DE LA BASE DE DONNÉES ---
def init_db():
    conn = sqlite3.connect("menu_pro.db", check_same_thread=False)
    c = conn.cursor()
    # Table Menu
    c.execute("""CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT, prix REAL, desc TEXT, img TEXT, disponible INTEGER DEFAULT 1)""")
    
    # Table Commandes avec séparation téléphone / adresse
    c.execute("""CREATE TABLE IF NOT EXISTS commandes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        articles TEXT, total REAL, type_commande TEXT, 
        telephone TEXT, adresse TEXT, table_num TEXT, date DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    
    # Sécurité : Mise à jour des colonnes si la DB existe déjà
    cursor = conn.execute('PRAGMA table_info(commandes)')
    cols = [col[1] for col in cursor.fetchall()]
    for field in ['telephone', 'adresse', 'table_num']:
        if field not in cols:
            c.execute(f'ALTER TABLE commandes ADD COLUMN {field} TEXT')
    
    conn.commit()
    return conn

conn = init_db()
c = conn.cursor()

# --- 4. NAVIGATION ---
if "admin_ok" not in st.session_state: st.session_state.admin_ok = False
if "cart" not in st.session_state: st.session_state.cart = []

with st.sidebar:
    st.markdown("# ⚜️ Menu Express")
    choice = st.radio("Aller vers :", ["🍽️ Commander", "📊 Espace Gérant"] if st.session_state.admin_ok else ["🍽️ Commander"])
    
    if not st.session_state.admin_ok:
        with st.expander("🔐 Accès Gérant"):
            pwd = st.text_input("Code Secret", type="password")
            if st.button("Connexion"):
                if pwd == st.secrets["PASSWORD"]:
                    st.session_state.admin_ok = True
                    st.rerun()
    else:
        if st.button("🔴 Quitter le mode Gérant"):
            st.session_state.admin_ok = False
            st.rerun()

# --- 5. INTERFACE CLIENT (COMMANDER) ---
if choice == "🍽️ Commander":
    st.markdown("<h1 style='text-align: center;'>🥘 Notre Carte</h1>", unsafe_allow_html=True)
    
    plats = pd.read_sql("SELECT * FROM menu WHERE disponible=1", conn)
    
    for _, row in plats.iterrows():
        st.markdown(f"""
        <div class="plat-card">
            <img src="{row['img'] or 'https://via.placeholder.com/150'}" style="width:110px;height:110px;border-radius:10px;margin-right:20px;object-fit:cover;">
            <div class="plat-info">
                <h2>{row['nom']}</h2>
                <p>{row['desc']}</p>
            </div>
            <div class="prix-vert">{int(row['prix'])} F</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 4])
        qte = col1.number_input("Qté", 1, 10, 1, key=f"q_{row['id']}")
        if col2.button(f"Ajouter {row['nom']}", key=f"btn_{row['id']}", use_container_width=True):
            st.session_state.cart.append({"nom": row["nom"], "prix": row["prix"], "qte": qte})
            st.toast(f"✅ {row['nom']} ajouté !")

    # --- PANIER ET FINALISATION ---
    if st.session_state.cart:
        st.markdown("<br><hr>", unsafe_allow_html=True)
        st.markdown("## 🛒 Votre Panier")
        total_cmd = sum(item['prix'] * item['qte'] for item in st.session_state.cart)
        
        for item in st.session_state.cart:
            st.write(f"• {item['nom']} (x{item['qte']}) : {int(item['prix']*item['qte'])} F")
        
        st.markdown(f"### TOTAL : {int(total_cmd)} FCFA")
        
        mode = st.radio("Mode de réception", ["Sur place", "Livraison"], horizontal=True)
        
        t_num, tel, adr = "", "", ""
        if mode == "Sur place":
            t_num = st.text_input("Numéro de Table / Nom")
        else:
            c1, c2 = st.columns(2)
            tel = c1.text_input("📞 Numéro de Téléphone")
            adr = c2.text_input("📍 Adresse de Livraison")

        if st.button("🚀 VALIDER LA COMMANDE", use_container_width=True):
            if (mode == "Sur place" and not t_num) or (mode == "Livraison" and (not tel or not adr)):
                st.warning("Veuillez remplir les informations de contact.")
            else:
                c.execute("INSERT INTO commandes (articles, total, type_commande, telephone, adresse, table_num) VALUES (?,?,?,?,?,?)",
                          (json.dumps(st.session_state.cart, ensure_ascii=False), total_cmd, mode, tel, adr, t_num))
                conn.commit()
                st.success("Commande envoyée au gérant !")
                st.session_state.cart = []

# --- 6. ESPACE GÉRANT (BASE DE DONNÉES) ---
elif choice == "📊 Espace Gérant":
    st.markdown("<h1>📊 Administration</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📋 Commandes", "🥘 Gérer la Carte"])

    with tab1:
        # Affichage des commandes depuis la base
        commandes_df = pd.read_sql("SELECT * FROM commandes ORDER BY date DESC", conn)
        for _, r in commandes_df.iterrows():
            with st.expander(f"📦 Commande #{r['id']} - {r['type_commande']}"):
                st.write(f"**Client :** {r['table_num'] if r['table_num'] else r['telephone']}")
                if r['adresse']: st.write(f"**Lieu :** {r['adresse']}")
                st.write("**Articles :**")
                st.table(pd.DataFrame(json.loads(r['articles'])))
                if st.button("✔️ Terminer la commande", key=f"fin_{r['id']}"):
                    c.execute("DELETE FROM commandes WHERE id=?", (r['id'],))
                    conn.commit()
                    st.rerun()

    with tab2:
        st.subheader("Ajouter un nouveau plat")
        with st.form("ajout_plat"):
            n = st.text_input("Nom du plat")
            p = st.number_input("Prix (F)", 0)
            d = st.text_area("Description")
            i = st.text_input("URL Image")
            if st.form_submit_button("Ajouter"):
                c.execute("INSERT INTO menu (nom, prix, desc, img) VALUES (?,?,?,?)", (n, p, d, i))
                conn.commit()
                st.rerun()
