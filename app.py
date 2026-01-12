import streamlit as st
import sqlite3
import pandas as pd
import time

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Menu Express PRO", page_icon="🍴", layout="wide")

# Rafraîchissement automatique toutes les 60 secondes pour la gérante
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

# --- 2. DESIGN ---
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?q=80&w=2070&auto=format&fit=crop");
        background-size: cover; background-attachment: fixed; color: #ffffff;
    }
    .stApp::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.8); z-index: -1;
    }
    .plat-card {
        padding: 20px; border-radius: 15px; background-color: rgba(30, 30, 30, 0.9);
        border: 1px solid #d4af37; margin-bottom: 20px; display: flex; align-items: center;
    }
    .plat-image {
        width: 110px; height: 110px; border-radius: 10px;
        object-fit: cover; margin-right: 20px; border: 1px solid #d4af37;
    }
    h1, h2, h3 { color: #d4af37 !important; }
    .prix { color: #d4af37; font-weight: bold; font-size: 1.4rem; margin-left: auto; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DONNÉES ---
def init_db():
    conn = sqlite3.connect('menu_pro.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS menu (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prix REAL, desc TEXT, img TEXT)')
    c.execute('''CREATE TABLE IF NOT EXISTS commandes 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, articles TEXT, total REAL, 
                  type_commande TEXT, detail_logistique TEXT, statut TEXT DEFAULT 'En attente', 
                  date DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    return conn

conn = init_db()
c = conn.cursor()

# --- 4. SESSION STATE ---
if 'admin_ok' not in st.session_state: st.session_state.admin_ok = False
if 'cart' not in st.session_state: st.session_state.cart = []
if 'commande_validee' not in st.session_state: st.session_state.commande_validee = False

# --- 5. BARRE LATÉRALE ---
with st.sidebar:
    st.title("⚜️ Menu Express")
    pages = ["🍽️ Menu Client", "🛒 Mon Panier"]
    if st.session_state.admin_ok:
        pages.extend(["👩‍💼 Gérante (Admin)", "📊 Commandes Reçues"])
    
    choice = st.radio("Navigation", pages)
    
    if st.session_state.admin_ok:
        st.write("---")
        if st.button("🔴 Déconnexion"):
            st.session_state.admin_ok = False
            st.rerun()
    else:
        with st.expander("🔐 Admin"):
            pwd = st.text_input("Code", type="password")
            if st.button("OK"):
                if pwd == "admin123":
                    st.session_state.admin_ok = True
                    st.rerun()

# --- 6. PAGES ---

if choice == "🍽️ Menu Client":
    st.header("🍴 Notre Carte")
    df = pd.read_sql('SELECT * FROM menu', conn)
    if df.empty:
        st.info("Menu vide.")
    else:
        for _, row in df.iterrows():
            img = row['img'] if row['img'] else "https://via.placeholder.com/150"
            st.markdown(f'<div class="plat-card"><img src="{img}" class="plat-image"><div><h3>{row["nom"]}</h3><p>{row["desc"]}</p></div><span class="prix">{int(row["prix"])} FCFA</span></div>', unsafe_allow_html=True)
            if st.button(f"Ajouter", key=f"btn_{row['id']}"):
                st.session_state.cart.append({"nom": row['nom'], "prix": row['prix']})
                st.toast("Ajouté !")

elif choice == "🛒 Mon Panier":
    st.header("🛍️ Votre Panier")
    if not st.session_state.cart:
        if st.session_state.commande_validee:
            st.success("✅ Commande envoyée !")
            if st.button("Faire une autre commande"):
                st.session_state.commande_validee = False
                st.rerun()
        else:
            st.write("Le panier est vide.")
    else:
        total = sum(i['prix'] for i in st.session_state.cart)
        txt_items = ""
        for i in st.session_state.cart:
            st.write(f"- {i['nom']} : {int(i['prix'])} FCFA")
            txt_items += f"%0A- {i['nom']}"
        
        service = st.radio("Service", ["Sur place", "Livraison"])
        infos = st.text_input("Numéro de table" if service == "Sur place" else "Adresse et Téléphone")
        
        if st.button("🚀 CONFIRMER ET PRÉVENIR PAR WHATSAPP"):
            if not infos:
                st.error("Remplissez les infos !")
            else:
                # 1. Enregistre
                c.execute('INSERT INTO commandes (articles, total, type_commande, detail_logistique) VALUES (?,?,?,?)',
                          (str(st.session_state.cart), total, service, infos))
                conn.commit()
                
                # 2. Prépare WhatsApp
                num_gerante = "221XXXXXXXXX" # <--- METS TON NUMÉRO ICI
                msg = f"Nouvelle Commande!{txt_items}%0A%0A*Total:* {int(total)} FCFA%0A*Mode:* {service}%0A*Infos:* {infos}"
                link = f"https://wa.me/{num_gerante}?text={msg}"
                
                # 3. Vide le panier (Sécurité)
                st.session_state.cart = []
                st.session_state.commande_validee = True
                
                # 4. Ouvre WhatsApp et refresh
                st.markdown(f'<meta http-equiv="refresh" content="0; url={link}">', unsafe_allow_html=True)
                st.rerun()

elif choice == "👩‍💼 Gérante (Admin)":
    st.header("⚙️ Gestion")
    with st.form("add"):
        n, p, i, d = st.text_input("Nom"), st.number_input("Prix", 0), st.text_input("Image URL"), st.text_area("Description")
        if st.form_submit_button("Ajouter"):
            c.execute('INSERT INTO menu (nom, prix, desc, img) VALUES (?,?,?,?)', (n,p,d,i))
            conn.commit()
            st.rerun()
    
    st.write("---")
    items = pd.read_sql('SELECT * FROM menu', conn)
    for _, row in items.iterrows():
        col1, col2 = st.columns([4, 1])
        col1.write(f"{row['nom']} - {int(row['prix'])} FCFA")
        if col2.button("Supprimer", key=f"del_{row['id']}"):
            c.execute('DELETE FROM menu WHERE id=?', (row['id'],))
            conn.commit()
            st.rerun()

elif choice == "📊 Commandes Reçues":
    st.header("📋 Commandes")
    # Auto-refresh toutes les 30 secondes pour cette page
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=30000, key="datarefresh")
    
    cmds = pd.read_sql('SELECT * FROM commandes ORDER BY date DESC', conn)
    for _, row in cmds.iterrows():
        with st.expander(f"Commande #{row['id']} - {row['type_commande']} - {int(row['total'])} FCFA"):
            st.error(f"📍 INFOS : {row['detail_logistique']}")
            st.write(f"Détails : {row['articles']}")
            if st.button("Terminer", key=f"fin_{row['id']}"):
                c.execute('DELETE FROM commandes WHERE id=?', (row['id'],))
                conn.commit()
                st.rerun()
