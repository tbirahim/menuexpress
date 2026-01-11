import streamlit as st
import sqlite3
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Menu Express PRO", page_icon="🍴", layout="wide")

# --- 2. CSS LUXE ---
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
def get_db():
    conn = sqlite3.connect('menu_pro.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS menu (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prix REAL, desc TEXT, img TEXT)')
    c.execute('''CREATE TABLE IF NOT EXISTS commandes 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, articles TEXT, total REAL, 
                  type_commande TEXT, detail_logistique TEXT, statut TEXT DEFAULT 'En attente', 
                  date DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    return conn

conn = get_db()
c = conn.cursor()

# --- 4. GESTION DE LA CONNEXION (Mémoire de session) ---
if 'admin_ok' not in st.session_state:
    st.session_state.admin_ok = False

# --- 5. BARRE LATÉRALE ---
with st.sidebar:
    st.title("⚜️ Menu Express")
    
    pages = ["🍽️ Menu Client", "🛒 Mon Panier"]
    if st.session_state.admin_ok:
        pages.extend(["👩‍💼 Gérante (Admin)", "📊 Commandes Reçues"])
    
    choice = st.radio("Navigation", pages)
    
    st.divider()
    if not st.session_state.admin_ok:
        with st.expander("🔐 Espace Gérante"):
            p_admin = st.text_input("Code", type="password")
            if st.button("Se connecter"):
                if p_admin == "admin123":
                    st.session_state.admin_ok = True
                    st.rerun()
                else:
                    st.error("Mauvais code")
    else:
        if st.button("🔴 Se déconnecter"):
            st.session_state.admin_ok = False
            st.rerun()

# --- 6. PAGES ---

if choice == "🍽️ Menu Client":
    st.header("🍴 Notre Carte")
    df = pd.read_sql('SELECT * FROM menu', conn)
    if df.empty:
        st.info("Menu vide. La gérante doit ajouter des plats.")
    else:
        for _, row in df.iterrows():
            img = row['img'] if row['img'] else "https://via.placeholder.com/150"
            st.markdown(f"""
                <div class="plat-card">
                    <img src="{img}" class="plat-image">
                    <div><h3>{row['nom']}</h3><p>{row['desc']}</p></div>
                    <span class="prix">{int(row['prix'])} FCFA</span>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Ajouter au panier", key=f"add_{row['id']}"):
                if 'cart' not in st.session_state: st.session_state.cart = []
                st.session_state.cart.append({"nom": row['nom'], "prix": row['prix']})
                st.toast(f"✅ {row['nom']} ajouté !")

elif choice == "🛒 Mon Panier":
    st.header("🛍️ Votre Panier")
    if 'cart' not in st.session_state or not st.session_state.cart:
        st.write("Le panier est vide.")
    else:
        total = sum(i['prix'] for i in st.session_state.cart)
        for i in st.session_state.cart:
            st.write(f"- {i['nom']} : {int(i['prix'])} FCFA")
        
        st.divider()
        service = st.radio("Mode de service :", ["Sur place", "Livraison"])
        
        infos = ""
        if service == "Sur place":
            infos = st.text_input("Numéro de table")
        else:
            tel = st.text_input("Téléphone")
            adr = st.text_input("Adresse de livraison")
            infos = f"Tel: {tel} | Adresse: {adr}"
            
        st.subheader(f"Total : {int(total)} FCFA")
        if st.button("🚀 Confirmer la commande"):
            if not infos:
                st.error("Remplissez les informations de service !")
            else:
                c.execute('INSERT INTO commandes (articles, total, type_commande, detail_logistique) VALUES (?,?,?,?)',
                          (str(st.session_state.cart), total, service, infos))
                conn.commit()
                st.session_state.cart = []
                st.success("Commande envoyée !")
                st.balloons()

elif choice == "👩‍💼 Gérante (Admin)":
    st.header("⚙️ Ajouter un plat")
    with st.form("add_form"):
        n = st.text_input("Nom")
        p = st.number_input("Prix (FCFA)", min_value=0)
        i = st.text_input("Lien Image")
        d = st.text_area("Description")
        if st.form_submit_button("Enregistrer"):
            c.execute('INSERT INTO menu (nom, prix, desc, img) VALUES (?,?,?,?)', (n,p,d,i))
            conn.commit()
            st.success("Plat ajouté !")
            st.rerun()

elif choice == "📊 Commandes Reçues":
    st.header("📋 Historique")
    cmds = pd.read_sql('SELECT * FROM commandes ORDER BY date DESC', conn)
    for _, row in cmds.iterrows():
        with st.expander(f"Commande #{row['id']} - {row['type_commande']} - {int(row['total'])} FCFA"):
            st.write(f"**Articles:** {row['articles']}")
            st.write(f"**Service:** {row['detail_logistique']}")
            if st.button("🗑️ Supprimer", key=f"del_{row['id']}"):
                c.execute('DELETE FROM commandes WHERE id=?', (row['id'],))
                conn.commit()
                st.rerun()
