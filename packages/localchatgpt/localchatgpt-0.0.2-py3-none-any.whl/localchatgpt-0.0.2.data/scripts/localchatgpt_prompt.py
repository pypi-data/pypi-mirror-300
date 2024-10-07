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
    #print(f'Setting this system message : {new_sm}')
    oClient.edit_system_message(new_sm)

def setSM(sm: str) -> None:
    #print(f'Setting this system message : {sm}')
    oClient.set_system_message(sm)
