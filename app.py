import streamlit as st
import sqlite3
import pandas as pd
import json
import urllib.parse

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Menu Express PRO", page_icon="🥘", layout="wide")

if "PASSWORD" not in st.secrets:
    st.error("Mot de passe admin non configuré.")
    st.stop()

ADMIN_PASSWORD = st.secrets["PASSWORD"]

# --- 2. DESIGN ---
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

.plat-card {
    padding: 20px;
    border-radius: 20px;
    background-color: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 20px;
    display: flex;
    align-items: center;
}

.prix {
    color: #25D366;
    font-size: 1.4rem;
    font-weight: bold;
    margin-left: auto;
}

.cart-section {
    background-color: rgba(0,0,0,0.9);
    padding: 25px;
    border-radius: 20px;
    border: 2px solid #25D366;
}
</style>
""", unsafe_allow_html=True)

# --- 3. BASE DE DONNÉES ---
def init_db():
    conn = sqlite3.connect("menu_pro.db", check_same_thread=False)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT, prix REAL, desc TEXT, img TEXT)""")
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
if "wa_link" not in st.session_state: st.session_state.wa_link = ""

# --- 5. NAVIGATION ---
with st.sidebar:
    st.title("⚜️ Menu Express")
    choice = st.radio("Aller vers", ["🍽️ Commander", "📊 Espace Gérant"] if st.session_state.admin_ok else ["🍽️ Commander"])

    if not st.session_state.admin_ok:
        with st.expander("🔐 Connexion Gérant"):
            pwd = st.text_input("Mot de passe", type="password")
            if st.button("Se connecter"):
                if pwd == ADMIN_PASSWORD:
                    st.session_state.admin_ok = True
                    st.rerun()
                else:
                    st.error("Code incorrect")
    else:
        if st.button("🔴 Déconnexion"):
            st.session_state.admin_ok = False
            st.rerun()

# --- 6. PAGE CLIENT ---
if choice == "🍽️ Commander":
    st.title("👨‍🍳 Notre Carte")

    df = pd.read_sql("SELECT * FROM menu", conn)

    for _, row in df.iterrows():
        img = row["img"] if row["img"] else "https://via.placeholder.com/150"
        st.markdown(f"""
        <div class="plat-card">
            <img src="{img}" style="width:100px;height:100px;border-radius:12px;margin-right:20px;">
            <div>
                <h3>{row['nom']}</h3>
                <p style="color:#ccc;">{row['desc']}</p>
            </div>
            <span class="prix">{int(row['prix'])} F</span>
        </div>
        """, unsafe_allow_html=True)

        qte = st.number_input(f"Quantité pour {row['nom']}", 1, 20, 1, key=f"qte_{row['id']}")
        if st.button("Ajouter au panier", key=f"add_{row['id']}"):
            st.session_state.cart.append({
                "nom": row["nom"],
                "prix": row["prix"],
                "qte": qte
            })
            st.toast("Ajouté au panier")

    # --- PANIER ---
    if st.session_state.cart:
        st.markdown('<div class="cart-section">', unsafe_allow_html=True)
        st.header("🛒 Mon panier")

        total = 0
        for i, item in enumerate(st.session_state.cart):
            sous_total = item["prix"] * item["qte"]
            total += sous_total

            col1, col2, col3 = st.columns([5,2,1])
            col1.write(f"{item['nom']} x {item['qte']}")
            col2.write(f"{int(sous_total)} F")
            if col3.button("❌", key=f"del_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()

        st.subheader(f"Total : {int(total)} FCFA")

        service = st.radio("Mode", ["Sur place", "Livraison"], horizontal=True)

        if service == "Sur place":
            logistique = st.text_input("Numéro de table")
        else:
            tel = st.text_input("Téléphone")
            adr = st.text_input("Adresse")
            if not tel.isdigit() or len(tel) < 9:
                st.warning("Numéro invalide")
            logistique = f"📞 {tel} | 📍 {adr}"

        if st.button("🚀 Valider la commande"):
            if not logistique:
                st.warning("Informations manquantes")
            else:
                articles_json = json.dumps(st.session_state.cart, ensure_ascii=False)
                c.execute("INSERT INTO commandes (articles, total, type_commande, detail_logistique) VALUES (?,?,?,?)",
                          (articles_json, total, service, logistique))
                conn.commit()

                txt = ""
                for item in st.session_state.cart:
                    txt += f"- {item['nom']} x {item['qte']}%0A"

                msg = f"Nouvelle commande:%0A{txt}%0ATotal: {int(total)} F%0AMode: {service}%0AInfos: {logistique}"
                msg = urllib.parse.quote(msg)

                num = "221XXXXXXXXX"
                st.session_state.wa_link = f"https://wa.me/{num}?text={msg}"

                st.session_state.cart = []
                st.session_state.cmd_faite = True
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.cmd_faite:
        st.success("Commande prête !")
        st.balloons()
        st.markdown(f"""
        <a href="{st.session_state.wa_link}" target="_blank">
        <div style="background:#25D366;color:white;padding:20px;text-align:center;border-radius:15px;">
        📲 Envoyer sur WhatsApp
        </div></a>
        """, unsafe_allow_html=True)

# --- 7. ESPACE GÉRANT ---
elif choice == "📊 Espace Gérant":
    st.title("🛡️ Administration")

    t1, t2 = st.tabs(["📋 Commandes", "🥘 Carte"])

    with t1:
        cmds = pd.read_sql("SELECT * FROM commandes ORDER BY date DESC", conn)
        for _, r in cmds.iterrows():
            with st.expander(f"Commande #{r['id']} - {int(r['total'])} F"):
                st.write("Infos :", r["detail_logistique"])
                st.write("Articles :", r["articles"])
                if st.button("✔️ Terminer", key=f"done_{r['id']}"):
                    c.execute("DELETE FROM commandes WHERE id=?", (r["id"],))
                    conn.commit()
                    st.rerun()

    with t2:
        with st.form("ajout"):
            st.subheader("Ajouter un plat")
            n = st.text_input("Nom")
            p = st.number_input("Prix", 0)
            i = st.text_input("Image URL")
            d = st.text_area("Description")
            if st.form_submit_button("Ajouter"):
                c.execute("INSERT INTO menu (nom, prix, desc, img) VALUES (?,?,?,?)", (n,p,d,i))
                conn.commit()
                st.success("Ajouté")
                st.rerun()

        plats = pd.read_sql("SELECT * FROM menu", conn)
        for _, r in plats.iterrows():
            col1, col2 = st.columns([4,1])
            col1.write(f"{r['nom']} - {int(r['prix'])} F")
            if col2.button("Supprimer", key=f"del_{r['id']}"):
                c.execute("DELETE FROM menu WHERE id=?", (r["id"],))
                conn.commit()
                st.rerun()
