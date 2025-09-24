import streamlit as st
from msal import ConfidentialClientApplication
import requests

# Titkos adatok a .streamlit/secrets.toml fájlból
client_id = st.secrets["azure"]["client_id"]
tenant_id = st.secrets["azure"]["tenant_id"]
client_secret = st.secrets["azure"]["client_secret"]
my_email = st.secrets["azure"]["my_email"]

# Authority és scope beállítása
authority = f"https://login.microsoftonline.com/{tenant_id}"
scopes = ["https://graph.microsoft.com/.default"]

# Hitelesítés az MSAL könyvtárral
app = ConfidentialClientApplication(
    client_id=client_id,
    client_credential=client_secret,
    authority=authority
)

result = app.acquire_token_for_client(scopes=scopes)

if "access_token" not in result:
    st.error(f"Token hiba: {result}")
else:
    token = result["access_token"]

    # Email üzenet felépítése a Graph API elvárásainak megfelelően
    email_msg = {
        "message": {
            "subject": "Teszt e-mail Streamlitből",
            "body": {
                "contentType": "Text",
                "content": "Ez egy teszt üzenet, amit a Streamlit alkalmazás küldött a Microsoft Graph API segítségével."
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": my_email   # saját email címre küldi
                    }
                }
            ]
        },
        "saveToSentItems": "true"
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    r = requests.post(
        f"https://graph.microsoft.com/v1.0/users/{my_email}/sendMail",
        headers=headers,
        json=email_msg
    )

    if r.status_code == 202:
        st.success("Email sikeresen elküldve!")
    else:
        st.error(f"Hiba történt: {r.status_code} - {r.text}")
