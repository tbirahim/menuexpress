import streamlit as st
import uuid, urllib.parse, datetime
from constants import *
from storage import load_menu, save_menu, save_order

st.set_page_config("Teranga Web", layout="wide")

# CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- STATE ----------------
if "view" not in st.session_state:
    st.session_state.view = "Accueil"

if "menu" not in st.session_state:
    st.session_state.menu = load_menu()

if "cart" not in st.session_state:
    st.session_state.cart = []

if "admin_ok" not in st.session_state:
    st.session_state.admin_ok = False

# ---------------- HELPERS ----------------
def total():
    return sum(i["price"] * i["quantity"] for i in st.session_state.cart)

def add_to_cart(item):
    for i in st.session_state.cart:
        if i["id"] == item["id"]:
            i["quantity"] += 1
            return
    st.session_state.cart.append({**item, "quantity": 1})

# ---------------- SIDEBAR ----------------
st.sidebar.title("🍽 Teranga Web")
st.sidebar.caption("Dakar, Sénégal")

st.session_state.view = st.sidebar.radio(
    "Navigation",
    ["Accueil", "Menu", "Réservation", f"Panier ({len(st.session_state.cart)})", "Admin"]
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"📞 **{CALL_NUMBER}**")

# ---------------- ACCUEIL ----------------
if st.session_state.view == "Accueil":
    st.title("Teranga Gourmet Express 🇸🇳")
    st.info("Cuisine sénégalaise authentique • Commande & réservation en ligne")

    col1, col2 = st.columns(2)
    if col1.button("🍴 Voir le menu"):
        st.session_state.view = "Menu"
        st.experimental_rerun()
    if col2.button("📅 Réserver"):
        st.session_state.view = "Réservation"
        st.experimental_rerun()

# ---------------- MENU ----------------
elif st.session_state.view == "Menu":
    st.title("🍴 Carte du jour")

    for item in st.session_state.menu:
        with st.container(border=True):
            c1, c2, c3 = st.columns([1,3,1])
            c1.image(item["image"], use_column_width=True)
            c2.markdown(f"### {item['name']}\n{item['description']}")
            c3.markdown(f"**{item['price']} FCFA**")
            if c3.button("Ajouter", key=item["id"]):
                add_to_cart(item)
                st.success("Ajouté au panier")

# ---------------- RESERVATION ----------------
elif st.session_state.view == "Réservation":
    st.title("📅 Réservation")

    with st.form("reserve"):
        nom = st.text_input("Nom complet")
        pers = st.number_input("Personnes", 1, 20, 2)
        date = st.date_input("Date")
        heure = st.time_input("Heure")
        ok = st.form_submit_button("Confirmer")

        if ok:
            msg = f"RÉSERVATION\nNom: {nom}\nDate: {date}\nHeure: {heure}\nCouverts: {pers}"
            link = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(msg)}"
            st.markdown(f"[👉 Confirmer sur WhatsApp]({link})")

# ---------------- PANIER ----------------
elif st.session_state.view.startswith("Panier"):
    st.title("🛒 Votre commande")

    if not st.session_state.cart:
        st.warning("Panier vide")
    else:
        for i in st.session_state.cart:
            c1, c2, c3 = st.columns([3,1,1])
            c1.write(f"{i['name']} x{i['quantity']}")
            c2.write(f"{i['price'] * i['quantity']} F")
            if c3.button("❌", key=i["id"]+"rm"):
                st.session_state.cart.remove(i)
                st.experimental_rerun()

        st.subheader(f"Total : {total()} FCFA")

        with st.form("order"):
            service = st.selectbox("Service", ["Sur place", "Livraison"])
            details = st.text_area("Adresse / Table")
            ok = st.form_submit_button("Commander")

            if ok:
                items = "\n".join([f"- {i['name']} x{i['quantity']}" for i in st.session_state.cart])
                msg = f"COMMANDE\n{items}\nTotal: {total()} F\nMode: {service}\nLieu: {details}"
                link = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(msg)}"

                save_order({
                    "date": datetime.datetime.now().isoformat(),
                    "items": items,
                    "total": total(),
                    "mode": service,
                    "details": details
                })

                st.session_state.cart = []
                st.markdown(f"[👉 Envoyer la commande]({link})")

# ---------------- ADMIN ----------------
elif st.session_state.view == "Admin":
    st.title("⚙️ Administration")

    if not st.session_state.admin_ok:
        code = st.text_input("Code admin", type="password")
        if code == ADMIN_PASS:
            st.session_state.admin_ok = True
            st.experimental_rerun()
    else:
        st.subheader("➕ Ajouter un plat")
        with st.form("add"):
            name = st.text_input("Nom")
            price = st.number_input("Prix", 0)
            desc = st.text_area("Description")
            img = st.text_input("Image URL")
            ok = st.form_submit_button("Ajouter")

            if ok:
                st.session_state.menu.append({
                    "id": str(uuid.uuid4()),
                    "name": name,
                    "price": price,
                    "description": desc,
                    "image": img or "https://via.placeholder.com/400",
                    "category": "Plat"
                })
                save_menu(st.session_state.menu)
                st.success("Plat ajouté")

        st.download_button(
            "📥 Export commandes CSV",
            open(ORDERS_FILE, "rb"),
            file_name="commandes.csv"
        )
