import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# --- CONFIGURATION ---
st.set_page_config(page_title="Teranga Gourmet", page_icon="🥘", layout="wide")

# Initialisation des données (Simule le localStorage)
if 'menu' not in st.session_state:
    st.session_state.menu = [
        {"id": "1", "name": "Thieboudienne", "price": 5500, "category": "Plat", "description": "Riz rouge au mérou bronzé et légumes tropicaux.", "image": "https://images.unsplash.com/photo-1556910103-1c02745aae4d?q=80&w=800"},
        {"id": "2", "name": "Pastels Thon", "price": 2500, "category": "Entrée", "description": "6 beignets croustillants sauce tomate pimentée.", "image": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=800"},
        {"id": "3", "name": "Bissap Royal", "price": 1500, "category": "Boisson", "description": "Infusion d'hibiscus rouge, menthe fraîche et vanille.", "image": "https://images.unsplash.com/photo-1544145945-f904253d0c7b?q=80&w=800"},
    ]
if 'cart' not in st.session_state: st.session_state.cart = {}
if 'orders' not in st.session_state: st.session_state.orders = []
if 'view' not in st.session_state: st.session_state.view = 'home'

WHATSAPP_NUMBER = "221770000000"
ADMIN_PASS = "1234"

# --- DESIGN CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #09090b; color: #f4f4f5; }}
    [data-testid="stHeader"] {{ background: rgba(0,0,0,0); }}
    
    /* Boutons de Navigation */
    .nav-container {{
        display: flex; justify-content: center; gap: 10px; padding: 10px;
        background: rgba(24, 24, 27, 0.9); border-bottom: 1px solid rgba(245, 158, 11, 0.2);
        position: sticky; top: 0; z-index: 99; backdrop-filter: blur(10px);
    }}
    
    /* Cartes Menu */
    .menu-card {{
        background: #18181b; border: 1px solid #27272a; border-radius: 20px;
        padding: 0px; overflow: hidden; transition: 0.3s; margin-bottom: 20px;
    }}
    .menu-card:hover {{ border-color: #f59e0b; transform: translateY(-5px); }}
    
    /* Typographie */
    .gold-text {{ color: #f59e0b !important; font-family: 'Serif'; }}
    .price-tag {{ background: #f59e0b; color: black; padding: 5px 12px; border-radius: 50px; font-weight: 900; }}
    </style>
""", unsafe_allow_html=True)

# --- NAVIGATION CUSTOM ---
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
with c1: 
    if st.button("🏠 Accueil", use_container_width=True): st.session_state.view = 'home'
with c2: 
    if st.button("📖 Menu", use_container_width=True): st.session_state.view = 'menu'
with c3: 
    if st.button("📅 Réserver", use_container_width=True): st.session_state.view = 'reserve'
with c4: 
    count = sum(st.session_state.cart.values())
    label = f"🛒 Panier ({count})" if count > 0 else "🛒 Panier"
    if st.button(label, use_container_width=True): st.session_state.view = 'cart'
with c5: 
    if st.button("⚙️ Admin", use_container_width=True): st.session_state.view = 'admin'
st.markdown('</div>', unsafe_allow_html=True)

# --- VUE : ACCUEIL ---
if st.session_state.view == 'home':
    st.markdown("""
        <div style="text-align: center; padding: 50px 0;">
            <h1 class="gold-text" style="font-size: 4rem;">Teranga Gourmet</h1>
            <p style="font-size: 1.2rem; opacity: 0.8;">L'excellence de la cuisine Sénégalaise à votre portée.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image("https://images.unsplash.com/photo-1556910103-1c02745aae4d?q=80&w=800", use_container_width=True)
    with col2:
        st.markdown("<h3 class='gold-text'>👨‍🍳 Le Conseil du Chef</h3>", unsafe_allow_html=True)
        query = st.text_input("Posez une question sur nos plats...")
        if query:
            st.info("Le Chef vous recommande le Thieboudienne aujourd'hui : le riz est particulièrement parfumé !")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Voir la carte maintenant", type="primary"):
            st.session_state.view = 'menu'
            st.rerun()

# --- VUE : MENU ---
elif st.session_state.view == 'menu':
    st.markdown("<h1 class='gold-text'>La Carte</h1>", unsafe_allow_html=True)
    
    categories = ["Tous", "Entrée", "Plat", "Dessert", "Boisson"]
    cat = st.pills("Catégories", categories, default="Tous")
    
    items = st.session_state.menu if cat == "Tous" else [i for i in st.session_state.menu if i['category'] == cat]
    
    cols = st.columns(3)
    for idx, item in enumerate(items):
        with cols[idx % 3]:
            st.markdown(f"""
                <div class="menu-card">
                    <img src="{item['image']}" style="width:100%; height:200px; object-fit:cover;">
                    <div style="padding: 20px;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <h4 style="margin:0;">{item['name']}</h4>
                            <span class="price-tag">{item['price']} F</span>
                        </div>
                        <p style="font-size:0.8rem; color:#71717a; margin:15px 0;">{item['description']}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Ajouter au panier", key=f"btn_{item['id']}", use_container_width=True):
                st.session_state.cart[item['id']] = st.session_state.cart.get(item['id'], 0) + 1
                st.toast(f"Ajouté : {item['name']}")

# --- VUE : PANIER ---
elif st.session_state.view == 'cart':
    st.markdown("<h1 class='gold-text'>Votre Sélection</h1>", unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.write("Votre panier est vide.")
    else:
        total = 0
        summary = []
        for item_id, qty in list(st.session_state.cart.items()):
            item = next(i for i in st.session_state.menu if i['id'] == item_id)
            total += item['price'] * qty
            summary.append(f"- {item['name']} (x{qty})")
            
            with st.container(border=True):
                ca, cb, cc = st.columns([3, 1, 1])
                ca.write(f"**{item['name']}**")
                cb.write(f"{item['price'] * qty} F")
                if cc.button("Enlever", key=f"rem_{item_id}"):
                    del st.session_state.cart[item_id]
                    st.rerun()
        
        st.markdown(f"### Total : {total} FCFA")
        
        with st.form("checkout"):
            service = st.selectbox("Mode", ["Sur place", "Livraison"])
            infos = st.text_area("Table n° ou Adresse précise")
            if st.form_submit_button("Commander via WhatsApp 🚀", use_container_width=True):
                msg = f"COMMANDE TERANGA\n" + "\n".join(summary) + f"\nTotal: {total}F\nMode: {service}\nInfos: {infos}"
                url = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(msg)}"
                st.markdown(f'<meta http-equiv="refresh" content="0;URL={url}">', unsafe_allow_html=True)

# --- VUE : ADMIN ---
elif st.session_state.view == 'admin':
    pwd = st.text_input("Code Admin", type="password")
    if pwd == ADMIN_PASS:
        st.success("Mode Gestionnaire")
        
        tab1, tab2 = st.tabs(["Gérer le Menu", "Commandes"])
        
        with tab1:
            df = pd.DataFrame(st.session_state.menu)
            edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
            if st.button("Sauvegarder les modifications"):
                st.session_state.menu = edited_df.to_dict('records')
                st.success("Menu mis à jour !")
    elif pwd:
        st.error("Accès refusé.")
