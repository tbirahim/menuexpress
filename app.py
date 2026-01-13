import streamlit as st
import sqlite3
import pandas as pd
import json
import urllib.parse
from datetime import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Menu Express PRO", page_icon="🥘", layout="wide")

# Sécurité pour le mot de passe
if "PASSWORD" not in st.secrets:
    st.error("Le secret 'PASSWORD' n'est pas configuré.")
    st.stop()

# --- 2. DESIGN & LISIBILITÉ (DORÉ ET NOIR) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
* { font-family: 'Montserrat', sans-serif; }

/* Fond et assombrissement */
.stApp {
    background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
    url("https://images.unsplash.com/photo-1504674900247-0877df9cc836?q=80&w=2070");
    background-size: cover;
    background-attachment: fixed;
}

/* SIDEBAR : ÉCRITURES DORÉES */
[data-testid="stSidebar"] * {
    color: #D4AF37 !important;
    font-weight: 700 !important;
}

/* CARTES DES PLATS */
.plat-card {
    padding: 25px;
    border-radius: 20px;
    background-color: rgba(0, 0, 0, 0.95);
    border: 1px solid #D4AF37;
    margin-bottom: 15px;
    display: flex;
    align-items: center;
}

.plat-info h2 { color: #FFFFFF !important; margin: 0; font-size: 1.7rem; }
.plat-info p { color: #BBBBBB !important; font-size: 1.1rem; margin-top: 5px; }

/* PRIX EN VERT ÉCLATANT */
.prix-vert {
    color: #25D366 !important;
    font-size: 2rem;
    font-weight: bold;
    margin-left: auto;
    white-space: nowrap;
}

/* BOUTONS ET INPUTS */
.stButton>button {
    background-color: #D4AF37 !important;
    color: black !important;
    font-weight: bold;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# --- 3. BASE DE DONNÉES (CORRECTION DU KEYERROR) ---
def init_db():
    conn = sqlite3.connect("menu_pro.db", check_same_thread=False)
    c = conn.cursor()
    
    # Table Menu
    c.execute("""CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT, prix REAL, desc TEXT, img TEXT, disponible INTEGER DEFAULT 1)""")
    
    # Table Commandes avec toutes les colonnes nécessaires
    c.execute("""CREATE TABLE IF NOT EXISTS commandes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        articles TEXT, total REAL, type_commande TEXT, 
        telephone TEXT, adresse TEXT, table_num TEXT, 
        date DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    
    # Sécurité : Vérifier si les colonnes existent (évite l'erreur KeyError si la DB est vieille)
    cursor = conn.execute('PRAGMA table_info(commandes)')
    colonnes_existantes = [col[1] for col in cursor.fetchall()]
    
    colonnes_a_ajouter = {
        'telephone': 'TEXT',
        'adresse': 'TEXT',
        'table_num': 'TEXT'
    }
    
    for col, type_col in colonnes_a_ajouter.items():
        if col not in colonnes_existantes:
            c.execute(f'ALTER TABLE commandes ADD COLUMN {col} {type_col}')
    
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
            pwd = st.text_input("Code Secret", type="password")
            if st.button("Se connecter"):
                if pwd == st.secrets["PASSWORD"]:
                    st.session_state.admin_ok = True
                    st.rerun()
                else:
                    st.error("Code incorrect")
    else:
        if st.button("🔴 Déconnexion"):
            st.session_state.admin_ok = False
            st.rerun()

# --- 5. PAGE CLIENT : COMMANDER ---
if choice == "🍽️ Commander":
    st.markdown("<h1 style='text-align:center; color:white;'>🥘 Notre Carte</h1>", unsafe_allow_html=True)
    
    plats = pd.read_sql("SELECT * FROM menu WHERE disponible=1", conn)
    
    if plats.empty:
        st.info("La carte est vide pour le moment.")
    
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

        col_q, col_b = st.columns([1, 4])
        qte = col_q.number_input("Qté", 1, 10, 1, key=f"qte_{row['id']}")
        if col_b.button(f"🛒 Ajouter au panier", key=f"btn_{row['id']}", use_container_width=True):
            st.session_state.cart.append({"nom": row["nom"], "prix": row["prix"], "qte": qte})
            st.toast(f"✅ {row['nom']} ajouté !")

    # --- AFFICHAGE DU PANIER ---
    if st.session_state.cart:
        st.markdown("<br><hr>", unsafe_allow_html=True)
        st.markdown("<h2 style='color: #D4AF37;'>🛒 Finaliser ma Commande</h2>", unsafe_allow_html=True)
        
        total_cmd = sum(item['prix'] * item['qte'] for item in st.session_state.cart)
        
        # Résumé visuel
        for i, item in enumerate(st.session_state.cart):
            c1, c2 = st.columns([5, 1])
            c1.write(f"🔹 **{item['nom']}** x{item['qte']}")
            if c2.button("❌", key=f"del_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()
        
        st.markdown(f"### TOTAL À PAYER : <span style='color:#25D366'>{int(total_cmd)} FCFA</span>", unsafe_allow_html=True)
        
        mode = st.radio("Mode de réception", ["Sur place", "Livraison"], horizontal=True)
        t_num, tel, adr = "", "", ""
        
        if mode == "Sur place":
            t_num = st.text_input("Numéro de table ou Nom du client")
        else:
            col_t, col_a = st.columns(2)
            tel = col_t.text_input("📞 Votre Téléphone")
            adr = col_a.text_input("📍 Adresse précise")

        if st.button("🚀 CONFIRMER ET ENVOYER", use_container_width=True):
            if (mode == "Sur place" and not t_num) or (mode == "Livraison" and (not tel or not adr)):
                st.error("Veuillez remplir les informations manquantes !")
            else:
                # Sauvegarde SQL
                c.execute("INSERT INTO commandes (articles, total, type_commande, telephone, adresse, table_num) VALUES (?,?,?,?,?,?)",
                          (json.dumps(st.session_state.cart, ensure_ascii=False), total_cmd, mode, tel, adr, t_num))
                conn.commit()
                
                # Lien WhatsApp
                msg = f"*NOUVELLE COMMANDE ({mode})*\n"
                for it in st.session_state.cart:
                    msg += f"• {it['nom']} x{it['qte']}\n"
                msg += f"\n💰 *TOTAL : {int(total_cmd)} F*"
                msg += f"\n\n👤 Infos: {t_num if mode == 'Sur place' else tel + ' - ' + adr}"
                
                wa_url = f"https://wa.me/221777743766?text={urllib.parse.quote(msg)}"
                st.session_state.cart = []
                st.success("Commande validée !")
                st.link_button("📲 Envoyer sur WhatsApp", wa_url, use_container_width=True)

# --- 6. ESPACE GÉRANT : GESTION ET STATS ---
elif choice == "📊 Espace Gérant":
    st.markdown("<h1 style='color: #D4AF37;'>📊 Administration</h1>", unsafe_allow_html=True)
    t_cmd, t_menu = st.tabs(["📋 Commandes Reçues", "🥘 Gérer la Carte"])

    with t_cmd:
        cmds = pd.read_sql("SELECT * FROM commandes ORDER BY date DESC", conn)
        if cmds.empty:
            st.info("Aucune commande enregistrée.")
        for _, r in cmds.iterrows():
            with st.expander(f"📦 Commande #{r['id']} - {r['type_commande']}"):
                st.write(f"**Client :** {r['table_num'] if r['table_num'] else r['telephone']}")
                if r['adresse']: st.write(f"**Adresse :** {r['adresse']}")
                st.write("**Articles :**")
                st.table(pd.DataFrame(json.loads(r['articles'])))
                if st.button("Marquer comme terminé", key=f"fin_{r['id']}"):
                    c.execute("DELETE FROM commandes WHERE id=?", (r['id'],))
                    conn.commit()
                    st.rerun()

    with t_menu:
        st.subheader("🛠️ Ajouter un nouveau plat")
        with st.form("add_form"):
            n = st.text_input("Nom du plat")
            p = st.number_input("Prix (F)", 0)
            d = st.text_area("Description")
            i = st.text_input("URL de l'image")
            if st.form_submit_button("Ajouter à la carte"):
                c.execute("INSERT INTO menu (nom, prix, desc, img) VALUES (?,?,?,?)", (n, p, d, i))
                conn.commit()
                st.rerun()
        
        st.divider()
        st.subheader("📋 État de la carte")
        plats_edit = pd.read_sql("SELECT * FROM menu", conn)
        for _, mi in plats_edit.iterrows():
            c1, c2, c3 = st.columns([3, 2, 1])
            c1.write(f"**{mi['nom']}** ({int(mi['prix'])} F)")
            label = "✅ En Stock" if mi['disponible'] else "❌ Rupture"
            if c2.button(label, key=f"stk_{mi['id']}"):
                c.execute("UPDATE menu SET disponible=? WHERE id=?", (0 if mi['disponible'] else 1, mi['id']))
                conn.commit()
                st.rerun()
            if c3.button("🗑️", key=f"del_{mi['id']}"):
                c.execute("DELETE FROM menu WHERE id=?", (mi['id'],))
                conn.commit()
                st.rerun()
