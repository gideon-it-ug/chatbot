# ◈ ORA — AI Chat Assistant

A sleek, production-grade conversational AI built with Streamlit and powered by **Anthropic's Claude** models. Features real-time streaming, a dark editorial UI, and a configurable system prompt.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

---

## Features

- 🔮 **Powered by Claude** — choose between Opus, Sonnet, or Haiku
- ⚡ **Streaming responses** — text appears in real time
- 🎨 **Distinctive dark UI** — custom typography and amber/orange accents
- 🛠 **Configurable** — edit the system prompt, model, and token limit from the sidebar
- 💬 **Full conversation memory** — all turns sent as context each request

---

## How to run it on your own machine

### 1. Clone the repo

```bash
git clone https://github.com/gideon-it-ug/chatbot.git
cd chatbot
```

### 2. Install the requirements

```bash
pip install -r requirements.txt
```

### 3. Get an Anthropic API key

Sign up at [console.anthropic.com](https://console.anthropic.com) and create an API key.

### 4. Run the app

```bash
streamlit run streamlit_app.py
```

Enter your API key (`sk-ant-…`) in the input field when the app opens.

---

## Project structure

```
chatbot/
├── streamlit_app.py   # Main application
├── requirements.txt   # Python dependencies
└── README.md
```

---

## License

Apache 2.0 — see [LICENSE](LICENSE) for details.
