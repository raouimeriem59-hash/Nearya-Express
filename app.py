import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
import os
from datetime import datetime
from contextlib import contextmanager

# ==========================================
# 1. PAGE CONFIG & DARK GOLD PREMIUM DESIGN
# ==========================================
st.set_page_config(page_title="NearYa Express", page_icon="📦", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* ============================================
       DESIGN TOKENS — identité "waybill / cachet postal"
       Un accent ambre (déjà la couleur de marque NearYa), une encre
       chaude au lieu du noir pur, un papier parcheminé au lieu du
       blanc froid. Une seule audace : le sceau + la bordure perforée
       sur la carte de connexion (voir plus bas).
       ============================================ */
    :root {
        --accent: #C77A2B;
        --accent-soft: rgba(199, 122, 43, 0.10);
        --accent-border: rgba(199, 122, 43, 0.35);

        --bg-page: #F5F3EC;
        --bg-surface: #FFFFFF;
        --bg-surface-raised: #EFEBDF;

        --border: #E2DDCD;
        --border-strong: #CFC8B2;

        --text-primary: #1E251F;
        --text-secondary: #5B6459;
        --text-tertiary: #8C9488;

        --success: #1E7A4C;
        --danger: #B8442F;

        --radius: 10px;
        --radius-sm: 6px;

        --font-display: 'Fraunces', serif;
        --font-body: 'Inter', sans-serif;
        --font-mono: 'JetBrains Mono', monospace;
    }

    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"],
    [data-testid="stAppViewBlockContainer"], [data-testid="stMain"] {
        background: var(--bg-page) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
    }

    [data-testid="stHeader"] { background: transparent !important; }

    /* ---------- Bouton pour rouvrir la sidebar ---------- */
    [data-testid="collapsedControl"] {
        background: var(--bg-surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
    }
    [data-testid="collapsedControl"] svg { fill: var(--text-secondary) !important; }
    [data-testid="collapsedControl"] button { background: transparent !important; }

    /* ---------- Titres : couleur pleine, pas de dégradé sur chaque titre ---------- */
    h1 {
        color: var(--text-primary) !important;
        font-family: var(--font-display) !important;
        font-weight: 600 !important;
        font-size: 2rem !important;
        letter-spacing: -0.3px;
        border-bottom: 1px solid var(--border);
        padding-bottom: 12px;
        margin-bottom: 20px !important;
    }

    h2, h3 {
        color: var(--text-primary) !important;
        font-family: var(--font-display) !important;
        font-weight: 600 !important;
    }

    h4 {
        color: var(--text-primary) !important;
        font-family: var(--font-body) !important;
        font-weight: 700 !important;
    }

    /* Sous-titres de section (##### dans le code) : discrets, en majuscule espacée */
    h5 {
        color: var(--text-tertiary) !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        margin-bottom: 12px !important;
    }

    p, span, label, .stMarkdown, .stCaption { color: var(--text-primary); }

    [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label, [data-testid="stWidgetLabel"] {
        color: var(--text-secondary) !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        opacity: 1 !important;
    }

    input::placeholder, textarea::placeholder {
        color: var(--text-tertiary) !important;
        opacity: 1 !important;
    }

    input, textarea, div[data-baseweb="select"] span {
        color: var(--text-primary) !important;
        -webkit-text-fill-color: var(--text-primary) !important;
    }

    button[title="Show password"] svg, button[title="Hide password"] svg,
    div[data-baseweb="input"] button svg {
        fill: var(--text-tertiary) !important;
    }

    /* ---------- Cards : un seul style, pas de lift+glow au hover partout ---------- */
    div[data-testid="stContainer"], div[data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--bg-surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        padding: 20px !important;
        transition: border-color 0.15s ease !important;
    }

    div[data-testid="stContainer"]:hover, div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: var(--border-strong) !important;
    }

    /* ---------- Expander ---------- */
    [data-testid="stExpander"] {
        background: var(--bg-surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        margin-bottom: 16px !important;
    }
    [data-testid="stExpander"] summary {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }
    [data-testid="stExpander"] summary:hover { color: var(--accent) !important; }

    /* ---------- Sidebar ---------- */
    [data-testid="stSidebar"] {
        background: var(--bg-page) !important;
        border-right: 1px solid var(--border) !important;
    }
    [data-testid="stSidebar"] * { color: var(--text-primary) !important; }

    /* ---------- Inputs / Selects / Textareas ---------- */
    div[data-baseweb="input"],
    div[data-baseweb="base-input"],
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] div,
    div[data-baseweb="textarea"],
    div[data-testid="stTextInput"] div,
    div[data-testid="stTextArea"] div,
    div[data-testid="stNumberInput"] div,
    textarea, input {
        background-color: var(--bg-surface-raised) !important;
        color: var(--text-primary) !important;
        -webkit-text-fill-color: var(--text-primary) !important;
    }

    div[data-baseweb="input"], div[data-baseweb="select"] > div, div[data-baseweb="textarea"] {
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        transition: border-color 0.15s ease !important;
    }

    input:-webkit-autofill,
    input:-webkit-autofill:hover,
    input:-webkit-autofill:focus,
    input:-webkit-autofill:active,
    textarea:-webkit-autofill,
    textarea:-webkit-autofill:focus {
        -webkit-box-shadow: 0 0 0px 1000px var(--bg-surface-raised) inset !important;
        box-shadow: 0 0 0px 1000px var(--bg-surface-raised) inset !important;
        -webkit-text-fill-color: var(--text-primary) !important;
        caret-color: var(--text-primary) !important;
        transition: background-color 9999s ease-in-out 0s, color 9999s ease-in-out 0s !important;
    }

    div[data-baseweb="input"]:focus-within, div[data-baseweb="select"] > div:focus-within, div[data-baseweb="textarea"]:focus-within {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px var(--accent-soft) !important;
    }

    /* ---------- Radio (menu sidebar) : état actif visible, pas de glow ---------- */
    div[data-testid="stRadio"] label {
        background-color: var(--bg-surface) !important;
        border: 1px solid var(--border) !important;
        padding: 10px 14px !important;
        border-radius: var(--radius-sm) !important;
        margin-bottom: 6px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        cursor: pointer !important;
        transition: border-color 0.15s ease, background-color 0.15s ease !important;
    }
    div[data-testid="stRadio"] label:hover {
        border-color: var(--border-strong) !important;
        background-color: var(--bg-surface-raised) !important;
    }

    /* ---------- Boutons : couleur pleine, ombre discrète ---------- */
    div.stButton > button, div[data-testid="stFormSubmitButton"] button, div[data-testid="stDownloadButton"] button {
        background: var(--accent) !important;
        color: #14100A !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        padding: 10px 18px !important;
        width: 100% !important;
        transition: filter 0.15s ease !important;
    }
    div.stButton > button:hover, div[data-testid="stFormSubmitButton"] button:hover, div[data-testid="stDownloadButton"] button:hover {
        filter: brightness(1.1) !important;
    }
    div.stButton > button:active { filter: brightness(0.95) !important; }

    div[data-baseweb="input"] button {
        background: transparent !important;
        width: auto !important;
        box-shadow: none !important;
        padding: 4px !important;
    }
    div[data-baseweb="input"] button svg { fill: var(--text-tertiary) !important; }

    /* ---------- Barre de décoration : fine ligne fixe, pas d'animation ---------- */
    [data-testid="stDecoration"] { background: var(--accent) !important; height: 2px !important; }

    /* ---------- Dataframes ---------- */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        overflow: hidden;
    }

    /* ---------- Alertes ---------- */
    div[data-testid="stAlert"] {
        border-radius: var(--radius-sm) !important;
        border: 1px solid var(--border) !important;
    }

    /* ---------- Scrollbar ---------- */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: var(--bg-page); }
    ::-webkit-scrollbar-thumb { background: var(--border-strong); border-radius: 8px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--text-tertiary); }

    hr { border-color: var(--border) !important; }

    /* ---------- Cache l'icône de lien (ancre) qui apparaît automatiquement à côté des titres ---------- */
    [data-testid="stHeaderActionElements"], h1 a, h2 a, h3 a, h4 a {
        display: none !important;
    }

    /* ---------- Carte de connexion : contenue, centrée. Ciblée UNIQUEMENT sur le
       container "login_card" (via key), pas sur tous les formulaires de l'app.
       Avant, la règle visait [data-testid="stForm"] en général, ce qui rétrécissait
       aussi le formulaire de commande (Ajouter Commande) en une petite carte de 400px.

       Le nom "NearYa Express" vit maintenant à un seul endroit : en haut de cette
       carte (plus de titre dupliqué en haut de la page, plus de sceau séparé). ---------- */
    .st-key-login_card {
        background: var(--bg-surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        padding: 40px 36px 36px 36px !important;
        max-width: 420px !important;
        margin: 60px auto 0 auto !important;
        box-shadow: 0 20px 40px -24px rgba(26, 31, 41, 0.18) !important;
    }

    .st-key-login_card [data-testid="stForm"] {
        background: transparent !important;
        border: none !important;
        padding: 12px 0 0 0 !important;
        margin: 0 !important;
        box-shadow: none !important;
        max-width: none !important;
    }

    .st-key-login_card [data-testid="stTextInput"] {
        margin-bottom: 4px !important;
    }

    [data-testid="stImage"] img {
        display: block !important;
        margin: 0 auto !important;
    }

    /* ---------- Chiffres / IDs / dates : police mono pour lisibilité des données ---------- */
    .mono-data { font-family: 'JetBrains Mono', monospace !important; }

    /* ---------- Responsive Mobile ---------- */
    html, body { overflow-x: hidden !important; }
    [data-testid="stAppViewContainer"], [data-testid="stMain"], .main, section.main {
        max-width: 100vw !important;
        overflow-x: hidden !important;
    }
    @media (max-width: 768px) {
        .block-container { padding-left: 1rem !important; padding-right: 1rem !important; max-width: 100vw !important; }
        h1 { font-size: 1.5rem !important; }
        h2 { font-size: 1.2rem !important; }
        h3, h4 { font-size: 1rem !important; }
        div[data-testid="stContainer"], div[data-testid="stVerticalBlockBorderWrapper"] { padding: 14px !important; }
        div[data-testid="column"] { width: 100% !important; flex: 1 1 100% !important; min-width: 100% !important; }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DB_PATH : chemin ABSOLU basé sur l'emplacement du script.
# Avant : DB_PATH = "nearya_express.db" (chemin relatif) -> si tu lances
# `streamlit run app.py` depuis un dossier différent (nouveau terminal,
# codespace redémarré, etc.), Python créait un NOUVEAU fichier .db vide
# dans le dossier courant, et tes anciennes données "disparaissaient".
# Avec le chemin absolu, c'est toujours EXACTEMENT le même fichier,
# peu importe d'où tu lances le script.
# ==========================================
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nearya_express.db")

# ==========================================
# 2. DATABASE: CONNECTION CENTRALE + INIT
# ==========================================
@contextmanager
def get_connection():
    """
    Connexion centralisée à la base.
    - timeout=15 : si la base est occupée (écriture concurrente), on attend
      au lieu de planter direct avec 'database is locked'.
    - WAL mode : permet plusieurs lectures + une écriture en même temps,
      essentiel vu que plusieurs commerciaux utilisent l'app en parallèle.
    - check_same_thread=False : Streamlit peut exécuter le script dans des
      threads différents selon les sessions.
    """
    conn = sqlite3.connect(DB_PATH, timeout=15, check_same_thread=False)
    try:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA busy_timeout=15000;")
        yield conn
    finally:
        conn.close()


def init_db():
    # Si un ancien fichier corrompu (pas une vraie base SQLite) existe, on le détecte et on le régénère.
    if os.path.exists(DB_PATH):
        try:
            test_conn = sqlite3.connect(DB_PATH, timeout=5)
            test_conn.execute("SELECT name FROM sqlite_master LIMIT 1;")
            test_conn.close()
        except sqlite3.DatabaseError:
            # Fichier corrompu / pas une vraie base -> on le sauvegarde de côté et on repart propre
            backup_name = f"{DB_PATH}.corrupted_{datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
            os.rename(DB_PATH, backup_name)
            st.warning(f"⚠️ L'ancienne base était corrompue, elle a été sauvegardée sous '{backup_name}' et une nouvelle base a été créée.")

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, role TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, client_name TEXT, phone TEXT,
                    address TEXT, maps_link TEXT, product TEXT, quantity INTEGER,
                    nb_colis INTEGER, ramassage TEXT, type_colis TEXT, weight REAL,
                    payment_mode TEXT, zone TEXT, notes TEXT, time_slot TEXT,
                    status TEXT, created_by TEXT, date_created TEXT, shop_photo TEXT
                )
            """)

            # ==========================================
            # Comptes fixes de l'application.
            # Avant : les comptes n'étaient créés qu'une seule fois (INSERT simple),
            # et si le username existait déjà, toute modification du mot de passe
            # dans le code était ignorée (IntegrityError -> pass). Résultat :
            # le mot de passe "réel" dans la base ne correspondait jamais à ce
            # qui était écrit ici, ce qui donnait l'impression que le mot de
            # passe "changeait tout seul".
            #
            # Maintenant : on utilise INSERT OR REPLACE, donc à CHAQUE démarrage
            # de l'app, ces 5 comptes sont garantis d'avoir exactement le
            # username/mot de passe/role définis ci-dessous. Si tu veux changer
            # un mot de passe, tu le changes ici et il sera appliqué au prochain
            # lancement, sans exception ni ambiguïté.
            # ==========================================
            fixed_accounts = [
                ("admin",       "Nqse2340", "Admin"),
                ("commercial1", "Nqse2341", "Commercial"),
                ("commercial2", "Nqse2342", "Commercial"),
                ("commercial3", "Nqse2343", "Commercial"),
                ("commercial4", "Nqse2344", "Commercial"),
            ]
            cursor.executemany(
                "INSERT OR REPLACE INTO users (username, password, role) VALUES (?, ?, ?)",
                fixed_accounts
            )
            conn.commit()
    except sqlite3.OperationalError as e:
        st.error(f"❌ Erreur d'initialisation de la base : {e}")
        st.stop()


init_db()


def get_orders_df():
    try:
        with get_connection() as conn:
            return pd.read_sql_query("SELECT * FROM orders", conn)
    except sqlite3.OperationalError as e:
        st.error(f"❌ Impossible de lire les commandes (base occupée ou erreur) : {e}")
        return pd.DataFrame(columns=[
            "id", "client_name", "phone", "address", "maps_link", "product", "quantity",
            "nb_colis", "ramassage", "type_colis", "weight", "payment_mode", "zone",
            "notes", "time_slot", "status", "created_by", "date_created", "shop_photo"
        ])


def insert_order(values):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO orders (client_name, phone, address, maps_link, product, quantity, nb_colis, ramassage, type_colis, weight, payment_mode, zone, notes, time_slot, status, created_by, date_created, shop_photo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'En attente', ?, ?, ?)
            """, values)
            conn.commit()
        return True, None
    except sqlite3.OperationalError as e:
        return False, str(e)


def check_login(username, password):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
            return cursor.fetchone()
    except sqlite3.OperationalError as e:
        st.error(f"❌ Erreur de connexion à la base : {e}")
        return None


def get_commercial_usernames():
    """Retourne la liste des commerciaux enregistrés (table users), pas seulement ceux qui ont déjà une commande."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users WHERE role = 'Commercial' ORDER BY username")
            return [row[0] for row in cursor.fetchall()]
    except sqlite3.OperationalError:
        return []


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.session_state["role"] = ""

LOGO_FILE = "WhatsApp Image 2026-07-05 at 3.43.54 AM.jpeg"

# ==========================================
# 3. PAGES LOGIC
# ==========================================

def commercial_page(current_menu):
    st.markdown("""
        <div style='background: var(--bg-surface); border: 1px solid var(--border); padding: 14px 20px; border-radius: 10px; margin-bottom: 25px; display: flex; align-items: center; gap: 10px;'>
            <span style='font-size: 20px; font-weight: 800; color: var(--text-primary); letter-spacing: -0.3px;'>NearYa</span>
            <span style='color: var(--accent); font-size: 12px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; margin-top: 3px;'>Express</span>
        </div>
    """, unsafe_allow_html=True)

    df = get_orders_df()

    if current_menu == "📦 Ajouter Commande":
        st.subheader("Saisie Complète d'Expédition")
        main_col1, main_col2 = st.columns([2, 1])

        with main_col1:
            st.markdown(
                "<p style='font-size:13px; color:var(--text-secondary); font-weight:600; margin-bottom:6px;'>"
                "📍 Cliquez sur la carte pour choisir l'adresse exacte du client, puis copiez le lien généré "
                "dans le champ « Lien Google Maps » ci-dessous.</p>",
                unsafe_allow_html=True
            )
            components.html(
                """
                <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
                <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
                <div id="nearya-map" style="height: 260px; border-radius: 10px; border: 1px solid #E2DDCD;"></div>
                <div style="display:flex; gap:8px; align-items:center; margin-top:8px;">
                    <input id="mapsLinkOutput" readonly
                        style="flex:1; padding:9px 10px; border-radius:6px; border:1px solid #E2DDCD;
                               font-family: 'JetBrains Mono', monospace; font-size:12px; color:#1E251F; background:#F5F3EC;"
                        placeholder="Le lien apparaîtra ici après un clic sur la carte..." />
                    <button id="copyBtn"
                        style="padding:9px 16px; border-radius:6px; border:none; background:#C77A2B;
                               color:white; font-weight:600; cursor:pointer; font-family:sans-serif; font-size:13px;">
                        Copier
                    </button>
                </div>
                <script>
                    var map = L.map('nearya-map').setView([33.5731, -7.5898], 12);
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                        attribution: '&copy; OpenStreetMap contributors',
                        maxZoom: 19
                    }).addTo(map);
                    var marker;
                    map.on('click', function(e) {
                        var lat = e.latlng.lat.toFixed(6);
                        var lng = e.latlng.lng.toFixed(6);
                        if (marker) { map.removeLayer(marker); }
                        marker = L.marker([lat, lng]).addTo(map);
                        document.getElementById('mapsLinkOutput').value =
                            "https://www.google.com/maps?q=" + lat + "," + lng;
                    });
                    document.getElementById('copyBtn').addEventListener('click', function() {
                        var input = document.getElementById('mapsLinkOutput');
                        if (!input.value) { return; }
                        input.select();
                        input.setSelectionRange(0, 99999);
                        navigator.clipboard.writeText(input.value).catch(function() {
                            document.execCommand('copy');
                        });
                    });
                </script>
                """,
                height=340,
            )

            with st.form("manual_order_form"):
                st.markdown(
                    "<div style='display:flex; align-items:center; gap:10px; margin-bottom:14px;'>"
                    "<span style='display:inline-flex; align-items:center; justify-content:center; width:26px; height:26px; "
                    "border-radius:50%; background:var(--accent-soft); border:1px solid var(--accent-border); color:var(--accent); "
                    "font-family:var(--font-mono); font-weight:600; font-size:13px;'>1</span>"
                    "<h4 style='margin:0; color:var(--text-primary);'>👤 Destinataire (Client)</h4></div>",
                    unsafe_allow_html=True
                )
                c_name, c_phone = st.columns(2)
                with c_name:
                    client_name = st.text_input("Nom Complet du Client *")
                with c_phone:
                    phone = st.text_input("Téléphone du Client *")

                zone = st.selectbox("Zone de livraison *", ["Casablanca - Centre", "Casablanca - Oulfa", "Casablanca - Ain Sebaa", "Rabat", "Marrakech"])
                address = st.text_input("Adresse de Livraison exacte *")
                maps_link = st.text_input("Lien Google Maps (Optionnel)")

                st.markdown("<hr style='border-color:var(--border);'>", unsafe_allow_html=True)
                st.markdown(
                    "<div style='display:flex; align-items:center; gap:10px; margin-bottom:14px;'>"
                    "<span style='display:inline-flex; align-items:center; justify-content:center; width:26px; height:26px; "
                    "border-radius:50%; background:var(--accent-soft); border:1px solid var(--accent-border); color:var(--accent); "
                    "font-family:var(--font-mono); font-weight:600; font-size:13px;'>2</span>"
                    "<h4 style='margin:0; color:var(--text-primary);'>📦 Logistique & Upload Photos</h4></div>",
                    unsafe_allow_html=True
                )

                col_ram, col_nb = st.columns(2)
                with col_ram:
                    ramassage = st.radio("Besoin d'un ramassage ? *", ["Non", "Oui"], horizontal=True)
                with col_nb:
                    nb_colis = st.number_input("Nombre de colis *", min_value=1, value=1)

                uploaded_file = st.file_uploader("📸 Upload Photo du magasin / colis", type=["png", "jpg", "jpeg"])

                col_type, col_weight = st.columns(2)
                with col_type:
                    type_colis = st.selectbox("Type de colis", ["Standard", "Fragile ⚠️", "Volume encombrant 📐"])
                with col_weight:
                    weight = st.number_input("Poids estimé (KG)", min_value=0.1, value=1.0)

                st.markdown("<hr style='border-color:var(--border);'>", unsafe_allow_html=True)
                st.markdown(
                    "<div style='display:flex; align-items:center; gap:10px; margin-bottom:14px;'>"
                    "<span style='display:inline-flex; align-items:center; justify-content:center; width:26px; height:26px; "
                    "border-radius:50%; background:var(--accent-soft); border:1px solid var(--accent-border); color:var(--accent); "
                    "font-family:var(--font-mono); font-weight:600; font-size:13px;'>3</span>"
                    "<h4 style='margin:0; color:var(--text-primary);'>💰 Produit & Facturation</h4></div>",
                    unsafe_allow_html=True
                )

                product = st.selectbox("Désignation Produit", ["Carton emballage renforcé", "Étiquettes adresse (x100)"])
                quantity = st.number_input("Quantité", min_value=1, value=1)
                payment_mode = st.selectbox("Mode de Paiement", ["COD (Cash on Delivery)", "Payé d'avance"])
                time_slot = st.text_input("Tranche Horaire", value="15:00 - 18:00")
                notes = st.text_area("Notes pour le livreur")

                if st.form_submit_button("🚀 Valider la Commande"):
                    if client_name and phone and address:
                        photo_path = ""
                        if uploaded_file is not None:
                            os.makedirs("uploaded_shops", exist_ok=True)
                            photo_path = f"uploaded_shops/{datetime.now().strftime('%Y%m%d%H%M%S')}_{uploaded_file.name}"
                            with open(photo_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())

                        today_str = datetime.now().strftime("%Y-%m-%d")
                        values = (client_name, phone, address, maps_link, product, quantity, nb_colis, ramassage, type_colis, weight, payment_mode, zone, notes, time_slot, st.session_state["username"], today_str, photo_path)
                        ok, err = insert_order(values)
                        if ok:
                            st.success("Commande et Photo enregistrées !")
                        else:
                            st.error(f"❌ Erreur lors de l'enregistrement : {err}. Réessayez dans un instant.")
                    else:
                        st.error("Veuillez remplir les champs obligatoires (*)")

        with main_col2:
            with st.container():
                st.markdown("<h4>📋 Récapitulatif Rapide</h4>", unsafe_allow_html=True)
                st.write(f"Vendeur: {st.session_state['username']}")
                st.caption("Veillez à ce que la photo du magasin soit claire si le ramassage est coché Oui.")

    elif current_menu == "🔍 Recherche & Suivi":
        st.subheader("🔍 Recherche multicritères (Mes Commandes)")
        my_df = df[df['created_by'] == st.session_state["username"]] if not df.empty else df

        s_name = st.text_input("Rechercher par nom de client")
        zone_options = ["Tous"] + list(my_df['zone'].unique()) if not my_df.empty else ["Tous"]
        s_zone = st.selectbox("Filtrer par Zone", zone_options)

        if s_name:
            my_df = my_df[my_df['client_name'].str.contains(s_name, case=False, na=False)]
        if s_zone != "Tous":
            my_df = my_df[my_df['zone'] == s_zone]

        display_df = my_df[['id', 'client_name', 'phone', 'zone', 'product', 'status', 'date_created']].rename(columns={
            'id': 'N°', 'client_name': 'Client', 'phone': 'Téléphone', 'zone': 'Zone',
            'product': 'Produit', 'status': 'Statut', 'date_created': 'Date'
        }) if not my_df.empty else my_df
        st.dataframe(display_df, use_container_width=True, hide_index=True)


def admin_page(current_menu):
    df = get_orders_df()

    if current_menu == "📋 Suivi Global & Recherche":
        st.title("👑 Suivi des Expéditions & Recherche Multicritères")

        commercial_names = get_commercial_usernames()
        if commercial_names:
            with st.expander(f"🧑‍💼 Commerciaux enregistrés ({len(commercial_names)})", expanded=False):
                badges = "".join([
                    f"<span style='background: var(--accent-soft); border: 1px solid var(--accent-border); color: var(--accent); padding: 5px 14px; border-radius: 20px; font-size: 13px; font-weight: 700; margin-right: 8px; display: inline-block; margin-bottom: 8px;'>🧑‍💼 {name}</span>"
                    for name in commercial_names
                ])
                st.markdown(f"<div>{badges}</div>", unsafe_allow_html=True)

        with st.container():
            st.markdown("##### 🛠️ Zone de Filtrage")
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1:
                search_client = st.text_input("Nom du Client")
            with col_f2:
                search_user = st.selectbox("Commercial", ["Tous"] + get_commercial_usernames())
            with col_f3:
                search_status = st.selectbox("Statut", ["Tous", "En attente", "Livré"])

        if not df.empty:
            if search_client:
                df = df[df['client_name'].str.contains(search_client, case=False, na=False)]
            if search_user != "Tous":
                df = df[df['created_by'] == search_user]
            if search_status != "Tous":
                df = df[df['status'] == search_status]

            st.markdown("##### 📥 Extraction des Données")
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(label="🟢 Exporter les commandes vers Excel (CSV)", data=csv, file_name=f"orders_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")

            st.markdown("##### 📋 Liste des ordres")
            for _, row in df.iterrows():
                with st.container(border=True):
                    st.markdown(
                        f"<span style='background: var(--accent-soft); "
                        f"border: 1px solid var(--accent-border); color: var(--accent); padding: 4px 12px; border-radius: 8px; "
                        f"font-size: 13px; font-weight: 700;'>🧑‍💼 Commercial : {row['created_by']}</span>",
                        unsafe_allow_html=True
                    )
                    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                    c1, c2, c3 = st.columns([2, 2, 1])
                    with c1:
                        st.markdown(f"**Client :** {row['client_name']} | **Tél :** {row['phone']}")
                        st.markdown(f"**Adresse :** {row['address']} ({row['zone']})")
                        if row['shop_photo'] and os.path.exists(row['shop_photo']):
                            st.image(row['shop_photo'], caption="Photo du magasin / colis", width=150)
                    with c2:
                        st.markdown(f"**Produit :** {row['product']} | **Colis :** {row['nb_colis']}")
                        st.markdown(f"**Ramassage :** {row['ramassage']}")
                    with c3:
                        st.markdown(f"⏰ {row['time_slot']}")
                        st.markdown(f"📅 {row['date_created']}")
        else:
            st.info("Aucune commande dans le système.")

    elif current_menu == "📊 Statistiques & Performance":
        st.title("📊 Analyses & Statistiques Avancées")
        if not df.empty:
            col_s1, col_s2 = st.columns(2)

            with col_s1:
                st.markdown("##### 👥 Statistiques par Commercial")
                stats_commercial = df['created_by'].value_counts()
                st.bar_chart(stats_commercial)

            with col_s2:
                st.markdown("##### 📅 Nombre de clients / commandes par jour")
                stats_jours = df['date_created'].value_counts().sort_index()
                st.line_chart(stats_jours)

            st.markdown("---")
            st.markdown("##### 📋 Détail par Commercial (clients apportés)")
            perf_table = df.groupby('created_by').agg(
                nb_commandes=('id', 'count'),
                nb_clients_uniques=('client_name', 'nunique'),
                derniere_commande=('date_created', 'max')
            ).reset_index().rename(columns={'created_by': 'Commercial'})
            perf_table = perf_table.sort_values('nb_commandes', ascending=False)
            st.dataframe(perf_table, use_container_width=True, hide_index=True)
        else:
            st.info("Pas assez de données pour générer des graphiques. Ajoutez des commandes pour voir apparaître les statistiques ici.")

    elif current_menu == "📅 Rapport Journalier":
        st.title("📅 Rapport Journalier")
        if not df.empty:
            available_dates = sorted(df['date_created'].unique(), reverse=True)
            selected_date = st.selectbox("Choisir une date", available_dates)
            day_df = df[df['date_created'] == selected_date]

            col_r1, col_r2, col_r3 = st.columns(3)
            col_r1.metric("📦 Commandes du jour", len(day_df))
            col_r2.metric("👤 Clients uniques", day_df['client_name'].nunique())
            col_r3.metric("🧑‍💼 Commerciaux actifs", day_df['created_by'].nunique())

            st.markdown("##### Répartition par commercial ce jour-là")
            st.bar_chart(day_df['created_by'].value_counts())

            st.markdown("##### Détail des commandes")
            report_view = day_df[['id', 'created_by', 'client_name', 'phone', 'zone', 'product', 'status', 'time_slot']].rename(columns={
                'id': 'N°', 'created_by': 'Commercial', 'client_name': 'Client', 'phone': 'Téléphone',
                'zone': 'Zone', 'product': 'Produit', 'status': 'Statut', 'time_slot': 'Créneau'
            })
            st.dataframe(report_view, use_container_width=True, hide_index=True)

            csv_day = day_df.to_csv(index=False).encode('utf-8')
            st.download_button(label="🟢 Exporter le rapport du jour (CSV)", data=csv_day, file_name=f"rapport_{selected_date}.csv", mime="text/csv")
        else:
            st.info("Aucune commande enregistrée pour le moment, donc pas encore de rapport journalier à afficher.")

    elif current_menu == "🗺️ Carte Google Maps":
        st.title("🗺️ Localisation des Livraisons")
        st.markdown("Visualisation sur la carte (Simulation des adresses de livraison)")
        map_data = pd.DataFrame({
            'lat': [33.5731, 33.5615, 33.5892],
            'lon': [-7.5898, -7.6532, -7.5512]
        })
        st.map(map_data)


# ==========================================
# 4. MAIN ROUTING & SUPER SIDEBAR FILLING
# ==========================================
if not st.session_state["logged_in"]:
    st.markdown("<div style='height: 70px'></div>", unsafe_allow_html=True)

    with st.container(key="login_card"):
        if os.path.exists(LOGO_FILE):
            st.image(LOGO_FILE, width=120)
        else:
            st.markdown(
                "<h1 style='text-align: center !important; color: var(--text-primary) !important; border-bottom: none !important; padding-bottom: 0 !important; margin-bottom: 20px !important; font-size: 1.9rem !important; letter-spacing: -0.4px !important;'>"
                "NearYa <span style='color: var(--accent);'>Express</span></h1>",
                unsafe_allow_html=True
            )

        with st.form("login_form"):
            username_input = st.text_input("Nom d'utilisateur")
            password_input = st.text_input("Mot de passe", type="password")
            if st.form_submit_button("Se connecter"):
                user = check_login(username_input, password_input)
                if user:
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username_input
                    st.session_state["role"] = user[0]
                    st.rerun()
                else:
                    st.error("Identifiants incorrects.")
else:
    st.sidebar.markdown("<h1 style='text-align: center !important; font-size: 26px !important; font-weight: 700 !important; color: var(--text-primary) !important; margin-bottom: 0 !important; border-bottom: none !important; padding-bottom: 0 !important;'>NearYa</h1>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align: center; font-size: 11px; color: var(--accent); margin-top: 2px; letter-spacing: 2px; font-weight:700;'>EXPRESS LOGISTICS</p>", unsafe_allow_html=True)

    if os.path.exists(LOGO_FILE):
        st.sidebar.image(LOGO_FILE, use_container_width=True)
    st.sidebar.markdown("<hr style='border-color:var(--border); margin: 15px 0;'>", unsafe_allow_html=True)

    st.sidebar.markdown(f"""
        <div style='background: var(--bg-surface); border: 1px solid var(--border); padding: 15px; border-radius: 14px;'>
            <div style='display: flex; align-items: center; gap: 8px;'>
                <div style='width: 8px; height: 8px; background-color: var(--success); border-radius: 50%; display: inline-block;'></div>
                <span style='font-size: 13px; color: var(--text-secondary); font-weight: 600;'>En ligne</span>
            </div>
            <p style='margin: 8px 0 6px 0; font-size: 16px; font-weight: 700; color: var(--text-primary);'>{st.session_state['username']}</p>
            <span style='background: var(--accent-soft); border: 1px solid var(--accent-border); color: var(--accent); padding: 3px 10px; border-radius: 6px; font-size: 11px; font-weight: 700;'>Espace {st.session_state['role']}</span>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("<hr style='border-color:var(--border); margin: 20px 0;'>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='font-size: 11px; font-weight: 700; color: var(--text-secondary); letter-spacing: 0.5px; margin-bottom: 10px;'>MENU CONTROL</p>", unsafe_allow_html=True)

    if st.session_state["role"] == "Commercial":
        menu = st.sidebar.radio("Navigation", ["📦 Ajouter Commande", "🔍 Recherche & Suivi"], label_visibility="collapsed")
    else:
        menu = st.sidebar.radio("Navigation", ["📋 Suivi Global & Recherche", "📊 Statistiques & Performance", "📅 Rapport Journalier", "🗺️ Carte Google Maps"], label_visibility="collapsed")

    st.sidebar.markdown("<hr style='border-color:var(--border); margin: 20px 0;'>", unsafe_allow_html=True)

    if st.sidebar.button("🚪 Se déconnecter"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.session_state["role"] = ""
        st.rerun()

    if st.session_state["role"] == "Admin":
        admin_page(menu)
    elif st.session_state["role"] == "Commercial":
        commercial_page(menu)
