import streamlit as st
import sqlite3
import pandas as pd
import urllib.parse
import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Teranga Gourmet", page_icon="🥘", layout="wide", initial_sidebar_state="collapsed")

# 🔴 CONFIGURATION PERSONNELLE
NUMERO_WHATSAPP = "221778615900"
NUMERO_PAYEMENT = "77 861 59 00" # Le numéro qui reçoit l'argent
NUMERO_APPEL = "778615900"

try:
    ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]
except:
    ADMIN_PASSWORD = "admin123"

# --- 2. STYLE CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@400;700&display=swap');
    .stApp { background-color: #0c0c0c; color: #f0f0f0; font-family: 'Lato', sans-serif; }
    h1, h2, h3 { font-family: 'Playfair Display', serif; color: #d4af37; text-align: center; }
    .plat-card { background:#1a1a1a; border-radius:15px; overflow:hidden; margin-bottom:20px; border: 1px solid #333; }
    .plat-img { width: 100%; height: 200px; object-fit: cover; }
    .btn-whatsapp { display: block; width: 100%; background-color: #25D366; color: white !important; text-align: center; padding: 15px; border-radius: 12px; font-weight: bold; text-decoration: none; margin-top: 10px; }
    .payment-box { background: #d4af3722; border: 1px dashed #d4af37; padding: 15px; border-radius: 10px; text-align: center; margin: 10px 0; }
    [data-testid="stSidebar"] { background-color: #1a1a1a; border-right: 1px solid #d4af37; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE ---
def get_connection():
    return sqlite3.connect('teranga_resto.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS menu (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prix REAL, img TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS commandes (id INTEGER PRIMARY KEY AUTOINCREMENT, articles TEXT, total REAL, paiement TEXT, detail TEXT, date DATETIME DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
init_db()

# --- 4. PANIER ---
if 'cart' not in st.session_state: st.session_state.cart = []

def add_to_cart(item):
    for p in st.session_state.cart:
        if p['id'] == item['id']:
            p['qty'] += 1
            st.toast("➕ Quantité mise à jour")
            return
    item['qty'] = 1
    st.session_state.cart.append(item)
    st.toast("✅ Ajouté au panier")

# --- 5. NAVIGATION ---
with st.sidebar:
    st.title("Teranga Gourmet")
    page = st.radio("Aller vers", ["Accueil", "La Carte", "Réserver", f"Mon Panier ({len(st.session_state.cart)})", "Admin"])

# --- PAGE: ACCUEIL ---
if page == "Accueil":
    st.image("https://images.unsplash.com/photo-1599481238640-4c1288750d7a?q=80&w=2070")
    st.markdown("<h1>La Gastronomie Sénégalaise</h1>", unsafe_allow_html=True)

# --- PAGE: LA CARTE ---
elif page == "La Carte":
    st.header("Le Menu")
    df = pd.read_sql('SELECT * FROM menu', get_connection())
    for _, row in df.iterrows():
        st.markdown(f'<div class="plat-card"><img src="{row["img"]}" class="plat-img"><div style="padding:15px;"><h3>{row["nom"]}</h3><p style="color:#d4af37; font-weight:bold;">{int(row["prix"])} FCFA</p></div></div>', unsafe_allow_html=True)
        if st.button(f"Commander {row['nom']}", key=f"btn_{row['id']}", use_container_width=True):
            add_to_cart({"id": row['id'], "nom": row['nom'], "prix": row['prix']})

# --- PAGE: PANIER & PAIEMENT ---
elif "Panier" in page:
    st.header("Finaliser ma commande")
    if not st.session_state.cart:
        st.info("Votre panier est vide.")
    else:
        total = 0
        summary = ""
        for i, item in enumerate(st.session_state.cart):
            sub = item['prix'] * item['qty']
            total += sub
            summary += f"- {item['nom']} (x{item['qty']})\n"
            st.write(f"**{item['nom']}** x{item['qty']} : {int(sub)} F")
        
        st.divider()
        st.write(f"### Total à payer : {int(total)} FCFA")

        # LOGISTIQUE
        mode = st.radio("Réception", ["Livraison", "Sur place"], horizontal=True)
        details = st.text_input("Adresse de livraison ou N° Table")

        # PAIEMENT
        st.write("### 💳 Mode de Paiement")
        pay_method = st.selectbox("Choisir votre moyen de paiement", ["Wave", "Orange Money", "Espèces à la livraison"])

        if pay_method == "Wave":
            st.markdown(f"""<div class="payment-box">🔵 <b>Paiement par WAVE</b><br>Veuillez transférer <b>{int(total)} F</b> au :<br><h2 style="color:#d4af37;">{NUMERO_PAYEMENT}</h2></div>""", unsafe_allow_html=True)
        elif pay_method == "Orange Money":
            st.markdown(f"""<div class="payment-box">🟠 <b>Paiement par ORANGE MONEY</b><br>Veuillez transférer <b>{int(total)} F</b> au :<br><h2 style="color:#d4af37;">{NUMERO_PAYEMENT}</h2></div>""", unsafe_allow_html=True)

        if st.button("🚀 VALIDER ET ENVOYER", use_container_width=True):
            if not details:
                st.error("Veuillez préciser votre adresse ou table.")
            else:
                # Enregistrement DB
                conn = get_connection()
                conn.cursor().execute('INSERT INTO commandes (articles, total, paiement, detail) VALUES (?,?,?,?)', (summary, total, pay_method, details))
                conn.commit()

                # Message WhatsApp avec infos de paiement
                msg = f"🥘 *NOUVELLE COMMANDE*\n\n{summary}\n💰 *TOTAL:* {int(total)} FCFA\n💳 *PAIEMENT:* {pay_method}\n📍 *LIVRAISON:* {details}\n\n_Veuillez vérifier la réception du transfert avant de valider._"
                link = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg)}"
                st.markdown(f'<a href="{link}" target="_blank" class="btn-whatsapp">✅ ENVOYER SUR WHATSAPP</a>', unsafe_allow_html=True)

# --- PAGE: ADMIN ---
elif page == "Admin":
    st.header("Gérant")
    if st.text_input("Code", type="password") == ADMIN_PASSWORD:
        t1, t2 = st.tabs(["Ajouter Plat", "Historique"])
        with t1:
            with st.form("add"):
                n = st.text_input("Nom"); p = st.number_input("Prix", step=500); i = st.text_input("Lien Image")
                if st.form_submit_button("Ajouter"):
                    get_connection().cursor().execute('INSERT INTO menu (nom, prix, img) VALUES (?,?,?)', (n,p,i)).connection.commit(); st.rerun()
        with t2:
            st.dataframe(pd.read_sql('SELECT * FROM commandes ORDER BY id DESC', get_connection()))
