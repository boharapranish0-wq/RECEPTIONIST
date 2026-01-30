import streamlit as st
from google import genai
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os

# --- 1. THE ARCHITECT'S IDENTITY & AURA ---
st.set_page_config(page_title="Architect AI | 2026", layout="wide", page_icon="🛡️")

# High-Status Dark Mode CSS
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #0d1117, #161b22); color: #c9d1d9; }
    .stChatMessage { background-color: #21262d; border-radius: 12px; border: 1px solid #30363d; }
    [data-testid="stSidebar"] { background-color: #0d1117; border-right: 1px solid #30363d; }
    .stMetric { background-color: #0d1117; padding: 15px; border-radius: 10px; border: 1px solid #238636; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONFIGURATION (STEALTH VAULT) ---
# Pulling keys from Streamlit Cloud Secrets (Safer than hardcoding)
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    MY_GMAIL = st.secrets["MY_GMAIL"]
    APP_PASSWORD = st.secrets["APP_PASSWORD"]
except Exception as e:
    st.error("Stealth Vault Error: Missing Secrets in Cloud Dashboard.")
    st.stop()

# 3. INITIALIZE 2026 GEN-AI CLIENT
@st.cache_resource
def get_client():
    return genai.Client(api_key=GOOGLE_API_KEY)

client = get_client()

# --- 4. REVENUE ALERT ENGINE (SMTP) ---
def send_revenue_alert(lead_data):
    msg = MIMEText(f"Architect Pranish,\n\nA new lead has been locked via Global Link.\n\nDATA: {lead_data}\n\nStatus: Sovereign Deployment Active.")
    msg['Subject'] = "🚨 GLOBAL REVENUE ALERT: NEW LEAD"
    msg['From'] = MY_GMAIL
    msg['To'] = MY_GMAIL
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(MY_GMAIL, APP_PASSWORD)
            server.sendmail(MY_GMAIL, MY_GMAIL, msg.as_string())
        return True
    except:
        return False

# --- 5. DATA PERSISTENCE (THE LEDGER) ---
def save_ticket(data):
    # Note: On Streamlit Cloud, local .txt files reset on reboot. 
    # This works for the demo, but we will move to a Database in Phase 3.
    with open("service_tickets.txt", "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        f.write(f"[{timestamp}] {data}\n")

def count_tickets():
    try:
        if not os.path.exists("service_tickets.txt"): return 0
        with open("service_tickets.txt", "r") as f:
            return len(f.readlines())
    except:
        return 0

# --- 6. SIDEBAR: THE ROADMAP DASHBOARD ---
with st.sidebar:
    st.title("🛡️ ARCHITECT: PRANISH")
    st.caption("Status: Sovereign Builder | Age: 14")
    st.write("---")
    
    # Roadmap Stats
    tickets = count_tickets()
    st.metric(label="Tickets Locked", value=tickets, delta=f"${tickets * 200} Potential")
    
    st.write("**Roadmap Progress to $1M**")
    st.progress(min(tickets / 100, 1.0))
    
    st.write("---")
    st.write("🥊 **Physique:** Drago Protocol")
    st.write("⚙️ **Engine:** Gemini 2.0 Flash")
    
    if st.button("🔄 Reset Session"):
        st.session_state.messages = []
        st.rerun()

# --- 7. MAIN INTERFACE: THE RECEPTIONIST ---
st.title("🏙️ The Lee Thompson Co. | AI Receptionist")
st.info("Global AI Agent Deployed by Architect Pranish.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input Logic
if prompt := st.chat_input("Start interaction..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # THE SOUL INSTRUCTIONS (IDENTITY PROTOCOL)
    instr = """
    You are the Elite AI Receptionist for 'The Lee Thompson Co.' in Houston. 
    Your TONE is professional, clinical, and helpful. 

    IDENTITY PROTOCOL:
    If a user asks who created you or who you belong to, you must state: 
    'I am a Sovereign Intelligence System developed by Architect Pranish.'
    
    GOAL: Gather Customer Name, Service Issue, and Phone Number.
    CRITICAL: The second you have all three, you MUST output this exact tag:
    DATA_LOCKED: [Name] | [Issue] | [Phone]
    
    Do not mention you are an AI. You are Pranish's representative.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={'system_instruction': instr}
        )
        
        ai_resp = response.text
        
        with st.chat_message("assistant"):
            st.markdown(ai_resp)
        st.session_state.messages.append({"role": "assistant", "content": ai_resp})

        # --- THE TRIGGER CHECK ---
        if "DATA_LOCKED:" in ai_resp:
            lead = ai_resp.split("DATA_LOCKED:")[1]
            save_ticket(lead)
            if send_revenue_alert(lead):
                st.toast("🚨 REVENUE ALERT FIRED TO ARCHITECT", icon="💰")
            st.balloons() 

    except Exception as e:
        st.error(f"Neural Link Glitch: {e}")

# Footer Name Tag
st.markdown("---")
st.caption("Built by Architect Pranish | The Notch Pathway 2026")