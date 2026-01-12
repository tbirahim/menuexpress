import streamlit as st
import sqlite3
import pandas as pd
import json
import urllib.parse
from datetime import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Menu Express PRO", page_icon="🥘", layout="wide")

if "PASSWORD" not in st.secrets:
    st.error("Configurez 'PASSWORD' dans les secrets Streamlit.")
    st.stop()

# --- 2. STYLE CSS (LISIBILITÉ MAXIMALE) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
* { font-family: 'Montserrat', sans-serif; }

.stApp {
    background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
    url("https://images.unsplash.com/photo-1504674900247-0877df9cc836?q=80&w=2070");
    background-size: cover;
    background-attachment: fixed;
}

/* SIDEBAR : DORÉ ÉCLATANT ET LISIBLE */
[data-testid="stSidebar"] * {
    color: #FFD700 !important; /* Doré plus brillant */
    font-weight: 700 !important;
    text-shadow: 2px 2px 4px #000000; /* Ombre portée pour détacher du fond */
}

/* CARTES DES PLATS : CONTRASTE NOIR/BLANC */
.plat-card {
    padding: 25px;
    border-radius: 20px;
    background-color: rgba(0, 0, 0, 0.95); /* Fond quasiment noir pour la lisibilité */
    border: 2px solid #FFD700; 
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
}

/* TEXTES DE DROITE : BLANC PUR */
.plat-info h2 { 
    color: #FFFFFF !important; 
    margin: 0; 
    font-size: 1.8rem; 
    text-shadow: 1px 1px 2px #000000;
}
.plat-info p { 
    color: #FFFFFF !important; /* Passé de gris à blanc pur */
    font-size: 1.1rem; 
    opacity: 0.9;
}

/* PRIX EN VERT FLUO */
.prix-vert {
    color: #00FF66 !important;
    font-size: 2.2rem;
    font-weight: bold;
    margin-left: auto;
    text-shadow: 1px 1px 5px rgba(0,0,0,0.8);
}

/* RESUMÉ PANIER ET TITRES */
h1, h2, h3, label, .stMarkdown {
    color: #FFFFFF !important;
    text-shadow: 2px 2px 4px #000000;
}
</style>
""", unsafe_allow_html=True)

# --- 3. BASE DE DONNÉES (SÉCURISÉE) ---
def init_db():
    conn = sqlite3.connect("menu_pro.db", check_same_thread=False)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT, prix REAL, desc TEXT, img TEXT, disponible INTEGER DEFAULT 1)""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS commandes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        articles TEXT, total REAL, type_commande TEXT, 
        telephone TEXT, adresse TEXT, table_num TEXT, date DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    
    # Correction automatique des colonnes pour éviter le KeyError
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
    choice = st.radio("Navigation", ["🍽️ Commander", "📊 Espace Gérant"] if st.session_state.admin_ok else ["🍽️ Commander"])
    
    if not st.session_state.admin_ok:
        with st.expander("🔐 Accès Gérant"):
            pwd = st.text_input("Code", type="password")
            if st.button("Connexion"):
                if pwd == st.secrets["PASSWORD"]:
                    st.session_state.admin_ok = True
                    st.rerun()
    else:
        if st.button("🔴 Quitter l'admin"):
            st.session_state.admin_ok = False
            st.rerun()

# --- 5. PAGE CLIENT ---
if choice == "🍽️ Commander":
    st.markdown("<h1 style='text-align: center;'>👨‍🍳 Notre Carte</h1>", unsafe_allow_html=True)
    
    plats = pd.read_sql("SELECT * FROM menu WHERE disponible=1", conn)
    
    for _, row in plats.iterrows():
        st.markdown(f"""
        <div class="plat-card">
            <img src="{row['img'] or 'https://via.placeholder.com/150'}" style="width:120px;height:120px;border-radius:15px;margin-right:20px;object-fit:cover;">
            <div class="plat-info">
                <h2>{row['nom']}</h2>
                <p>{row['desc']}</p>
            </div>
            <div class="prix-vert">{int(row['prix'])} F</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 3])
        qte = col1.number_input("Qté", 1, 10, 1, key=f"q_{row['id']}")
        if col2.button(f"Ajouter {row['nom']}", key=f"btn_{row['id']}", use_container_width=True):
            st.session_state.cart.append({"nom": row["nom"], "prix": row["prix"], "qte": qte})
            st.toast(f"✅ {row['nom']} ajouté !")

    # --- PANIER ---
    if st.session_state.cart:
        st.markdown("<br><hr>", unsafe_allow_html=True)
        st.markdown("## 🛒 Votre Commande")
        
        total_cmd = 0
        for i, item in enumerate(st.session_state.cart):
            st.markdown(f"**{item['nom']}** x{item['qte']} : `{int(item['prix']*item['qte'])} F`")
            total_cmd += item["prix"] * item["qte"]
        
        st.markdown(f"### TOTAL : <span style='color:#00FF66'>{int(total_cmd)} FCFA</span>", unsafe_allow_html=True)
        
        mode = st.radio("Réception", ["Sur place", "Livraison"], horizontal=True)
        
        if mode == "Sur place":
            t_num = st.text_input("Numéro de Table / Nom")
            tel, adr = "", ""
        else:
            c1, c2 = st.columns(2)
            tel = c1.text_input("📞 Téléphone")
            adr = c2.text_input("📍 Adresse")
            t_num = ""

        if st.button("🚀 VALIDER LA COMMANDE", use_container_width=True):
            if (mode == "Sur place" and not t_num) or (mode == "Livraison" and (not tel or not adr)):
                st.warning("Veuillez remplir les informations.")
            else:
                c.execute("INSERT INTO commandes (articles, total, type_commande, telephone, adresse, table_num) VALUES (?,?,?,?,?,?)",
                          (json.dumps(st.session_state.cart, ensure_ascii=False), total_cmd, mode, tel, adr, t_num))
                conn.commit()
                
                # WhatsApp
                txt = f"*NOUVELLE COMMANDE (%s)*\n\n" % mode
                for it in st.session_state.cart: txt += f"- {it['nom']} x{it['qte']}\n"
                txt += f"\n💰 *TOTAL : {int(total_cmd)} F*"
                info = f"\n📍 Table: {t_num}" if mode == "Sur place" else f"\n📞 Tel: {tel}\n📍 Adresse: {adr}"
                
                wa_url = f"https://wa.me/221777743766?text={urllib.parse.quote(txt + info)}"
                st.success("Enregistré !")
                st.link_button("📲 Finaliser sur WhatsApp", wa_url, use_container_width=True)
                st.session_state.cart = []

# --- 6. ESPACE GÉRANT ---
elif choice == "📊 Espace Gérant":
    st.markdown("<h1 style='color: #FFD700;'>📊 Administration</h1>", unsafe_allow_html=True)
    t_cmd, t_carte = st.tabs(["📋 Commandes", "🥘 Menu"])

    with t_cmd:
        cmds = pd.read_sql("SELECT * FROM commandes ORDER BY date DESC", conn)
        for _, r in cmds.iterrows():
            with st.expander(f"📦 Commande #{r['id']} - {r['type_commande']}"):
                st.write(f"**Client :** {r['table_num'] if r['table_num'] else r['telephone']}")
                if r['adresse']: st.write(f"**Lieu :** {r['adresse']}")
                st.table(pd.DataFrame(json.loads(r['articles'])))
                if st.button("✔️ Terminer", key=f"fin_{r['id']}"):
                    c.execute("DELETE FROM commandes WHERE id=?", (r['id'],))
                    conn.commit()
                    st.rerun()

    with t_carte:
        st.subheader("Ajouter un plat")
        with st.form("new"):
            n = st.text_input("Nom")
            p = st.number_input("Prix", 0)
            d = st.text_area("Description")
            i = st.text_input("URL Image")
            if st.form_submit_button("Ajouter"):
                c.execute("INSERT INTO menu (nom, prix, desc, img) VALUES (?,?,?,?)", (n,p,d,i))
                conn.commit()
                st.rerun()
