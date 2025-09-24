import streamlit as st
from msal import ConfidentialClientApplication
import requests

client_id = st.secrets["azure"]["client_id"]
tenant_id = st.secrets["azure"]["tenant_id"]
client_secret = st.secrets["azure"]["client_secret"]
my_email = st.secrets["azure"]["my_email"]

authority = f"https://login.microsoftonline.com/{tenant_id}"
scopes = ["https://graph.microsoft.com/.default"]

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
    # példa: üzenet küldése a saját mailboxra
    email_msg = { ... }  # lásd korábbi példák
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    r = requests.post(f"https://graph.microsoft.com/v1.0/users/{my_email}/sendMail",
                      headers=headers, json=email_msg)
