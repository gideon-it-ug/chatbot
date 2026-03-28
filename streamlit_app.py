import streamlit as st
import google.generativeai as genai

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ORA · AI Assistant",
    page_icon="◈",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:ital,wght@0,300;0,400;1,300&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    color: #e8e4dc !important;
    font-family: 'DM Mono', monospace !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(255,200,80,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 80% 80%, rgba(255,100,60,0.05) 0%, transparent 50%),
        #0a0a0f !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none !important; }

/* ── Main container ── */
.block-container {
    max-width: 760px !important;
    padding: 3rem 2rem 6rem !important;
    margin: 0 auto !important;
}

/* ── Hero Header ── */
.ora-header {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
    position: relative;
}
.ora-header::before {
    content: '';
    display: block;
    width: 1px;
    height: 60px;
    background: linear-gradient(to bottom, transparent, rgba(255,200,80,0.6));
    margin: 0 auto 2rem;
}
.ora-logo {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 3.8rem;
    letter-spacing: -0.04em;
    background: linear-gradient(135deg, #ffc850 0%, #ff6c3c 60%, #e8e4dc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin-bottom: 0.4rem;
}
.ora-tagline {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    font-weight: 300;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: rgba(232,228,220,0.35);
}
.ora-divider {
    width: 100%;
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(255,200,80,0.3), transparent);
    margin: 2.5rem 0;
}

/* ── API Key Input ── */
[data-testid="stTextInput"] > div > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,200,80,0.2) !important;
    border-radius: 4px !important;
    color: #e8e4dc !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
    transition: border-color 0.2s ease !important;
}
[data-testid="stTextInput"] > div > div:focus-within {
    border-color: rgba(255,200,80,0.6) !important;
    box-shadow: 0 0 0 3px rgba(255,200,80,0.06) !important;
}
[data-testid="stTextInput"] input {
    color: #e8e4dc !important;
    font-family: 'DM Mono', monospace !important;
}
[data-testid="stTextInput"] label {
    color: rgba(232,228,220,0.5) !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    font-family: 'DM Mono', monospace !important;
}

/* ── Info / Alert boxes ── */
[data-testid="stAlert"] {
    background: rgba(255,200,80,0.05) !important;
    border: 1px solid rgba(255,200,80,0.2) !important;
    border-radius: 4px !important;
    color: rgba(232,228,220,0.6) !important;
    font-size: 0.78rem !important;
    font-family: 'DM Mono', monospace !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
    gap: 0 !important;
}

/* User bubble */
[data-testid="stChatMessage"][data-testid*="user"],
.stChatMessage:has([data-testid="chatAvatarIcon-user"]) {
    flex-direction: row-reverse !important;
}

/* Avatar icons */
[data-testid="chatAvatarIcon-user"] > div,
[data-testid="chatAvatarIcon-assistant"] > div {
    width: 28px !important;
    height: 28px !important;
    border-radius: 4px !important;
    font-size: 0.7rem !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
}
[data-testid="chatAvatarIcon-user"] > div {
    background: rgba(255,200,80,0.15) !important;
    border: 1px solid rgba(255,200,80,0.3) !important;
    color: #ffc850 !important;
}
[data-testid="chatAvatarIcon-assistant"] > div {
    background: rgba(255,108,60,0.12) !important;
    border: 1px solid rgba(255,108,60,0.25) !important;
    color: #ff6c3c !important;
}

/* Message content */
[data-testid="stChatMessage"] .stMarkdown {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 6px !important;
    padding: 0.85rem 1.1rem !important;
    font-size: 0.88rem !important;
    line-height: 1.7 !important;
    color: #e8e4dc !important;
    font-family: 'DM Mono', monospace !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown {
    background: rgba(255,200,80,0.06) !important;
    border-color: rgba(255,200,80,0.15) !important;
}

/* ── Chat input ── */
[data-testid="stChatInputContainer"] {
    background: rgba(10,10,15,0.95) !important;
    border-top: 1px solid rgba(255,255,255,0.06) !important;
    backdrop-filter: blur(20px) !important;
    padding: 1rem 2rem !important;
}
[data-testid="stChatInput"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 6px !important;
    color: #e8e4dc !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.88rem !important;
    transition: border-color 0.2s ease !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: rgba(255,200,80,0.4) !important;
    box-shadow: 0 0 0 3px rgba(255,200,80,0.05) !important;
}

/* Send button */
[data-testid="stChatInputSubmitButton"] button {
    background: linear-gradient(135deg, #ffc850, #ff6c3c) !important;
    border: none !important;
    border-radius: 4px !important;
    color: #0a0a0f !important;
    transition: opacity 0.2s ease !important;
}
[data-testid="stChatInputSubmitButton"] button:hover {
    opacity: 0.85 !important;
}

/* ── Select / Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 4px !important;
    color: #e8e4dc !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
}
[data-testid="stSelectbox"] label {
    color: rgba(232,228,220,0.5) !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    font-family: 'DM Mono', monospace !important;
}

/* ── Columns gap ── */
[data-testid="stHorizontalBlock"] { gap: 1rem !important; }

/* ── Spinner ── */
[data-testid="stSpinner"] { color: #ffc850 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,200,80,0.2); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ora-header">
    <div class="ora-logo">ORA</div>
    <div class="ora-tagline">Intelligent Conversation · Powered by Claude</div>
</div>
<div class="ora-divider"></div>
""", unsafe_allow_html=True)

# ── Password login wall ─────────────────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 2rem;">
        <div style="font-family:'DM Mono',monospace; font-size:0.72rem; letter-spacing:0.2em;
                    text-transform:uppercase; color:rgba(232,228,220,0.35); margin-bottom:1.5rem;">
            Access Required
        </div>
    </div>
    """, unsafe_allow_html=True)
    pwd = st.text_input("Password", type="password", placeholder="Enter access password…")
    if st.button("Enter", use_container_width=True):
        if pwd == st.secrets.get("APP_PASSWORD", "ora2024"):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    st.stop()

# ── API key from secrets (no user input needed) ─────────────────────────────────
api_key = st.secrets.get("GEMINI_API_KEY", "")
if not api_key:
    st.error("API key not configured. Add GEMINI_API_KEY to your Streamlit secrets.")
    st.stop()

# ── Sidebar / Settings ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ◈ Settings")
    system_prompt = st.text_area(
        "System Prompt",
        value="You are ORA, a razor-sharp, insightful AI assistant. Be concise, precise, and occasionally brilliant. Avoid filler phrases.",
        height=120,
        help="Define ORA's personality and behaviour."
    )
    model_choice = st.selectbox(
        "Model",
        ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash"],
        index=1,
    )
    max_tokens = st.slider("Max tokens", 256, 4096, 1024, 128)
    if st.button("🗑 Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    if st.button("🔒 Log out", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.messages = []
        st.rerun()

# ── Session state ───────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Render history ──────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🙂" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])

# ── Chat input ──────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask anything…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🙂"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name=model_choice,
            system_instruction=system_prompt,
        )
        # Build history for Gemini (exclude last user message, already appended)
        history = []
        for m in st.session_state.messages[:-1]:
            role = "user" if m["role"] == "user" else "model"
            history.append({"role": role, "parts": [m["content"]]})
        chat = model.start_chat(history=history)
        response_placeholder = st.empty()
        full_response = ""
        for chunk in chat.send_message_stream(prompt, generation_config={"max_output_tokens": max_tokens}):
            full_response += chunk.text
            response_placeholder.markdown(full_response + "▍")
        response_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
