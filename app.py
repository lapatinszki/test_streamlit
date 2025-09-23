import streamlit as st
import requests
from msal import ConfidentialClientApplication

st.set_page_config(page_title="Céges e-mail küldés", layout="centered")

st.title("📧 Céges e-mail küldés Microsoft Graph API-val")

# --- Titkok betöltése (Streamlit Cloud Secrets) ---
client_id = st.secrets["azure"]["client_id"]
tenant_id = st.secrets["azure"]["tenant_id"]
client_secret = st.secrets["azure"]["client_secret"]
my_email = st.secrets["azure"]["my_email"]

authority = f"https://login.microsoftonline.com/{tenant_id}"
scopes = ["https://graph.microsoft.com/.default"]

# --- Token szerzés ---
app = ConfidentialClientApplication(
    client_id=client_id,
    client_credential=client_secret,
    authority=authority
)

result = app.acquire_token_for_client(scopes=scopes)

if "access_token" not in result:
    st.error(f"❌ Token hiba: {result}")
    st.stop()

token = result["access_token"]

# --- Űrlap a levélhez ---
st.subheader("Új e-mail létrehozása")
to_address = st.text_input("Címzett e-mail címe", value=my_email)
subject = st.text_input("Tárgy", value="Teszt üzenet a Streamlitből")
body = st.text_area("Üzenet szövege", value="Ez egy teszt e-mail, amit a Microsoft Graph API küldött ki.")

if st.button("✉️ E-mail küldése"):
    email_msg = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body
            },
            "toRecipients": [
                {"emailAddress": {"address": to_address}}
            ]
        }
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    url = f"https://graph.microsoft.com/v1.0/users/{my_email}/sendMail"
    r = requests.post(url, headers=headers, json=email_msg)

    if r.status_code == 202:
        st.success(f"✅ E-mail elküldve {to_address} címre!")
    else:
        st.error(f"❌ Hiba a küldésnél: {r.status_code} {r.text}")

