import streamlit as st
import sqlite3
import pandas as pd
import urllib.parse

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Menu Express Mboro", page_icon="🥘", layout="wide", initial_sidebar_state="collapsed")

# 🔴 CONFIGURATION PERSONNELLE
NUMERO_WHATSAPP = "221778615900"
# Format international pour Wave (ex: 221778615900)
NUMERO_MARCHAND_WAVE = "221778615900" 

try:
    ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]
except:
    ADMIN_PASSWORD = "admin"

# --- 2. STYLE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0c0c0c; color: white; }
    .pay-button-wave {
        display: block; width: 100%; background-color: #0096ff; color: white !important;
        text-align: center; padding: 20px; border-radius: 15px; font-weight: bold;
        font-size: 1.2rem; text-decoration: none; margin: 15px 0; border: none;
    }
    .pay-button-om {
        display: block; width: 100%; background-color: #ff6600; color: white !important;
        text-align: center; padding: 20px; border-radius: 15px; font-weight: bold;
        font-size: 1.2rem; text-decoration: none; margin: 15px 0;
    }
    .btn-whatsapp { 
        display: block; width: 100%; background-color: #25D366; color: white !important; 
        text-align: center; padding: 15px; border-radius: 12px; font-weight: bold; text-decoration: none; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIQUE PANIER ---
if 'cart' not in st.session_state:
    st.session_state.cart = {}

def add_to_cart(item_id, nom, prix):
    item_id = str(item_id)
    if item_id in st.session_state.cart:
        st.session_state.cart[item_id]['qty'] += 1
    else:
        st.session_state.cart[item_id] = {'nom': nom, 'prix': prix, 'qty': 1}
    st.toast(f"✅ {nom} ajouté !")

# --- 4. NAVIGATION ---
with st.sidebar:
    st.title("Menu Express")
    page = st.radio("Navigation", ["La Carte", f"Panier ({len(st.session_state.cart)})", "Admin"])

# --- PAGE: LA CARTE ---
if page == "La Carte":
    st.header("🍴 Notre Menu")
    # Simulation de menu pour l'exemple
    col1, col2 = st.columns([1, 2])
    with col1: st.image("https://images.unsplash.com/photo-1546069901-ba9599a7e63c", width=150)
    with col2:
        st.subheader("Plat du jour")
        st.write("3500 FCFA")
        st.button("Ajouter au panier", on_click=add_to_cart, args=(1, "Plat du jour", 3500))

# --- PAGE: PANIER & PAIEMENT PAR LIEN ---
elif "Panier" in page:
    st.header("🛒 Votre Panier")
    if not st.session_state.cart:
        st.info("Panier vide.")
    else:
        total = sum(v['prix'] * v['qty'] for v in st.session_state.cart.values())
        recap = "".join([f"- {v['nom']} x{v['qty']}\n" for v in st.session_state.cart.values()])
        
        st.write(f"### TOTAL : {int(total)} FCFA")
        
        pay_method = st.selectbox("💳 Choisissez votre mode de paiement", ["Wave", "Orange Money", "Espèces"])
        details = st.text_input("📍 Adresse de livraison")

        if pay_method == "Wave":
            # Génération du lien de paiement Wave
            # Note: Wave utilise souvent des liens personnalisés via leur API ou interface Business
            link_wave = f"https://wave.com/pay/{NUMERO_MARCHAND_WAVE}" # Lien direct marchand
            
            st.markdown(f"""
                <div style="background:#f0f9ff; padding:20px; border-radius:15px; color:#333; text-align:center;">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/d/d0/Wave_Logo.png" width="80"><br>
                    <p>Cliquez sur le bouton ci-dessous pour payer <b>{int(total)} F</b></p>
                    <a href="{link_wave}" target="_blank" class="pay-button-wave">📱 PAYER AVEC WAVE</a>
                    <p style="font-size:0.8rem; color:#666;">Une fois payé, revenez ici pour confirmer.</p>
                </div>
            """, unsafe_allow_html=True)

        elif pay_method == "Orange Money":
            st.markdown(f"""
                <div style="background:#fff5ee; padding:20px; border-radius:15px; color:#333; text-align:center;">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/c/c8/Orange_logo.svg" width="50"><br>
                    <p>Composez le <b>#144#39#...#</b> ou payez via l'application Orange Money</p>
                    <a href="tel:#144#39#" class="pay-button-om">📱 PAYER AVEC OM</a>
                </div>
            """, unsafe_allow_html=True)

        st.divider()
        if st.button("✅ J'AI PAYÉ, ENVOYER MA COMMANDE", use_container_width=True):
            if not details:
                st.error("Veuillez entrer une adresse.")
            else:
                msg = f"🥘 *NOUVELLE COMMANDE*\n{recap}\n💰 TOTAL: {int(total)} F\n💳 PAIEMENT: {pay_method}\n📍 LIEU: {details}"
                link_wa = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(msg)}"
                st.markdown(f'<a href="{link_wa}" target="_blank" class="btn-whatsapp">📲 CONFIRMER SUR WHATSAPP</a>', unsafe_allow_html=True)
