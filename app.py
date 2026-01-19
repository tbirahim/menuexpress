import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Teranga Gourmet",
    page_icon="🍲",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CONSTANTES & ETAT (SESSION STATE) ---
WHATSAPP_NUMBER = "221XXXXXXXXX"  # Remplace par ton numéro
CALL_NUMBER = "+221 XX XXX XX XX"
ADMIN_PASS = "1234"

# Menu Initial
INITIAL_MENU = [
    {"id": "1", "name": "Thieboudienne Penda Mbaye", "price": 5500, "category": "Plat", "description": "Le riz au poisson légendaire du Sénégal, servi avec ses légumes fondants.", "image": "https://www.luxe-infinity-afrique.com/wp-content/uploads/2025/08/La-Cuisine-Africaine-Conquiert-la-France-1200x675.webp"},
    {"id": "2", "name": "Yassa au Poulet", "price": 4500, "category": "Plat", "description": "Poulet mariné au citron et oignons caramélisés.", "image": "https://images.unsplash.com/photo-1556910103-1c02745aae4d?q=80&w=800"},
    {"id": "3", "name": "Pastels (x6)", "price": 2500, "category": "Entrée", "description": "Petits chaussons frits au poisson avec sauce tomate épicée.", "image": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=800"}
]

# Initialisation des variables de session
if 'menu' not in st.session_state:
    st.session_state.menu = INITIAL_MENU
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'view' not in st.session_state:
    st.session_state.view = 'Accueil'

# --- STYLE CSS (Custom Design) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;700;900&display=swap');
    
    .main {{ background-color: #09090b; color: #f4f4f5; }}
    h1, h2, h3 {{ font-family: 'Playfair Display', serif !important; color: #f59e0b !important; }}
    .stButton>button {{
        border-radius: 12px;
        background-color: #18181b;
        color: #f59e0b;
        border: 1px solid #f59e0b33;
        font-weight: bold;
        transition: all 0.3s;
        width: 100%;
    }}
    .stButton>button:hover {{
        background-color: #f59e0b;
        color: black;
        border-color: #f59e0b;
    }}
    .card {{
        background: #18181b;
        padding: 20px;
        border-radius: 25px;
        border: 1px solid #ffffff1a;
        margin-bottom: 20px;
    }}
    .badge {{
        background: #f59e0b;
        color: black;
        padding: 2px 8px;
        border-radius: 10px;
        font-weight: 900;
        font-size: 12px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- NAVIGATION ---
cols = st.columns([2, 1, 1, 1, 1, 1])
with cols[0]:
    st.markdown("<h2 style='margin:0;'>Teranga Express</h2>", unsafe_allow_html=True)

# Calcul du nombre d'articles dans le panier
cart_count = sum(st.session_state.cart.values())

with cols[1]: 
    if st.button("🏠 Accueil"): st.session_state.view = 'Accueil'
with cols[2]: 
    if st.button("📖 La Carte"): st.session_state.view = 'Menu'
with cols[3]: 
    if st.button("📅 Réserver"): st.session_state.view = 'Reserver'
with cols[4]: 
    label = f"🛒 Panier ({cart_count})" if cart_count > 0 else "🛒 Panier"
    if st.button(label): st.session_state.view = 'Panier'
with cols[5]: 
    if st.button("⚙️ Admin"): st.session_state.view = 'Admin'

st.divider()

# --- LOGIQUE DES VUES ---

# 1. ACCUEIL
if st.session_state.view == 'Accueil':
    st.markdown(f"""
        <div style="position: relative; border-radius: 30px; overflow: hidden; height: 400px; background: url('https://www.luxe-infinity-afrique.com/wp-content/uploads/2025/08/La-Cuisine-Africaine-Conquiert-la-France-1200x675.webp') center; background-size: cover;">
            <div style="position: absolute; inset: 0; background: linear-gradient(to top, #09090b, transparent); display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 20px;">
                <p style="text-transform: uppercase; letter-spacing: 3px; font-weight: 900; color: #f59e0b; font-size: 12px;">Teranga Express - Dakar</p>
                <h1 style="font-size: 4rem; margin-bottom: 10px;">Teranga Gourmet</h1>
                <p style="font-size: 1.5rem; font-style: italic; color: #d4d4d8;">Une invitation au voyage culinaire entre tradition et excellence.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("👨‍🍳 Le Chef Virtuel")
        prompt = st.text_input("Posez une question au chef (ex: Qu'est-ce qui est frais aujourd'hui ?)")
        if prompt:
            st.info(f"Chef: Le {st.session_state.menu[0]['name']} est particulièrement réussi aujourd'hui, avec des arrivages frais du matin !")
    
    with col_b:
        st.markdown("<br>", unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1556910103-1c02745aae4d?q=80&w=800", caption="Notre Cuisine Authentique")

# 2. MENU
elif st.session_state.view == 'Menu':
    st.title("La Carte Gourmet")
    
    categories = ["Tous", "Entrée", "Plat", "Dessert", "Boisson"]
    cat_sel = st.segmented_control("Filtrer par catégorie", categories, default="Tous")
    
    items = st.session_state.menu if cat_sel == "Tous" else [i for i in st.session_state.menu if i['category'] == cat_sel]
    
    cols = st.columns(3)
    for idx, item in enumerate(items):
        with cols[idx % 3]:
            st.markdown(f"""
                <div class="card">
                    <img src="{item['image']}" style="width:100%; height:200px; object-fit:cover; border-radius:15px;">
                    <div style="display:flex; justify-content:between; align-items:center; margin-top:15px;">
                        <h4 style="margin:0; color:#f59e0b;">{item['name']}</h4>
                        <span class="badge">{item['price']} F</span>
                    </div>
                    <p style="font-size:0.8rem; color:#a1a1aa; margin-top:10px;">{item['description']}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Ajouter au panier", key=f"add_{item['id']}"):
                st.session_state.cart[item['id']] = st.session_state.cart.get(item['id'], 0) + 1
                st.toast(f"✅ {item['name']} ajouté !")

# 3. RÉSERVER
elif st.session_state.view == 'Reserver':
    st.title("Réservation Privée")
    with st.form("reserve_form"):
        nom = st.text_input("Nom complet")
        pers = st.number_input("Nombre de personnes", min_value=1, value=2)
        date = st.date_input("Date choisie")
        heure = st.time_input("Heure prévue")
        
        if st.form_submit_button("Confirmer via WhatsApp"):
            msg = f"RESERVATION TABLE\nNom: {nom}\nDate: {date}\nHeure: {heure}\nCouverts: {pers}"
            url = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(msg)}"
            st.markdown(f'<a href="{url}" target="_blank">Ouvrir WhatsApp pour finaliser</a>', unsafe_allow_html=True)

# 4. PANIER
elif st.session_state.view == 'Panier':
    st.title("Votre Panier")
    if not st.session_state.cart:
        st.warning("Votre panier est vide.")
    else:
        total = 0
        items_list = []
        for item_id, qty in list(st.session_state.cart.items()):
            item = next(i for i in st.session_state.menu if i['id'] == item_id)
            subtotal = item['price'] * qty
            total += subtotal
            items_list.append(f"- {item['name']} (x{qty})")
            
            c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
            c1.markdown(f"**{item['name']}**")
            c2.write(f"{item['price']} F")
            c3.write(f"Qté: {qty}")
            if c4.button("🗑️", key=f"del_{item_id}"):
                del st.session_state.cart[item_id]
                st.rerun()
        
        st.divider()
        st.subheader(f"Total: {total} FCFA")
        
        with st.expander("Détails de la commande"):
            mode = st.selectbox("Mode de service", ["Sur place", "Livraison"])
            details = st.text_area("Numéro de table ou adresse de livraison")
            
            if st.button("Commander sur WhatsApp 🚀"):
                order_msg = f"NOUVELLE COMMANDE\n\n" + "\n".join(items_list) + f"\n\nTotal: {total} F\nMode: {mode}\nInfos: {details}"
                st.session_state.orders.append({"id": datetime.now().timestamp(), "items": items_list, "total": total})
                url = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(order_msg)}"
                st.markdown(f'<a href="{url}" target="_blank">Cliquez ici pour envoyer la commande</a>', unsafe_allow_html=True)

# 5. ADMIN
elif st.session_state.view == 'Admin':
    st.title("Pilotage Gérant")
    code = st.text_input("Code Secret", type="password")
    if code == ADMIN_PASS:
        st.success("Accès autorisé")
        st.subheader("Historique des Commandes")
        if st.session_state.orders:
            st.table(pd.DataFrame(st.session_state.orders))
        else:
            st.write("Aucune commande enregistrée.")
    elif code:
        st.error("Code incorrect")

# --- FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"""
    <div style="text-align:center; color:#52525b; font-size:0.7rem;">
        © 2026 Teranga Gourmet - Excellence Culinaire | Contact: {CALL_NUMBER}
    </div>
""", unsafe_allow_html=True)
