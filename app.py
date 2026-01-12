import streamlit as st
import sqlite3
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Menu Express PRO", page_icon="🍴", layout="wide")

# --- 2. DESIGN & STYLE ---
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

# --- 4. SESSION STATE (Connexion unique) ---
if 'admin_ok' not in st.session_state:
    st.session_state.admin_ok = False
if 'commande_validee' not in st.session_state:
    st.session_state.commande_validee = False

# --- 5. BARRE LATÉRALE ---
with st.sidebar:
    st.title("⚜️ Menu Express")
    pages = ["🍽️ Menu Client", "🛒 Mon Panier"]
    if st.session_state.admin_ok:
        pages.extend(["👩‍💼 Gérante (Admin)", "📊 Commandes Reçues"])
    
    choice = st.radio("Navigation", pages)
    
    st.divider()
    if not st.session_state.admin_ok:
        with st.expander("🔐 Accès Gérante"):
            p_admin = st.text_input("Code secret", type="password")
            if st.button("Connexion"):
                if p_admin == "admin123":
                    st.session_state.admin_ok = True
                    st.rerun()
                else:
                    st.error("Code incorrect")
    else:
        if st.button("🔴 Se déconnecter"):
            st.session_state.admin_ok = False
            st.rerun()

# --- 6. LOGIQUE DES PAGES ---

if choice == "🍽️ Menu Client":
    st.header("🍴 Notre Carte")
    df = pd.read_sql('SELECT * FROM menu', conn)
    if df.empty:
        st.info("Le menu est vide. La gérante doit ajouter des plats.")
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
        txt_wa = ""
        for i in st.session_state.cart:
            st.write(f"- {i['nom']} : {int(i['prix'])} FCFA")
            txt_wa += f"%0A- {i['nom']}"
        
        st.divider()
        service = st.radio("Comment voulez-vous manger ?", ["Sur place", "Livraison"])
        infos = ""
        if service == "Sur place":
            infos = st.text_input("Numéro de table")
        else:
            tel = st.text_input("Téléphone")
            adr = st.text_input("Adresse de livraison")
            infos = f"Tel: {tel} | Adresse: {adr}"
            
        st.subheader(f"Total : {int(total)} FCFA")
        
        if st.button("🚀 1. Valider la commande"):
            if not infos:
                st.error("Veuillez remplir les infos de table ou livraison.")
            elif not st.session_state.cart:
                st.warning("Votre panier est déjà vide ou la commande a été envoyée.")
            else:
                # On enregistre en base de données
                c.execute('INSERT INTO commandes (articles, total, type_commande, detail_logistique) VALUES (?,?,?,?)',
                          (str(st.session_state.cart), total, service, infos))
                conn.commit()
                
                # LA SÉCURITÉ : On vide le panier IMMÉDIATEMENT
                # On garde une copie pour WhatsApp avant d'effacer
                st.session_state.dernier_recap = txt_wa 
                st.session_state.dernier_total = total
                st.session_state.cart = [] 
                
                st.session_state.commande_validee = True
                st.success("✅ Commande enregistrée avec succès !")
                st.rerun() # On rafraîchit pour faire disparaître le panier
        if st.session_state.commande_validee:
            # CONFIGURATION WHATSAPP
            num_gerante = "221777743766" # <--- METS TON NUMÉRO ICI
            msg = f"Bonjour! Nouvelle commande : {txt_wa}%0A%0A*Total:* {int(total)} FCFA%0A*Mode:* {service}%0A*Infos:* {infos}"
            wa_link = f"https://wa.me/{num_gerante}?text={msg}"
            
            st.markdown(f"""
                <a href="{wa_link}" target="_blank">
                    <div style="background-color:#25D366; color:white; padding:15px; text-align:center; border-radius:10px; font-weight:bold; margin-top:10px;">
                        📲 2. ENVOYER SUR WHATSAPP
                    </div>
                </a>
            """, unsafe_allow_html=True)
            
            if st.button("🔄 Nouvelle commande"):
                st.session_state.cart = []
                st.session_state.commande_validee = False
                st.rerun()

elif choice == "👩‍💼 Gérante (Admin)":
    st.header("⚙️ Gestion des Plats")
    with st.form("admin_add"):
        n = st.text_input("Nom")
        p = st.number_input("Prix (FCFA)", min_value=0)
        i = st.text_input("URL Image")
        d = st.text_area("Description")
        if st.form_submit_button("Ajouter à la carte"):
            c.execute('INSERT INTO menu (nom, prix, desc, img) VALUES (?,?,?,?)', (n,p,d,i))
            conn.commit()
            st.rerun()
    
    st.divider()
    st.subheader("🗑️ Supprimer un plat")
    items = pd.read_sql('SELECT * FROM menu', conn)
    for _, row in items.iterrows():
        col1, col2 = st.columns([4, 1])
        col1.write(f"**{row['nom']}** ({int(row['prix'])} FCFA)")
        if col2.button("Supprimer", key=f"del_{row['id']}"):
            c.execute('DELETE FROM menu WHERE id=?', (row['id'],))
            conn.commit()
            st.rerun()

elif choice == "📊 Commandes Reçues":
    st.header("📋 Historique des Commandes")
    if st.button("🧹 Vider toutes les commandes"):
        c.execute("DELETE FROM commandes")
        conn.commit()
        st.rerun()

    cmds = pd.read_sql('SELECT * FROM commandes ORDER BY date DESC', conn)
    for _, row in cmds.iterrows():
        color = "red" if row['type_commande'] == "Sur place" else "orange"
        with st.expander(f"Commande #{row['id']} - {row['type_commande']} - {int(row['total'])} FCFA"):
            st.markdown(f":{color}[**LIEU : {row['detail_logistique']}**]")
            st.write(f"**Plats :** {row['articles']}")
            st.write(f"**Date :** {row['date']}")
            if st.button("Terminer", key=f"done_{row['id']}"):
                c.execute('DELETE FROM commandes WHERE id=?', (row['id'],))
                conn.commit()
                st.rerun()

