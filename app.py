import streamlit as st
from logic import ElectionLogicEngine

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="VoteWise AI | Future of Democracy",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------
# LOAD ENGINE
# -----------------------------------
@st.cache_resource
def get_engine():
    return ElectionLogicEngine()

engine = get_engine()

# -----------------------------------
# SESSION STATE
# -----------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

# -----------------------------------
# SIMPLE CSS (KEEP YOUR FULL CSS IF YOU WANT)
# -----------------------------------
st.markdown("""
<style>
body, .stApp {
    background: linear-gradient(135deg,#020617,#0f172a,#111827);
    color:white;
}
.block-container {
    padding-top:1rem !important;
    max-width:100% !important;
}
.glass-panel {
    background: rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:20px;
    padding:1.2rem;
    margin-bottom:1rem;
    backdrop-filter: blur(10px);
}
.hero-title {
    text-align:center;
    font-size:4rem;
    font-weight:800;
    margin-bottom:0;
}
.hero-sub {
    text-align:center;
    color:#00f2ff;
    margin-bottom:2rem;
}
.stButton>button {
    width:100%;
    border-radius:12px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# SIDEBAR
# -----------------------------------
with st.sidebar:
    st.markdown("## CITIZEN PROFILE")

    age = st.number_input("Age", 1, 120, 25)
    is_first_time = st.checkbox("First-time voter", False)

    location = st.selectbox(
        "Location",
        ["New York", "California", "Texas", "Florida", "Other"]
    )

    language = st.selectbox(
        "Language",
        ["English", "Spanish", "French", "Hindi", "Mandarin"]
    )

    urgency = st.select_slider(
        "Urgency",
        ["Low", "Standard", "Critical"],
        value="Standard"
    )

# -----------------------------------
# HERO
# -----------------------------------
st.markdown("<h1 class='hero-title'>VoteWise AI</h1>", unsafe_allow_html=True)
st.markdown("<div class='hero-sub'>Intelligent Election Assistant</div>", unsafe_allow_html=True)

# -----------------------------------
# LAYOUT
# -----------------------------------
col_console, col_terminal, col_insights = st.columns([1, 2.2, 1], gap="large")

# ===================================
# LEFT PANEL
# ===================================
with col_console:
    st.markdown("### SYSTEM MODULES")

    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)

    if st.button("📍 GEO LOOKUP", key="geo_lookup"):
        st.session_state.pending_prompt = f"Where is my polling station in {location}?"

    if st.button("⚖️ ELIGIBILITY", key="eligibility"):
        st.session_state.pending_prompt = f"Am I eligible to vote in {location}? I am {age} years old."

    if st.button("📜 HANDBOOK", key="handbook"):
        st.session_state.pending_prompt = "Give me a beginner handbook for first-time voters."

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-panel">
        <small>UPCOMING EVENT</small><br>
        <b>General Election 2026</b><br>
        Nov 3rd, 2026
    </div>
    """, unsafe_allow_html=True)

# ===================================
# CENTER PANEL
# ===================================
with col_terminal:
    st.markdown("### VoteWise Terminal")

    # Chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Quick prompts
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("How do I register?", key="p1"):
            st.session_state.pending_prompt = "How do I register to vote?"

    with c2:
        if st.button("First-time help", key="p2"):
            st.session_state.pending_prompt = "I am a first-time voter. Help me."

    with c3:
        if st.button("Polling checklist", key="p3"):
            st.session_state.pending_prompt = "What is the polling day checklist?"

    # Chat input
    prompt = st.chat_input("Ask VoteWise anything...")

    # Use button prompt if clicked
    if st.session_state.pending_prompt:
        prompt = st.session_state.pending_prompt
        st.session_state.pending_prompt = None

    # Run prompt
    if prompt:
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        context = {
            "age": age,
            "is_first_time": is_first_time,
            "location": location,
            "language": language,
            "urgency": urgency
        }

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = engine.process_query(prompt, context)
                final = engine.translate_text(response, language)
                st.markdown(final)

        st.session_state.messages.append({
            "role": "assistant",
            "content": final
        })

# ===================================
# RIGHT PANEL
# ===================================
with col_insights:
    st.markdown("### CIVIC INSIGHTS")

    readiness = 85 if age >= 18 else 15

    st.markdown(f"""
    <div class="glass-panel">
        <small>READINESS SCORE</small><br>
        <h1>{readiness}%</h1>
    </div>
    """, unsafe_allow_html=True)

    status = "ELIGIBLE CITIZEN" if age >= 18 else "UNDERAGE / FUTURE VOTER"

    st.markdown(f"""
    <div class="glass-panel">
        <small>STATUS</small><br>
        <b>{status}</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-panel">
        <small>ACTION PLAN</small>
        <ul>
            <li>Verify ID</li>
            <li>Check registration</li>
            <li>Find polling place</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)