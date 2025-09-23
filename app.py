import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Secrets betöltése
smtp_server = st.secrets["email"]["smtp_server"]
smtp_port = st.secrets["email"]["smtp_port"]
smtp_username = st.secrets["email"]["smtp_username"]
smtp_password = st.secrets["email"]["smtp_password"]
smtp_helo = st.secrets["email"]["smtp_helo"]

# Email felépítése
sender_email = "idm@idm-systems.hu"
receiver_email = "lapatinszki18@gmail.com"  # ide küldöd a teszt emailt
subject = "Streamlit Mailtrap teszt"
body = "Ez egy teszt üzenet Mailtrap SMTP-vel."

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo(smtp_helo)
        server.starttls()  # mert a Mailtrap port 587 STARTTLS-t használ
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        st.success("Email sikeresen elküldve!")
except Exception as e:
    st.error(f"Hiba történt: {e}")
