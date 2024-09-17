from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import PromptTemplate
from langchain.tools import DuckDuckGoSearchRun
from langchain.utilities.wikipedia import WikipediaAPIWrapper
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import PromptTemplate

from pages.config.custom_tools.wrapper import GetScholarInfoTool
# from pages.config.custom_tools.wrapper import GetScholarInfoTool

TEMPLATE = """You are a helpful and respectful assistant.
Your goal is to provide help users with legal assistance by providing them relevant and correct information to their queries and concerns in a respectful manner.
Use the tools available to you to provide the best possible answer.
Check the chat history for more context.

History:
{chat_history}

User: {user_input}
"""


TEMPLATE_2 = """You are a helpful and respectful assistant.
You have also a knowledge base of research papers how to write a reference page of research paper based on the topic with the help of google and also explain it in detail.
reference page: references points are always consider "Author(s) ,Title(s), Source or venue name ,Editor(s) ,Volume and edition ,Date or year of publication ,Page numbers , City and country"
Your goal is to creating the Research paper and review paper help users with research paper assistance by providing them relevant and correct information to their queries and concerns in a respectful manner.
Use the tools available to you to provide the best possible answer.
Check the chat history for more context.

History:
{chat_history_2}

User: {user_input}
"""

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", convert_system_message_to_human=True)


class Legal_Config:

    system_prompt = TEMPLATE
    prompt = PromptTemplate(
        input_variables=["chat_history", "user_input"], template=system_prompt
    )


class Scholar_Config:

    system_prompt = TEMPLATE_2
    prompt = PromptTemplate(
        input_variables=["chat_history_2", "user_input"], template=system_prompt
    )


def setup_agent(prompt, kwargs, memory):
    search = DuckDuckGoSearchRun()
    wikipedia = WikipediaAPIWrapper()
    tools = [
        Tool(
            name="DuckDuckGo",
            func=search.run,
            description="useful for when you need to answer questions about current events. You should ask targeted questions",
        ),
        Tool(
            name="Wikipedia",
            func=wikipedia.run,
            description="useful when you need an answer about encyclopedic general knowledge",
        ),
        GetScholarInfoTool(),
    ]

    return initialize_agent(
        tools,
        llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        prompt=prompt,
        verbose=True,
        agent_kwargs=kwargs,
        memory=memory,
        handle_parsing_errors=True,
    )
