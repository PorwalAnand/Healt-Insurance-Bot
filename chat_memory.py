from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

def get_memory():
    return ConversationBufferMemory(return_messages=True)
