import streamlit as st
import sqlite3
import pandas as pd
from fpdf import FPDF

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Menu Express PRO", page_icon="🍴", layout="wide")

# --- 2. DESIGN LUXE & IMAGE DE SECOND PLAN (CSS) ---
st.markdown("""
    <style>
    /* Image de fond et overlay sombre */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
        color: #ffffff;
    }
    .stApp::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.75); z-index: -1;
    }

    /* Barre latérale */
    [data-testid="stSidebar"] { background-color: #111111; border-right: 1px solid #d4af37; }
    
    /* Cartes des plats */
    .plat-card {
        padding: 20px; border-radius: 15px; background-color: rgba(38, 38, 38, 0.9);
        box-shadow: 0 4px 20px rgba(0,0,0,0.5); border: 1px solid #d4af37;
        margin-bottom: 20px; display: flex; align-items: center;
    }
    
    .plat-image {
        width: 120px; height: 120px; border-radius: 10px;
        object-fit: cover; margin-right: 20px; border: 1px solid #d4af37;
    }

    h1, h2, h3 { color: #d4af37 !important; }
    .prix { color: #d4af37; font-weight: bold; font-size: 1.8rem; margin-left: auto; }
    
    /* Barre de recherche stylisée */
    .stTextInput > div > div > input {
        border: 2px solid #d4af37 !important;
        border-radius: 25px !important;
        background-color: #333333 !important;
        color: white !important;
        padding: 10px 20px !important;
    }

    .stButton>button {
        background-color: #d4af37 !important; color: #1a1a1a !important;
        font-weight: bold; border-radius: 25px; border: none; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DONNÉES ---
conn = sqlite3.connect('menu_pro.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS menu (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prix REAL, desc TEXT, img TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS commandes (id INTEGER PRIMARY KEY AUTOINCREMENT, articles TEXT, total REAL, statut TEXT, date DATETIME DEFAULT CURRENT_TIMESTAMP)')
conn.commit()

# --- 4. NAVIGATION & SÉCURITÉ ---
if 'admin_mode' not in st.session_state: st.session_state.admin_mode = False

with st.sidebar:
    st.title("⚜️ Menu Express")
    pages = ["🍽️ Menu Client", "🛒 Mon Panier"]
    if st.session_state.admin_mode: pages.extend(["👩‍💼 Gérante (Admin)", "📊 Historique"])
    page = st.radio("Navigation", pages)
    
    st.divider()
    with st.expander("🔐 Accès Gérante"):
        pwd = st.text_input("Code secret", type="password")
        if pwd == "admin123":
            st.session_state.admin_mode = True
            st.success("Accès Gérante Activé")
        else: st.session_state.admin_mode = False

# --- 5. LOGIQUE DES PAGES ---

if page == "🍽️ Menu Client":
    st.header("🍴 Menu Express")
    
    # Barre de recherche personnalisée
    search_term = st.text_input("", placeholder="🔍 Quel délice recherchez-vous ? (ex: Burger, Pizza...)", label_visibility="collapsed")
    
    items = pd.read_sql('SELECT * FROM menu', conn)
    if search_term:
        items = items[items['nom'].str.contains(search_term, case=False) | items['desc'].str.contains(search_term, case=False)]

    if items.empty:
        st.info("Aucun plat trouvé. Revenez plus tard !")
    else:
        for _, row in items.iterrows():
            st.markdown(f"""
                <div class="plat-card">
                    <img src="{row['img'] if row['img'] else 'https://via.placeholder.com/150'}" class="plat-image">
                    <div>
                        <h3>{row['nom']}</h3>
                        <p>{row['desc']}</p>
                    </div>
                    <span class="prix">{row['prix']} €</span>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Ajouter au panier", key=row['id']):
                if 'cart' not in st.session_state: st.session_state.cart = []
                st.session_state.cart.append({"nom": row['nom'], "prix": row['prix']})
                st.toast(f"✅ {row['nom']} ajouté !")

elif page == "🛒 Mon Panier":
    st.header("🛍️ Votre Panier")
    if 'cart' not in st.session_state or not st.session_state.cart:
        st.write("Votre panier est vide.")
    else:
        total = sum(item['prix'] for item in st.session_state.cart)
        for i, item in enumerate(st.session_state.cart):
            st.write(f"• **{item['nom']}** - {item['prix']} €")
        st.divider()
        st.subheader(f"Total à payer : {total} €")
        if st.button("Confirmer la commande", type="primary"):
            c.execute('INSERT INTO commandes (articles, total, statut) VALUES (?,?,?)', (str(st.session_state.cart), total, "En attente"))
            conn.commit()
            st.balloons()
            st.success("Commande envoyée en cuisine !")
            st.session_state.cart = []

elif page == "👩‍💼 Gérante (Admin)" and st.session_state.admin_mode:
    st.header("Gestion de la Carte")
    with st.form("ajout_plat"):
        col1, col2 = st.columns(2)
        n = col1.text_input("Nom du plat")
        p = col1.number_input("Prix (€)", min_value=0.0)
        i = col2.text_input("Lien de la photo (URL)")
        d = col2.text_area("Description")
        if st.form_submit_button("Ajouter à la carte"):
            c.execute('INSERT INTO menu (nom, prix, desc, img) VALUES (?,?,?,?)', (n,p,d,i))
            conn.commit()
            st.success("Plat ajouté !")
            st.rerun()
    st.divider()
    st.subheader("Plats actuels")
    st.dataframe(pd.read_sql('SELECT * FROM menu', conn), use_container_width=True)

elif page == "📊 Historique" and st.session_state.admin_mode:
    st.header("Commandes Reçues")
    cmds = pd.read_sql('SELECT * FROM commandes ORDER BY date DESC', conn)
    for _, cmd in cmds.iterrows():
        with st.expander(f"Commande #{cmd['id']} - {cmd['total']} € - {cmd['date']}"):
            st.write(f"Détail : {cmd['articles']}")