from localchatgpt_ollamaClient import OllamaClient
from typing import List

oClient = OllamaClient()

def setLLMServer(server):
    oClient.setServer(server)

def getModelList() -> List[str]:
    return oClient.getModelList()

def chatWithModel(prompt:str, model: str):
    return oClient.chat(prompt=prompt, model=model, temp=0.4)

def clearHistory():
    oClient.clear_history()

def modifySM(new_sm: str) -> None:
    oClient.edit_system_message(new_sm)
