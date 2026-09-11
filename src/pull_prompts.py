"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import sys
import yaml
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()

class LiteralString(str):
    pass


def literal_representer(dumper, data):
    return dumper.represent_scalar(
        "tag:yaml.org,2002:str",
        data,
        style="|"
    )


yaml.add_representer(LiteralString, literal_representer)

def pull_prompts_from_langsmith():
    prompt = hub.pull("leonanluppi/bug_to_user_story_v1")
    print("tipo do prompt:", type(prompt))
    save_yaml(promptToDict(prompt), Path("prompts/bug_to_user_story_v1.yml"))

def promptToDict(prompt: ChatPromptTemplate) -> dict:
    data = {
        prompt.metadata["lc_hub_repo"]: {
            "system_prompt": LiteralString(prompt.messages[0].prompt.template),
            "user_prompt": prompt.messages[1].prompt.template
        }
    }
    
    return data

def main():
    """Função principal"""
    print_section_header("Verificando variáveis de ambiente")
    check_env_vars(["LANGSMITH_API_KEY"])

    print_section_header("Fazendo pull dos prompts do LangSmith")
    pull_prompts_from_langsmith()


if __name__ == "__main__":
    sys.exit(main())
