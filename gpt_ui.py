import streamlit as st
import model
from PIL import Image

# Load your logo (update the path as needed)
footer_logo = Image.open("S:/Luddy Hackathon/Project Logo.png")

# === Page setup ===
st.set_page_config(page_title="EduPilot", layout="wide")

st.markdown("""
    <style>
    /* Sidebar background color */
    [data-testid="stSidebar"] {
        background-color: #0C4F80;
    }

    [data-testid="stSidebar"] > div:first-child {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# === Session state ===
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "text": "👋 Hi! I'm your Smart Course Recommender. Tell me about your career goals and I’ll suggest the right courses!"}
    ]

# === Custom CSS Theme ===
st.markdown("""
    <style>
    body {
        background-color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
    }
    .blue-header {
        background-color: #0C4F80;
        color: white;
        padding: 1.5rem;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.4);
    }
    .user-msg, .bot-msg {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 80%;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }
    .user-msg {
        background-color: #e6f7ff;
        text-align: right;
        max-width: 60%;
        padding: 10px;
        border-radius: 10px;
        align-self: flex-end;
    }
    .bot-msg {
        background-color: #f0f0f0;
        align-self: flex-start;
        margin-right: auto;
        padding: 10px;
        border-radius: 10px;
        max-width: 60%;
        font size: 50px;
    }

    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    </style>
""", unsafe_allow_html=True)

# === Header ===
st.markdown("<div class='blue-header'>EduPilot 🚀</div>", unsafe_allow_html=True)


# === Chat area ===
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    is_user = msg["role"] == "user"
    role_class = "user-msg" if is_user else "bot-msg"
    icon_url = (
        "https://cdn-icons-png.flaticon.com/512/3899/3899618.png"
        if is_user
        else "https://cdn-icons-png.flaticon.com/512/10479/10479785.png"
    )
    align_style = "row-reverse" if is_user else "row"

    st.markdown(f"""
        <div style="display: flex; flex-direction: {align_style}; align-items: flex-start; margin-bottom: 10px;">
            <img src="{icon_url}" style="width: 30px; height: 30px; margin: 0 10px;">
            <div class="{role_class}">
                {msg['text']}
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)



# === Message input ===
with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([18, 1])
    user_input = col1.text_input("Type your message", placeholder="Tell me about your goals (e.g. I want to be a data analyst)", label_visibility="collapsed")
    submitted = col2.form_submit_button("➤")

if submitted and user_input:
    st.session_state.messages.append({"role": "user", "text": user_input})
    with st.spinner("Thinking..."):
        try:
            reply = model.get_recommendations_from_input(
                user_input,
                api_key="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"
            )
        except Exception as e:
            st.error("⚠ Something went wrong while generating your recommendations.")
            st.exception(e)
            reply = "Sorry, something went wrong. Please try again later."
    st.session_state.messages.append({"role": "bot", "text": reply})
    st.rerun()

# === Sidebar ===
st.sidebar.markdown("""
    <div style='text-align: center'>
        <img 
            src="https://iuself.iu.edu/cs/SSERV/cache/IU_BL_WHITE_BRAND_1.PNG" 
            alt="Bloomington go to Springboard" 
            title="Go to Springboard"
            style="max-width: 100%; max-height: 110px; transition: height 0.5s, width 0.5s; margin-bottom: 50px;">
        <h3 style='color: white;'>🤵🏻 John Smith</h3>
        <p style='color: white;'><strong>Profession:</strong> Student</p>
        <p style='color: white;'><strong>Skills:</strong> Python, SQL, PowerBi</p>            
    </div>
""", unsafe_allow_html=True)

# === Dashboards dropdown ===

# === Dashboards dropdown styling ===
with st.sidebar:
    # Dashboards dropdown
    with st.expander("📊 Dashboards", expanded=False):
        st.markdown("""
           <style>
.dashboard-link {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: white;
    color: white;
    padding: 10px 0;
    font-weight: 500;
    text-decoration: none;
    border-radius: 4px;
    transition: background-color 0.2s, padding-left 0.2s;
}

div[data-testid="stExpander"] {
    background-color: white;
    border-radius: 8px;
    padding: 0px;
}

div[data-testid="stExpander"] > summary {
    background-color: white;
    color: black;
    border-radius: 8px;
    padding: 10px;
    transition: background-color 0.2s ease;
    font-size: 80px !important;                
}

div[data-testid="stExpander"] > summary:hover {
    background-color: #f0f0f0;
}

div[data-testid="stExpander"][aria-expanded="true"] > summary {
    background-color: white;
}

.dashboard-link a {
    color: black;
    text-decoration: none;
    flex-grow: 1;
}

.dashboard-link:hover {
    background-color: white;
    padding-left: 5px;
    color: black;
}

.dashboard-link:hover a {
    color: black;
}
</style>

<div class="dashboard-link">
    <a href="https://app.powerbi.com/view?r=eyJrIjoiMWM3NzI1ZTQtNDY0Zi00ZWYwLTg0NzQtYzI4NGY1ODY5ZGQ5IiwidCI6IjExMTNiZTM0LWFlZDEtNGQwMC1hYjRiLWNkZDAyNTEwYmU5MSIsImMiOjN9" target="_blank">📘 Course Dashboard</a>
</div>

<div class="dashboard-link">
    <a href="https://app.powerbi.com/view?r=eyJrIjoiNGE5ZjZlODUtMDhkMi00ZTE0LWEwOTMtMWMwZWM2NzYyMDkzIiwidCI6IjExMTNiZTM0LWFlZDEtNGQwMC1hYjRiLWNkZDAyNTEwYmU5MSIsImMiOjN9" target="_blank">🧑‍🏫 Professor Dashboard</a>
</div>
        """, unsafe_allow_html=True)

    # All Courses dropdown
    with st.expander("📚 All Courses", expanded=False):
        st.markdown("""
<div class="dashboard-link">
    <a href="https://indiana-my.sharepoint.com/:w:/g/personal/samarath_iu_edu/Ec5bV9dxGE9Bp74-UTtS3K0BjI-PsuHqS30fZ-CjZpputQ?e=6EaKF8" target="_blank">🗂️ Course Catalog</a>
</div>
        """, unsafe_allow_html=True)

    # Enrollment Resource Guide dropdown
    with st.expander("📚 Enrollment Guide", expanded=False):
        st.markdown("""
<div class="dashboard-link">
    <a href="https://indiana-my.sharepoint.com/personal/samarath_iu_edu/Documents/Enrollment%20Guide%20and%20Slide%20Deck%20-%20MSDS.pdf?login_hint=samarath%40iu.edu" target="_blank">🗂️ Enrollment Guide</a>
</div>
        """, unsafe_allow_html=True)