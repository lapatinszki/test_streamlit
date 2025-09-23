import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

# Secrets betöltése
smtp_server = st.secrets["email"]["smtp_server"]
smtp_port = st.secrets["email"]["smtp_port"]
smtp_username = st.secrets["email"]["smtp_username"]
smtp_password = st.secrets["email"]["smtp_password"]
smtp_helo = st.secrets["email"]["smtp_helo"]

# Email adatok
sender_name = "IDM Systems Zrt."
sender_email = "idm@idm-systems.hu"
receiver_email = "lapatinszki18@gmail.com"
subject = "Streamlit Mailtrap teszt"
body = "Ez egy teszt üzenet Mailtrap SMTP-vel."

# Session state inicializálás a gombnyomás kezeléséhez
if "email_sent" not in st.session_state:
    st.session_state.email_sent = False

def send_email():
    message = MIMEMultipart()
    message["From"] = formataddr((sender_name, sender_email))
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo(smtp_helo)
            server.starttls()  # STARTTLS a Mailtrap port 587-hez
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        st.success("Email sikeresen elküldve!")
        st.session_state.email_sent = True
    except Exception as e:
        st.error(f"Hiba történt: {e}")

# Gomb megjelenítése
if st.button("Email küldése"):
    if not st.session_state.email_sent:
        send_email()
    else:
        st.info("Az email már elküldve.")
