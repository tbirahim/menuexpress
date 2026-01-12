import streamlit as st
import sqlite3
import pandas as pd
import json
import urllib.parse
import re
from datetime import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Menu Express PRO", page_icon="🥘", layout="wide")

if "PASSWORD" not in st.secrets:
    st.error("Le mot de passe admin n'est pas configuré dans les secrets Streamlit.")
    st.stop()

ADMIN_PASSWORD = st.secrets["PASSWORD"]

# --- 2. DESIGN & LISIBILITÉ MAXIMALE (CSS) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
* { font-family: 'Montserrat', sans-serif; }

/* Fond d'écran */
.stApp {
    background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
    url("https://images.unsplash.com/photo-1504674900247-0877df9cc836?q=80&w=2070");
    background-size: cover;
    background-attachment: fixed;
}

/* --- MODIFICATION : DORÉ POUR LA PARTIE GAUCHE (SIDEBAR) --- */
[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] label, 
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] .stMarkdown p {
    color: #D4AF37 !important; /* Couleur Dorée */
    font-weight: bold !important;
    text-shadow: 1px 1px 2px black;
}

/* Couleur des options radio dans la sidebar */
[data-testid="stSidebar"] .st-bd {
    color: #D4AF37 !important;
}

/* Cartes des plats - Contraste élevé */
.plat-card {
    padding: 25px;
    border-radius: 20px;
    background-color: rgba(0, 0, 0, 0.85); 
    border: 2px solid rgba(255, 255, 255, 0.1);
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    color: #FFFFFF !important;
}

/* Forcer la couleur blanche sur les textes de droite */
h1, h2, h3, p, span, .stMarkdown {
    color: #FFFFFF !important;
    text-shadow: 1px 1px 2px black;
}

.prix {
    color: #25D366 !important; 
    font-size: 1.8rem;
    font-weight: bold;
    margin-left: auto;
}

.cart-section {
    background-color: #000000;
    padding: 30px;
    border-radius: 20px;
    border: 3px solid #25D366;
    color: white;
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
        detail_logistique TEXT, date DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    conn.commit()
    return conn

conn = init_db()
c = conn.cursor()

# --- 4. NAVIGATION ---
if "admin_ok" not in st.session_state: st.session_state.admin_ok = False
if "cart" not in st.session_state: st.session_state.cart = []

with st.sidebar:
    st.markdown("# ⚜️ Menu Express")
    pages = ["🍽️ Commander", "📊 Espace Gérant"] if st.session_state.admin_ok else ["🍽️ Commander"]
    choice = st.radio("Navigation", pages)

    if not st.session_state.admin_ok:
        with st.expander("🔐 Accès Gérant"):
            pwd = st.text_input("Code", type="password")
            if st.button("Valider"):
                if pwd == ADMIN_PASSWORD:
                    st.session_state.admin_ok = True
                    st.rerun()
    else:
        if st.button("🔴 Quitter l'admin"):
            st.session_state.admin_ok = False
            st.rerun()

# --- 5. PAGE CLIENT (COMMANDER) ---
if choice == "🍽️ Commander":
    st.markdown("# 👨‍🍳 Notre Carte")
    
    plats = pd.read_sql("SELECT * FROM menu", conn)
    
    for _, row in plats.iterrows():
        is_dispo = row["disponible"] == 1
        card_opacity = "1" if is_dispo else "0.4; filter: grayscale(1);"
        
        st.markdown(f"""
        <div class="plat-card" style="opacity: {card_opacity}">
            <img src="{row['img'] or 'https://via.placeholder.com/150'}" style="width:130px;height:130px;border-radius:15px;margin-right:20px;object-fit:cover;">
            <div style="flex-grow: 1;">
                <h2 style="margin:0; font-size: 1.5rem;">{row['nom']}</h2>
                <p style="margin:5px 0; font-size: 1rem;">{row['desc']}</p>
                {"<b style='color:#FF4B4B;'>🚫 Rupture de stock</b>" if not is_dispo else ""}
            </div>
            <div class="prix">{int(row['prix'])} F</div>
        </div>
        """, unsafe_allow_html=True)

        if is_dispo:
            col_q, col_b = st.columns([1, 2])
            qte = col_q.number_input(f"Quantité", 1, 10, 1, key=f"q_{row['id']}")
            if col_b.button(f"Ajouter {row['nom']}", key=f"btn_{row['id']}", use_container_width=True):
                st.session_state.cart.append({"nom": row["nom"], "prix": row["prix"], "qte": qte})
                st.toast(f"✅ {row['nom']} ajouté !")

    # --- AFFICHAGE DU PANIER ---
    if st.session_state.cart:
        st.markdown("---")
        st.markdown('<div class="cart-section">', unsafe_allow_html=True)
        st.markdown("## 🛒 Votre Panier")
        
        total_cmd = 0
        for i, item in enumerate(st.session_state.cart):
            st.markdown(f"**{item['nom']}** x{item['qte']} : `{int(item['prix'] * item['qte'])} F`")
            total_cmd += item["prix"] * item["qte"]
        
        st.markdown(f"### TOTAL : {int(total_cmd)} FCFA")
        
        mode = st.radio("Réception", ["Sur place", "Livraison"], horizontal=True)
        infos = st.text_input("Numéro de table ou Adresse complète")

        if st.button("✅ CONFIRMER LA COMMANDE", use_container_width=True):
            if not infos:
                st.error("Précisez votre table ou adresse.")
            else:
                c.execute("INSERT INTO commandes (articles, total, type_commande, detail_logistique) VALUES (?,?,?,?)",
                          (json.dumps(st.session_state.cart, ensure_ascii=False), total_cmd, mode, infos))
                conn.commit()
                
                msg = f"*NOUVELLE COMMANDE*\nItems: {len(st.session_state.cart)}\nTotal: {int(total_cmd)} F\nInfos: {infos}"
                wa_url = f"https://wa.me/221777743766?text={urllib.parse.quote(msg)}"
                
                st.session_state.cart = []
                st.success("Commande envoyée !")
                st.link_button("📲 Ouvrir WhatsApp pour finaliser", wa_url, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- 6. ESPACE GÉRANT (ADMIN & STATS) ---
elif choice == "📊 Espace Gérant":
    st.markdown("# 🛡️ Administration")
    
    t_cmd, t_carte, t_stats = st.tabs(["📋 Commandes", "🥘 Ma Carte", "📈 Statistiques"])

    with t_cmd:
        cmds = pd.read_sql("SELECT * FROM commandes ORDER BY date DESC", conn)
        for _, r in cmds.iterrows():
            with st.expander(f"📦 Commande #{r['id']} - {int(r['total'])} F"):
                st.write(f"**Détails :** {r['detail_logistique']}")
                st.table(pd.DataFrame(json.loads(r['articles'])))
                if st.button("Terminer / Livrer", key=f"fin_{r['id']}"):
                    c.execute("DELETE FROM commandes WHERE id=?", (r["id"],))
                    conn.commit()
                    st.rerun()

    with t_carte:
        st.subheader("Ajouter un nouveau plat")
        with st.form("new_plat"):
            nom = st.text_input("Nom")
            prix = st.number_input("Prix", 0)
            desc = st.text_area("Description")
            img = st.text_input("URL de l'image")
            if st.form_submit_button("Ajouter"):
                c.execute("INSERT INTO menu (nom, prix, desc, img) VALUES (?,?,?,?)", (nom, prix, desc, img))
                conn.commit()
                st.rerun()

        st.divider()
        st.subheader("Gérer les stocks")
        menu_items = pd.read_sql("SELECT * FROM menu", conn)
        for _, mi in menu_items.iterrows():
            col1, col2, col3 = st.columns([3, 2, 1])
            col1.write(f"**{mi['nom']}**")
            
            btn_txt = "✅ En Stock" if mi['disponible'] else "❌ Rupture"
            if col2.button(btn_txt, key=f"stock_{mi['id']}"):
                new_val = 0 if mi['disponible'] else 1
                c.execute("UPDATE menu SET disponible=? WHERE id=?", (new_val, mi['id']))
                conn.commit()
                st.rerun()
                
            if col3.button("🗑️", key=f"del_{mi['id']}"):
                c.execute("DELETE FROM menu WHERE id=?", (mi['id'],))
                conn.commit()
                st.rerun()

    with t_stats:
        st.subheader("📈 Performances")
        df_ventes = pd.read_sql("SELECT articles, total FROM commandes", conn)
        if not df_ventes.empty:
            st.metric("Chiffre d'affaires (en cours)", f"{int(df_ventes['total'].sum())} FCFA")
            all_ordered = []
            for row in df_ventes['articles']:
                all_ordered.extend(json.loads(row))
            stats_df = pd.DataFrame(all_ordered)
            top_plats = stats_df.groupby('nom')['qte'].sum().sort_values(ascending=False)
            st.bar_chart(top_plats)
        else:
            st.info("Aucune donnée.")
