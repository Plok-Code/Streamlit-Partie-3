import streamlit as st
import pandas as pd
from streamlit_authenticator import Authenticate

st.set_page_config(page_title="Album de mon chat", page_icon="🐱", layout="wide")

df_users = pd.read_csv("users.csv")

lesDonneesDesComptes = {"usernames": {}}
for _, row in df_users.iterrows():
    username = row["name"]
    lesDonneesDesComptes["usernames"][username] = {
        "name": row["name"],
        "password": row["password"],
        "email": row["email"],
        "failed_login_attemps": int(row["failed_login_attemps"]),
        "logged_in": bool(row["logged_in"]),
        "role": row["role"],
    }

authenticator = Authenticate(
    lesDonneesDesComptes,
    "cookie_name",
    "cookie_key",
    30,
)

authenticator.login()

auth_status = st.session_state.get("authentication_status")
username = st.session_state.get("username")

if auth_status:
    with st.sidebar:
        authenticator.logout("Déconnexion")
        st.write(f"Bienvenue {username}")
        page = st.radio(
            "Menu",
            ["😃 Accueil", "🐱 Les photos de mon chat"],
            index=0,
        )

    if page == "😃 Accueil":
        st.title("Bienvenue sur ma page")
        st.image("images/applaudissements.png", width=500)

    elif page == "🐱 Les photos de mon chat":
        st.title("Bienvenue dans l'album de mon chat 🐱")
        col1, col2, col3 = st.columns(3)
        col1.image("images/chat1.png", use_container_width=True)
        col2.image("images/chat2.png", use_container_width=True)
        col3.image("images/chat3.png", use_container_width=True)

elif auth_status is False:
    st.error("L'username ou le mot de passe est incorrect.")
else:
    st.warning("Les champs username et mot de passe doivent être remplis.")