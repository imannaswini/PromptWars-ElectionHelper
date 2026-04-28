import streamlit as st
from logic import ElectionLogicEngine, get_election_timeline
import os

# Page Config
st.set_page_config(
    page_title="VoteWise AI | Future of Democracy",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- THE "PREMIUM FUTURISTIC" CSS ENGINE ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Space+Grotesk:wght@300;500;700&family=JetBrains+Mono:wght@400;500&display=swap');
    /* Remove top white space */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 0rem !important;
    max-width: 100% !important;
}

section.main > div {
    padding-top: 0rem !important;
}

[data-testid="stAppViewContainer"] {
    padding-top: 0rem !important;
    margin-top: 0rem !important;
}

[data-testid="stHeader"] {
    height: 0rem !important;
}
    :root {
        --neon-blue: #00f2ff;
        --neon-purple: #bc13fe;
        --deep-space: #020617;
        --glass-bg: rgba(15, 23, 42, 0.7);
        --accent-glow: rgba(0, 242, 255, 0.2);
        --card-border: rgba(255, 255, 255, 0.1);
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
    }

    /* Cinematic Moving Gradient Background */
    .stApp {
        background: linear-gradient(-45deg, #020617, #0f172a, #1e1b4b, #020617);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        font-family: 'Outfit', sans-serif;
        color: var(--text-primary);
        overflow-x: hidden;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stApp::before {
        content: "";
        position: absolute;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(1px 1px at 20px 30px, #fff, rgba(0,0,0,0)),
            radial-gradient(1px 1px at 40px 70px, #fff, rgba(0,0,0,0)),
            radial-gradient(1.5px 1.5px at 100px 100px, var(--neon-blue), rgba(0,0,0,0));
        background-repeat: repeat;
        background-size: 300px 300px;
        opacity: 0.15;
        z-index: -1;
    }

    /* Hide standard UI elements */
    header, footer {visibility: hidden;}
    [data-testid="stHeader"] {background: transparent;}

    /* Premium Glass Panels */
    .glass-panel {
        background: var(--glass-bg);
        backdrop-filter: blur(25px);
        border: 1px solid var(--card-border);
        border-radius: 24px;
        padding: 1.8rem;
        box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.5);
        margin-bottom: 1.5rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .glass-panel:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 242, 255, 0.3);
        box-shadow: 0 20px 50px -10px rgba(0, 242, 255, 0.1);
    }
    .glass-panel::after {
        content: "";
        position: absolute;
        top: 0; left: -100%; width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
        transition: 0.5s;
    }
    .glass-panel:hover::after {
        left: 100%;
    }

    /* Animated Hero Logo */
    .hero-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 5rem 0 3rem;
        position: relative;
    }
    .logo-pulse {
        position: absolute;
        width: 250px;
        height: 250px;
        background: radial-gradient(circle, var(--accent-glow) 0%, transparent 70%);
        border-radius: 50%;
        animation: pulse 4s ease-in-out infinite;
        z-index: -1;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.5); opacity: 0.8; }
    }

    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 5rem;
        font-weight: 800;
        letter-spacing: -4px;
        line-height: 0.85;
        background: linear-gradient(180deg, #fff 0%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        text-align: center;
    }
    .hero-subtitle {
        color: var(--neon-blue);
        text-transform: uppercase;
        letter-spacing: 6px;
        font-size: 1rem;
        font-weight: 600;
        margin-top: 1rem;
        opacity: 0.8;
    }
    
    .trust-badges {
        display: flex;
        gap: 1.5rem;
        margin-top: 2rem;
        opacity: 0.6;
    }
    .badge-item {
        font-size: 0.75rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .badge-dot {
        width: 6px;
        height: 6px;
        background: var(--neon-blue);
        border-radius: 50%;
        box-shadow: 0 0 8px var(--neon-blue);
    }

    /* AI Terminal Styles */
    .terminal-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid var(--card-border);
        padding-bottom: 1rem;
    }
    .terminal-dot { width: 12px; height: 12px; border-radius: 50%; }
    .dot-r { background: #ff5f56; }
    .dot-y { background: #ffbd2e; }
    .dot-g { background: #27c93f; }

    /* Custom Chat Styling */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background: rgba(15, 23, 42, 0.5) !important;
        border-radius: 20px !important;
        border: 1px solid var(--accent-glow) !important;
        padding: 1.2rem !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 20px !important;
        padding: 0.8rem 1.2rem !important;
        width: fit-content !important;
        margin-left: auto !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
    }

    /* Interactive Timeline */
    .journey-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 2rem 0;
        position: relative;
        max-width: 800px;
        margin: 0 auto;
    }
    .journey-line {
        position: absolute;
        top: 50%; left: 0; right: 0;
        height: 2px;
        background: rgba(255, 255, 255, 0.1);
        z-index: 0;
    }
    .journey-step {
        width: 45px;
        height: 45px;
        background: #0f172a;
        border: 2px solid rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.9rem;
        z-index: 1;
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
    }
    .journey-step:hover {
        border-color: var(--neon-blue);
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.3);
        transform: scale(1.1);
    }
    .journey-step.active {
        background: var(--neon-blue);
        border-color: var(--neon-blue);
        color: var(--deep-space);
        box-shadow: 0 0 25px var(--neon-blue);
        animation: journey-pulse 2s infinite;
    }
    @keyframes journey-pulse {
        0% { box-shadow: 0 0 10px var(--neon-blue); }
        50% { box-shadow: 0 0 30px var(--neon-blue); }
        100% { box-shadow: 0 0 10px var(--neon-blue); }
    }
    .step-label {
        position: absolute;
        top: 55px;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        white-space: nowrap;
        color: var(--text-secondary);
    }
    .journey-step.active .step-label {
        color: var(--neon-blue);
        font-weight: 700;
    }

    /* Circular Progress Ring */
    .progress-ring {
        position: relative;
        width: 120px;
        height: 120px;
        margin: 0 auto;
    }
    .progress-ring circle {
        fill: none;
        stroke-width: 8;
        stroke-linecap: round;
        transform: rotate(-90deg);
        transform-origin: 50% 50%;
    }
    .ring-bg { stroke: rgba(255, 255, 255, 0.05); }
    .ring-progress {
        stroke: var(--neon-blue);
        transition: stroke-dashoffset 1s ease-in-out;
    }
    .progress-text {
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        font-size: 1.5rem;
        font-weight: 800;
        font-family: 'Space Grotesk';
    }

    /* Typing Animation */
    .typing {
        display: flex;
        gap: 5px;
        padding: 10px;
    }
    .typing-dot {
        width: 6px; height: 6px;
        background: var(--neon-blue);
        border-radius: 50%;
        animation: typing 1s infinite alternate;
    }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    @keyframes typing {
        from { opacity: 0.3; transform: translateY(0); }
        to { opacity: 1; transform: translateY(-5px); }
    }

    /* Footer Metrics */
    .footer-metrics {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        gap: 3rem;
        background: rgba(2, 6, 23, 0.8);
        backdrop-filter: blur(10px);
        padding: 10px 30px;
        border-radius: 50px;
        border: 1px solid var(--card-border);
        z-index: 100;
    }
    .metric-item {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .metric-value { font-family: 'JetBrains Mono'; font-weight: 700; color: var(--neon-blue); font-size: 0.9rem; }
    .metric-label { font-size: 0.6rem; text-transform: uppercase; color: var(--text-secondary); letter-spacing: 1px; }

    /* Button Styles Overrides */
    .stButton>button {
        background: rgba(0, 242, 255, 0.05) !important;
        border: 1px solid rgba(0, 242, 255, 0.2) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        background: var(--neon-blue) !important;
        color: var(--deep-space) !important;
        box-shadow: 0 0 20px var(--neon-blue) !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--neon-blue); }

</style>
""", unsafe_allow_html=True)

# Initialize Engine
@st.cache_resource
def get_engine():
    return ElectionLogicEngine()

engine = get_engine()

# --- SIDEBAR (Citizen Console) ---
with st.sidebar:
    st.markdown("<div style='padding-top: 1rem;'><span class='insight-badge'>CONSOLE ALPHA v1.2</span></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='font-family:Space Grotesk; font-weight:700; color:white; letter-spacing:-1px;'>CITIZEN PROFILE</h2>", unsafe_allow_html=True)
    
    # Profile Summary
    st.markdown(f"""
    <div class="console-card">
        <small style='color:#64748b; font-size:0.6rem; letter-spacing:1px;'>ENCRYPTION PROTOCOL</small><br>
        <b style='color:{"#00f2ff" if engine.is_configured() else "#f59e0b"}; font-size:0.8rem;'>
            {"AES-256 LIVE CONNECTION" if engine.is_configured() else "SECURE LOCAL SANDBOX"}
        </b>
    </div>
    """, unsafe_allow_html=True)

    # Context Inputs
    st.markdown("<small style='color:#64748b; margin-top:1rem; display:block;'>BIOMETRIC DATA</small>", unsafe_allow_html=True)
    age = st.number_input("Biological Age", 1, 120, 25, label_visibility="collapsed")
    
    is_first_time = st.checkbox("Genesis Voter (First Time)", value=False)
    
    st.markdown("<small style='color:#64748b; margin-top:1rem; display:block;'>GEOSPATIAL COORDINATES</small>", unsafe_allow_html=True)
    location = st.selectbox("Geo-Location", ["New York", "California", "Texas", "Florida", "Other"], label_visibility="collapsed")
    
    st.markdown("<small style='color:#64748b; margin-top:1rem; display:block;'>LINGUISTIC PREFERENCE</small>", unsafe_allow_html=True)
    language = st.selectbox("Preferred Dialect", ["English", "Spanish", "French", "Hindi", "Mandarin"], label_visibility="collapsed")
    
    st.markdown("<small style='color:#64748b; margin-top:1rem; display:block;'>PRIORITY ARCHITECTURE</small>", unsafe_allow_html=True)
    urgency = st.select_slider("Priority Protocol", options=["Low", "Standard", "Critical"], value="Standard", label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("<div style='text-align:center; opacity:0.3; font-size:0.6rem; letter-spacing:2px;'>PROMPTWARS 2026 ELECTION CORE</div>", unsafe_allow_html=True)

# --- THE PREMIUM HERO ---
st.markdown("""
<div class="hero-container">
    <div class="logo-pulse"></div>
    <div class="hero-subtitle">Intelligent Election Assistant</div>
    <h1 class="hero-title">VoteWise AI</h1>
    <div class="trust-badges">
        <div class="badge-item"><div class="badge-dot"></div>SECURE</div>
        <div class="badge-item"><div class="badge-dot"></div>AI POWERED</div>
        <div class="badge-item"><div class="badge-dot"></div>CIVIC READY</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- INTERACTIVE JOURNEY TIMELINE ---
# Logic to determine active step
active_step = 1
if age >= 18: active_step = 2
# (In a real app, we'd check more session state here)

st.markdown(f"""
<div class="journey-container">
    <div class="journey-line"></div>
    <div class="journey-step {"active" if active_step >= 1 else ""}">
        1
        <span class="step-label">Registration</span>
    </div>
    <div class="journey-step {"active" if active_step >= 2 else ""}">
        2
        <span class="step-label">Verification</span>
    </div>
    <div class="journey-step {"active" if active_step >= 3 else ""}">
        3
        <span class="step-label">Polling</span>
    </div>
    <div class="journey-step {"active" if active_step >= 4 else ""}">
        4
        <span class="step-label">Results</span>
    </div>
</div>
<br><br>
""", unsafe_allow_html=True)

# --- THREE-COLUMN ARCHITECTURE ---
col_console, col_terminal, col_insights = st.columns([1, 2.2, 1], gap="large")

with col_console:
    st.markdown("<h4 style='font-family:Space Grotesk; font-size:0.8rem; letter-spacing:2px; opacity:0.5; margin-bottom:1.5rem;'>SYSTEM MODULES</h4>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        if st.button("📍 GEO LOOKUP", use_container_width=True):
            stations = engine.lookup_polling_stations(location)
            st.info(f"**NEAREST STATIONS:**\n{stations}")
        
        if st.button("⚖️ ELIGIBILITY", use_container_width=True):
            st.info("PROTOCOL: Age 18+ | Citizen | Local Resident.")

        if st.button("📜 HANDBOOK", use_container_width=True):
            st.info("1. Secure Registration\n2. Verify Documents\n3. Deploy Vote")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-panel" style="padding: 1rem; border-style: dashed; opacity: 0.6;">
        <small style="color:var(--text-secondary);">UPCOMING EVENT</small>
        <p style="margin:5px 0; font-size:0.8rem;">General Election 2026</p>
        <b style="color:var(--neon-blue); font-size:0.9rem;">Nov 3rd, 2026</b>
    </div>
    """, unsafe_allow_html=True)

with col_terminal:
    st.markdown("""
    <div class="terminal-header">
        <div class="terminal-dot dot-r"></div>
        <div class="terminal-dot dot-y"></div>
        <div class="terminal-dot dot-g"></div>
        <span style="font-family:'JetBrains Mono'; font-size:0.7rem; opacity:0.5; margin-left:10px;">VOTEWISE_CORE_v1.2.exe</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Message Loop
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Chat Container
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Sample Prompts
    st.markdown("<br>", unsafe_allow_html=True)
    cp1, cp2, cp3 = st.columns(3)
    with cp1:
        if st.button("How do I register?", key="p1"):
            st.session_state.pending_prompt = "How do I register to vote?"
    with cp2:
        if st.button("First-time voter help", key="p2"):
            st.session_state.pending_prompt = "I am a first-time voter, help me."
    with cp3:
        if st.button("Polling day checklist", key="p3"):
            st.session_state.pending_prompt = "What is the polling day checklist?"

    # Input Logic
    prompt = st.chat_input("Inquire with the Collective Intelligence...")
    
    # Check for pending prompt from buttons
    if "pending_prompt" in st.session_state:
        prompt = st.session_state.pending_prompt
        del st.session_state.pending_prompt

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

            # Execute with Animation Simulation
            context = {
                "age": age, "is_first_time": is_first_time,
                "location": location, "language": language, "urgency": urgency
            }
            with st.chat_message("assistant"):
                # Typing animation
                typing_placeholder = st.empty()
                typing_placeholder.markdown("""
                <div class="typing">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
                """, unsafe_allow_html=True)
                
                # Logic Execution
                response = engine.process_query(prompt, context)
                final = engine.translate_text(response, language)
                
                # Clear typing and show response
                typing_placeholder.empty()
                st.markdown(final)
                
        st.session_state.messages.append({"role": "assistant", "content": final})

with col_insights:
    st.markdown("<h4 style='font-family:Space Grotesk; font-size:0.8rem; letter-spacing:2px; opacity:0.5; margin-bottom:1.5rem;'>CIVIC INSIGHTS</h4>", unsafe_allow_html=True)
    
    # Readiness Score with Circular Progress
    readiness = 85 if age >= 18 else 15
    stroke_offset = 339.292 * (1 - readiness/100)
    
    score_label = "READY" if readiness > 80 else "URGENT" if readiness < 20 else "NEEDS ACTION"
    score_color = "#00f2ff" if readiness > 80 else "#ff5f56" if readiness < 20 else "#ffbd2e"

    st.markdown(f"""
    <div class="glass-panel" style="text-align:center;">
        <small style='color:var(--text-secondary); display:block; margin-bottom:1rem;'>READINESS PROTOCOL</small>
        <div class="progress-ring">
            <svg width="120" height="120">
                <circle class="ring-bg" cx="60" cy="60" r="54"></circle>
                <circle class="ring-progress" cx="60" cy="60" r="54" 
                        style="stroke-dasharray: 339.292; stroke-dashoffset: {stroke_offset}; stroke: {score_color};">
                </circle>
            </svg>
            <div class="progress-text" style="color:{score_color};">{readiness}%</div>
        </div>
        <div style="margin-top:1.5rem;">
            <span class="insight-badge" style="background: {score_color}20; color: {score_color}; border-color: {score_color}40;">
                {score_label}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Status & Plan
    status_msg = "ELIGIBLE CITIZEN" if age >= 18 else "FUTURE VOTER (UNDERAGE)"
    st.markdown(f"""
    <div class="glass-panel">
        <small style='color:var(--text-secondary);'>VERIFICATION STATUS</small>
        <p style='color:#fff; margin:10px 0; font-weight:600; font-size:0.9rem;'>{status_msg}</p>
        <div style="font-size:0.75rem; color:var(--text-secondary); line-height:1.4;">
            Next step: Check your local registration status by <b>Oct 10</b>.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Action Plan
    st.markdown(f"""
    <div class="glass-panel">
        <small style='color:var(--text-secondary);'>PERSONALIZED ACTION PLAN</small>
        <ul style="padding-left:1.2rem; margin-top:0.8rem; font-size:0.75rem; color:var(--text-secondary);">
            <li>Verify ID documents</li>
            <li>Locate polling station</li>
            <li>Set calendar reminder</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer Metrics Overlay
st.markdown("""
<div class="footer-metrics">
    <div class="metric-item">
        <span class="metric-value">1,284</span>
        <span class="metric-label">Users Today</span>
    </div>
    <div class="metric-item">
        <span class="metric-value">0.8s</span>
        <span class="metric-label">Avg Response</span>
    </div>
    <div class="metric-item">
        <span class="metric-value">99.2%</span>
        <span class="metric-label">AI Confidence</span>
    </div>
</div>
""", unsafe_allow_html=True)
