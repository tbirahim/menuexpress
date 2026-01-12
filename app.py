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

# --- 2. STYLE CSS (LISIBILITÉ ET DORÉ) ---
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

/* SIDEBAR : ÉCRITURES EN DORÉ */
[data-testid="stSidebar"] * {
    color: #D4AF37 !important;
    font-weight: 700 !important;
}

/* CARTES DES PLATS : LISIBILITÉ AMÉLIORÉE */
.plat-card {
    padding: 25px;
    border-radius: 20px;
    background-color: rgba(0, 0, 0, 0.9); /* Noir profond */
    border: 2px solid #D4AF37; /* Bordure dorée fine */
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    color: white !important;
}

.plat-info h2 { color: #FFFFFF !important; margin: 0; font-size: 1.8rem; }
.plat-info p { color: #CCCCCC !important; font-size: 1.1rem; }

/* PRIX EN VERT */
.prix-vert {
    color: #25D366 !important;
    font-size: 2rem;
    font-weight: bold;
    margin-left: auto;
    text-shadow: 0px 0px 10px rgba(37, 211, 102, 0.3);
}

.stButton>button {
    background-color: #D4AF37 !important;
    color: black !important;
    font-weight: bold;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# --- 3. BASE DE DONNÉES ---
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
        with st.expander("🔐 Gérant"):
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
    st.markdown("<h1 style='text-align: center; color: white;'>👨‍🍳 Notre Carte</h1>", unsafe_allow_html=True)
    
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
        st.markdown("<h2 style='color: #D4AF37;'>🛒 Votre Commande</h2>", unsafe_allow_html=True)
        
        total_cmd = 0
        for i, item in enumerate(st.session_state.cart):
            st.write(f"⭐ **{item['nom']}** x{item['qte']} : {int(item['prix']*item['qte'])} F")
            total_cmd += item["prix"] * item["qte"]
        
        st.markdown(f"### TOTAL : <span style='color:#25D366'>{int(total_cmd)} FCFA</span>", unsafe_allow_html=True)
        
        mode = st.radio("Comment souhaitez-vous recevoir votre commande ?", ["Sur place", "Livraison"], horizontal=True)
        
        t_num, tel, adr = "", "", ""
        if mode == "Sur place":
            t_num = st.text_input("Numéro de Table / Nom pour l'appel")
        else:
            col_tel, col_adr = st.columns(2)
            tel = col_tel.text_input("📞 Numéro de Téléphone")
            adr = col_adr.text_input("📍 Adresse de Livraison")

        if st.button("🚀 VALIDER ET ENVOYER LA COMMANDE", use_container_width=True):
            if (mode == "Sur place" and not t_num) or (mode == "Livraison" and (not tel or not adr)):
                st.warning("Veuillez remplir les informations de réception.")
            else:
                # Sauvegarde SQL
                c.execute("INSERT INTO commandes (articles, total, type_commande, telephone, adresse, table_num) VALUES (?,?,?,?,?,?)",
                          (json.dumps(st.session_state.cart, ensure_ascii=False), total_cmd, mode, tel, adr, t_num))
                conn.commit()
                
                # Message WhatsApp
                txt = f"*NOUVELLE COMMANDE (%s)*\n\n" % mode
                for it in st.session_state.cart:
                    txt += f"- {it['nom']} x{it['qte']}\n"
                txt += f"\n💰 *TOTAL : {int(total_cmd)} F*"
                info_wa = f"\n📍 Table: {t_num}" if mode == "Sur place" else f"\n📞 Tel: {tel}\n📍 Adresse: {adr}"
                
                wa_url = f"https://wa.me/22177XXXXXXX?text={urllib.parse.quote(txt + info_wa)}"
                st.success("Commande enregistrée !")
                st.link_button("📲 Envoyer sur WhatsApp", wa_url, use_container_width=True)
                st.session_state.cart = []

# --- 6. ESPACE GÉRANT ---
elif choice == "📊 Espace Gérant":
    st.markdown("<h1 style='color: #D4AF37;'>📊 Administration</h1>", unsafe_allow_html=True)
    t_cmd, t_carte, t_stats = st.tabs(["📋 Commandes", "🥘 La Carte", "📈 Chiffres"])

    with t_cmd:
        cmds = pd.read_sql("SELECT * FROM commandes ORDER BY date DESC", conn)
        for _, r in cmds.iterrows():
            title = f"📦 Commande #{r['id']} - {r['type_commande']}"
            with st.expander(title):
                st.write(f"**Client :** {r['table_num'] if r['table_num'] else r['telephone']}")
                if r['adresse']: st.write(f"**Lieu :** {r['adresse']}")
                st.table(pd.DataFrame(json.loads(r['articles'])))
                if st.button("✔️ Archiver", key=f"arch_{r['id']}"):
                    c.execute("DELETE FROM commandes WHERE id=?", (r['id'],))
                    conn.commit()
                    st.rerun()

    with t_carte:
        st.subheader("🛠️ Ajouter un plat")
        with st.form("new"):
            n = st.text_input("Nom")
            p = st.number_input("Prix", 0)
            d = st.text_area("Description")
            i = st.text_input("URL Image")
            if st.form_submit_button("Ajouter"):
                c.execute("INSERT INTO menu (nom, prix, desc, img) VALUES (?,?,?,?)", (n,p,d,i))
                conn.commit()
                st.rerun()
        
        st.subheader("📋 État de la carte")
        plats_edit = pd.read_sql("SELECT * FROM menu", conn)
        for _, row in plats_edit.iterrows():
            col1, col2, col3 = st.columns([3, 2, 1])
            col1.write(f"**{row['nom']}**")
            label = "✅ En Stock" if row['disponible'] else "❌ Rupture"
            if col2.button(label, key=f"stk_{row['id']}"):
                c.execute("UPDATE menu SET disponible=? WHERE id=?", (0 if row['disponible'] else 1, row['id']))
                conn.commit()
                st.rerun()
            if col3.button("🗑️", key=f"del_{row['id']}"):
                c.execute("DELETE FROM menu WHERE id=?", (row['id'],))
                conn.commit()
                st.rerun()
