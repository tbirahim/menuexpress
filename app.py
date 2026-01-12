import streamlit as st
import pandas as pd
import sqlite3
import json
import re
import urllib.parse
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Système de Commande", page_icon="🍴")

# --- STYLE PERSONNALISÉ (CSS) ---
st.markdown("""
    <style>
    /* Style pour les cartes de menu */
    .menu-card {
        background-color: #1e1e1e;
        color: #f1c40f;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #f1c40f;
        margin-bottom: 10px;
        text-align: center;
    }
    /* Style pour le titre principal */
    .main-title {
        font-weight: bold;
        font-size: 42px;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALISATION BASE DE DONNÉES ---
def init_db():
    conn = sqlite3.connect('restau_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS commandes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_nom TEXT, telephone TEXT, articles_json TEXT,
            total_prix REAL, date_commande TEXT
        )
    ''')
    conn.commit()
    return conn

# --- GESTION DU PANIER ---
if 'panier' not in st.session_state:
    st.session_state.panier = []

def ajouter_au_panier(nom, prix):
    st.session_state.panier.append({"nom": nom, "prix": prix})
    st.toast(f"✅ **{nom}** ajouté !", icon="🛒")

# --- INTERFACE : MENU (Comme votre 3ème image) ---
st.markdown('<div class="main-title">🍴 Système de Commande</div>', unsafe_allow_html=True)

st.write("### Notre Menu")
col_m1, col_m2 = st.columns(2)

with col_m1:
    st.markdown('<div class="menu-card">🍱<br><b>Thieboudienne</b><br>2500 FCFA</div>', unsafe_allow_html=True)
    if st.button("Ajouter au panier", key="btn1"):
        ajouter_au_panier("Thieboudienne", 2500)

with col_m2:
    st.markdown('<div class="menu-card">🍗<br><b>Yassa Poulet</b><br>2000 FCFA</div>', unsafe_allow_html=True)
    if st.button("Ajouter au panier", key="btn2"):
        ajouter_au_panier("Yassa Poulet", 2000)

# --- INTERFACE : RÉCAPITULATIF (Comme votre 2ème image) ---
st.write("")
with st.expander("▼ Voir mon panier", expanded=True):
    if not st.session_state.panier:
        st.write("Votre panier est vide.")
        total_commande = 0
    else:
        for i, item in enumerate(st.session_state.panier):
            # Simulation des checkbox vertes de la capture
            st.checkbox(f"{item['nom']} - {item['prix']} FCFA", value=True, key=f"check_{i}")
        
        total_commande = sum(item['prix'] for item in st.session_state.panier)
        st.markdown(f"### Total : {total_commande} FCFA")

# --- FORMULAIRE FINAL ---
st.write("### Finaliser la commande")
with st.container():
    nom = st.text_input("Votre Nom", placeholder="vb")
    tel = st.text_input("Numéro de téléphone (9 chiffres min)", placeholder="999999999")
    
    if st.button("Enregistrer la commande", use_container_width=True, type="primary"):
        if len(st.session_state.panier) == 0:
            st.warning("Votre panier est vide !")
        elif not nom or not re.fullmatch(r'\d{9,}', tel):
            st.error("Veuillez vérifier vos informations (Nom et Téléphone).")
        else:
            # Sauvegarde SQL
            conn = init_db()
            conn.execute("INSERT INTO commandes (client_nom, telephone, articles_json, total_prix, date_commande) VALUES (?,?,?,?,?)",
                         (nom, tel, json.dumps(st.session_state.panier), total_commande, datetime.now().strftime("%H:%M")))
            conn.commit()
            
            # WhatsApp
            msg = f"*Commande de {nom}*\nTotal: {total_commande} FCFA"
            wa_link = f"https://wa.me/22177XXXXXXX?text={urllib.parse.quote(msg)}"
            
            st.success("✅ Commande enregistrée !")
            st.link_button("📲 Envoyer sur WhatsApp", wa_link, use_container_width=True)

# Bouton de gestion discret en bas à droite
st.markdown("---")
st.button("🔍 Gérer l'application", type="secondary")

