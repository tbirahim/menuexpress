# menuexpressimport streamlit as st
import sqlite3
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Menu Express PRO", page_icon="🍴", layout="wide")

# --- 2. CSS LUXE & DESIGN ---
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?q=80&w=2070&auto=format&fit=crop");
        background-size: cover; background-attachment: fixed; color: #ffffff;
    }
    .stApp::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.75); z-index: -1;
    }
    .plat-card {
        padding: 20px; border-radius: 15px; background-color: rgba(38, 38, 38, 0.9);
        border: 1px solid #d4af37; margin-bottom: 20px; display: flex; align-items: center;
    }
    .plat-image {
        width: 120px; height: 120px; border-radius: 10px;
        object-fit: cover; margin-right: 20px; border: 1px solid #d4af37;
    }
    h1, h2, h3 { color: #d4af37 !important; }
    .prix { color: #d4af37; font-weight: bold; font-size: 1.5rem; margin-left: auto; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DONNÉES (Initialisation Propre) ---
def init_db():
    conn = sqlite3.connect('menu_pro.db', check_same_thread=False)
    c = conn.cursor()
    # Table Menu
    c.execute('CREATE TABLE IF NOT EXISTS menu (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prix REAL, desc TEXT, img TEXT)')
    # Table Commandes avec toutes les colonnes nécessaires
    c.execute('''CREATE TABLE IF NOT EXISTS commandes 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, articles TEXT, total REAL, 
                  type_commande TEXT, detail_logistique TEXT, statut TEXT DEFAULT 'En attente', 
                  date DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    return conn

conn = init_db()
c = conn.cursor()

# --- 4. GESTION DE LA SESSION ADMIN (Une seule connexion) ---
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

# --- 5. NAVIGATION ---
with st.sidebar:
    st.title("⚜️ Menu Express")
    
    # Choix des pages selon le statut de connexion
    options = ["🍽️ Menu Client", "🛒 Mon Panier"]
    if st.session_state.admin_logged_in:
        options.extend(["👩‍💼 Gérante (Admin)", "📊 Commandes Reçues"])
    
    page = st.radio("Aller vers :", options)
    
    st.divider()
    
    # Zone de connexion (apparaît seulement si non connecté)
    if not st.session_state.admin_logged_in:
        with st.expander("🔐 Accès Gérante"):
            password_input = st.text_input("Code secret", type="password")
            if st.button("Valider le code"):
                if password_input == "admin123":
                    st.session_state.admin_logged_in = True
                    st.success("Connecté !")
                    st.rerun()
                else:
                    st.error("Code incorrect")
    else:
        st.info("✅ Mode Gérante Actif")
        if st.button("Se déconnecter"):
            st.session_state.admin_logged_in = False
            st.rerun()

# --- 6. LOGIQUE DES PAGES ---

if page == "🍽️ Menu Client":
    st.header("🍴 Notre Carte")
    items = pd.read_sql('SELECT * FROM menu', conn)
    
    if items.empty:
        st.info("Le menu est en préparation. Revenez bientôt !")
    else:
        for _, row in items.iterrows():
            img_url = row['img'] if row['img'] and row['img'].startswith('http') else "https://via.placeholder.com/150"
            st.markdown(f"""
                <div class="plat-card">
                    <img src="{img_url}" class="plat-image">
                    <div><h3>{row['nom']}</h3><p>{row['desc']}</p></div>
                    <span class="prix">{int(row['prix'])} FCFA</span>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Ajouter {row['nom']}", key=f"add_{row['id']}"):
                if 'cart' not in st.session_state: st.session_state.cart = []
                st.session_state.cart.append({"nom": row['nom'], "prix": row['prix']})
                st.toast(f"✅ {row['nom']} ajouté au panier")

elif page == "🛒 Mon Panier":
    st.header("🛍️ Votre Panier")
    if 'cart' not in st.session_state or not st.session_state.cart:
        st.write("Votre panier est vide.")
    else:
        total = sum(item['prix'] for item in st.session_state.cart)
        for item in st.session_state.cart:
            st.write(f"• **{item['nom']}** : {int(item['prix'])} FCFA")
        
        st.divider()
        st.subheader("Informations de service")
        type_com = st.selectbox("Comment souhaitez-vous être servi ?", ["Sur place", "Livraison"])
        
        info_client = ""
        if type_com == "Sur place":
            info_client = st.text_input("Numéro de table (obligatoire)")
        else:
            col_tel, col_adr = st.columns(2)
            tel = col_tel.text_input("Téléphone")
            adr = col_adr.text_input("Adresse de livraison")
            info_client = f"Tél: {tel} | Adresse: {adr}"
            
        st.subheader(f"Total à payer : {int(total)} FCFA")
        
        if st.button("🚀 Valider la commande"):
            if info_client.strip() == "" or (type_com == "Livraison" and (tel == "" or adr == "")):
                st.error("Veuillez remplir les informations (Table ou Coordonnées) !")
            else:
                c.execute('INSERT INTO commandes (articles, total, type_commande, detail_logistique, statut) VALUES (?,?,?,?,?)', 
                          (str(st.session_state.cart), total, type_com, info_client, 'En attente'))
                conn.commit()
                st.session_state.cart = []
                st.success("C'est envoyé ! Votre commande est en préparation.")
                st.balloons()

elif page == "👩‍💼 Gérante (Admin)":
    st.header("⚙️ Gestion de la Carte")
    with st.form("nouveau_plat"):
        c1, c2 = st.columns(2)
        n = c1.text_input("Nom du plat")
        p = c1.number_input("Prix (FCFA)", min_value=0)
        i = c2.text_input("Lien de l'image (URL)")
        d = c2.text_area("Description")
        if st.form_submit_button("Ajouter à la carte"):
            c.execute('INSERT INTO menu (nom, prix, desc, img) VALUES (?,?,?,?)', (n,p,d,i))
            conn.commit()
            st.success("Plat ajouté avec succès !")
            st.rerun()
            
    st.divider()
    st.subheader("Plats actuels")
    menu_df = pd.read_sql('SELECT id, nom, prix FROM menu', conn)
    for _, row in menu_df.iterrows():
        col_n, col_d = st.columns([5, 1])
        col_n.write(f"**{row['nom']}** - {int(row['prix'])} FCFA")
        if col_d.button("🗑️", key=f"del_p_{row['id']}"):
            c.execute('DELETE FROM menu WHERE id=?', (row['id'],))
            conn.commit()
            st.rerun()

elif page == "📊 Commandes Reçues":
    st.header("📋 Suivi des Commandes")
    
    if st.button("🧹 Effacer les commandes terminées"):
        c.execute("DELETE FROM commandes WHERE statut='Terminé'")
        conn.commit()
        st.rerun()

    cmds = pd.read_sql('SELECT * FROM commandes ORDER BY date DESC', conn)
    for _, row in cmds.iterrows():
        status_label = "🟠" if row['statut'] == "En attente" else "🟢"
        with st.expander(f"{status_label} Commande #{row['id']} - {row['type_commande']} - {int(row['total'])} FCFA"):
            st.write(f"**Articles :** {row['articles']}")
            st.write(f"**Logistique :** {row['detail_logistique']}")
            st.write(f"**Heure :** {row['date']}")
            
            c1, c2, c3 = st.columns(3)
            if c1.button("⏳ Attente", key=f"st_w_{row['id']}"):
                c.execute("UPDATE commandes SET statut='En attente' WHERE id=?", (row['id'],))
                conn.commit()
                st.rerun()
            if c2.button("✅ Terminer", key=f"st_d_{row['id']}"):
                c.execute("UPDATE commandes SET statut='Terminé' WHERE id=?", (row['id'],))
                conn.commit()
                st.rerun()
            if c3.button("❌ Supprimer", key=f"st_x_{row['id']}"):
                c.execute("DELETE FROM commandes WHERE id=?", (row['id'],))
                conn.commit()
                st.rerun()
