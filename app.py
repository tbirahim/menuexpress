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
    st.error("Mot de passe admin non configuré.")
    st.stop()

ADMIN_PASSWORD = st.secrets["PASSWORD"]

# --- 2. DESIGN & LISIBILITÉ AMÉLIORÉE ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
* { font-family: 'Montserrat', sans-serif; }

.stApp {
    background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
    url("https://images.unsplash.com/photo-1504674900247-0877df9cc836?q=80&w=2070");
    background-size: cover;
    background-attachment: fixed;
}

/* Amélioration de la lisibilité des cartes */
.plat-card {
    padding: 25px;
    border-radius: 20px;
    background-color: rgba(0, 0, 0, 0.7); /* Fond plus sombre pour le contraste */
    border: 1px solid rgba(255, 255, 255, 0.2);
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    color: white;
}

h1, h2, h3 { color: #ffffff !important; font-weight: 700 !important; }
p { color: #f0f0f0 !important; font-size: 1.1rem; }

.prix {
    color: #25D366;
    font-size: 1.6rem;
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
        articles TEXT, total REAL,
        type_commande TEXT, detail_logistique TEXT,
        date DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    conn.commit()
    return conn

conn = init_db()
c = conn.cursor()

# --- 4. SESSION ---
if "admin_ok" not in st.session_state: st.session_state.admin_ok = False
if "cart" not in st.session_state: st.session_state.cart = []
if "cmd_faite" not in st.session_state: st.session_state.cmd_faite = False

# --- 5. NAVIGATION ---
with st.sidebar:
    st.title("⚜️ Menu Express")
    choice = st.radio("Navigation", ["🍽️ Commander", "📊 Espace Gérant"])

    if not st.session_state.admin_ok:
        with st.expander("🔐 Connexion Gérant"):
            pwd = st.text_input("Mot de passe", type="password")
            if st.button("Connexion"):
                if pwd == ADMIN_PASSWORD:
                    st.session_state.admin_ok = True
                    st.rerun()
                else: st.error("Code incorrect")
    else:
        if st.button("🔴 Déconnexion"):
            st.session_state.admin_ok = False
            st.rerun()

# --- 6. PAGE CLIENT ---
if choice == "🍽️ Commander":
    st.title("👨‍🍳 Notre Carte")
    df_menu = pd.read_sql("SELECT * FROM menu", conn)

    for _, row in df_menu.iterrows():
        is_dispo = row["disponible"] == 1
        status_style = "" if is_dispo else "filter: grayscale(1); opacity: 0.4;"
        
        st.markdown(f"""
        <div class="plat-card" style="{status_style}">
            <img src="{row['img'] or 'https://via.placeholder.com/150'}" style="width:120px;height:120px;border-radius:15px;margin-right:20px;object-fit:cover;">
            <div>
                <h2 style="margin:0;">{row['nom']}</h2>
                <p>{row['desc']}</p>
                {"<b style='color:#ff4b4b;'>⚠️ Rupture de stock</b>" if not is_dispo else ""}
            </div>
            <span class="prix">{int(row['prix'])} F</span>
        </div>
        """, unsafe_allow_html=True)

        if is_dispo:
            col_q, col_b = st.columns([1, 2])
            qte = col_q.number_input(f"Quantité", 1, 20, 1, key=f"q_{row['id']}")
            if col_b.button(f"🛒 Ajouter {row['nom']}", key=f"add_{row['id']}", use_container_width=True):
                st.session_state.cart.append({"nom": row["nom"], "prix": row["prix"], "qte": qte})
                st.toast(f"✅ {row['nom']} ajouté !")

    # --- PANIER ---
    if st.session_state.cart:
        st.markdown('<div class="cart-section">', unsafe_allow_html=True)
        st.header("🛒 Votre Panier")
        total = 0
        for i, item in enumerate(st.session_state.cart):
            sous_total = item["prix"] * item["qte"]
            total += sous_total
            c1, c2, c3 = st.columns([5,2,1])
            c1.markdown(f"**{item['nom']}** x {item['qte']}")
            c2.write(f"{int(sous_total)} F")
            if c3.button("❌", key=f"del_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()

        st.divider()
        st.markdown(f"## Total : {int(total)} FCFA")
        
        service = st.radio("Mode", ["Sur place", "Livraison"], horizontal=True)
        logistique = st.text_input("Numéro de table ou Adresse & Téléphone")

        if st.button("🚀 VALIDER LA COMMANDE", use_container_width=True):
            if not logistique:
                st.warning("Veuillez remplir les informations de livraison/table.")
            else:
                c.execute("INSERT INTO commandes (articles, total, type_commande, detail_logistique) VALUES (?,?,?,?)",
                          (json.dumps(st.session_state.cart, ensure_ascii=False), total, service, logistique))
                conn.commit()
                
                # WhatsApp
                msg = f"*NOUVELLE COMMANDE*\nTotal: {int(total)} F\nInfos: {logistique}"
                wa_url = f"https://wa.me/221777743766?text={urllib.parse.quote(msg)}"
                st.session_state.wa_link = wa_url
                st.session_state.cart = []
                st.session_state.cmd_faite = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.cmd_faite:
        st.balloons()
        st.link_button("📲 ENVOYER SUR WHATSAPP", st.session_state.wa_link, use_container_width=True)

# --- 7. ESPACE GÉRANT (AVEC STATISTIQUES) ---
elif choice == "📊 Espace Gérant" and st.session_state.admin_ok:
    st.title("🛡️ Tableau de Bord Gérant")
    
    t1, t2, t3 = st.tabs(["📋 Commandes", "🥘 Ma Carte", "📈 Statistiques"])

    with t1:
        cmds = pd.read_sql("SELECT * FROM commandes ORDER BY date DESC", conn)
        for _, r in cmds.iterrows():
            with st.expander(f"📦 Commande #{r['id']} - {int(r['total'])} F"):
                st.write(f"**Mode:** {r['type_commande']} | **Détails:** {r['detail_logistique']}")
                st.table(pd.DataFrame(json.loads(r['articles'])))
                if st.button("✔️ Archiver", key=f"done_{r['id']}"):
                    c.execute("DELETE FROM commandes WHERE id=?", (r["id"],))
                    conn.commit()
                    st.rerun()

    with t2:
        # Formulaire ajout et liste des plats (disponibilité)
        st.subheader("Ajouter un plat")
        with st.form("add_form"):
            col_n, col_p = st.columns(2)
            n = col_n.text_input("Nom")
            p = col_p.number_input("Prix", 0)
            d = st.text_area("Description")
            i = st.text_input("Lien image")
            if st.form_submit_button("Valider"):
                c.execute("INSERT INTO menu (nom, prix, desc, img) VALUES (?,?,?,?)", (n,p,d,i))
                conn.commit()
                st.rerun()
        
        st.divider()
        plats = pd.read_sql("SELECT * FROM menu", conn)
        for _, pr in plats.iterrows():
            c_n, c_s, c_d = st.columns([3, 2, 1])
            c_n.write(f"**{pr['nom']}**")
            label = "✅ En Stock" if pr['disponible'] else "❌ Rupture"
            if c_s.button(label, key=f"stk_{pr['id']}"):
                c.execute("UPDATE menu SET disponible=? WHERE id=?", (0 if pr['disponible'] else 1, pr['id']))
                conn.commit()
                st.rerun()
            if c_d.button("🗑️", key=f"delp_{pr['id']}"):
                c.execute("DELETE FROM menu WHERE id=?", (pr['id'],))
                conn.commit()
                st.rerun()

    with t3:
        st.header("📈 Analyse des Ventes")
        df_stats = pd.read_sql("SELECT articles, total FROM commandes", conn)
        if not df_stats.empty:
            st.metric("Chiffre d'affaires en attente", f"{int(df_stats['total'].sum())} FCFA")
            
            # Calcul des plats les plus populaires
            all_items = []
            for row in df_stats['articles']:
                all_items.extend(json.loads(row))
            
            df_items = pd.DataFrame(all_items)
            pop_plats = df_items.groupby('nom')['qte'].sum().sort_values(ascending=False)
            
            st.write("### Plats les plus commandés")
            st.bar_chart(pop_plats)
        else:
            st.info("Pas encore de données de ventes.")
