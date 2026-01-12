import streamlit as st
import pandas as pd
import sqlite3
import json
import re
import urllib.parse
from datetime import datetime

# --- 1. CONFIGURATION ET BASE DE DONNÉES ---
def init_db():
    """Initialise la connexion SQLite et crée la table si nécessaire."""
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

# --- 2. FONCTIONS UTILITAIRES ---
def valider_tel(numero):
    """Vérifie si le numéro contient uniquement des chiffres et fait au moins 9 caractères."""
    return bool(re.fullmatch(r'\d{9,}', numero))

def generer_lien_whatsapp(nom, tel, panier, total):
    """Crée un lien WhatsApp sécurisé avec les détails de la commande."""
    details_articles = "\n".join([f"- {item['nom']} ({item['prix']} FCFA)" for item in panier])
    message = (
        f"*Nouvelle Commande*\n\n"
        f"*Client:* {nom}\n"
        f"*Tel:* {tel}\n"
        f"--- \n"
        f"*Articles:*\n{details_articles}\n"
        f"--- \n"
        f"*Total:* {total} FCFA"
    )
    # encodage sécurisé pour URL
    message_encode = urllib.parse.quote(message)
    return f"https://wa.me/22177XXXXXXX?text={message_encode}" # Remplacez par votre numéro

# --- 3. INTERFACE UTILISATEUR (UI) ---
st.set_page_config(page_title="Gestion Restau", layout="centered")

st.title("🍽️ Système de Commande")

# Simulation d'un panier en session (à remplir via votre menu)
if 'panier' not in st.session_state:
    st.session_state.panier = [
        {"nom": "Thieboudienne", "prix": 2500},
        {"nom": "Yassa Poulet", "prix": 2000}
    ]

total_commande = sum(item['prix'] for item in st.session_state.panier)

# Affichage du panier
with st.expander("Voir mon panier", expanded=True):
    for item in st.session_state.panier:
        st.write(f"✅ {item['nom']} - {item['prix']} FCFA")
    st.markdown(f"**Total : {total_commande} FCFA**")

# Formulaire de validation
st.subheader("Finaliser la commande")
with st.form("form_validation"):
    nom_client = st.text_input("Votre Nom")
    tel_client = st.text_input("Numéro de téléphone (9 chiffres min)")
    
    soumettre = st.form_submit_button("Enregistrer la commande")

    if soumettre:
        if not nom_client or not tel_client:
            st.error("⚠️ Veuillez remplir tous les champs.")
        elif not valider_tel(tel_client):
            st.error("❌ Numéro de téléphone invalide (chiffres uniquement, min 9).")
        else:
            # Sauvegarde en base de données
            try:
                conn = init_db()
                cursor = conn.cursor()
                # Conversion du panier en JSON pour un stockage propre
                panier_json = json.dumps(st.session_state.panier)
                date_now = datetime.now().strftime("%d/%m/%Y %H:%M")
                
                cursor.execute('''
                    INSERT INTO commandes (client_nom, telephone, articles_json, total_prix, date_commande)
                    VALUES (?, ?, ?, ?, ?)
                ''', (nom_client, tel_client, panier_json, total_commande, date_now))
                
                conn.commit()
                conn.close()
                
                st.success("🎉 Commande enregistrée en base de données !")
                
                # Bouton WhatsApp
                lien_wa = generer_lien_whatsapp(nom_client, tel_client, st.session_state.panier, total_commande)
                st.link_button("📲 Envoyer le récapitulatif sur WhatsApp", lien_wa)
                
            except Exception as e:
                st.error(f"Erreur lors de l'enregistrement : {e}")

# --- 4. TABLEAU DE BORD (ADMIN) ---
st.divider()
if st.checkbox("📊 Afficher le Tableau de Bord (Admin)"):
    conn = init_db()
    df = pd.read_sql("SELECT * FROM commandes", conn)
    conn.close()
    
    if not df.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Ventes Totales", f"{df['total_prix'].sum()} FCFA")
        col2.metric("Nb Commandes", len(df))
        col3.metric("Moyenne", f"{round(df['total_prix'].mean(), 2)} FCFA")
        
        st.write("Détails des dernières transactions :")
        st.dataframe(df.sort_values(by="id", ascending=False))
    else:
        st.info("Aucune commande enregistrée pour le moment.")
