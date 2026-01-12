import streamlit as st
import sqlite3
import pandas as pd
import urllib.parse

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Menu Express PRO", page_icon="🍴", layout="wide")

# --- 2. DESIGN LUXE ---
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

# --- 4. GESTION DE SESSION ---
if 'admin_ok' not in st.session_state: st.session_state.admin_ok = False
if 'cart' not in st.session_state: st.session_state.cart = []
if 'cmd_faite' not in st.session_state: st.session_state.cmd_faite = False

# --- 5. BARRE LATÉRALE ---
with st.sidebar:
    st.title("⚜️ Menu Express")
    pages = ["🍽️ Menu Client", "🛒 Mon Panier"]
    if st.session_state.admin_ok:
        pages.extend(["👩‍💼 Gérante (Admin)", "📊 Commandes Reçues"])
    
    choice = st.radio("Navigation", pages)
    
    st.write("---")
    if not st.session_state.admin_ok:
        with st.expander("🔐 Admin"):
            pwd = st.text_input("Code", type="password")
            if st.button("Se connecter"):
                if pwd == "admin123":
                    st.session_state.admin_ok = True
                    st.rerun()
    else:
        if st.button("🔴 Déconnexion"):
            st.session_state.admin_ok = False
            st.rerun()

# --- 6. PAGES ---

if choice == "🍽️ Menu Client":
    st.header("🍴 Notre Carte")
    df = pd.read_sql('SELECT * FROM menu', conn)
    if df.empty:
        st.info("La carte est vide pour le moment.")
    else:
        for _, row in df.iterrows():
            img = row['img'] if row['img'] else "https://via.placeholder.com/150"
            st.markdown(f'<div class="plat-card"><img src="{img}" class="plat-image"><div><h3>{row["nom"]}</h3><p>{row["desc"]}</p></div><span class="prix">{int(row["prix"])} FCFA</span></div>', unsafe_allow_html=True)
            if st.button(f"Ajouter au panier", key=f"add_{row['id']}"):
                st.session_state.cart.append({"nom": row['nom'], "prix": row['prix']})
                st.toast(f"✅ {row['nom']} ajouté !")

elif choice == "🛒 Mon Panier":
    st.header("🛍️ Votre Panier")
    if not st.session_state.cart:
        if st.session_state.cmd_faite:
            st.success("✅ Commande enregistrée !")
            # BOUTON DE SECOURS AU CAS OÙ LE LIEN NE S'OUVRE PAS TOUT SEUL
            if 'wa_link' in st.session_state:
                st.markdown(f"""
                    <a href="{st.session_state.wa_link}" target="_blank" style="text-decoration:none;">
                        <div style="background-color:#25D366; color:white; padding:15px; text-align:center; border-radius:10px; font-weight:bold; font-size:1.2rem; margin:20px 0;">
                            📲 CLIQUER ICI POUR ENVOYER SUR WHATSAPP
                        </div>
                    </a>
                """, unsafe_allow_html=True)
            
            if st.button("🔄 Faire une nouvelle commande"):
                st.session_state.cmd_faite = False
                st.rerun()
        else:
            st.write("Votre panier est vide.")
    else:
        total = sum(i['prix'] for i in st.session_state.cart)
        txt_items = ""
        for i in st.session_state.cart:
            st.write(f"- {i['nom']} : {int(i['prix'])} FCFA")
            txt_items += f"- {i['nom']}\n"
        
        st.divider()
        service = st.radio("Mode de service", ["Sur place", "Livraison"])
        infos = st.text_input("N° de Table" if service == "Sur place" else "Téléphone et Adresse")
        
        if st.button("🚀 VALIDER LA COMMANDE"):
            if not infos:
                st.error("Veuillez remplir les informations !")
            else:
                # 1. Sauvegarde Database
                c.execute('INSERT INTO commandes (articles, total, type_commande, detail_logistique) VALUES (?,?,?,?)',
                          (str(st.session_state.cart), total, service, infos))
                conn.commit()
                
                # 2. Préparation WhatsApp (Formatage Ultra-Robuste)
                num_gerante = "22177XXXXXXX" # <--- METS TON NUMÉRO ICI SANS LE +
                msg_brut = f"Bonjour ! Nouvelle commande :\n{txt_items}\n*Total :* {int(total)} FCFA\n*Mode :* {service}\n*Infos :* {infos}"
                msg_final = urllib.parse.quote(msg_brut)
                st.session_state.wa_link = f"https://api.whatsapp.com/send?phone={num_gerante}&text={msg_final}"
                
                # 3. Nettoyage Session
                st.session_state.cart = []
                st.session_state.cmd_faite = True
                
                # 4. Tentative de redirection automatique
                st.markdown(f'<meta http-equiv="refresh" content="0; url={st.session_state.wa_link}">', unsafe_allow_html=True)
                st.rerun()
                
                # 2. Préparation WhatsApp
                num_gerante = "221777743766" # <--- METS TON NUMÉRO ICI
                msg_brut = f"Bonjour ! Nouvelle commande :\n{txt_items}\n*Total :* {int(total)} FCFA\n*Mode :* {service}\n*Infos :* {infos}"
                msg_final = urllib.parse.quote(msg_brut)
                wa_link = f"https://wa.me/{num_gerante}?text={msg_final}"
                
                # 3. Nettoyage Session
                st.session_state.cart = []
                st.session_state.cmd_faite = True
                
                # 4. Redirection automatique
                st.markdown(f'<meta http-equiv="refresh" content="0; url={wa_link}">', unsafe_allow_html=True)
                st.rerun()

elif choice == "👩‍💼 Gérante (Admin)":
    st.header("⚙️ Gestion de la Carte")
    with st.form("ajout_plat"):
        n, p, i, d = st.text_input("Nom"), st.number_input("Prix", 0), st.text_input("URL Image"), st.text_area("Description")
        if st.form_submit_button("Ajouter à la carte"):
            c.execute('INSERT INTO menu (nom, prix, desc, img) VALUES (?,?,?,?)', (n,p,d,i))
            conn.commit()
            st.success("Plat ajouté !")
            st.rerun()
    
    st.write("---")
    plats = pd.read_sql('SELECT * FROM menu', conn)
    for _, row in plats.iterrows():
        col1, col2 = st.columns([4, 1])
        col1.write(f"**{row['nom']}** - {int(row['prix'])} FCFA")
        if col2.button("Supprimer", key=f"del_{row['id']}"):
            c.execute('DELETE FROM menu WHERE id=?', (row['id'],))
            conn.commit()
            st.rerun()

elif choice == "📊 Commandes Reçues":
    st.header("📋 Suivi des Commandes")
    # Rafraîchissement automatique (optionnel mais recommandé)
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=30000, key="refresh_cmd")
    
    if st.button("🧹 Vider l'historique"):
        c.execute("DELETE FROM commandes")
        conn.commit()
        st.rerun()

    cmds = pd.read_sql('SELECT * FROM commandes ORDER BY date DESC', conn)
    for _, row in cmds.iterrows():
        type_icon = "🪑" if row['type_commande'] == "Sur place" else "🚚"
        with st.expander(f"{type_icon} {row['type_commande']} - {int(row['total'])} FCFA"):
            st.error(f"📍 {row['detail_logistique']}")
            st.write(f"**Articles :** {row['articles']}")
            if st.button("Marquer comme servi", key=f"done_{row['id']}"):
                c.execute('DELETE FROM commandes WHERE id=?', (row['id'],))
                conn.commit()
                st.rerun()

