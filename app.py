import streamlit as st
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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    :root {
        --gold: #F0B84D;
        --gold-light: #FFD57E;
        --gold-dark: #C6912E;
        --bg-main: #0B0F19;
        --bg-card: #131A2A;
        --bg-card-hover: #171F33;
        --border-soft: #232D42;
        --text-main: #EAEEF7;
        --text-muted: #8895AD;
    }

    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stAppViewBlockContainer"], [data-testid="stMain"] {
        background: radial-gradient(circle at top left, #121a2b 0%, #0B0F19 55%, #090c14 100%) !important;
        color: var(--text-main) !important;
        font-family: 'Inter', sans-serif !important;
    }

    [data-testid="stHeader"] { background: transparent !important; }

    /* ---------- Bouton pour rouvrir la sidebar (flèche >>) ---------- */
    [data-testid="collapsedControl"] {
        background: rgba(19, 26, 42, 0.6) !important;
        border: 1px solid var(--border-soft) !important;
        border-radius: 8px !important;
        opacity: 1 !important;
        visibility: visible !important;
    }

    [data-testid="collapsedControl"] svg {
        fill: var(--text-muted) !important;
        color: var(--text-muted) !important;
    }

    [data-testid="collapsedControl"] button {
        background: transparent !important;
    }

    /* ---------- Titres ---------- */
    h1, h2 {
        background: linear-gradient(135deg, var(--gold-light) 0%, var(--gold) 50%, var(--gold-dark) 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }

    h3, h4 {
        color: var(--text-main) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
    }

    p, span, label, .stMarkdown, .stCaption { color: var(--text-main); }

    /* ---------- Labels des champs (Nom d'utilisateur, Mot de passe, etc.) ---------- */
    [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label, [data-testid="stWidgetLabel"] {
        color: var(--text-main) !important;
        font-weight: 600 !important;
        opacity: 1 !important;
    }

    /* ---------- Texte tapé + placeholder dans les champs ---------- */
    input::placeholder, textarea::placeholder {
        color: var(--text-muted) !important;
        opacity: 1 !important;
    }

    input, textarea, div[data-baseweb="select"] span {
        color: var(--text-main) !important;
        -webkit-text-fill-color: var(--text-main) !important;
    }

    /* ---------- Icône œil (afficher/cacher mot de passe) ---------- */
    button[title="Show password"] svg, button[title="Hide password"] svg,
    div[data-baseweb="input"] button svg {
        fill: var(--text-muted) !important;
    }

    /* ---------- Cards / Containers (effet glassmorphism + glow au survol) ---------- */
    div[data-testid="stContainer"], div[data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(145deg, var(--bg-card) 0%, #0F1524 100%) !important;
        border: 1px solid var(--border-soft) !important;
        border-radius: 18px !important;
        padding: 24px !important;
        box-shadow: 0 8px 24px -8px rgba(0, 0, 0, 0.6) !important;
        backdrop-filter: blur(10px);
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease !important;
    }

    div[data-testid="stContainer"]:hover, div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 16px 40px -12px rgba(240, 184, 77, 0.25), 0 0 0 1px rgba(240, 184, 77, 0.3) !important;
        border-color: var(--gold) !important;
    }

    /* ---------- Expander (menu déroulant show/hide) ---------- */
    [data-testid="stExpander"] {
        background: linear-gradient(145deg, var(--bg-card) 0%, #0F1524 100%) !important;
        border: 1px solid var(--border-soft) !important;
        border-radius: 14px !important;
        margin-bottom: 18px !important;
    }

    [data-testid="stExpander"] summary {
        color: var(--text-main) !important;
        font-weight: 700 !important;
    }

    [data-testid="stExpander"] summary:hover {
        color: var(--gold) !important;
    }

    /* ---------- Sidebar ---------- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0D1220 0%, #090C14 100%) !important;
        border-right: 1px solid var(--border-soft) !important;
    }

    [data-testid="stSidebar"] * { color: var(--text-main) !important; }

    /* ---------- Inputs / Selects / Textareas (tous les niveaux imbriqués) ---------- */
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
        background-color: #0F1524 !important;
        color: var(--text-main) !important;
        -webkit-text-fill-color: var(--text-main) !important;
    }

    div[data-baseweb="input"], div[data-baseweb="select"] > div, div[data-baseweb="textarea"] {
        border: 1px solid var(--border-soft) !important;
        border-radius: 10px !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }

    /* ---------- Empêche le navigateur d'imposer un fond blanc (autofill / saisie) ---------- */
    input:-webkit-autofill,
    input:-webkit-autofill:hover,
    input:-webkit-autofill:focus,
    input:-webkit-autofill:active,
    textarea:-webkit-autofill,
    textarea:-webkit-autofill:focus {
        -webkit-box-shadow: 0 0 0px 1000px #0F1524 inset !important;
        box-shadow: 0 0 0px 1000px #0F1524 inset !important;
        -webkit-text-fill-color: var(--text-main) !important;
        caret-color: var(--text-main) !important;
        transition: background-color 9999s ease-in-out 0s, color 9999s ease-in-out 0s !important;
    }

    div[data-baseweb="input"]:focus-within, div[data-baseweb="select"] > div:focus-within, div[data-baseweb="textarea"]:focus-within {
        border-color: var(--gold) !important;
        box-shadow: 0 0 0 3px rgba(240, 184, 77, 0.15) !important;
    }

    /* ---------- Radio (menu sidebar) ---------- */
    div[data-testid="stRadio"] label {
        background-color: #0F1524 !important;
        border: 1px solid var(--border-soft) !important;
        padding: 10px 15px !important;
        border-radius: 10px !important;
        margin-bottom: 8px !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
    }

    div[data-testid="stRadio"] label:hover {
        border-color: var(--gold) !important;
        background-color: #171F33 !important;
    }

    /* ---------- Boutons dorés avec glow ---------- */
    div.stButton > button, div[data-testid="stFormSubmitButton"] button, div[data-testid="stDownloadButton"] button {
        background: linear-gradient(135deg, var(--gold-light) 0%, var(--gold) 55%, var(--gold-dark) 100%) !important;
        color: #0B0F19 !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 11px 20px !important;
        width: 100% !important;
        box-shadow: 0 4px 16px rgba(240, 184, 77, 0.35) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease, filter 0.15s ease !important;
    }

    div.stButton > button:hover, div[data-testid="stFormSubmitButton"] button:hover, div[data-testid="stDownloadButton"] button:hover {
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 8px 28px rgba(240, 184, 77, 0.5) !important;
        filter: brightness(1.08) !important;
    }

    div.stButton > button:active {
        transform: translateY(0) scale(0.99) !important;
    }

    /* ---------- Bouton icône œil (show/hide password) - reste discret, PAS un bouton doré ---------- */
    div[data-baseweb="input"] button {
        background: transparent !important;
        width: auto !important;
        box-shadow: none !important;
        padding: 4px !important;
    }

    div[data-baseweb="input"] button svg {
        fill: var(--text-muted) !important;
    }

    /* ---------- Barre de décoration en haut (glow animé) ---------- */
    [data-testid="stDecoration"] {
        background: linear-gradient(90deg, var(--gold-dark), var(--gold-light), var(--gold-dark)) !important;
        background-size: 200% auto !important;
        animation: shimmer 3s linear infinite;
    }

    @keyframes shimmer {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }

    /* ---------- Dataframes / tableaux ---------- */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--border-soft) !important;
        border-radius: 12px !important;
        overflow: hidden;
    }

    /* ---------- Alertes (success / error / warning / info) ---------- */
    div[data-testid="stAlert"] {
        border-radius: 12px !important;
        border: 1px solid var(--border-soft) !important;
        backdrop-filter: blur(6px);
    }

    /* ---------- Scrollbar dorée fine ---------- */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #0B0F19; }
    ::-webkit-scrollbar-thumb { background: var(--gold-dark); border-radius: 8px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--gold); }

    /* ---------- hr ---------- */
    hr { border-color: var(--border-soft) !important; }

    /* ---------- Responsive Mobile : empêche le débordement horizontal ---------- */
    html, body { overflow-x: hidden !important; }

    [data-testid="stAppViewContainer"], [data-testid="stMain"], .main, section.main {
        max-width: 100vw !important;
        overflow-x: hidden !important;
    }

    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 100vw !important;
        }

        h1 { font-size: 1.6rem !important; }
        h2 { font-size: 1.3rem !important; }
        h3, h4 { font-size: 1.05rem !important; }

        div[data-testid="stContainer"], div[data-testid="stVerticalBlockBorderWrapper"] {
            padding: 14px !important;
        }

        div[data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }
    }
</style>
""", unsafe_allow_html=True)

DB_PATH = "nearya_express.db"

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
            try:
                cursor.execute("INSERT INTO users (username, password, role) VALUES ('admin1', 'admin123', 'Admin')")
                cursor.execute("INSERT INTO users (username, password, role) VALUES ('commercial1', 'comm123', 'Commercial')")
                cursor.execute("INSERT INTO users (username, password, role) VALUES ('commercial2', 'comm456', 'Commercial')")
                conn.commit()
            except sqlite3.IntegrityError:
                pass  # les utilisateurs existent déjà
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
        <div style='background: linear-gradient(135deg, rgba(240,184,77,0.12), rgba(240,184,77,0.04)); border: 1px solid rgba(240,184,77,0.35); padding: 14px 20px; border-radius: 10px; margin-bottom: 25px; display: flex; align-items: center; gap: 10px;'>
            <span style='font-size: 22px; font-weight: 900; background: linear-gradient(135deg, #FFD57E 0%, #F0B84D 50%, #C6912E 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; letter-spacing: -0.5px;'>NearYa</span>
            <span style='color: #8895AD; font-size: 12px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; margin-top: 3px;'>Express</span>
        </div>
    """, unsafe_allow_html=True)

    df = get_orders_df()

    if current_menu == "📦 Ajouter Commande":
        st.subheader("Saisie Complète d'Expédition")
        main_col1, main_col2 = st.columns([2, 1])

        with main_col1:
            with st.form("manual_order_form"):
                st.markdown("<h4 style='margin-top:0; color:#F0B84D;'>👤 1. Destinataire (Client)</h4>", unsafe_allow_html=True)
                c_name, c_phone = st.columns(2)
                with c_name:
                    client_name = st.text_input("Nom Complet du Client *")
                with c_phone:
                    phone = st.text_input("Téléphone du Client *")

                zone = st.selectbox("Zone de livraison *", ["Casablanca - Centre", "Casablanca - Oulfa", "Casablanca - Ain Sebaa", "Rabat", "Marrakech"])
                address = st.text_input("Adresse de Livraison exacte *")
                maps_link = st.text_input("Lien Google Maps (Optionnel)")

                st.markdown("<hr style='border-color:#232D42;'>", unsafe_allow_html=True)
                st.markdown("<h4 style='color:#F0B84D;'>📦 2. Logistique & Upload Photos</h4>", unsafe_allow_html=True)

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

                st.markdown("<hr style='border-color:#232D42;'>", unsafe_allow_html=True)
                st.markdown("<h4 style='color:#F0B84D;'>💰 3. Produit & Facturation</h4>", unsafe_allow_html=True)

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
                    f"<span style='background: linear-gradient(135deg, rgba(240,184,77,0.18), rgba(240,184,77,0.06)); border: 1px solid rgba(240,184,77,0.4); color: #F0B84D; padding: 5px 14px; border-radius: 20px; font-size: 13px; font-weight: 700; margin-right: 8px; display: inline-block; margin-bottom: 8px;'>🧑‍💼 {name}</span>"
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
                        f"<span style='background: linear-gradient(135deg, rgba(240,184,77,0.2), rgba(240,184,77,0.08)); "
                        f"border: 1px solid rgba(240,184,77,0.4); color: #F0B84D; padding: 4px 12px; border-radius: 8px; "
                        f"font-size: 13px; font-weight: 800;'>🧑‍💼 Commercial : {row['created_by']}</span>",
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
    col_space1, col_logo, col_space2 = st.columns([1.5, 1, 1.5])
    with col_logo:
        if os.path.exists(LOGO_FILE):
            st.image(LOGO_FILE, use_container_width=True)
        else:
            st.markdown("<h1 style='text-align: center; color: #F0B84D;'>NearYa</h1>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; margin-bottom: 30px;'>🔐 Connexion</h3>", unsafe_allow_html=True)
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
    st.sidebar.markdown("<h1 style='text-align: center; font-size: 38px; font-weight: 800; color: #F0B84D; margin-bottom: 0;'>NearYa</h1>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align: center; font-size: 11px; color: #94A3B8; margin-top: 0; letter-spacing: 2px; font-weight:700;'>EXPRESS LOGISTICS</p>", unsafe_allow_html=True)

    if os.path.exists(LOGO_FILE):
        st.sidebar.image(LOGO_FILE, use_container_width=True)
    st.sidebar.markdown("<hr style='border-color:#232D42; margin: 15px 0;'>", unsafe_allow_html=True)

    st.sidebar.markdown(f"""
        <div style='background: linear-gradient(145deg, #131A2A, #0F1524); border: 1px solid #232D42; padding: 15px; border-radius: 14px; box-shadow: 0 8px 20px -8px rgba(0,0,0,0.5);'>
            <div style='display: flex; align-items: center; gap: 10px;'>
                <div style='width: 10px; height: 10px; background-color: #22C55E; border-radius: 50%; display: inline-block; box-shadow: 0 0 8px #22C55E;'></div>
                <span style='font-size: 13px; color: #8895AD; font-weight: 600;'>En ligne</span>
            </div>
            <p style='margin: 8px 0 2px 0; font-size: 16px; font-weight: 700; color: #EAEEF7;'>{st.session_state['username']}</p>
            <span style='background: linear-gradient(135deg, rgba(240,184,77,0.2), rgba(240,184,77,0.08)); border: 1px solid rgba(240,184,77,0.4); color: #F0B84D; padding: 3px 10px; border-radius: 6px; font-size: 11px; font-weight: 700;'>✨ Espace {st.session_state['role']}</span>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("<hr style='border-color:#232D42; margin: 20px 0;'>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='font-size: 11px; font-weight: 700; color: #94A3B8; letter-spacing: 0.5px; margin-bottom: 10px;'>MENU CONTROL</p>", unsafe_allow_html=True)

    if st.session_state["role"] == "Commercial":
        menu = st.sidebar.radio("Navigation", ["📦 Ajouter Commande", "🔍 Recherche & Suivi"], label_visibility="collapsed")
    else:
        menu = st.sidebar.radio("Navigation", ["📋 Suivi Global & Recherche", "📊 Statistiques & Performance", "📅 Rapport Journalier", "🗺️ Carte Google Maps"], label_visibility="collapsed")

    st.sidebar.markdown("<hr style='border-color:#232D42; margin: 20px 0;'>", unsafe_allow_html=True)

    st.sidebar.markdown("""
        <div style='background-color: #131A2A; border: 1px solid #232D42; padding: 12px; border-radius: 10px;'>
            <div style='display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 5px; font-weight:600;'>
                <span style='color: #8895AD;'>Performance Réseau</span>
                <span style='color: #F0B84D;'>100%</span>
            </div>
            <div style='background-color: #232D42; border-radius: 4px; height: 8px; overflow: hidden;'>
                <div style='background: linear-gradient(90deg, #C6912E, #FFD57E); width: 100%; height: 100%; box-shadow: 0 0 8px rgba(240,184,77,0.6);'></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.caption(f"📅 Système Live 2026")
    st.sidebar.markdown("<br>", unsafe_allow_html=True)

    if st.sidebar.button("🚪 Se déconnecter"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.session_state["role"] = ""
        st.rerun()

    if st.session_state["role"] == "Admin":
        admin_page(menu)
    elif st.session_state["role"] == "Commercial":
        commercial_page(menu)