import streamlit as st
import pandas as pd
import sqlite3
import json
import re
import urllib.parse
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Système de Commande", page_icon="🍴", layout="centered")

# --- STYLE CSS POUR LE DESIGN ---
st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
    }
    .stCheckbox {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 5px;
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
            client_nom TEXT,
            telephone TEXT,
            articles_json TEXT,
            total_prix REAL,
            date_commande TEXT
        )
    ''')
    conn.commit()
    return conn

# --- LOGIQUE MÉTIER ---
def valider_tel(numero):
    return bool(re.fullmatch(r'\d{9,}', numero))

# --- TITRE AVEC ICÔNE ---
st.markdown("# 🍴 Système de Commande")

# --- SECTION : VOIR MON PANIER ---
with st.expander("▼ Voir mon panier", expanded=True):
    # Simulation des articles cochés comme sur l'image
    col1, col2 = st.columns([0.1, 0.9])
    
    # Articles avec le style de l'image (Checkboxes vertes par défaut)
    st.checkbox("Thieboudienne - 2500 FCFA", value=True, key="item1")
    st.checkbox("Yassa Poulet - 2000 FCFA", value=True, key="item2")
    
    st.markdown("---")
    total = 4500 # Correspond à l'image
    st.markdown(f"**Total : {total} FCFA**")

# --- SECTION : FINALISER LA COMMANDE ---
st.markdown("### Finaliser la commande")

with st.container():
    nom_client = st.text_input("Votre Nom", placeholder="Entrez votre nom ici")
    tel_client = st.text_input("Numéro de téléphone (9 chiffres min)", placeholder="999999999")
    
    # Bouton d'enregistrement
    if st.button("Enregistrer la commande", use_container_width=True):
        if not nom_client or not tel_client:
            st.error("⚠️ Veuillez remplir tous les champs.")
        elif not valider_tel(tel_client):
            st.error("❌ Numéro de téléphone invalide.")
        else:
            # Sauvegarde SQL
            conn = init_db()
            cursor = conn.cursor()
            panier_exemple = [{"nom": "Thieboudienne", "prix": 2500}, {"nom": "Yassa Poulet", "prix": 2000}]
            
            cursor.execute('''
                INSERT INTO commandes (client_nom, telephone, articles_json, total_prix, date_commande)
                VALUES (?, ?, ?, ?, ?)
            ''', (nom_client, tel_client, json.dumps(panier_exemple), total, datetime.now().strftime("%d/%m/%Y %H:%M")))
            conn.commit()
            conn.close()
            
            st.success("✅ Commande enregistrée avec succès !")
            
            # WhatsApp Link
            msg = f"Commande de {nom_client} ({tel_client}): 4500 FCFA"
            link = f"https://wa.me/22177XXXXXXX?text={urllib.parse.quote(msg)}"
            st.link_button("📲 Envoyer sur WhatsApp", link, use_container_width=True)

# --- PIED DE PAGE ---
st.markdown("<br><br>", unsafe_allow_html=True)
if st.button("🔍 Gérer l'application", type="secondary"):
    st.info("Section administration bientôt disponible.")
