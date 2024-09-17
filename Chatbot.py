import streamlit as st
from streamlit_option_menu import option_menu

from dotenv import load_dotenv
from langchain.agents import AgentExecutor
import time
# from pages.config.config import Legal_Config, Scholar_Config
from pages.config.memory import setup_memory

load_dotenv()

from pages.config.config import Legal_Config, Scholar_Config, setup_agent

legal = Legal_Config()
scholar = Scholar_Config()


LEGAL_HISTORY: str = "chat_history"
SCHOLAR_HISTORY: str = "chat_history_2"


def stream_text(text: str, placeholder: st.empty):
    for i in range(len(text)):
        time.sleep(0.005)
        placeholder.write(text[: i + 1])


legal_kwargs, legal_mem = setup_memory(LEGAL_HISTORY)


@st.cache_resource()
def get_legal_agent() -> AgentExecutor:
    return setup_agent(legal.prompt, legal_kwargs, legal_mem)


scholar_kwargs, scholar_mem = setup_memory(SCHOLAR_HISTORY)


@st.cache_resource()
def get_scholar_agent() -> AgentExecutor:
    return setup_agent(scholar.prompt, scholar_kwargs, scholar_mem)


def get_response(user_question: str, agent_executor: AgentExecutor) -> str:
    return agent_executor.run(user_question)


def research_chat_tab():
    st.title("Scholar Bot")
    for message in st.session_state[SCHOLAR_HISTORY]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    user_question = st.chat_input("Ask")
    if user_question:

        try:
            st.chat_message("user").markdown(user_question)
            st.session_state[SCHOLAR_HISTORY].append(
                {"role": "user", "content": user_question}
            )

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = get_response(str(user_question), get_scholar_agent())
                placeholder = st.empty()
                stream_text(response, placeholder)
            st.session_state[SCHOLAR_HISTORY].append(
                {"role": "assistant", "content": response}
            )

        except Exception as e:
            st.error(f"Error occurred: {e}")


def legal_chat_tab():
    st.title("Legal Bot")
    for message in st.session_state[LEGAL_HISTORY]:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    user_question = st.chat_input("Ask")
    if user_question:

        try:
            st.chat_message("user").markdown(user_question)
            st.session_state[LEGAL_HISTORY].append(
                {"role": "user", "content": user_question}
            )

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = get_response(str(user_question), get_legal_agent())
                placeholder = st.empty()
                stream_text(response, placeholder)
            st.session_state[LEGAL_HISTORY].append(
                {"role": "assistant", "content": response}
            )

        except Exception as e:
            st.error(f"Error occurred: {e}")


# def side_bar_history(history):
#     user_messages = [message["content"] for message in st.session_state[history] if message["role"] == "user"]
#     assistant_messages = [message["content"] for message in st.session_state[history] if message["role"] == "assistant"]
#     if st.checkbox("Show history in sidebar"):

#         st.sidebar.subheader("Chat History")
#         for i in range(len(user_messages)):
#             st.sidebar.caption(f"User: {user_messages[i]}")
#             st.sidebar.caption(f"Tootle: {assistant_messages[i]}")


def streamlit_interface():
    st.set_page_config(page_title="Assistants", layout="wide", page_icon="🤖")
    # Remove the bar
    st.markdown(
        """
    <style>
	[data-testid="stDecoration"] {
		display: none;
	}
    </style>""",
        unsafe_allow_html=True,
    )

    hide_streamlit_style = """
<style>
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
</style>

"""

    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    if LEGAL_HISTORY and SCHOLAR_HISTORY not in st.session_state:
        st.session_state[LEGAL_HISTORY], st.session_state[SCHOLAR_HISTORY] = [{"role": "assistant", "content": "I am your Legal Concierge"}], [{"role": "assistant", "content": "I am your Research Concierge"}]

    with st.sidebar:
        st.header("Tabs")
        # Tab options
        selected_tab = option_menu(
            None,
            ["Legal Chat", "Scholar Chat"],
            icons=["chat-square-dots-fill", "clock-fill"],
            orientation="vertical",
            styles={
                "container": {"padding": "0!important"},
                "nav": {"padding-bottom": "0px"},
                "nav-item": {
                    "font-weight": "200",
                    "font-family": "'Outfit', monospace",
                },
                "nav-link": {"text-align": "left", "margin": "0px"},
            },
        )

    if selected_tab == "Legal Chat":
        legal_chat_tab()
    else:
        research_chat_tab()


if __name__ == "__main__":
    streamlit_interface()
