from langchain.memory import ConversationBufferMemory
from langchain.prompts.chat import MessagesPlaceholder
from typing import Tuple, Dict

SYSTEM_PROMPT_MESSAGE = """You are a helpful and respectful assistant.
Your goal is to provide help users with legal and rsearch assistance by providing them relevant and correct information to their queries and concerns in a respectful manner.
Use the tools available to you to provide the best possible answer.
Check the chat history for more context.

The first query is:
Hello, who are you?
"""


def setup_memory(history:str) -> Tuple[Dict, ConversationBufferMemory]:
    agent_kwargs = {
        "extra_prompt_messages": [MessagesPlaceholder(variable_name=history)],
    }
    memory = ConversationBufferMemory(memory_key=history, return_messages=True)
    memory.chat_memory.add_user_message(SYSTEM_PROMPT_MESSAGE)
    memory.chat_memory.add_ai_message(
        "Hello, I am your assistant I am here to help you with your legal and scholarly work. How can I help you today?"
    )

    return agent_kwargs, memory
