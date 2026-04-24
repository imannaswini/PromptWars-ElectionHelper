import streamlit as st
from logic import ElectionLogicEngine, get_election_timeline
import os

# Page Config
st.set_page_config(
    page_title="VoteWise | Election Helper",
    page_icon="🗳️",
    layout="wide"
)

# Custom CSS for modern look
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
    .timeline-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #ffffff;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Logic Engine
engine = ElectionLogicEngine()

# Sidebar for Context
st.sidebar.title("👤 Voter Context")
st.sidebar.info("Tell us about yourself for better assistance.")

age = st.sidebar.number_input("Age", min_value=1, max_value=120, value=25)
is_first_time = st.sidebar.checkbox("First-time voter?", value=False)
location = st.sidebar.selectbox("Location (State)", ["New York", "California", "Texas", "Florida", "Other"])
language = st.sidebar.selectbox("Language Preference", ["English", "Spanish", "French", "Hindi", "Mandarin"])
urgency = st.sidebar.select_slider("Urgency Level", options=["Low", "Normal", "High"], value="Normal")

# Main Header
st.title("🗳️ VoteWise: Your Election Assistant")
st.markdown("---")

# Layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Ask Anything about the Election")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("How do I register to vote?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Prepare Context
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
                # Apply mock translation
                translated_response = engine.translate_text(response, language)
                st.markdown(translated_response)
        
        st.session_state.messages.append({"role": "assistant", "content": translated_response})

with col2:
    st.subheader("📅 Key Dates")
    timeline = get_election_timeline()
    for event, date in timeline.items():
        st.markdown(f"""
        <div class="timeline-card">
            <strong>{event}</strong><br>
            <span style="color: #007bff;">{date}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📍 Polling Station Lookup")
    if st.button("Find Nearest Stations"):
        stations = engine.lookup_polling_stations(location)
        st.success(f"Stations in {location}:")
        st.info(stations)

    st.markdown("---")
    st.subheader("📜 Quick Guides")
    if st.button("Eligibility Guide"):
        st.info("General eligibility: 18+ years old, Citizen, Resident of your state.")
    if st.button("Registration Steps"):
        st.info("1. Verify Eligibility\n2. Fill Application\n3. Submit to Election Office")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>Built for PromptWars | Powered by Gemini & Google Services</p>", unsafe_allow_html=True)
