import streamlit as st
import sqlite3
import pandas as pd
import json
import urllib.parse
from datetime import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Menu Express PRO", page_icon="🥘", layout="wide")

if "PASSWORD" not in st.secrets:
    st.error("Erreur : Mot de passe non configuré dans les secrets.")
    st.stop()

# --- 2. STYLE CSS (LISIBILITÉ MAXIMALE) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
* { font-family: 'Montserrat', sans-serif; }

/* Fond assombri */
.stApp {
    background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
    url("https://images.unsplash.com/photo-1504674900247-0877df9cc836?q=80&w=2070");
    background-size: cover;
    background-attachment: fixed;
}

/* SIDEBAR : BLANC PUR SANS DORÉ */
[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
    font-weight: 700 !important;
    text-shadow: 2px 2px 4px #000000;
}

/* CARTES DES PLATS */
.plat-card {
    padding: 25px;
    border-radius: 20px;
    background-color: rgba(0, 0, 0, 0.95); 
    border: 1px solid rgba(255, 255, 255, 0.3);
    margin-bottom: 15px;
    display: flex;
    align-items: center;
}

/* LISIBILITÉ TOTALE : TEXTE BLANC + OMBRE NOIRE ÉPAISSE */
h1, h2, h3, p, label, span, .stMarkdown {
    color: #FFFFFF !important;
    text-shadow: 2px 2px 5px #000000, -1px -1px 0 #000000, 1px -1px 0 #000000;
}

/* PRIX EN VERT FLUO */
.prix-vert {
    color: #00FF66 !important;
    font-size: 2rem;
    font-weight: bold;
    margin-left: auto;
}

/* BOUTONS */
.stButton>button {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    font-weight: 900;
    border-radius: 10px;
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
        if st.button("🔴 Déconnexion"):
            st.session_state.admin_ok = False
            st.rerun()

# --- 5. PAGE CLIENT (COMMANDER) ---
if choice == "🍽️ Commander":
    st.markdown("<h1 style='text-align: center;'>👨‍🍳 Notre Carte</h1>", unsafe_allow_html=True)
    
    plats = pd.read_sql("SELECT * FROM menu WHERE disponible=1", conn)
    
    for _, row in plats.iterrows():
        st.markdown(f"""
        <div class="plat-card">
            <img src="{row['img'] or 'https://via.placeholder.com/150'}" style="width:110px;height:110px;border-radius:12px;margin-right:20px;object-fit:cover;">
            <div class="plat-info">
                <h2>{row['nom']}</h2>
                <p>{row['desc']}</p>
            </div>
            <div class="prix-vert">{int(row['prix'])} F</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 4])
        qte = col1.number_input("Qté", 1, 10, 1, key=f"q_{row['id']}")
        if col2.button(f"Ajouter {row['nom']} au panier", key=f"btn_{row['id']}", use_container_width=True):
            st.session_state.cart.append({"nom": row["nom"], "prix": row["prix"], "qte": qte})
            st.toast(f"✅ {row['nom']} ajouté !")

    # --- PANIER ---
    if st.session_state.cart:
        st.markdown("<br><hr>", unsafe_allow_html=True)
        st.markdown("## 🛒 Votre Panier")
        total_cmd = sum(item['prix'] * item['qte'] for item in st.session_state.cart)
        
        for item in st.session_state.cart:
            st.write(f"• **{item['nom']}** x{item['qte']} : {int(item['prix']*item['qte'])} F")
        
        st.markdown(f"### TOTAL : <span style='color:#00FF66'>{int(total_cmd)} FCFA</span>", unsafe_allow_html=True)
        
        mode = st.radio("Comment voulez-vous recevoir votre commande ?", ["Sur place", "Livraison"], horizontal=True)
        
        t_num, tel, adr = "", "", ""
        if mode == "Sur place":
            t_num = st.text_input("Numéro de Table ou Nom")
        else:
            c1, c2 = st.columns(2)
            tel = c1.text_input("📞 Numéro de Téléphone")
            adr = c2.text_input("📍 Adresse de Livraison")

        if st.button("✅ CONFIRMER ET ENVOYER LA COMMANDE", use_container_width=True):
            if (mode == "Sur place" and not t_num) or (mode == "Livraison" and (not tel or not adr)):
                st.error("Veuillez remplir les informations de contact.")
            else:
                c.execute("INSERT INTO commandes (articles, total, type_commande, telephone, adresse, table_num) VALUES (?,?,?,?,?,?)",
                          (json.dumps(st.session_state.cart, ensure_ascii=False), total_cmd, mode, tel, adr, t_num))
                conn.commit()
                
                # WhatsApp
                msg = f"*COMMANDE ({mode})*\n"
                for it in st.session_state.cart: msg += f"- {it['nom']} x{it['qte']}\n"
                msg += f"\n💰 *TOTAL : {int(total_cmd)} F*"
                info = f"\n📍 Table: {t_num}" if mode == "Sur place" else f"\n📞 Tel: {tel}\n📍 Adresse: {adr}"
                
                wa_url = f"https://wa.me/221777743766?text={urllib.parse.quote(msg + info)}"
                st.session_state.cart = []
                st.success("Commande enregistrée !")
                st.link_button("📲 Envoyer sur WhatsApp", wa_url, use_container_width=True)

# --- 6. ESPACE GÉRANT (DATABASE) ---
elif choice == "📊 Espace Gérant":
    st.markdown("<h1>📊 Administration</h1>", unsafe_allow_html=True)
    t_cmd, t_menu = st.tabs(["📋 Liste des Commandes", "🥘 Gérer la Carte"])

    with t_cmd:
        cmds = pd.read_sql("SELECT * FROM commandes ORDER BY date DESC", conn)
        for _, r in cmds.iterrows():
            with st.expander(f"📦 Commande #{r['id']} - {r['type_commande']} ({int(r['total'])} F)"):
                st.write(f"**Client :** {r['table_num'] if r['table_num'] else r['telephone']}")
                if r['adresse']: st.write(f"**Lieu :** {r['adresse']}")
                st.table(pd.DataFrame(json.loads(r['articles'])))
                if st.button("✔️ Archiver / Terminer", key=f"fin_{r['id']}"):
                    c.execute("DELETE FROM commandes WHERE id=?", (r['id'],))
                    conn.commit()
                    st.rerun()

    with t_menu:
        st.subheader("🛠️ Ajouter un plat")
        with st.form("new_plat"):
            n = st.text_input("Nom du plat")
            p = st.number_input("Prix", 0)
            d = st.text_area("Description")
            i = st.text_input("URL de l'image")
            if st.form_submit_button("Ajouter à la carte"):
                c.execute("INSERT INTO menu (nom, prix, desc, img) VALUES (?,?,?,?)", (n,p,d,i))
                conn.commit()
                st.rerun()
        
        st.divider()
        st.subheader("📋 État du Menu")
        plats_edit = pd.read_sql("SELECT * FROM menu", conn)
        for _, row in plats_edit.iterrows():
            c1, c2, c3 = st.columns([3, 2, 1])
            c1.write(f"**{row['nom']}**")
            label = "✅ En Stock" if row['disponible'] else "❌ Rupture"
            if c2.button(label, key=f"stk_{row['id']}"):
                c.execute("UPDATE menu SET disponible=? WHERE id=?", (0 if row['disponible'] else 1, row['id']))
                conn.commit()
                st.rerun()
            if c3.button("🗑️", key=f"del_{row['id']}"):
                c.execute("DELETE FROM menu WHERE id=?", (row['id'],))
                conn.commit()
                st.rerun()
