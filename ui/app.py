# import streamlit as st
# import requests

# API_URL = "http://127.0.0.1:8000/chat"

# st.set_page_config(
#     page_title="TaskFlow Support Assistant",
#     page_icon="💬",
# )

# st.title("TaskFlow Support Assistant")
# st.caption("Ask questions about TaskFlow support documentation.")

# if "messages" not in st.session_state:
#     st.session_state.messages = []


# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.write(message["content"])


# question = st.chat_input("Ask a TaskFlow question...")

# if question:
#     st.session_state.messages.append({
#         "role": "user",
#         "content": question,
#     })

#     with st.chat_message("user"):
#         st.write(question)

#     payload = {
#         "question": question,
#         "history": st.session_state.messages[:-1],
#     }

#     response = requests.post(
#         API_URL,
#         json=payload,
#         timeout=60,
#     )

#     # st.write("STATUS:", response.status_code)
#     # st.write("RAW RESPONSE:", response.text)

#     if not response.text.strip():
#         st.error("FastAPI returned an empty response.")
#         st.stop()

#     try:
#         data = response.json()
#     except Exception:
#         st.error("FastAPI did not return valid JSON.")
#         st.stop()

#     answer = data["answer"]
#     sources = data.get("sources", [])

#     with st.chat_message("assistant"):
#         st.write(answer)

#         if sources:
#             st.write("Sources:")

#             for source in sources:
#                 st.write(
#                     f"- {source['title']} "
#                     f"({source['source_path']})"
#                 )

#     st.session_state.messages.append({
#         "role": "assistant",
#         "content": answer,
#     })

import html

import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/chat"


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="TaskFlow Support",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# STYLES
# =========================================================

st.markdown(
    """
<style>

/* =========================================================
   GLOBAL
   ========================================================= */

html,
body,
[class*="css"] {
    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}

html,
body,
.stApp {
    min-height: 100vh;
}

.stApp {
    background:
        radial-gradient(
            circle at 55% -10%,
            rgba(99, 102, 241, 0.13),
            transparent 34%
        ),
        #090c12;

    color: #f5f7fb;
}


/* Remove centered Streamlit page constraint */

[data-testid="stMainBlockContainer"] {
    width: 100% !important;
    max-width: none !important;

    padding-top: 2rem !important;
    padding-left: 3rem !important;
    padding-right: 3rem !important;
    padding-bottom: 7rem !important;
}

.block-container {
    width: 100% !important;
    max-width: none !important;
}


/* =========================================================
   HIDE STREAMLIT CHROME
   ========================================================= */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

[data-testid="stSidebar"] {
    width: 300px !important;
    min-width: 300px !important;

    background: #0c1017;

    border-right: 1px solid #1c2330;
}

[data-testid="stSidebar"] > div:first-child {
    width: 300px !important;
}

[data-testid="stSidebar"] .block-container {
    width: 100% !important;
    max-width: none !important;

    padding: 2rem 1.35rem !important;
}

.sidebar-brand {
    color: #f5f7fb;

    font-size: 20px;
    font-weight: 760;

    letter-spacing: -0.4px;
}

.sidebar-copy {
    margin-top: 8px;

    color: #8b95a6;

    font-size: 13px;
    line-height: 1.65;
}

.sidebar-label {
    margin-top: 4px;
    margin-bottom: 11px;

    color: #626d7e;

    font-size: 10px;
    font-weight: 750;

    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.example-question {
    margin-bottom: 8px;

    padding: 11px 12px;

    border: 1px solid #202835;
    border-radius: 10px;

    background: #111720;

    color: #aeb6c4;

    font-size: 12px;
    line-height: 1.45;
}

.sidebar-footer {
    margin-top: 28px;

    color: #5f697a;

    font-size: 11px;
    line-height: 1.65;
}


/* =========================================================
   MAIN WORKSPACE
   ========================================================= */

.main-shell {
    width: 100%;
}

.app-header {
    width: 100%;

    display: flex;
    align-items: center;

    gap: 16px;

    margin-bottom: 32px;

    padding-bottom: 24px;

    border-bottom: 1px solid #1b2230;
}

.brand-mark {
    width: 50px;
    height: 50px;

    flex-shrink: 0;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 14px;

    background: linear-gradient(
        145deg,
        #818cf8,
        #6366f1
    );

    color: #ffffff;

    font-size: 21px;
    font-weight: 800;

    box-shadow:
        0 10px 28px rgba(99, 102, 241, 0.22);
}

.header-content {
    flex: 1;
}

.app-title {
    margin: 0;

    color: #f8fafc;

    font-size: 30px;
    line-height: 1.15;

    font-weight: 760;

    letter-spacing: -0.9px;
}

.app-subtitle {
    margin: 6px 0 0 0;

    color: #8e98aa;

    font-size: 14px;
    line-height: 1.55;
}

.status-pill {
    display: inline-flex;
    align-items: center;

    gap: 7px;

    flex-shrink: 0;

    padding: 7px 12px;

    border: 1px solid #293140;
    border-radius: 999px;

    background: #121722;

    color: #b8c0cd;

    font-size: 12px;
    font-weight: 500;
}

.status-dot {
    width: 7px;
    height: 7px;

    border-radius: 50%;

    background: #22c55e;

    box-shadow:
        0 0 0 3px rgba(34, 197, 94, 0.10);
}


/* =========================================================
   EMPTY STATE
   ========================================================= */

.empty-state {
    width: 100%;

    min-height: 320px;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    margin-top: 10px;

    border: 1px solid #1d2532;
    border-radius: 18px;

    background:
        linear-gradient(
            180deg,
            rgba(18, 23, 32, 0.82),
            rgba(13, 17, 24, 0.72)
        );
}

.empty-icon {
    width: 44px;
    height: 44px;

    display: flex;
    align-items: center;
    justify-content: center;

    margin-bottom: 15px;

    border: 1px solid #293241;
    border-radius: 12px;

    background: #141a24;

    color: #aeb7c5;

    font-size: 18px;
    font-weight: 700;
}

.empty-title {
    color: #e7eaf0;

    font-size: 17px;
    font-weight: 650;
}

.empty-copy {
    max-width: 520px;

    margin-top: 7px;

    text-align: center;

    color: #737e90;

    font-size: 13px;
    line-height: 1.65;
}


/* =========================================================
   CHAT
   ========================================================= */

[data-testid="stChatMessage"] {
    width: 100% !important;

    margin-bottom: 13px;

    padding: 18px 20px;

    border: 1px solid #202937;
    border-radius: 16px;

    background: rgba(16, 21, 30, 0.92);
}

[data-testid="stChatMessageContent"] {
    width: 100% !important;
}

[data-testid="stChatMessageContent"] p {
    margin: 0;

    color: #e6e9ef;

    font-size: 15px;
    line-height: 1.75;
}


/* =========================================================
   SOURCES
   ========================================================= */

.sources-heading {
    margin-top: 20px;
    margin-bottom: 9px;

    color: #707b8e;

    font-size: 10px;
    font-weight: 750;

    text-transform: uppercase;

    letter-spacing: 0.1em;
}

.sources-grid {
    width: 100%;
}

.source-card {
    width: 100%;

    margin-top: 7px;

    padding: 12px 14px;

    border: 1px solid #252e3c;
    border-radius: 11px;

    background: #131925;
}

.source-card-title {
    color: #e1e5ec;

    font-size: 13px;
    font-weight: 650;
}

.source-card-path {
    margin-top: 4px;

    color: #687486;

    font-family:
        "SFMono-Regular",
        Consolas,
        monospace;

    font-size: 11px;
    line-height: 1.5;

    word-break: break-all;
}


/* =========================================================
   CHAT INPUT
   ========================================================= */

[data-testid="stBottomBlockContainer"] {
    width: calc(100% - 300px) !important;

    left: 300px !important;

    padding-left: 3rem !important;
    padding-right: 3rem !important;
    padding-bottom: 1.2rem !important;

    background:
        linear-gradient(
            180deg,
            rgba(9, 12, 18, 0),
            #090c12 32%
        );
}

[data-testid="stChatInput"] {
    width: 100% !important;

    border-radius: 14px;
}

[data-testid="stChatInput"] textarea {
    font-size: 15px;
}


/* =========================================================
   BUTTON
   ========================================================= */

.stButton > button {
    width: 100%;

    min-height: 40px;

    border: 1px solid #293241;
    border-radius: 10px;

    background: #151b25;

    color: #dce1e9;

    font-size: 13px;
    font-weight: 550;

    transition:
        background 0.15s ease,
        border 0.15s ease;
}

.stButton > button:hover {
    border-color: #465267;

    background: #1a2230;

    color: #ffffff;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 900px) {

    [data-testid="stMainBlockContainer"] {
        padding-left: 1.3rem !important;
        padding-right: 1.3rem !important;
    }

    [data-testid="stBottomBlockContainer"] {
        width: 100% !important;

        left: 0 !important;

        padding-left: 1.3rem !important;
        padding-right: 1.3rem !important;
    }

    .app-header {
        align-items: flex-start;

        flex-wrap: wrap;
    }

    .status-pill {
        margin-left: 66px;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
<div class="sidebar-brand">TaskFlow</div>
<div class="sidebar-copy">
Citation-aware AI support assistant powered by hybrid retrieval,
reranking and grounded generation.
</div>
""",
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown(
        '<div class="sidebar-label">Try asking</div>',
        unsafe_allow_html=True,
    )

    examples = [
        "How do I reset my password?",
        "Can I get a refund?",
        "How do I connect Slack?",
        "What happens after I delete my account?",
    ]

    for example in examples:

        st.markdown(
            f"""
<div class="example-question">
{html.escape(example)}
</div>
""",
            unsafe_allow_html=True,
        )

    st.divider()

    if st.button(
        "Clear conversation",
        use_container_width=True,
    ):

        st.session_state.messages = []

        st.rerun()

    st.markdown(
        """
<div class="sidebar-footer">
Answers are generated from the TaskFlow support knowledge base.
Sources are shown with grounded responses.
</div>
""",
        unsafe_allow_html=True,
    )


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
<div class="main-shell">
<div class="app-header">

<div class="brand-mark">T</div>

<div class="header-content">
<h1 class="app-title">TaskFlow Support</h1>
<p class="app-subtitle">
AI support assistant grounded in TaskFlow documentation.
Ask about accounts, billing, workspaces, integrations and policies.
</p>
</div>

<div class="status-pill">
<span class="status-dot"></span>
Knowledge base connected
</div>

</div>
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# EMPTY STATE
# =========================================================

if not st.session_state.messages:

    st.markdown(
        """
<div class="empty-state">

<div class="empty-icon">T</div>

<div class="empty-title">
How can we help?
</div>

<div class="empty-copy">
Ask a TaskFlow support question below.
The assistant searches the knowledge base,
generates a grounded answer and shows the supporting sources.
</div>

</div>
""",
        unsafe_allow_html=True,
    )


# =========================================================
# SOURCE RENDERER
# =========================================================

def render_sources(sources):

    if not sources:
        return

    st.markdown(
        '<div class="sources-heading">Sources</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sources-grid">',
        unsafe_allow_html=True,
    )

    for source in sources:

        title = html.escape(
            str(
                source.get(
                    "title",
                    "Unknown source",
                )
            )
        )

        path = html.escape(
            str(
                source.get(
                    "source_path",
                    "",
                )
            )
        )

        st.markdown(
            f"""
<div class="source-card">
<div class="source-card-title">{title}</div>
<div class="source-card-path">{path}</div>
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


# =========================================================
# EXISTING CHAT
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )

        render_sources(
            message.get(
                "sources",
                [],
            )
        )


# =========================================================
# INPUT
# =========================================================

question = st.chat_input(
    "Ask a question about TaskFlow..."
)


if question:

    # -----------------------------------------------------
    # USER MESSAGE
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):

        st.write(question)


    # -----------------------------------------------------
    # CONVERSATION HISTORY
    # -----------------------------------------------------

    history = [
        {
            "role": message["role"],
            "content": message["content"],
        }
        for message
        in st.session_state.messages[:-1]
    ]

    payload = {
        "question": question,
        "history": history,
    }


    # =====================================================
    # API REQUEST
    # =====================================================

    try:

        with st.spinner(
            "Searching TaskFlow documentation..."
        ):

            response = requests.post(
                API_URL,
                json=payload,
                timeout=60,
            )

        response.raise_for_status()

        data = response.json()

        answer = data.get(
            "answer",
            "I could not generate an answer.",
        )

        sources = data.get(
            "sources",
            [],
        )


    except requests.exceptions.ConnectionError:

        st.error(
            "Cannot connect to the TaskFlow API. "
            "Make sure FastAPI is running."
        )

        st.stop()


    except requests.exceptions.Timeout:

        st.error(
            "The request took too long. "
            "Please try again."
        )

        st.stop()


    except requests.exceptions.RequestException as error:

        st.error(
            f"API request failed: {error}"
        )

        st.stop()


    except ValueError:

        st.error(
            "The API returned an invalid response."
        )

        st.stop()


    # =====================================================
    # ASSISTANT RESPONSE
    # =====================================================

    with st.chat_message(
        "assistant"
    ):

        st.write(answer)

        render_sources(sources)


    # -----------------------------------------------------
    # SAVE ASSISTANT MESSAGE
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources,
        }
    )