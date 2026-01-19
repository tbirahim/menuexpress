import json, os, csv
from constants import MENU_FILE, ORDERS_FILE

def load_menu():
    if not os.path.exists(MENU_FILE):
        return []
    with open(MENU_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_menu(menu):
    with open(MENU_FILE, "w", encoding="utf-8") as f:
        json.dump(menu, f, indent=2, ensure_ascii=False)

def save_order(order):
    file_exists = os.path.exists(ORDERS_FILE)
    with open(ORDERS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=order.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(order)
