import streamlit as st
import sqlite3
import pandas as pd
import urllib.parse

# --- 1. CONFIGURATION & SÉCURITÉ ---
st.set_page_config(page_title="Menu Express PRO", page_icon="🥘", layout="wide")

# Récupération sécurisée du mot de passe
ADMIN_PASSWORD = st.secrets.get("PASSWORD", "admin123")

# --- 2. DESIGN PERSONNALISÉ (CSS PRO) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    
    * {{ font-family: 'Montserrat', sans-serif; }}

    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                    url("https://images.unsplash.com/photo-1504674900247-0877df9cc836?q=80&w=2070");
        background-size: cover; background-attachment: fixed;
    }}
    
    .plat-card {{
        padding: 20px; border-radius: 20px; background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 20px;
        transition: transform 0.3s ease; display: flex; align-items: center;
    }}
    .plat-card:hover {{
        transform: scale(1.01); border-color: #25D366;
    }}
    
    .prix {{ color: #25D366; font-size: 1.5rem; font-weight: bold; margin-left: auto; }}
    
    .cart-section {{
        background-color: rgba(0, 0, 0, 0.9); padding: 25px; border-radius: 20px;
        border: 2px solid #25D366; margin-top: 30px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DONNÉES ---
def init_db():
    conn = sqlite3.connect('menu_pro.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS menu (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prix REAL, desc TEXT, img TEXT)')
    c.execute('''CREATE TABLE IF NOT EXISTS commandes 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, articles TEXT, total REAL, 
                  type_commande TEXT, detail_logistique TEXT, date DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    return conn

conn = init_db()
c = conn.cursor()

# --- 4. GESTION DE SESSION ---
if 'admin_ok' not in st.session_state: st.session_state.admin_ok = False
if 'cart' not in st.session_state: st.session_state.cart = []
if 'cmd_faite' not in st.session_state: st.session_state.cmd_faite = False
if 'wa_link' not in st.session_state: st.session_state.wa_link = ""

# --- 5. NAVIGATION ---
with st.sidebar:
    st.title("⚜️ Menu Express")
    choice = st.radio("Aller vers", ["🍽️ Commander", "📊 Espace Gérant"] if st.session_state.admin_ok else ["🍽️ Commander"])
    
    st.write("---")
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

# --- 6. PAGE CLIENT : COMMANDER ---
if choice == "🍽️ Commander":
    st.title("👨‍🍳 Notre Carte Gourmande")
    
    df = pd.read_sql('SELECT * FROM menu', conn)
    if df.empty:
        st.info("Le menu est en cours de préparation...")
    else:
        for _, row in df.iterrows():
            img = row['img'] if row['img'] else "https://via.placeholder.com/150"
            st.markdown(f'''
                <div class="plat-card">
                    <img src="{img}" style="width:100px; height:100px; border-radius:12px; object-fit:cover; margin-right:20px;">
                    <div>
                        <h3>{row['nom']}</h3>
                        <p style="color:#ccc; font-size:0.9rem;">{row['desc']}</p>
                    </div>
                    <span class="prix">{int(row['prix'])} F</span>
                </div>
            ''', unsafe_allow_html=True)
            if st.button(f"Ajouter au panier", key=f"add_{row['id']}"):
                st.session_state.cart.append({"nom": row['nom'], "prix": row['prix']})
                st.toast(f"✅ {row['nom']} ajouté !")

    st.divider()

    # AFFICHAGE DU PANIER
    if st.session_state.cmd_faite:
        st.balloons() # <--- LES BALLONS ICI !
        st.success("🎉 Félicitations ! Votre commande est prête à être envoyée.")
        st.markdown(f"""
            <a href="{st.session_state.wa_link}" target="_blank" style="text-decoration:none;">
                <div style="background-color:#25D366; color:white; padding:20px; text-align:center; border-radius:15px; font-weight:bold; font-size:1.3rem; border: 2px solid white; box-shadow: 0px 4px 15px rgba(0,0,0,0.3);">
                    📲 CLIQUEZ ICI POUR ENVOYER SUR WHATSAPP
                </div>
            </a>
        """, unsafe_allow_html=True)
        if st.button("🔄 Commander autre chose"):
            st.session_state.cmd_faite = False
            st.rerun()

    elif st.session_state.cart:
        st.markdown('<div class="cart-section">', unsafe_allow_html=True)
        st.header("🛒 Récapitulatif de ma commande")
        total = sum(item['prix'] for item in st.session_state.cart)
        txt_items = ""
        for item in st.session_state.cart:
            st.write(f"• {item['nom']} ({int(item['prix'])} F)")
            txt_items += f"- {item['nom']}%0A"
        
        st.subheader(f"Total : {int(total)} FCFA")
        
        service = st.radio("Comment souhaitez-vous être servi ?", ["Sur place", "Livraison"], horizontal=True)
        
        if service == "Sur place":
            logistique = st.text_input("Numéro de Table", placeholder="Ex: Table 5")
        else:
            col1, col2 = st.columns(2)
            tel = col1.text_input("Votre Téléphone", placeholder="Ex: 77 000 00 00")
            adr = col2.text_input("Votre Adresse", placeholder="Ex: Quartier Médina")
            logistique = f"📞 {tel} | 📍 {adr}"
        
        if st.button("🚀 VALIDER MA COMMANDE"):
            if not logistique or (service == "Livraison" and (not tel or not adr)):
                st.warning("⚠️ Veuillez remplir les informations demandées.")
            else:
                # Sauvegarde en base
                c.execute('INSERT INTO commandes (articles, total, type_commande, detail_logistique) VALUES (?,?,?,?)',
                          (str(st.session_state.cart), total, service, logistique))
                conn.commit()
                
                # Lien WhatsApp
                num = "221775187725" # <--- TON NUMÉRO ICI
                msg = f"Bonjour ! Nouvelle commande :%0A{txt_items}%0A*Total:* {int(total)} F%0A*Mode:* {service}%0A*Infos:* {logistique}"
                st.session_state.wa_link = f"https://wa.me/{num}?text={msg}"
                
                # Reset
                st.session_state.cart = []
                st.session_state.cmd_faite = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- 7. PAGE GÉRANT : SUIVI ET MODIF ---
elif choice == "📊 Espace Gérant":
    st.title("🛡️ Administration")
    t1, t2 = st.tabs(["📋 Commandes Reçues", "🥘 Gérer la Carte"])
    
    with t1:
        from streamlit_autorefresh import st_autorefresh
        st_autorefresh(interval=30000, key="auto_refresh")
        
        cmds = pd.read_sql('SELECT * FROM commandes ORDER BY date DESC', conn)
        for _, r in cmds.iterrows():
            with st.expander(f"Commande #{r['id']} - {r['total']} F"):
                st.error(f"Détails : {r['detail_logistique']}")
                st.write(f"Articles : {r['articles']}")
                if st.button("✔️ Terminer", key=f"f_{r['id']}"):
                    c.execute('DELETE FROM commandes WHERE id=?', (r['id'],))
                    conn.commit()
                    st.rerun()
                    
    with t2:
        with st.form("nouveau_plat"):
            st.subheader("Ajouter un plat")
            n = st.text_input("Nom du plat")
            p = st.number_input("Prix (FCFA)", min_value=0)
            i = st.text_input("Lien de l'image (URL)")
            d = st.text_area("Description")
            if st.form_submit_button("Ajouter à la carte"):
                c.execute('INSERT INTO menu (nom, prix, desc, img) VALUES (?,?,?,?)', (n,p,d,i))
                conn.commit()
                st.success("Plat ajouté !")
                st.rerun()
        
        st.write("---")
        plats = pd.read_sql('SELECT * FROM menu', conn)
        for _, r in plats.iterrows():
            col1, col2 = st.columns([4, 1])
            col1.write(f"**{r['nom']}** - {int(r['prix'])} F")
            if col2.button("Supprimer", key=f"del_{r['id']}"):
                c.execute('DELETE FROM menu WHERE id=?', (r['id'],))
                conn.commit()
                st.rerun()
